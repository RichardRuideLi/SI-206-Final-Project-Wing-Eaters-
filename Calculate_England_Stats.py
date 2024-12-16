import sqlite3
import pandas as pd

# Database file
DB_NAME = "England_weekly_covid_deaths.db"

def setup_months_info():
    """
    Create a months_info table and populate it with data.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create a table with information about each month
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS months_info (
            month INTEGER PRIMARY KEY,
            month_name TEXT,
            days_in_month INTEGER,
            season TEXT
        )
    """)

    # Insert data into months_info table (if not already present)
    cursor.execute("SELECT COUNT(*) FROM months_info;")
    if cursor.fetchone()[0] == 0:  # Populate only if empty
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
        cursor.executemany("INSERT INTO months_info VALUES (?, ?, ?, ?)", months_data)

    conn.commit()
    conn.close()

def calculate_weekly_averages_with_join():
    """
    Calculate the weekly average of deaths for each month and year, using a JOIN with months_info.
    """
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)

    # SQL Query to join covid_deaths with months_info and calculate weekly averages
    query = """
    SELECT 
        cd.year,
        cd.month,
        mi.month_name,
        mi.season,
        SUM(cd.deaths) AS monthly_deaths,
        SUM(cd.deaths) / 4 AS weekly_average  -- Manually calculate weekly average
    FROM 
        covid_deaths cd
    JOIN 
        months_info mi
    ON 
        cd.month = mi.month
    GROUP BY 
        cd.year, cd.month
    ORDER BY 
        cd.year, cd.month;
    """

    # Execute the query and fetch results
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Display the DataFrame
    print(df)

    # Save the results to a CSV file
    df.to_csv("weekly_averages_with_join.csv", index=False)
    print("Weekly averages with month info have been saved to 'weekly_averages_with_join.csv'.")

    # Write the results to a text file
    with open("weekly_averages_with_join.txt", "w") as file:
        file.write("Weekly Averages by Year, Month, and Season\n")
        file.write("=" * 50 + "\n")
        for index, row in df.iterrows():
            file.write(
                f"Year: {int(row['year'])}, Month: {row['month_name']} ({row['season']}), "
                f"Monthly Deaths: {row['monthly_deaths']:.2f}, "
                f"Weekly Average: {row['weekly_average']:.2f}\n"
            )
    print("Weekly averages with join have also been saved to 'weekly_averages_with_join.txt'.")

if __name__ == "__main__":
    # Step 1: Set up the months_info table
    setup_months_info()

    # Step 2: Calculate weekly averages with a JOIN
    calculate_weekly_averages_with_join()



