# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 23:27:07 2019

@author: PMuhuri
"""
#Ex7_pathlib_rglob_pandas.py
import pandas as pd
from pathlib import Path
import time

p = Path("/SASCourse/Week2")
all_files = []
for i in p.rglob('*.*'):
    all_files.append((i.name, i.parent, time.ctime(i.stat().st_ctime)))

columns = ["File_Name", "Parent", "Created"]
df = pd.DataFrame.from_records(all_files, columns=columns)

print(df.iloc[:,0])