# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 23:00:38 2023

@author: PMuhuri
"""

import pandas as pd
# Create a data frame
df = pd.DataFrame({'gender':[1,2]})
# Print the DataFrame
print(df)

# Create dictionary
dic = {1:'Male', 2:'Female'}
# Use the .map() method to transform the original data values
df['gender'] = df['gender'].map(dic)
# Print matching values
print(df)

 