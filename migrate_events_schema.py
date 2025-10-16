import sqlite3

con = sqlite3.connect("data.sqlite")
cur = con.cursor()

def add(coldef):
    name = coldef.split()[0]
    have = {r[1] for r in cur.execute("PRAGMA table_info(events)").fetchall()}
    if name not in have:
        cur.execute(f"ALTER TABLE events ADD COLUMN {coldef}")

# Add columns WITHOUT non-constant defaults
add("disease TEXT")
add("country TEXT")
add("event_type TEXT NOT NULL DEFAULT 'event'")
add("source TEXT")
add("url TEXT")
add("reported_date TEXT")
add("content_hash TEXT")
add("first_seen_at TEXT")   # no default here
add("last_seen_at TEXT")    # no default here
add("last_changed_at TEXT")

# Backfill event_type
cur.execute("""
UPDATE events
SET event_type='announcement'
WHERE lower(title) LIKE 'introducing %'
   OR lower(title) LIKE 'announcements:%'
""")

# Backfill disease/country
cur.execute("""
UPDATE events
SET disease = trim(substr(title, 1, instr(title, ',')-1)),
    country = trim(substr(title, instr(title, ',')+1))
WHERE event_type='event' AND instr(title, ',') > 0
""")

# Backfill timestamps safely
cur.execute("UPDATE events SET first_seen_at = COALESCE(first_seen_at, CURRENT_TIMESTAMP)")
cur.execute("UPDATE events SET last_seen_at  = COALESCE(last_seen_at,  CURRENT_TIMESTAMP)")

con.commit()
con.close()
print("Migration complete.")
