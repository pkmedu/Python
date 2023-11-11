# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 10:58:50 2019

@author: PMuhuri
"""
from pathlib import Path
#import glob
dir =  Path('C:/Users/pmuhuri/Documents')
files = dir.glob('*.docx')
for i in files:
    print(i)

