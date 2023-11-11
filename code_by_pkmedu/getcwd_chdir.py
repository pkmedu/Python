# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 23:17:13 2019

@author: PMuhuri
"""
#Ex6_getcwd_chdir.py
import os
os.getcwd()
os.chdir('C:\\SASCourse\\Week1')
os.getcwd()
files = os.listdir(os.curdir)
print(files)