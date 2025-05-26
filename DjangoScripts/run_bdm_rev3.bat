@echo off
set LOGFILE=C:\Users\pmuhuri\DjangoProjects\bdmsite\startup_log.txt
set REPO_DIR=C:\Users\pmuhuri\DjangoProjects\bdmsite

REM === Overwrite the log file at the start ===
echo === Script started at %DATE% %TIME% === > "%LOGFILE%"

setlocal EnableDelayedExpansion

REM === Step 1: Initialize Conda and Activate Environment ===
call :logStep "Initializing and activating Conda environment bd_minority_videos..."
CALL C:\Users\pmuhuri\AppData\Local\anaconda3\condabin\conda.bat activate bd_minority_videos
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

REM === Step 3: Install Pillow ===
call :logStep "Installing Pillow..."
pip install Pillow >> "%LOGFILE%" 2>&1
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to install Pillow."
    exit /b
)

REM === Step 4: Run Migrations ===
call :logStep "Running Django migrations..."
python manage.py migrate >> "%LOGFILE%" 2>&1
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Django migration failed."
    exit /b
)

REM === Step 5: Launch Local Server in Browser After Short Delay ===
call :logStep "Launching browser..."
timeout /t 5 >nul
start http://127.0.0.1:8000/

REM === Step 6: Run Django Development Server ===
call :logStep "Starting Django development server..."
python manage.py runserver

REM === Keep Command Prompt Open After Server Stops ===
pause

goto :eof

REM === Logging Functions ===
:logStep
echo [%DATE% %TIME%] [STEP] %~1
echo [%DATE% %TIME%] [STEP] %~1 >> "%LOGFILE%"
goto :eof

:logError
echo [%DATE% %TIME%] [ERROR] %~1
echo [%DATE% %TIME%] [ERROR] %~1 >> "%LOGFILE%"
goto :eof
