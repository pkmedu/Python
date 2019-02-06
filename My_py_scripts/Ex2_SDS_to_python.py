#!/usr/bin/env python
# coding: utf-8

# In[5]:
#Ex2_SDS_to_python.py
import sas7bdat
from sas7bdat import *
foo= SAS7BDAT('D:\\My_py_scripts\\class.sas7bdat')
ds=foo.to_data_frame()  
print(ds)



# In[ ]:




