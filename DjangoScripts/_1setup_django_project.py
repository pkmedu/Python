# -*- coding: utf-8 -*-
"""
Created on Fri May 16 04:10:52 2025

@author: muhuri
"""

"""
Django Project Setup Script for Spyder
--------------------------------------
This script automates the creation of a Django project and app,
configures the basic settings, and validates the setup.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the output"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                                text=True, capture_output=True, cwd=cwd)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error Output: {e.stderr}")
        return False

def create_django_project():
    """Set up a new Django project with an app"""
    
    # Configuration parameters - Changed these as needed
    PROJECT_NAME = "bdm_project"
    APP_NAME = "bdm_app"
    BASE_DIR = "C:\\Users\\pmuhuri\\DjangoProject2\\bdm_django"  # Changed this to my preferred directory
    # Ensure base directory exists
    os.makedirs(BASE_DIR, exist_ok=True)
    
    # Create virtual environment
    venv_dir = os.path.join(BASE_DIR, f"{PROJECT_NAME}_venv")
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment at {venv_dir}...")
        if not run_command(f"python -m venv {venv_dir}"):
            print("Failed to create virtual environment. Exiting.")
            return False
    
    # Determine paths for pip and Python inside the virtual environment
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
        python_path = os.path.join(venv_dir, "Scripts", "python")
    else:  # macOS/Linux
        pip_path = os.path.join(venv_dir, "bin", "pip")
        python_path = os.path.join(venv_dir, "bin", "python")
    
    # Install Django in the virtual environment
    if not run_command(f"{pip_path} install django"):
        print("Failed to install Django. Exiting.")
        return False
    
    # Create project directory
    project_dir = os.path.join(BASE_DIR, PROJECT_NAME)
    if not os.path.exists(project_dir):
        print(f"Creating Django project: {PROJECT_NAME}...")
        if not run_command(f"{python_path} -m django startproject {PROJECT_NAME} {project_dir}"):
            print("Failed to create Django project. Exiting.")
            return False
    
    # Create app
    os.chdir(project_dir)
    if not run_command(f"{python_path} manage.py startapp {APP_NAME}"):
        print(f"Failed to create Django app: {APP_NAME}. Exiting.")
        return False
    
    # Update settings.py to include our app
    settings_path = os.path.join(project_dir, PROJECT_NAME, "settings.py")
    with open(settings_path, 'r') as f:
        settings_content = f.read()
    
    # Add app to INSTALLED_APPS
    if f"'{APP_NAME}'" not in settings_content:
        settings_content = settings_content.replace(
            "INSTALLED_APPS = [",
            f"INSTALLED_APPS = [\n    '{APP_NAME}',"
        )
        
        # Configure static files
        if "STATICFILES_DIRS" not in settings_content:
            static_settings = """
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / '{app_name}' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
""".format(app_name=APP_NAME)
            
            settings_content += static_settings
        
        with open(settings_path, 'w') as f:
            f.write(settings_content)
    
    # Create templates and static directories
    templates_dir = os.path.join(project_dir, APP_NAME, "templates", APP_NAME)
    static_dir = os.path.join(project_dir, APP_NAME, "static", APP_NAME)
    
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)
    
    # Create basic template
    index_template = os.path.join(templates_dir, "index.html")
    with open(index_template, 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>Welcome to {{ title }}</h1>
    <p>This is a Django project created with Spyder setup script.</p>
</body>
</html>""")
    
    # Create basic view
    views_path = os.path.join(project_dir, APP_NAME, "views.py")
    with open(views_path, 'w') as f:
        f.write("""from django.shortcuts import render

def index(request):
    \"\"\"
    Main index view for the app
    \"\"\"
    context = {
        'title': 'My Django App'
    }
    return render(request, '{app_name}/index.html', context)
""".format(app_name=APP_NAME))
    
    # Create app urls.py
    app_urls_path = os.path.join(project_dir, APP_NAME, "urls.py")
    with open(app_urls_path, 'w') as f:
        f.write("""from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]""")
    
    # Update project urls.py
    project_urls_path = os.path.join(project_dir, PROJECT_NAME, "urls.py")
    with open(project_urls_path, 'r') as f:
        urls_content = f.read()
    
    if "include" not in urls_content:
        urls_content = urls_content.replace(
            "from django.urls import path",
            "from django.urls import path, include"
        )
    
    if f"include('{APP_NAME}.urls')" not in urls_content:
        urls_content = urls_content.replace(
            "urlpatterns = [",
            f"urlpatterns = [\n    path('', include('{APP_NAME}.urls')),"
        )
    
    with open(project_urls_path, 'w') as f:
        f.write(urls_content)
    
    # Run initial migrations
    if not run_command(f"{python_path} manage.py migrate"):
        print("Failed to run migrations. Please check your setup.")
    
    # Create run_server.py in the base directory for easy launching
    run_server_path = os.path.join(BASE_DIR, "run_server.py")
    with open(run_server_path, 'w') as f:
        f.write("""import os
import sys
import subprocess

# Path to the project directory
PROJECT_DIR = r"{project_dir}"
# Path to the Python executable in the virtual environment
PYTHON_PATH = r"{python_path}"

def main():
    # Change to project directory
    os.chdir(PROJECT_DIR)
    
    # Run the development server
    subprocess.run([PYTHON_PATH, "manage.py", "runserver", "0.0.0.0:8090"])

if __name__ == "__main__":
    main()
""".format(project_dir=project_dir, python_path=python_path))
    
    # Print success message
    print("\nDjango project setup complete!")
    print(f"Project name: {PROJECT_NAME}")
    print(f"App name: {APP_NAME}")
    print(f"Project directory: {project_dir}")
    print("\nTo run the server from Spyder, execute:")
    print(f"runfile(r'{run_server_path}')")
    print("\nYou can then access your site at:")
    print("http://127.0.0.1:8090/")
    
    return True

if __name__ == "__main__":
    create_django_project()