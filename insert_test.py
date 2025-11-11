import sqlite3

conn = sqlite3.connect("smartmenu.db")
cur = conn.cursor()

cur.execute("INSERT INTO user_history (mood, dish_id) VALUES (?, ?)", ("debug_test", 123))
conn.commit()
conn.close()

print("✅ Inserted test row.")

