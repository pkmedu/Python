# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 14:17:53 2023

@author: PMuhuri
"""

# import pandas library
import pandas as pd
  
# dictionary with list object in values
details = {
    'name' : ['Dexiu', 'Doug', 'Fred', 'Yichi'],
    'level' : ['Graduate', 'Graduate', 'Undergraduate', 'Undergraduate'],
    'sas': ['yes', 'no', 'no', 'no'],
    'r': ['yes', 'yes', 'no', 'yes'],
    'python': ['yes', 'no', 'no', 'yes']
}
  
# creating a Dataframe object 
df = pd.DataFrame(details)
print(df)