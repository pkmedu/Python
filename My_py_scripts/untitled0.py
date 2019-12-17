# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:38:37 2019

@author: PMuhuri
"""

from pathlib import Path
dir =  Path('C:/Users/pmuhuri/AppData/Local/Continuum/anaconda3/Lib/site-packages/saspy/java')
files = dir.glob('*.*')
for i in files:
    print(i)