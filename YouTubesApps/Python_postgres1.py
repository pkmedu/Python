# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 10:44:07 2025

@author: muhuri
"""

import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="testuser",
    password="test",
    host="127.0.0.1",
    port="5432"
)

cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT);")
cur.execute("INSERT INTO items (name) VALUES (%s);", ("Sample Item",))
conn.commit()

cur.execute("SELECT * FROM items;")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()
