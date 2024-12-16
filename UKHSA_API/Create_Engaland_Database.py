import json
import sqlite3

# Database file
DB_NAME = "England_weekly_covid_deaths.db"

# JSON file containing the data
JSON_FILE = "England_Weekly_Covid_Death.json"

def setup_database():
    """
    Create SQLite database and tables.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table for COVID-19 data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS covid_deaths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            month INTEGER,
            week INTEGER,
            deaths REAL,
            UNIQUE (year, month, week)
        )
    """)

    conn.commit()
    conn.close()

def load_25_rows(file_path):
    """
    Load only 25 rows from JSON file and store them in the SQLite database.
    """
    with open(file_path, "r") as file:
        data = json.load(file)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check how many rows are already in the database
    cursor.execute("SELECT COUNT(*) FROM covid_deaths;")
    current_row_count = cursor.fetchone()[0]

    # Calculate how many rows to insert this time (limit to 25)
    start_index = current_row_count
    end_index = start_index + 25
    rows_to_insert = data[start_index:end_index]

    print(f"Inserting rows {start_index + 1} to {end_index}...")

    # Insert rows into the database
    for item in rows_to_insert:
        cursor.execute("""
            INSERT OR IGNORE INTO covid_deaths (year, month, week, deaths)
            VALUES (?, ?, ?, ?)
        """, (
            item["year"],
            item["month"],
            item["epiweek"],
            item["metric_value"]
        ))

    conn.commit()
    conn.close()
    print(f"Inserted {len(rows_to_insert)} rows into the database.")

def main():
    """
    Main execution flow.
    """
    # Step 1: Set up the database
    setup_database()

    # Step 2: Load 25 rows into the database
    load_25_rows(JSON_FILE)

if __name__ == "__main__":
    main()
