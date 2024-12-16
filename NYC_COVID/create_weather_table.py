
import sqlite3

def create_weather_table(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create the 'weather' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            weather_id INTEGER PRIMARY KEY,
            weather_name TEXT NOT NULL
        )
    """)
    
    # Insert the specified rows into the 'weather' table
    weather_data = [
        (1, 'hot'),
        (2, 'cold')
    ]
    cursor.executemany("INSERT OR IGNORE INTO weather (weather_id, weather_name) VALUES (?, ?)", weather_data)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    
    print("Weather table created and data inserted successfully.")

# Example usage
# Uncomment the following line to execute the function:
create_weather_table('covidNYC.db')

def create_monthly_info_table(db_file):
    # Define the month and weather mapping
    months = [
        (1, "January", 2),
        (2, "February", 2),
        (3, "March", 1),
        (4, "April", 1),
        (5, "May", 1),
        (6, "June", 1),
        (7, "July", 1),
        (8, "August", 1),
        (9, "September", 1),
        (10, "October", 2),
        (11, "November", 2),
        (12, "December", 2),
    ]

    # Establish a connection to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Create the monthly_info table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monthly_info (
                month_id INTEGER PRIMARY KEY,
                month_name TEXT NOT NULL,
                weather_id INTEGER NOT NULL
            );
        """)

        # Insert data into the table
        cursor.executemany("""
            INSERT INTO monthly_info (month_id, month_name, weather_id)
            VALUES (?, ?, ?)
        """, months)

        # Commit the changes
        conn.commit()
        print("monthly_info table created and populated successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        conn.close()

def join_covid_data_with_monthly_info(db_file):
    # Establish a connection to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Add month_id and weather_id columns to covid_data if they do not exist
        cursor.execute("""
            ALTER TABLE covid_data
            ADD COLUMN month_id INTEGER;
        """)
    except sqlite3.OperationalError:
        # Column already exists
        pass

    try:
        cursor.execute("""
            ALTER TABLE covid_data
            ADD COLUMN weather_id INTEGER;
        """)
    except sqlite3.OperationalError:
        # Column already exists
        pass

    try:
        # Update covid_data with month_id and weather_id by joining with monthly_info
        cursor.execute("""
            UPDATE covid_data
            SET month_id = CAST(strftime('%m', date_of_interest) AS INTEGER),
                weather_id = (
                    SELECT weather_id FROM monthly_info
                    WHERE monthly_info.month_id = CAST(strftime('%m', date_of_interest) AS INTEGER)
                );
        """)

        # Commit the changes
        conn.commit()
        print("covid_data table updated with month_id and weather_id from monthly_info.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        conn.close()

# Example usage
create_monthly_info_table("covidNYC.db")
join_covid_data_with_monthly_info("covidNYC.db")



