@echo off
setlocal EnableDelayedExpansion

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
    echo ======== DETAILED MIGRATION ERROR REPORT ========
    echo.
    echo Attempting to diagnose the migration issue:
    echo.
    
    REM Check DB connection
    call :logStep "Checking database connection..."
    python -c "from django.db import connections; connections['default'].ensure_connection(); print('Database connection successful')" 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Database connection issue detected. Check your database settings.
    )
    
    REM Run migration with higher verbosity
    call :logStep "Rerunning migration with verbosity=2 for detailed information..."
    python manage.py migrate --verbosity 2
    
    REM Show migration list for diagnostics
    call :logStep "Displaying migration status..."
    python manage.py showmigrations
    
    echo.
    echo ===============================================
    exit /b
)

REM === Step 7: Collect Static Files ===
call :logStep "Collecting static files..."
if "%VERBOSE_MODE%"=="true" (
    python manage.py collectstatic --noinput
) else (
    python manage.py collectstatic --noinput >> "%LOGFILE%" 2>&1
)
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to collect static files."
    exit /b
)

REM === Step 8: Start Django Development Server ===
call :logStep "Starting Django development server in new console..."
start "Django Server" cmd /k "cd /d %REPO_DIR% && echo Starting Django... && python manage.py runserver"

REM === Step 9: Wait for Server to Start ===
call :logStep "Waiting for server to become available..."
timeout /t 5 /nobreak > nul
call :checkServerAvailability "http://127.0.0.1:8000/"
IF %ERRORLEVEL% NEQ 0 (
    call :logWarning "Server may not be running properly. Attempting to launch browser anyway."
)

REM === Step 10: Launch Browser ===
call :logStep "Launching browser..."
start http://127.0.0.1:8000/

REM === Step 11: Done ===
if exist "C:\Python\DjangoScripts" (
    cd /d C:\Python\DjangoScripts
) else (
    call :logWarning "Directory C:\Python\DjangoScripts does not exist. Staying in current directory."
)
echo.
echo [%CD%] Django setup complete. Press any key to exit...
pause >nul
goto :eof

REM === Check Server Availability Function ===
:checkServerAvailability
set "url=%~1"
powershell -Command "try { $response = Invoke-WebRequest -Uri '%url%' -Method Head -TimeoutSec 5 -UseBasicParsing; exit 0 } catch { exit 1 }"
IF %ERRORLEVEL% NEQ 0 (
    call :logWarning "Could not connect to server at %url%"
    exit /b 1
)
goto :eof

REM === Logging Functions ===
:logStep
echo [%DATE% %TIME%] [STEP] %~1
echo [%DATE% %TIME%] [STEP] %~1 >> "%LOGFILE%"
goto :eof

:logWarning
echo [%DATE% %TIME%] [WARNING] %~1
echo [%DATE% %TIME%] [WARNING] %~1 >> "%LOGFILE%"
goto :eof

:logError
echo [%DATE% %TIME%] [ERROR] %~1
echo [%DATE% %TIME%] [ERROR] %~1 >> "%LOGFILE%"
goto :eof

:runAndLog
echo [%DATE% %TIME%] [RUN] %~1 >> "%LOGFILE%"
%~1 >> "%LOGFILE%" 2>&1
set "errcode=%ERRORLEVEL%"
exit /b %errcode%