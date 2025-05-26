@echo off
setlocal enabledelayedexpansion

REM === Configuration ===
set "REPO_DIR=C:\Users\pmuhuri\DjangoProjects\bdmsite"
set "LOGFILE=%REPO_DIR%\django_debug.log"

REM === Clear previous log ===
echo Django Debug Started at %DATE% %TIME% > "%LOGFILE%"

REM === Go to project directory ===
cd /d "%REPO_DIR%"

REM === Set environment variables ===
set "DJANGO_DEBUG=True"
set "PYTHONUNBUFFERED=1"

REM === Check Django project structure ===
echo Checking Django project structure... >> "%LOGFILE%"
if not exist "manage.py" (
  echo ERROR: manage.py not found in %REPO_DIR% >> "%LOGFILE%"
  echo ERROR: manage.py not found in %REPO_DIR%
  goto :error
)

REM === Check settings module - without using findstr ===
echo Finding settings module... >> "%LOGFILE%"
echo Checking manage.py for settings references >> "%LOGFILE%"
type manage.py >> "%LOGFILE%"

REM === List installed packages ===
echo Installed packages: >> "%LOGFILE%"
pip freeze >> "%LOGFILE%"

REM === List project structure - without using findstr ===
echo Project file structure: >> "%LOGFILE%"
dir /s /b "%REPO_DIR%\*.py" >> "%LOGFILE%"
echo Note: __pycache__ files not filtered >> "%LOGFILE%"

REM === Check static files configuration ===
echo Static files configuration: >> "%LOGFILE%"
echo STATIC_ROOT = !STATIC_ROOT! >> "%LOGFILE%"
echo STATIC_URL = !STATIC_URL! >> "%LOGFILE%"

REM === Check database file ===
echo Checking database... >> "%LOGFILE%"
dir "%REPO_DIR%\*.sqlite3" >> "%LOGFILE%" 2>&1

REM === Run Django check ===
echo Running Django system check... >> "%LOGFILE%"
python manage.py check >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo Django check failed. See %LOGFILE% for details.
  goto :error
)

REM === Show URLs ===
echo Available URLs: >> "%LOGFILE%"
python manage.py show_urls >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo Listing URLs failed, this might not be critical. >> "%LOGFILE%"
)

REM === Start server with maximum debug output ===
echo.
echo Starting Django server with debug output...
echo This window will show server logs. Check for errors when the server starts.
echo.
echo If you need more detailed debugging, Django debug log is at: %LOGFILE%
echo.
python -Wa manage.py runserver --traceback --insecure --settings=bdmsite.settings 0.0.0.0:8000

goto :end

:error
echo.
echo Error encountered. See %LOGFILE% for details.
echo.
pause
exit /b 1

:end
pause