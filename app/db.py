import sqlite3
import os

DB_PATH = os.path.abspath("smartmenu.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT,
            dish_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def get_connection():
    print("DEBUG — Using DB file at:", DB_PATH)
    return sqlite3.connect(DB_PATH)

