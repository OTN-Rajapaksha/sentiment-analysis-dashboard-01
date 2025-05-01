# database.py

import sqlite3
from datetime import datetime

# Create/initialize the database
def init_db():
    conn = sqlite3.connect('sentiment_analysis.db')
    cursor = conn.cursor()
    
    # Create the table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        score REAL NOT NULL,
        timestamp TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Insert sentiment data into the database
def insert_sentiment(text, sentiment, score):
    conn = sqlite3.connect('sentiment_analysis.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO comments (text, sentiment, score, timestamp) 
    VALUES (?, ?, ?, ?)''', (text, sentiment, score, datetime.now()))
    conn.commit()
    conn.close()

# Fetch all data from the database
def fetch_all():
    conn = sqlite3.connect('sentiment_analysis.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments')
    rows = cursor.fetchall()
    conn.close()
    return rows
