import sqlite3
import pandas as pd

# Database file name
DB_NAME = "England_weekly_covid_deaths.db"

def setup_season_table():
    """Create a table for seasons with unique values."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Create the seasons table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seasons (
                season_id INTEGER PRIMARY KEY AUTOINCREMENT,
                season_name TEXT UNIQUE
            )
        """)

        # Insert unique seasons into the table
        seasons = [("Winter",), ("Spring",), ("Summer",), ("Fall",)]
        cursor.executemany("""
            INSERT OR IGNORE INTO seasons (season_name) VALUES (?)
        """, seasons)

        conn.commit()

def setup_months_info():
    """Create the months_info table normalized with the seasons table."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Drop the table if it exists to recreate it properly
        cursor.execute("DROP TABLE IF EXISTS months_info;")

        # Create months_info table with a foreign key to seasons
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS months_info (
                month INTEGER PRIMARY KEY,
                month_name TEXT,
                days_in_month INTEGER,
                season_id INTEGER,
                FOREIGN KEY (season_id) REFERENCES seasons (season_id)
            )
        """)

        # Populate months_info with normalized data
        months_data = [
            (1, "January", 31, "Winter"),
            (2, "February", 28, "Winter"),
            (3, "March", 31, "Spring"),
            (4, "April", 30, "Spring"),
            (5, "May", 31, "Spring"),
            (6, "June", 30, "Summer"),
            (7, "July", 31, "Summer"),
            (8, "August", 31, "Summer"),
            (9, "September", 30, "Fall"),
            (10, "October", 31, "Fall"),
            (11, "November", 30, "Fall"),
            (12, "December", 31, "Winter"),
        ]

        # Insert data dynamically fetching season_id
        for month, month_name, days, season in months_data:
            cursor.execute("""
                INSERT INTO months_info (month, month_name, days_in_month, season_id)
                SELECT ?, ?, ?, season_id FROM seasons WHERE season_name = ?;
            """, (month, month_name, days, season))

        conn.commit()

def calculate_weekly_averages_with_join():
    """Calculate the weekly average of deaths for each month and year using a JOIN with months_info and seasons."""
    with sqlite3.connect(DB_NAME) as conn:
        # SQL query to calculate weekly averages with normalization
        query = """
        SELECT 
            cd.year,
            cd.month,
            mi.month_name,
            s.season_name,
            SUM(cd.deaths) / 4.0 AS weekly_average
        FROM 
            covid_deaths cd
        JOIN 
            months_info mi ON cd.month = mi.month
        JOIN 
            seasons s ON mi.season_id = s.season_id
        GROUP BY 
            cd.year, cd.month
        ORDER BY 
            cd.year, cd.month;
        """

        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Save results to a CSV file
        df.to_csv("England_Average_Covid_Weekly_Death.csv", index=False)
        print("Weekly averages with normalized data saved to 'England_Average_Covid_Weekly_Death.csv'.")

def export_deduplicated_data():
    """Export normalized data to two CSV files: main table and season reference."""
    with sqlite3.connect(DB_NAME) as conn:
        # Main table without duplicate season names
        main_query = """
            SELECT cd.year, cd.month, mi.month_name, mi.season_id, SUM(cd.deaths) / 4.0 AS weekly_average
            FROM covid_deaths cd
            JOIN months_info mi ON cd.month = mi.month
            GROUP BY cd.year, cd.month
            ORDER BY cd.year, cd.month;
        """
        main_df = pd.read_sql_query(main_query, conn)
        main_df.to_csv("England_Average_Covid_Weekly_Death.csv", index=False)
        print("Main table exported to 'England_Average_Covid_Weekly_Death.csv'.")

        # Season reference table (deduplicated)
        season_query = "SELECT season_id, season_name FROM seasons;"
        season_df = pd.read_sql_query(season_query, conn)
        season_df.to_csv("season_reference.csv", index=False)
        print("Season reference table exported to 'season_reference.csv'.")

        # Confirm seasons table exists in the database
        print("Seasons reference table successfully created and stored in the database.")

def verify_tables():
    """Verify that the reference and main tables exist in the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print("Existing tables in the database:", tables)

def export_with_season_id_to_txt():
    """Export normalized data with season_id to a text file in a human-readable format."""
    with sqlite3.connect(DB_NAME) as conn:
        # Query to include season_id and calculate weekly averages
        query = """
        SELECT 
            cd.year,
            cd.month,
            mi.month_name,
            mi.season_id,
            SUM(cd.deaths) / 4.0 AS weekly_average
        FROM 
            covid_deaths cd
        JOIN 
            months_info mi ON cd.month = mi.month
        GROUP BY 
            cd.year, cd.month
        ORDER BY 
            cd.year, cd.month;
        """

        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        # Write results to a text file
        with open("England_Average_Covid_Weekly_Death.txt", "w") as file:
            file.write("Weekly Average Deaths with Season ID by Year and Month\n")
            file.write("=" * 60 + "\n")
            for row in rows:
                year, month, month_name, season_id, weekly_average = row
                file.write(f"Year: {year}, Month: {month_name}, Season ID: {season_id}, Weekly Average: {weekly_average:.2f}\n")

        print("Weekly averages with season_id saved to 'England_Average_Covid_Weekly_Death.txt'.")


if __name__ == "__main__":
    # Step 1: Setup seasons table
    setup_season_table()

    # Step 2: Setup months_info table with season normalization
    setup_months_info()

    # Step 3: Calculate weekly averages and export
    calculate_weekly_averages_with_join()

    # Step 4: Export deduplicated data
    export_deduplicated_data()
    export_with_season_id_to_txt()

    # Step 5: Verify tables
    verify_tables()

