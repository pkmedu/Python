@echo off
setlocal EnableDelayedExpansion

REM — ensure we can always find timeout.exe & powershell.exe —
set "PATH=%SystemRoot%\System32;%SystemRoot%\System32\WindowsPowerShell\v1.0\;%PATH%"

REM === Configuration ===
set "REPO_DIR=C:\Users\pmuhuri\DjangoProjects\bdmsite"
set "LOGFILE=%REPO_DIR%\setup_log.txt"
set "CONDA_PATH=C:\Users\pmuhuri\AppData\Local\anaconda3"
set "VERBOSE_MODE=true"

REM === Step 0: Ensure Python is Available ===
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Python is not installed or not found in PATH."
    exit /b
)

REM === Step 1: Initialize and Activate Conda Environment ===
call :logStep "Initializing and activating Conda environment bd_minority_videos..."
CALL "%CONDA_PATH%\condabin\conda.bat" activate bd_minority_videos
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to initialize or activate Conda environment."
    exit /b
)

REM === Step 2: Navigate to Project Directory ===
call :logStep "Navigating to Django project directory..."
cd /d "%REPO_DIR%"
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to navigate to project directory."
    exit /b
)

REM === Step 3: Ensure requirements.txt Exists ===
IF NOT EXIST requirements.txt (
    call :logStep "requirements.txt not found. Generating from current environment..."
    pip freeze > requirements.txt
    IF %ERRORLEVEL% NEQ 0 (
        call :logError "Failed to generate requirements.txt."
        exit /b
    )
)

REM === Step 4: Install Dependencies ===
call :logStep "Installing project dependencies..."
if "%VERBOSE_MODE%"=="true" (
    pip install -r requirements.txt
) else (
    pip install -r requirements.txt >> "%LOGFILE%" 2>&1
)
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to install dependencies."
    exit /b
)

REM === Step 4b: Install python-dotenv package ===
call :logStep "Installing python-dotenv package (required by settings.py)..."
if "%VERBOSE_MODE%"=="true" (
    pip install python-dotenv
) else (
    pip install python-dotenv >> "%LOGFILE%" 2>&1
)
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to install python-dotenv."
    exit /b
)

REM === Step 4c: Install additional common dependencies ===
call :logStep "Installing additional common Django dependencies..."
if "%VERBOSE_MODE%"=="true" (
    pip install django-crispy-forms django-debug-toolbar djangorestframework pillow whitenoise
) else (
    pip install django-crispy-forms django-debug-toolbar djangorestframework pillow whitenoise >> "%LOGFILE%" 2>&1
)
IF %ERRORLEVEL% NEQ 0 (
    call :logWarning "Some additional dependencies failed to install, but continuing..."
)

REM === Step 5: Make Migrations (allow exit code 1 - 'no changes') ===
call :logStep "Making migrations..."
if "%VERBOSE_MODE%"=="true" (
    python manage.py makemigrations
) else (
    call :runAndLog "python manage.py makemigrations"
)
set "makemigrations_exitcode=%ERRORLEVEL%"
IF %makemigrations_exitcode% GTR 1 (
    call :logError "Unexpected error during makemigrations."
    exit /b %makemigrations_exitcode%
)

REM === Step 6: Apply Migrations ===
call :logStep "Running Django migrations..."
if "%VERBOSE_MODE%"=="true" (
    python manage.py migrate
    set "migrate_exitcode=%ERRORLEVEL%"
) else (
    python manage.py migrate >> "%LOGFILE%" 2>&1
    set "migrate_exitcode=%ERRORLEVEL%"
)
IF %migrate_exitcode% NEQ 0 (
    call :logError "Django migration failed with exit code %migrate_exitcode%."
    
    REM === Enhanced Error Reporting for Migrations ===
    echo.
    echo ====
