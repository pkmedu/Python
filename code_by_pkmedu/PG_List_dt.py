# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 01:28:24 2025

@author: muhuri
"""

import psycopg2
import pandas as pd

# Replace with your credentials
HOST = "localhost"
PORT = 5432
USER = "postgres"
PASSWORD = "Phariom108$"

# Connect to default 'postgres' database to get the list of databases
conn = psycopg2.connect(host=HOST, port=PORT, dbname="postgres", user=USER, password=PASSWORD)
conn.autocommit = True
cur = conn.cursor()

# Get list of non-template databases
cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
databases = [row[0] for row in cur.fetchall()]

all_tables = []

for db in databases:
    try:
        print(f"🔎 Scanning database: {db}")
        conn_db = psycopg2.connect(host=HOST, port=PORT, dbname=db, user=USER, password=PASSWORD)
        cur_db = conn_db.cursor()
        cur_db.execute("""
            SELECT current_database() AS database,
                   schemaname,
                   tablename
            FROM pg_tables
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
        """)
        tables = cur_db.fetchall()
        all_tables.extend(tables)
        cur_db.close()
        conn_db.close()
    except Exception as e:
        print(f"⚠️ Could not connect to {db}: {e}")

cur.close()
conn.close()

# Save to CSV or print
df = pd.DataFrame(all_tables, columns=["database", "schema", "table"])
df.to_csv("c:\\Data\postgres_all_tables.csv", index=False)
print("✅ Saved all database.table names to postgres_all_tables.csv")
