import sqlite3
import pandas as pd
import os

import options



DB_NAME = options.db_name
outputs_dir = options.outputs_dir


# Set up the SQLite database
def setup_database():
    conn = sqlite3.connect(os.path.join(outputs_dir, DB_NAME))
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

