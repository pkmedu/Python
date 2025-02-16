# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 08:55:21 2024

@author: muhuri
"""
import pandas as pd

# Load the dataset
data = pd.read_csv('C:\\Data\\class.csv')  # Assuming the data is in a CSV format

# Group by 'name' and 'age', and calculate mean for 'height' and 'weight'
grouped_data = data.groupby(['name', 'age']).agg({'height': 'mean', 'weight': 'mean'}).reset_index()

# Calculate BMI
grouped_data['bmi'] = (grouped_data['weight'] / (grouped_data['height'] / 100) ** 2) * 703

# Display the results
result = grouped_data[['name', 'age', 'height', 'weight', 'bmi']]
print(result)