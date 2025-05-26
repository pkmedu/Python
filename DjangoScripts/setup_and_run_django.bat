@echo off
REM === User Configuration ===
set "REPO_DIR=C:\Python\DjangoScripts"
set "LOGFILE=%REPO_DIR%\setup_log.txt"

REM === Step 1: Activate Conda Environment ===
call :logStep "Initializing and activating Conda environment bd_minority_videos..."
CALL C:\Users\pmuhuri\AppData\Local\anaconda3\condabin\conda.bat activate bd_minority_videos
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to initialize or activate Conda environment."
    exit /b
)

REM Define python and pip commands
set "PYTHON_EXE=python"
set "PIP_EXE=pip"

REM === Step 2: Navigate to Project Directory ===
call :logStep "Navigating to Django project directory..."
cd /d "%REPO_DIR%"
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to navigate to project directory."
    exit /b
)

REM === Check for manage.py ===
if not exist "manage.py" (
    call :logError "manage.py not found in %REPO_DIR%"
    exit /b
)

REM === Step 3: Install Pillow ===
call :logStep "Installing Pillow..."
%PIP_EXE% install Pillow >> "%LOGFILE%" 2>&1
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to install Pillow."
    exit /b
)

REM === Step 4: Run Migrations ===
call :logStep "Running Django migrations..."
%PYTHON_EXE% manage.py migrate >> "%LOGFILE%" 2>&1
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
%PYTHON_EXE% manage.py runserver

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
