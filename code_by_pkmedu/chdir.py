# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
retval = os.getcwd()
print("Current directory %s" % retval)
path = "/Users/Pradip Muhuri/Documents"
os.chdir(path)
retval = os.getcwd()
print ("Directory changed %s" % retval)


    

