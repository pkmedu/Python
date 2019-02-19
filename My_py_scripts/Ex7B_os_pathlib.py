# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pathlib
flist = []
for p in pathlib.Path('.').iterdir():
    if p.is_file():
      print(p)  
      flist.append



    

