import matplotlib.pyplot as plt
import pandas as pd
import numpy as np  # Import numpy

# Load the data from the CSV file
def load_data():
    # Load the CSV into a pandas DataFrame
    data = pd.read_csv('cleaned_LA_County_COVID_Cases.csv')

    # Convert the 'date' column to datetime format for easier manipulation
    data['date'] = pd.to_datetime(data['date'])

    return data

# Calculate yearly averages for cases and deaths
def calculate_yearly_averages(data):
    # Group the data by year and calculate the average cases and deaths
    data['year'] = data['date'].dt.year  # Extract the year from the date
    yearly_data = data.groupby('year').agg({'cases': 'mean', 'deaths': 'mean'}).reset_index()
    
    return yearly_data

# Plot the yearly averages
def plot_yearly_averages(yearly_data):
    years = yearly_data['year']
    avg_cases = yearly_data['cases']
    avg_deaths = yearly_data['deaths']

    # Set the bar width and positions
    bar_width = 0.35
    x = np.arange(len(years))  # Use np.arange to create a numeric array

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    bar1 = ax.bar(x - bar_width / 2, avg_cases, bar_width, label='Avg Cases', color='skyblue')
    bar2 = ax.bar(x + bar_width / 2, avg_deaths, bar_width, label='Avg Deaths', color='orange')

    # Add labels, title, and legend
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average Covid Count', fontsize=12)
    ax.set_title('Yearly Averages of LA County Covid Cases and Deaths', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=10)
    ax.legend(fontsize=10)

    # Annotate bars with values
    for bars in [bar1, bar2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # Offset text above the bar
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    # Show the plot
    plt.tight_layout()
    plt.show()

# Main function to load data, calculate averages, and plot the chart
def main():
    data = load_data()  # Load the data from the CSV
    yearly_data = calculate_yearly_averages(data)  # Calculate yearly averages
    plot_yearly_averages(yearly_data)  # Plot the data

# Run the main function
if __name__ == "__main__":
    main()

