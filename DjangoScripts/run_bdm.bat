@echo off
REM === Initialize Conda ===
CALL C:\Users\pmuhuri\AppData\Local\anaconda3\Scripts\activate.bat

REM === Activate Conda Environment for Django Project ===
CALL conda activate bd_minority_videos

REM === Navigate to Django Project Root ===
cd /d C:\Users\pmuhuri\DjangoProjects\bdmsite

CALL pip install Pillow

REM === Apply Database Migrations ===
python manage.py migrate

REM === OPTIONAL: Create a Superuser ===
REM python manage.py createsuperuser

REM === Launch Local Server in Browser ===
start http://127.0.0.1:8000/

REM === Run Django Development Server ===
python manage.py runserver

REM === Keep Command Prompt Open After Server Stops ===
pause

