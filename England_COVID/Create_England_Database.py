import json
import sqlite3
import time

# Database file
DB_NAME = "England_weekly_covid_deaths.db"

# JSON file containing the data
JSON_FILE = "England_Weekly_Covid_Death.json"

def setup_database():
    """
    Create SQLite database and a simplified table.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Simplified table for COVID-19 data with week
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS covid_deaths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            month INTEGER,
            week INTEGER,
            deaths REAL
        )
    """)

    conn.commit()
    conn.close()

def load_data_in_batches(file_path, batch_size=25):
    """
    Load data from JSON file in batches and store it in the SQLite database.
    """
    with open(file_path, "r") as file:
        data = json.load(file)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1} with {len(batch)} rows.")

        for item in batch:
            cursor.execute("""
                INSERT INTO covid_deaths (year, month, week, deaths)
                VALUES (?, ?, ?, ?)
            """, (
                item["year"],
                item["month"],
                item["epiweek"],  # Use epiweek for the week number
                item["metric_value"]
            ))

        conn.commit()
        time.sleep(1)  # Pause to simulate batch processing as required by assignment

    conn.close()
    print("All data has been processed and stored.")

def main():
    """
    Main execution flow.
    """
    # Step 1: Set up the database
    setup_database()

    # Step 2: Load and store data in batches
    load_data_in_batches(JSON_FILE)

if __name__ == "__main__":
    main()
