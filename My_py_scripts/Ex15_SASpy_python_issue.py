# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 17:33:16 2019

@author: PMuhuri
"""
import saspy
import pandas as pd
sas = saspy.SASsession(cfgname ='winlocal')
mydata = sas.sasdata('class', 'sashelp')
mydata.head()