@echo off
REM === Initialize Conda ===
CALL C:\Users\pmuhuri\AppData\Local\anaconda3\Scripts\activate.bat

REM === Activate Django Conda Environment ===
cd /d C:\Users\pmuhuri\AppData\Local\anaconda3\envs\bd_minority_videos
CALL conda activate bd_minority_videos

REM CALL pip install django

REM === Change to Django Project Root ===
cd /d C:\Users\pmuhuri\DjangoProjects\bdmsite

REM === Apply Migrations ===
python manage.py migrate

REM === OPTIONAL: Create a Superuser ===
REM python manage.py createsuperuser

REM === Launch Dev Server in Browser ===
start http://127.0.0.1:8000/

REM === Run Django Development Server ===
python manage.py runserver

REM === Keep CMD Window Open After Shutdown ===
pause
