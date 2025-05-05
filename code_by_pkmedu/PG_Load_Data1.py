# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 22:39:50 2025

@author: muhuri
"""
# Loading a SAS dataset and writing it to PistgreSQL, replacing myfirstdb (already existing) from Python
import pandas as pd
from sqlalchemy import create_engine

# Note: Use %24 for the dollar sign ($) in URL encoding
engine = create_engine("postgresql://postgres:Phariom108%24@localhost:5432/myfirstdb")

# Load the SAS dataset
df = pd.read_sas('c:\\data\\demographics.sas7bdat', format='sas7bdat', encoding='utf-8')

# Write to PostgreSQL, replacing the table if it already exists
df.to_sql('demographics', con=engine, if_exists='replace', index=False)

print("✅ Table 'demographics' has been replaced successfully in PostgreSQL.")
