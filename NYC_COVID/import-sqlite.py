import sqlite3
import pandas as pd

# Load the data from the provided CSV file
csv_file = 'nyc_data_cleaned.csv'
data = pd.read_csv(csv_file)

# Filter the data to include only relevant columns and clean date format
data = data[['date_of_interest', 'case_count', 'hospitalized_count', 'death_count']]

# Ensure 'date_of_interest' column has only the date portion (remove time)
data['date_of_interest'] = pd.to_datetime(data['date_of_interest']).dt.date

# Establish a connection to the SQLite database
# If the file does not exist, it will be created
conn = sqlite3.connect('covidNYC.db')
cursor = conn.cursor()

# Define the table name
table_name = "covid_data"

# Check the existing number of rows in the table (if it exists)
cursor.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
if cursor.fetchone()[0] == 1:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    offset = cursor.fetchone()[0]
else:
    offset = 0

# Dynamically create table schema based on the filtered columns (only on the first run)
if offset == 0:
    columns = data.columns
    data_types = data.dtypes

    # Create SQL statements for table creation
    column_definitions = []
    for column, dtype in zip(columns, data_types):
        if "int" in str(dtype):
            sql_type = "INTEGER"
        elif "float" in str(dtype):
            sql_type = "REAL"
        else:
            sql_type = "TEXT"
        column_definitions.append(f"{column} {sql_type}")

    columns_sql = ", ".join(column_definitions)
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"

    # Execute table creation
    cursor.execute(create_table_sql)

# Select the next 25 rows based on the offset
chunk = data[offset:offset + 25]

# If there are rows to insert, insert them into the table
if not chunk.empty:
    chunk.to_sql(table_name, conn, if_exists='append', index=False)
    print(f"Added {len(chunk)} rows to the table '{table_name}' in '/mnt/data/covidNYC.db'.")
else:
    print("No more rows to add.")

# Commit and close the database connection
conn.commit()
conn.close()
