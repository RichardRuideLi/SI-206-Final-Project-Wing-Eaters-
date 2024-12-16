import sqlite3
import pandas as pd

# Load the cleaned data
data = pd.read_csv('cleaned_LA_County_COVID_Cases.csv')

# Connect to SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect('covid_data.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS covid_cases (
    date TEXT,
    county TEXT,
    cases INTEGER,
    deaths INTEGER
);
''')

# Commit and close the connection
conn.commit()

# Insert data into the table
for index, row in data.iterrows():
    cursor.execute('''
    INSERT INTO covid_cases (date, county, cases, deaths)
    VALUES (?, ?, ?, ?);
    ''', (row['date'], row['county'], row['cases'], row['deaths']))

# Commit the changes
conn.commit()

# Calculate yearly averages for cases and deaths
cursor.execute('''
SELECT 
    SUBSTR(date, 1, 4) AS year, -- Extract year from the date column
    AVG(cases) AS avg_cases,
    AVG(deaths) AS avg_deaths
FROM 
    covid_cases
GROUP BY 
    year
ORDER BY 
    year ASC;
''')

# Fetch and print the results
results = cursor.fetchall()
print("Yearly Averages:")
print("Year | Avg Cases | Avg Deaths")
for year, avg_cases, avg_deaths in results:
    print(f"{year} | {avg_cases:.2f} | {avg_deaths:.2f}")

# Close the connection
conn.close()

print("Data inserted successfully, and yearly averages calculated.")

