# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 15:32:07 2025

@author: muhuri
"""

import sqlite3

def save_to_db(video_url, summary, db_name="youtube_summary.db"):
    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_url TEXT UNIQUE,
            summary TEXT
        )
    """)

    # Insert or replace the summary
    cursor.execute("""
        INSERT OR REPLACE INTO summaries (video_url, summary)
        VALUES (?, ?)
    """, (video_url, summary))

    conn.commit()
    conn.close()
    print(f"Saved summary to {db_name}")
