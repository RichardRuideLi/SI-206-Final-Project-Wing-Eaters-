import csv

def save_yearly_averages_to_files(yearly_data):
    """
    Saves yearly averages to both a CSV file and a plain text file.

    Args:
        yearly_data (dict): A dictionary where keys are years and values are dictionaries
                           with 'avg_cases' and 'avg_deaths'.

    Output:
        Creates two files:
            - my_yearly_averages.csv
            - my_yearly_averages.txt
    """
    # Prepare data for CSV
    csv_data = [["Year", "Avg Cases", "Avg Deaths"]]  # Header row
    for year, stats in yearly_data.items():
        csv_data.append([year, stats['avg_cases'], stats['avg_deaths']])

    # Write to CSV file
    csv_file_path = "my_yearly_averages.csv"
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_data)
    print(f"CSV file generated: {csv_file_path}")

    # Write to Text file
    text_file_path = "my_yearly_averages.txt"
    with open(text_file_path, 'w') as text_file:
        # Write header
        text_file.write(f"{'Year':<6}{'Avg Cases':<15}{'Avg Deaths':<15}\n")
        text_file.write("=" * 36 + "\n")

        # Write each year's data
        for year, stats in yearly_data.items():
            text_file.write(f"{year:<6}{stats['avg_cases']:<15.2f}{stats['avg_deaths']:<15.2f}\n")
    print(f"Text file generated: {text_file_path}")

# Example usage
yearly_data = {
    2021: {"avg_cases": 1326815.34, "avg_deaths": 24075.54},
    2022: {"avg_cases": 3095589.36, "avg_deaths": 32198.62},
    2023: {"avg_cases": 3710586.00, "avg_deaths": 35545.00}
}

save_yearly_averages_to_files(yearly_data)

