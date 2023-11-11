# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 05:53:34 2019

@author: PMuhuri
"""

import pandas as pd
# Use %cd magic command and Pandas to read SAS dataset
#https://www.pharmasug.org/proceedings/tokyo2018/posters/PharmaSUG-Tokyo-2018-PO03.pdf
#%cd C:\SASCourse\SAS_Windowing_JupyterLab\Ipynb
#pndata_class = pd.read_sas('class.sas7bdat', format='sas7bdat', encoding="utf-8")
#pndata_class.describe()

#Nakajima, 2018 - Utilization of Python in clinical study by SASPy
# import Python librsries
import saspy
import pandas as pd
#Establish SAS connection
sas = saspy.SASsession(cfgname = 'winlocal')
# set up file path in SAS
sas.saslib('new', path = "C:\\SASCourse\\SAS_Windowing_JupyterLab\\Ipynb")
# Read SAS dataset
class = sas.sasdata('class', libref = 'new')
pc2 = sas.sasdata2dataframe('class', libref = 'new')
pc2.describe()