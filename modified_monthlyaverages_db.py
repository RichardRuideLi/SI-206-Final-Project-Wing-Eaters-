
import pandas as pd
import sqlite3

# Connect to the SQLite database
db_file = 'covidNYC.db'
conn = sqlite3.connect(db_file)

# Query the necessary data from the table 'covid_data'
query = """
SELECT date_of_interest, case_count, death_count 
FROM covid_data
"""

# Load the data into a pandas DataFrame
data = pd.read_sql_query(query, conn)

# Ensure 'date_of_interest' is a datetime format
data['date_of_interest'] = pd.to_datetime(data['date_of_interest'])

# Extract month and year for grouping
data['month_year'] = data['date_of_interest'].dt.to_period('M')

# Calculate monthly averages for case_count and death_count
monthly_averages = data.groupby('month_year')[['case_count', 'death_count']].mean().reset_index()

# Rename columns for clarity
monthly_averages.rename(columns={
    'month_year': 'Month',
    'case_count': 'Average_Case_Count',
    'death_count': 'Average_Death_Count'
}, inplace=True)

# Save the results to a CSV file
csv_output_path = 'monthly_averages.csv'
monthly_averages.to_csv(csv_output_path, index=False)

# Save the results to a TXT file
txt_output_path = 'monthly_averages.txt'
with open(txt_output_path, 'w') as file:
    file.write(monthly_averages.to_string(index=False))

# Close the database connection
conn.close()
