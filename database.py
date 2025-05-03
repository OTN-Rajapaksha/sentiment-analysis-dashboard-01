# database.py
import sqlite3
from datetime import datetime

DB = "data.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
      CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY,
        text TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        score REAL NOT NULL,
        timestamp TEXT NOT NULL
      )
    """)
    conn.commit()
    conn.close()

def insert_comment(text, sentiment, score):
    ts = datetime.now().isoformat(sep=" ", timespec="seconds")
    conn = sqlite3.connect(DB)
    conn.execute(
      "INSERT INTO comments (text, sentiment, score, timestamp) VALUES (?,?,?,?)",
      (text, sentiment, score, ts)
    )
    conn.commit()
    conn.close()

def fetch_comments():
    conn = sqlite3.connect(DB)
    cur = conn.execute("SELECT id, text, sentiment, score, timestamp FROM comments ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
