# -*- coding: utf-8 -*-
"""
Created on Fri May 16 04:15:21 2025

@author: muhuri
"""

"""
Django Migrations Runner Script for Spyder
------------------------------------------
This script runs Django migrations programmatically.
Run this script in Spyder to apply migrations to your database.
"""

import os
import sys
import django
from django.core.management import call_command

def run_migrations():
    """
    Set up Django environment and run migrations
    """
    # Get the project directory (adjust if necessary)
    # Assumes this script is in the same directory as manage.py
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the project directory to the Python path
    sys.path.append(project_dir)
    
    # Set the Django settings module
    # Change 'bdm_project.settings' to your project's settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bdm_project.settings')
    
    # Initialize Django
    django.setup()
    
    print("Running makemigrations...")
    # Generate migration files
    call_command('makemigrations')
    
    print("Running migrate...")
    # Apply migrations
    call_command('migrate')
    
    print("Migrations complete!")
    
    # Optional: Show migration list
    print("\nMigration status:")
    call_command('showmigrations')

if __name__ == "__main__":
    run_migrations()