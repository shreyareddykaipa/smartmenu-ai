import sqlite3

conn = sqlite3.connect("smartmenu.db")
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
rows = cur.fetchall()

print("Tables in DB:", rows)
conn.close()
