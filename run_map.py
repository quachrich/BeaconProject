# run_map.py
import sqlite3
import pandas as pd
# change to from app import create_world_map if your function is in app.py
from map_viz import create_world_map

DB_PATH = "data.sqlite"

SQL = """
SELECT
  country AS Country,
  COUNT(*) AS Count,
  GROUP_CONCAT(DISTINCT disease) AS Description   -- no custom separator here
FROM events
WHERE event_type='event'
  AND country IS NOT NULL AND country <> ''
  AND disease IS NOT NULL AND disease <> ''
GROUP BY country
ORDER BY Count DESC
LIMIT 500;
"""

def load_country_summary(db_path=DB_PATH) -> pd.DataFrame:
    with sqlite3.connect(db_path) as con:
        df = pd.read_sql_query(SQL, con)
    # Pretty-up the separator for hover text
    if "Description" in df.columns and df["Description"].notna().any():
        df["Description"] = df["Description"].str.replace(",", ", ")
    return df

def main():
    df = load_country_summary()
    fig = create_world_map(df, country_col="Country", text_col="Description", size_col="Count")
    fig.show()
    fig.write_html("world_events_map.html")
    print("Saved: world_events_map.html")

if __name__ == "__main__":
    main()
