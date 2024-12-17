import pandas as pd

# Load the dataset 
data = pd.read_csv('cleaned_LA_County_COVID_Cases.csv')

# Display the first few rows
print("First 5 rows of the dataset:")
print(data.head())

# Display information about the dataset
print("\nDataset Information:")
print(data.info())

# Drop columns with all null values
data.dropna(axis=1, how='all', inplace=True)
print("\nColumns after dropping empty ones:")
print(data.columns)

# Convert 'date' column to datetime format for consistency (updated to match actual column name)
data['date'] = pd.to_datetime(data['date'], errors='coerce')  # Convert and handle errors

# Check for missing or erroneous values in the 'date' column
missing_dates = data[data['date'].isna()]
print(f"\nRows with missing dates:\n{missing_dates}")

# Handle missing values in other columns (if any)
missing_values = data.isna().sum()
print(f"\nMissing values in each column:\n{missing_values}")

# Handle missing values for 'cases' and 'deaths' columns
# Fill missing values with the median value for consistency
data['cases'].fillna(data['cases'].median(), inplace=True)
data['deaths'].fillna(data['deaths'].median(), inplace=True)

# After filling missing values, check again
missing_values = data.isna().sum()
print(f"\nMissing values after handling:\n{missing_values}")

# Check for duplicates in the dataset
duplicate_rows = data.duplicated().sum()
print(f"\nNumber of duplicate rows: {duplicate_rows}")

# Remove duplicates
data.drop_duplicates(inplace=True)
print(f"\nNumber of rows after removing duplicates: {len(data)}")

# Detect outliers using IQR (Interquartile Range) for the 'cases' and 'deaths' columns
Q1_cases = data['cases'].quantile(0.25)
Q3_cases = data['cases'].quantile(0.75)
IQR_cases = Q3_cases - Q1_cases
lower_bound_cases = Q1_cases - 1.5 * IQR_cases
upper_bound_cases = Q3_cases + 1.5 * IQR_cases

# Identify outliers in the 'cases' column
outliers_cases = data[(data['cases'] < lower_bound_cases) | (data['cases'] > upper_bound_cases)]
print(f"\nOutliers in 'cases' column:\n{outliers_cases}")

# Removing outliers
data = data[(data['cases'] >= lower_bound_cases) & (data['cases'] <= upper_bound_cases)]

# Similarly, for 'deaths' column
Q1_deaths = data['deaths'].quantile(0.25)
Q3_deaths = data['deaths'].quantile(0.75)
IQR_deaths = Q3_deaths - Q1_deaths
lower_bound_deaths = Q1_deaths - 1.5 * IQR_deaths
upper_bound_deaths = Q3_deaths + 1.5 * IQR_deaths

# Identify outliers in the 'deaths' column
outliers_deaths = data[(data['deaths'] < lower_bound_deaths) | (data['deaths'] > upper_bound_deaths)]
print(f"\nOutliers in 'deaths' column:\n{outliers_deaths}")

# Removing outliers
data = data[(data['deaths'] >= lower_bound_deaths) & (data['deaths'] <= upper_bound_deaths)]

aggregated_data = data.groupby(['date', 'county']).agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()

print(f"\nFirst 5 rows of the aggregated data:\n{aggregated_data.head()}")

print("\nFinal dataset information:")
print(aggregated_data.info())


aggregated_data.to_csv('cleaned_LA_County_COVID_Cases.csv', index=False)

print("\nData cleaning complete. The cleaned data has been saved as 'cleaned_LA_County_COVID_Cases.csv'.")

