import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'monthly_averages.csv'
data = pd.read_csv(file_path)

# Convert 'Month' to a datetime object for proper sorting
data['Month'] = pd.to_datetime(data['Month'])

# Sort data by month
data = data.sort_values(by='Month')

# Prepare data for plotting
months = data['Month'].dt.strftime('%Y-%m')
case_counts = data['Average_Case_Count']
death_counts = data['Average_Death_Count']

# Create the bar charts
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Bar chart for Average Case Count
ax1.bar(months, case_counts, color='blue', alpha=0.7)
ax1.set_title('Monthly Average Case Count')
ax1.set_xlabel('Month')
ax1.set_ylabel('Average Case Count')
ax1.tick_params(axis='x', rotation=45)

# Bar chart for Average Death Count
ax2.bar(months, death_counts, color='red', alpha=0.7)
ax2.set_title('Monthly Average Death Count')
ax2.set_xlabel('Month')
ax2.set_ylabel('Average Death Count')
ax2.tick_params(axis='x', rotation=45)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig('monthly_averages.png')
plt.show()


