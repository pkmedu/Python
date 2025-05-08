@echo off
set LOGFILE=C:\Users\pmuhuri\DjangoProjects\bdmsite\startup_log.txt

REM === Overwrite the log file at the start of the run ===
echo === Script started at %DATE% %TIME% === > "%LOGFILE%"

REM === Enable delayed expansion for logging ===
setlocal EnableDelayedExpansion

REM === Step 1: Initialize Conda ===
call :logStep "Initializing Conda..."
CALL C:\Users\pmuhuri\AppData\Local\anaconda3\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to initialize Conda."
    exit /b
)

REM === Step 2: Activate Conda Environment ===
call :logStep "Activating Conda environment bd_minority_videos..."
CALL conda activate bd_minority_videos
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to activate Conda environment."
    exit /b
)

REM === Step 3: Navigate to Django Project ===
call :logStep "Navigating to Django project directory..."
cd /d C:\Users\pmuhuri\DjangoProjects\bdmsite
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Failed to navigate to Django project directory."
    exit /b
)

REM === Step 4: Install Dependencies ===
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

REM === Optional: Create Superuser ===
REM call :logStep "Creating Django superuser..."
REM python manage.py createsuperuser
REM IF %ERRORLEVEL% NEQ 0 (
REM     call :logError "Failed to create superuser."
REM     exit /b
REM )

REM === Step 6: Open in Browser ===
call :logStep "Launching local server in browser..."
start http://127.0.0.1:8000/

REM === Step 7: Run Development Server ===
call :logStep "Starting Django development server..."
python manage.py runserver >> "%LOGFILE%" 2>&1
IF %ERRORLEVEL% NEQ 0 (
    call :logError "Django development server failed to start."
    exit /b
)

call :logStep "Django development server stopped. Exiting."
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
