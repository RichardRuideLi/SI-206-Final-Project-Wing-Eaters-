import requests
import json

# Base URL of the API
BASE_URL = "https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/sub_themes/respiratory/topics/COVID-19/geography_types/Nation/geographies/England/metrics/COVID-19_deaths_ONSRegByWeek"

OUTPUT_FILE = "all_covid_deaths_data.json"

def fetch_all_pages(base_url):
    """
    Fetch all pages from a paginated API and combine the results into a single list.
    """
    all_results = []  # List to store all results
    current_url = base_url  # Start with the base URL

    while current_url:
        print(f"Fetching data from: {current_url}")
        try:
            # Send a GET request to the current URL
            response = requests.get(current_url)
            response.raise_for_status()  # Raise an error for invalid responses
            
            # Parse the response JSON
            data = response.json()
            
            # Add the results from the current page to the overall list
            results = data.get("results", [])
            all_results.extend(results)
            print(f"Fetched {len(results)} records. Total so far: {len(all_results)}")
            
            # Get the next page URL
            current_url = data.get("next")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break

    return all_results

def save_to_file(data, output_file):
    """
    Save the combined data to a JSON file.
    """
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)
    print(f"All data successfully saved to {output_file}.")

if __name__ == "__main__":
    # Fetch all pages and save to a file
    all_data = fetch_all_pages(BASE_URL)
    save_to_file(all_data, OUTPUT_FILE)