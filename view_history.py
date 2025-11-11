import sqlite3

def view_all_history():
    conn = sqlite3.connect("smartmenu.db")
    cur = conn.cursor()

    cur.execute("SELECT id, mood, dish_id, timestamp FROM user_history ORDER BY id DESC")
    rows = cur.fetchall()

    if not rows:
        print("⚠️ No user history found.")
    else:
        print("✅ User History Records:")
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    view_all_history()
