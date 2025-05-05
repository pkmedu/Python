# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 08:40:19 2024

@author: muhuri
"""

import pandas as pd

# Create the DataFrame
data = {
    'service_type': [
        'Hospital Care', 
        'Physician and Clinical Services', 
        'Prescription Drugs', 
        'Nursing Care', 
        'Other Health Care', 
        'Dental Services', 
        'Home Health Care', 
        'Other Medical Products', 
        'Other Professional Services'
    ],
    'amount_in_B': [882.3, 556.0, 263.3, 151.5, 138.2, 110.9, 77.8, 95.0, 78.4]
}

df = pd.DataFrame(data)

# Calculate the total amount
total_amount = df['amount_in_B'].sum()

# Calculate the percentage
df['Percent'] = df['amount_in_B'] / total_amount

# Display the results
print("Health Care Expenditures, United States, 2012")
print(df[['service_type', 'amount_in_B', 'Percent']])
