import requests
import pandas as pd
import json

# URL to fetch the data
url = "https://data.cityofnewyork.us/api/views/rc75-m7u3/rows.json?accessType=DOWNLOAD"

# Fetching the data using the requests library
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad responses
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit()

# Extracting the rows and column names from the JSON response
columns = data['meta']['view']['columns']
column_names = [col['name'] for col in columns]
rows = data['data']

# Creating a DataFrame from the data
df = pd.DataFrame(rows, columns=column_names)

# Data cleaning (basic example)
# Dropping columns that are irrelevant or empty
df = df.dropna(how='all', axis=1)

# Standardizing column names (optional, depending on your needs)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=True)

# Saving the cleaned data to a CSV file
output_file = "nyc_data_cleaned.csv"
df.to_csv(output_file, index=False)

print(f"Data has been cleaned and saved to {output_file}")
