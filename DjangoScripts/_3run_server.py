# -*- coding: utf-8 -*-
"""
Created on Fri May 16 04:18:15 2025

@author: muhuri
"""

"""
Django Development Server Runner for Spyder IDE

This script allows you to run the Django development server directly from Spyder.
It provides options for specifying host, port, and other server configurations.
"""

import os
import sys
import django
from django.core.management import call_command

def run_django_server(host='127.0.0.1', port=8090, use_reloader=True, use_threading=True):
    """
    Run the Django development server with the specified parameters.
    
    Args:
        host (str): The hostname to serve on
        port (int): The port to serve on
        use_reloader (bool): Whether to use the auto-reloader
        use_threading (bool): Whether to run in threaded mode
    """
    # Set the DJANGO_SETTINGS_MODULE environment variable
    project_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
    
    # Make sure the app is found on the path
    project_path = os.path.dirname(os.path.abspath(__file__))
    if project_path not in sys.path:
        sys.path.append(project_path)
    
    # Initialize Django
    django.setup()
    
    # Run the development server
    # This passes through any provided parameters to the 'runserver' command
    call_command(
        'runserver',
        f'{host}:{port}',
        use_reloader=use_reloader,
        use_threading=use_threading
    )
    
if __name__ == '__main__':
    # If your Django project is in a subdirectory:
    # Example for a project structure where manage.py is in bdm_django/bdm_project/
    # os.chdir('bdm_project')  # Uncomment and modify this line if needed
    
    # Run the server with custom parameters
    run_django_server(
        host='0.0.0.0',  # Use '0.0.0.0' to make the server accessible from other devices on the network
        port=8090,       # Choose your preferred port
        use_reloader=True,  # Auto-reload when code changes
        use_threading=True   # Enable threading
    )