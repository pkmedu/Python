# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 09:43:45 2025

@author: muhuri
"""

import pandas as pd
import glob
import os

# Set your directory path
folder_path = 'C:/Links'
output_file = 'C:/Data/combined_all.csv'

# Find all CSV files in the directory
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Read and concatenate all CSV files
df_list = [pd.read_csv(file) for file in csv_files]
combined_df = pd.concat(df_list, ignore_index=True)

# Save the combined DataFrame to a single CSV
combined_df.to_csv(os.path.join(folder_path, output_file), index=False)


# Load your CSV
df = pd.read_csv('C:/Data/combined_all.csv')

# Drop duplicates based on a specific column, e.g., 'Link'
df_unique = df.drop_duplicates(subset='Link', keep='first')

# Save the deduplicated DataFrame to a new CSV
df_unique.to_csv('c:/Data/deduplicated_output.csv', index=False)
