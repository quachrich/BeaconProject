# db.py  — minimal SQLite layer
import sqlite3

DB_PATH = "data.sqlite"

def init_db():
    con = sqlite3.connect(DB_PATH)
    con.executescript("""
    CREATE TABLE IF NOT EXISTS events (
      id     INTEGER PRIMARY KEY,
      title  TEXT NOT NULL UNIQUE
    );
    """)
    con.commit()
    con.close()

def save_titles(titles):
    con = sqlite3.connect(DB_PATH)
    con.executemany(
        "INSERT OR IGNORE INTO events(title) VALUES(?)",
        [(t.strip(),) for t in titles if t and t.strip()]
    )
    con.commit()
    con.close()
