# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:17:57 2022

@author: PMuhuri
"""

with open(r"c:\Users\\pmuhuri\Final_Solution_Dec10.py", 'r') as program:
    data = program.readlines()

with open(r"c:\Data\Final_Solution_LN.py", 'w') as program:
    for (number, line) in enumerate(data):
        program.write('%d  %s' % (number + 1, line))