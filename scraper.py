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

# Perform web search using SerpAPI
def search_web(query, api_key):
    try:
        # query = "Give me the name of director of " + query
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

def get_raw_data(file_path, query):
    # File path
    load_dotenv()

    # file_path = "example_input.csv"  # Replace with your actual file path
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

    search_results = search_web(query, api_key)
    # print(search_results)

    return search_results
    # Print the results
    # for result in results:
    #     print(result)

