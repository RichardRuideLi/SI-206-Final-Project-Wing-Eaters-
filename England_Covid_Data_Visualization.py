import pandas as pd
import matplotlib.pyplot as plt

# Load the uploaded CSV files
weekly_averages_file = "England_Average_Covid_Weekly_Death.csv"
season_reference_file = "season_reference.csv"

# Read the CSV files into DataFrames
weekly_averages_df = pd.read_csv(weekly_averages_file)
season_reference_df = pd.read_csv(season_reference_file)

# Merge the weekly averages with the season reference table using season_id
merged_df = pd.merge(weekly_averages_df, season_reference_df, on="season_id")

# Ensure the 'month_name' column is ordered correctly
months_order = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]
merged_df['month_name'] = pd.Categorical(merged_df['month_name'], categories=months_order, ordered=True)

# Create a new column for x-axis labels: "Year, Month"
merged_df['year_month'] = merged_df['year'].astype(str) + ", " + merged_df['month_name'].astype(str)

# Sort the DataFrame by year and month
merged_df = merged_df.sort_values(['year', 'month_name'])

# Assign a color for each season
season_colors = {
    "Winter": "blue",
    "Spring": "green",
    "Summer": "orange",
    "Fall": "brown"
}
merged_df['color'] = merged_df['season_name'].map(season_colors)

# Visualization with Matplotlib
plt.figure(figsize=(16, 8))
plt.bar(
    merged_df['year_month'], 
    merged_df['weekly_average'], 
    color=merged_df['color']
)

# Add title and labels
plt.title("England Average Weekly Deaths from Covid by Year and Month (Season Highlighted)", fontsize=16)
plt.xlabel("Year, Month", fontsize=12)
plt.ylabel("Average Weekly Deaths", fontsize=12)

# Rotate x-axis labels for readability
plt.xticks(rotation=90)

# Add a legend for seasons
legend_labels = list(season_colors.keys())
legend_colors = list(season_colors.values())
patches = [plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors]
plt.legend(patches, legend_labels, title="Season")

# Adjust layout and save the figure
plt.tight_layout()
output_file = "England_Average_Weekly_Covid_Deaths.png"
plt.savefig(output_file)
plt.show()

output_file
