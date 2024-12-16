
import sqlite3
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

def save_monthly_averages_to_csv():
    """
    Saves monthly averages (from the SQLite database) to a CSV file and plots them.
    """
    try:
        # Connect to the database
        print("Connecting to the database...")
        conn = sqlite3.connect('covid_data.db')
        cursor = conn.cursor()
        
        # Fetch monthly average data
        print("Fetching monthly average data from the database...")
        cursor.execute('''
        SELECT 
            SUBSTR(date, 1, 7) AS month, 
            AVG(cases) AS avg_cases,
            AVG(deaths) AS avg_deaths
        FROM 
            covid_cases
        GROUP BY 
            month
        ORDER BY 
            month ASC;
        ''')
        data = cursor.fetchall()

        # Check if data is retrieved
        if not data:
            print("No data found for monthly averages.")
            return

        # Close connection to the database
        conn.close()

        # Ensure the directory exists for saving the file
        output_directory = "C:/Users/natha/Downloads/SI206/Final Final"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Prepare data for CSV
        csv_file_path = os.path.join(output_directory, "monthly_averages.csv")
        
        # Write to CSV file
        print(f"Writing data to {csv_file_path}...")
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Month", "Average Cases", "Average Deaths"])  # Header row
            writer.writerows(data)  # Data rows
        
        print(f"Monthly averages saved to {csv_file_path}")

        # Convert the data into a pandas DataFrame for plotting
        df = pd.DataFrame(data, columns=["Month", "Average Cases", "Average Deaths"])

        # Convert 'Month' column to datetime format for easier plotting
        df['Month'] = pd.to_datetime(df['Month'])

        # Plotting the monthly averages
        plt.figure(figsize=(12, 6))

        # Plot Average Cases and Average Deaths on the same graph
        plt.plot(df['Month'], df['Average Cases'], label='Average Cases', color='blue', marker='o', linestyle='-')
        plt.plot(df['Month'], df['Average Deaths'], label='Average Deaths', color='red', marker='o', linestyle='--')

        # Add labels, title, and legend
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Average Covid Count', fontsize=12)
        plt.title('Monthly Average COVID-19 Cases and Deaths', fontsize=14)
        plt.xticks(rotation=45, fontsize=10)
        plt.legend(fontsize=10)

        # Show the plot
        plt.tight_layout()
        plt.show()

    except sqlite3.Error as db_error:
        print(f"Database error occurred: {db_error}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
save_monthly_averages_to_csv()

