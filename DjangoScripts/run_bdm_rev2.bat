@echo off
set LOGFILE=C:\Users\pmuhuri\DjangoProjects\bdmsite\startup_log.txt
set REPO_DIR=C:\Users\pmuhuri\DjangoProjects\bdmsite

REM === Overwrite the log file at the start ===
echo === Script started at %DATE% %TIME% === > "%LOGFILE%"

setlocal EnableDelayedExpansion

REM === Step 1: Initialize Conda ===
call :logStep "Initializing Conda..."
CALL C:\Users\pmuhuri\AppData\Local\anaconda3\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to initialize Conda."
    exit /b
)

REM === Step 2: Activate Environment ===
call :logStep "Activating Conda environment bd_minority_videos..."
CALL conda activate bd_minority_videos
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to activate Conda environment."
    exit /b
)

REM === Step 3: Navigate to Project Directory ===
call :logStep "Navigating to Django project directory..."
cd /d "%REPO_DIR%"
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to navigate to project directory."
    exit /b
)

REM === Step 4: Install Pillow ===
call :logStep "Installing Pillow..."
pip install Pillow >> "%LOGFILE%" 2>&1
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to install Pillow."
    exit /b
)

REM === Step 5: Run Migrations ===
call :logStep "Running Django migrations..."
python manage.py migrate >> "%LOGFILE%" 2>&1
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Django migration failed."
    exit /b
)

REM === Step 6: Commit and Push to GitHub ===
call :logStep "Adding changes to Git..."
git add . >> "%LOGFILE%" 2>&1

call :logStep "Committing changes..."
git commit -m "Auto: Updated log and migration on %DATE% %TIME%" >> "%LOGFILE%" 2>&1

IF %ERRORLEVEL% NEQ 0 (
    call :logError "Git commit failed. Possibly no changes to commit."
) ELSE (
    call :logStep "Pushing changes to GitHub..."
    git push origin main >> "%LOGFILE%" 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        call :logError "Git push failed."
        exit /b
    )
)

call :logStep "Done. Changes pushed to GitHub."
echo === Script finished at %DATE% %TIME% === >> "%LOGFILE%"
pause
exit /b

REM === Logging Subroutines ===
:logStep
echo [%TIME%] %~1 >> "%LOGFILE%"
echo %~1
exit /b

:logError
echo [%TIME%] [ERROR] %~1 >> "%LOGFILE%"
echo [ERROR] %~1
exit /b
