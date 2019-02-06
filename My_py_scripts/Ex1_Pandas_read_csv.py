#!/usr/bin/env python
# coding: utf-8

# In[1]:

# Ex1_Pandas_csv.py
import os
os.getcwd()
import pandas as pd
df=pd.read_csv('TV_Data_noheader.csv', names=['opinion', 'party', 'income', 'age'])
print(df)



# In[ ]:




