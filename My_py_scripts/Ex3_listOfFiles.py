# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 23:02:48 2019
@author: PMuhuri
"""

# https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
import os
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

import pandas as pd
dirName = 'C:\\SASCourse\\Week3';
# Get the list of all files in directory tree at given path
listOfFiles = getListOfFiles(dirName)
df = pd.DataFrame(listOfFiles)
print(df)
