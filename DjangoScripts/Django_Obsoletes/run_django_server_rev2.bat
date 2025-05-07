@echo off
REM Set working directory to project root
cd /d C:\Users\pmuhuri\DjangoProjects\newsite

REM Initialize Conda
CALL C:\Users\pmuhuri\AppData\Local\anaconda3\Scripts\activate.bat

REM Activate your Django environment
CALL conda activate my_django_env

REM OPTIONAL: Run database migrations
python manage.py migrate

REM OPTIONAL: Create a superuser (uncomment if needed)
REM python manage.py createsuperuser

REM Launch the Django development server
start http://127.0.0.1:8000/
python manage.py runserver

REM Keep the window open after the server stops
pause
