import pandas as pd
import matplotlib.pyplot as plt

# CSV file with calculated weekly averages
CSV_FILE = "weekly_averages_with_join.csv"

def visualize_by_season_and_month():
    """
    Visualize weekly averages of deaths, with bar color representing seasons,
    and x-axis showing year and month (e.g., 2024, January).
    """
    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv(CSV_FILE)

    # Ensure the 'month_name' column is ordered correctly
    months_order = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    df['month_name'] = pd.Categorical(df['month_name'], categories=months_order, ordered=True)

    # Create a new column for x-axis labels: "Year, Month"
    df['year_month'] = df['year'].astype(str) + ", " + df['month_name'].astype(str)

    # Sort the DataFrame by year and month
    df = df.sort_values(['year', 'month_name'])

    # Assign a color for each season
    season_colors = {
        "Winter": "blue",
        "Spring": "green",
        "Summer": "orange",
        "Fall": "brown"
    }
    df['color'] = df['season'].map(season_colors)

    # Visualization with Matplotlib
    plt.figure(figsize=(16, 8))
    plt.bar(
        df['year_month'], 
        df['weekly_average'], 
        color=df['color']
    )

    # Add title and labels
    plt.title("Weekly Averages of Deaths from Covidi by Year and Month (Season Highlighted)", fontsize=16)
    plt.xlabel("Year, Month", fontsize=12)
    plt.ylabel("Weekly Average Deaths", fontsize=12)

    # Rotate x-axis labels for readability
    plt.xticks(rotation=90)

    # Add a legend for seasons
    legend_labels = list(season_colors.keys())
    legend_colors = list(season_colors.values())
    patches = [plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors]
    plt.legend(patches, legend_labels, title="Season")

    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig("weekly_averages_visualization_by_season.png")
    print("Visualization has been saved to 'weekly_averages_visualization_by_season.png'.")
    plt.show()

if __name__ == "__main__":
    visualize_by_season_and_month()

