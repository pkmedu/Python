# -*- coding: utf-8 -*-
"""
Created on Sat May 17 06:47:25 2025

@author: muhuri
"""
import os
import sys
import subprocess

# Step 1: Create the base directory using the OS command functions similar to the shell command
# mkdir C:\Users\pmuhuri\DjangoProject2\bdm_django
# and then change to that directory using the OS command functions similar to the shell command:
# cd C:\Users\pmuhuri\DjangoProject2\bdm_django.

# Since I am using the IPython environment (Spyder), I cannot use the shell command functions.
# I must use the OS command functions, etc, as below.

# Use OS command functions to create the directory from within Python:
os.makedirs(r"C:\Users\pmuhuri\DjangoProject2\bdm_django", exist_ok=True)

# Run the setup script - execute a shell command from within Python and 
# use the subprocess module
subprocess.run(["python", r"C:/Python/DjangoScripts2/_1setup_django_project_rev.py"], 
               cwd=r"C:/Python/DjangoScripts")


# Use Python's os module to change directory in a Python interpreter
os.chdir(r"C:\Users\pmuhuri\DjangoProject2\bdm_django")

# Step 2:  Create a virtual environment in the current directory
# similar to using the shell command: python -m venv bdm_project_venv.
# However, to create a virtual environment from within the Python interpreter, 
# use the venv module through the subprocess module.

import subprocess
subprocess.run([sys.executable, "-m", "venv", "bdm_project_venv"])

# The advantage of using sys.executable instead of just "python" is that 
# it ensures you're using the exact same Python interpreter that's currently 
# running, which can be important if you have multiple Python versions 
# installed on your system.

# Step 3: Activate the virtual environment similar to using:
# bdm_project_venv\Scripts\activate

# The proper way to use a virtual environment is to:
# Exit your current Python interpreter (exit())
# Activate the virtual environment in the command prompt
# Start a new Python session

sys.exit()


# Step 4: Install Django using the shell command: pip install django

# Step 5: Create the project using the shell command django-admin startproject bdm_project .


# Run a command using the virtual environment's Python: nt's Python
result = subprocess.run([python_path, "-c", "import sys; print(sys.executable)"])


