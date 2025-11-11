# check_history.py
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("smartmenu.db")        # adjust path if your DB is elsewhere
MENU_CSV = Path("data/menu.csv")     # used to map item IDs -> names (optional)

def get_connection(db_path=DB_PATH):
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found at: {db_path.resolve()}")
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

def fetch_user_history(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_history ORDER BY timestamp DESC")
    rows = cur.fetchall()
    return rows

def rows_to_dataframe(rows):
    if not rows:
        return pd.DataFrame()   # empty df
    df = pd.DataFrame([dict(row) for row in rows])
    return df

def join_with_menu(df_history, menu_csv=MENU_CSV):
    if df_history.empty:
        return df_history
    if not menu_csv.exists():
        print("Warning: menu CSV not found; returning raw history with item ids.")
        return df_history
    menu = pd.read_csv(menu_csv)
    # Expect menu has columns id and name
    return df_history.merge(menu[['id','name']], left_on='dish_id', right_on='id', how='left')

def popular_dishes(conn, top_n=10):
    query = """
    SELECT dish_id, COUNT(*) as cnt
    FROM user_history
    GROUP BY dish_id
    ORDER BY cnt DESC
    LIMIT ?
    """
    cur = conn.cursor()
    cur.execute(query, (top_n,))
    return cur.fetchall()

def main():
    conn = get_connection()
    try:
        rows = fetch_user_history(conn)
        df = rows_to_dataframe(rows)
        if df.empty:
            print("No user history found in database.")
            return

        # Pretty print raw history
        print("\n=== Last entries (raw) ===")
        print(df.head(20).to_string(index=False))

        # Join with menu.csv to show names
        df_named = join_with_menu(df)
        print("\n=== Last entries (with dish names if available) ===")
        print(df_named[['timestamp','mood','dish_id','name']].head(20).to_string(index=False))

        # Popular dishes
        print("\n=== Top 10 popular dishes by selections ===")
        top = popular_dishes(conn, top_n=10)
        for r in top:
            print(f"Dish id={r['dish_id']}  —  selections={r['cnt']}")

        # If menu CSV exists, map ids to names for popularity
        if MENU_CSV.exists():
            menu = pd.read_csv(MENU_CSV)
            top_df = pd.DataFrame([dict(row) for row in top])
            if not top_df.empty:
                top_df = top_df.merge(menu[['id','name']], left_on='dish_id', right_on='id', how='left')
                print("\n=== Top dishes with names ===")
                print(top_df[['name','cnt']].to_string(index=False))

    finally:
        conn.close()

if __name__ == "__main__":
    main()
