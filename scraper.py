import pandas as pd
import random
import requests
import os
from dotenv import load_dotenv

# Load the CSV file
def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"File loaded successfully. Columns available: {list(data.columns)}")
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Select a random column
def select_random_column(data):
    columns = list(data.columns)
    random_column = random.choice(columns)
    print(f"Randomly selected column: {random_column}")
    return random_column

# Perform web search using SerpAPI
def search_web(query, api_key):
    try:
        query = "Give me the name of director of " + query
        url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("organic_results", [])
        else:
            print(f"Error in search: {response.status_code}")
            return []
    except Exception as e:
        print(f"Search failed: {e}")
        return []

def get_raw_data():
    # File path
    load_dotenv()

    file_path = "example_input.csv"  # Replace with your actual file path
    api_key = os.getenv("SERPAPI_KEY")

    # Load CSV
    data = load_csv(file_path)
    if data is None:
        return

    if not file_path or not api_key:
        print("Error: Environment variables not set. Please check your .env file.")
        return

    # Load CSV
    data = load_csv(file_path)
    if data is None:
        return

    # Allow user to input the column name to select
    selected_column = input(f"Enter the column name from {list(data.columns)} to search: ").strip()

    # Check if the column exists in the dataframe
    if selected_column not in data.columns:
        print(f"Error: Column '{selected_column}' not found in the CSV file.")
        return

    # Perform search for each value in the column
    # results = []
    # for value in data[selected_column]:
    #     print(f"Searching for: {value}")
    #     search_results = search_web(value, api_key)
    #     results.append({value: search_results})

    search_results = search_web("IIIT Hyderabad", api_key)
    print(search_results)

    return search_results
    # Print the results
    # for result in results:
    #     print(result)

