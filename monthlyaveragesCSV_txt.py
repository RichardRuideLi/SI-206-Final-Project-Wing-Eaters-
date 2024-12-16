import pandas as pd

# Load the data from the CSV file
csv_file = 'nyc_data_cleaned.csv'  # Update with the correct file path if necessary
data = pd.read_csv(csv_file)

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

print(f"Monthly averages saved to {csv_output_path} and {txt_output_path}.")
