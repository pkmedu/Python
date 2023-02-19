# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 22:43:52 2023

@author: PMuhuri
"""

with open(r"c:\Python\Web_Scraping\Final_Solution_Feb18_2023.py", 'r') as program:
    data = program.readlines()

with open(r"c:\Python\Web_Scraping\Final_Solution_LN.py", 'w') as program:
    for (number, line) in enumerate(data):
        program.write('%d  %s' % (number + 1, line))