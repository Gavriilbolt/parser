import sqlite3
import pandas as pd


DB_NAME = "journal_data.db"


# Set up the SQLite database
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            issue TEXT,
            title TEXT,
            author TEXT,
            link TEXT UNIQUE
        )
    ''')
    conn.commit()
    return conn


conn = setup_database()

