# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 17:00:03 2025

@author: muhuri
"""

import json
import psycopg2

# Prompt for the password
password = input("Phariom108$")

# Load JSON file
with open('C:\\Python\\YouTubesApps\\STharoor_summary.JSON', 'r') as f:
    data = json.load(f)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="mfirstdb",
    user="pmuhuri",
    password=password,
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# Insert JSON into a table with a JSONB column named 'data'
insert_query = "INSERT INTO json_table (data) VALUES (%s);"

# If the JSON is a list of objects
if isinstance(data, list):
    for item in data:
        cursor.execute(insert_query, [json.dumps(item)])
else:
    cursor.execute(insert_query, [json.dumps(data)])

conn.commit()
cursor.close()
conn.close()

print("JSON data inserted successfully.")
