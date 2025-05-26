# -*- coding: utf-8 -*-
"""
Created on Thu May 15 22:51:28 2025

@author: muhuri
"""

import os
import subprocess
import shutil

# Set the project directory
project_dir = r"C:\Users\pmuhuri\DjangoProjects\bdm_django\bdm_project"
os.chdir(project_dir)

# Path to the virtual environment's Python
venv_python = r"C:\Users\pmuhuri\DjangoProjects\bdm_django\venv\Scripts\python.exe"

# 1. Delete the database (it will be recreated)
db_path = os.path.join(project_dir, "db.sqlite3")
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Deleted database: {db_path}")

# 2. Delete all migration files except __init__.py
migrations_dir = os.path.join(project_dir, "bdm_app", "migrations")
if os.path.exists(migrations_dir):
    for filename in os.listdir(migrations_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            file_path = os.path.join(migrations_dir, filename)
            os.remove(file_path)
            print(f"Deleted migration file: {filename}")

# 3. Make sure we have a proper __init__.py file
init_py = os.path.join(migrations_dir, "__init__.py")
if not os.path.exists(init_py):
    with open(init_py, "w") as f:
        pass
    print(f"Created {init_py}")

# 4. Make new migrations
print("\nCreating new migrations...")
subprocess.run([venv_python, "manage.py", "makemigrations", "bdm_app"])

# 5. Apply migrations
print("\nApplying migrations...")
subprocess.run([venv_python, "manage.py", "migrate"])

print("\nMigration reset complete!")
print("Now you can run the server with:")
print(f"{venv_python} manage.py runserver 8090")