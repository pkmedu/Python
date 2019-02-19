# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from path import Path
from glob import glob
x = [Path(f).abspath() for f in glob("C:/Users/Pradip Muhuri/Documents/*.sas")]
for f in x:
    print(f)



    

