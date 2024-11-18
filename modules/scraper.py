"""
Web Scraper Module

This module provides functionality to perform web searches using the SerpAPI and load data from CSV files.
It includes methods to handle raw data for both CSV files and Google Sheets.

Functions:
- load_csv: Loads a CSV file and returns its contents as a pandas DataFrame.
- search_web: Performs a web search using SerpAPI and returns organic results.
- get_raw_data: Fetches raw search results for a query using data from a CSV file.
- get_raw_data_sheets: Fetches raw search results for a query for Google Sheets data.
"""

import pandas as pd
import requests
import os
from dotenv import load_dotenv


def load_csv(file_path):
    """
    Loads a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the CSV data, or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"File loaded successfully. Columns available: {list(data.columns)}")
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None


def search_web(query, api_key):
    """
    Performs a web search using SerpAPI and retrieves organic search results.

    Args:
        query (str): The search query.
        api_key (str): The API key for SerpAPI.

    Returns:
        list: A list of organic search results. Returns an empty list if an error occurs.
    """
    try:
        url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("organic_results", [])
        else:
            print(f"Error in search: HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"Search failed: {e}")
        return []


def get_raw_data(file_path, query):
    """
    Fetches raw search results for a given query using a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        query (str): The query string to search.

    Returns:
        list: A list of search results. Returns None if an error occurs.
    """
    load_dotenv()
    api_key = os.getenv("SERPAPI_KEY")

    if not file_path or not api_key:
        print("Error: Environment variables not set. Please check your .env file.")
        return None

    # Load the CSV file
    data = load_csv(file_path)
    if data is None:
        return None

    # Perform the web search
    search_results = search_web(query, api_key)
    return search_results


def get_raw_data_sheets(query):
    """
    Fetches raw search results for a given query for Google Sheets data.

    Args:
        query (str): The query string to search.

    Returns:
        list: A list of search results. Returns None if an error occurs.
    """
    load_dotenv()
    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        print("Error: Environment variables not set. Please check your .env file.")
        return None

    # Perform the web search
    search_results = search_web(query, api_key)
    return search_results
