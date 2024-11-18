"""
Google Sheets Handler Module

This module provides utilities for interacting with Google Sheets using the Google Sheets API.
It includes functionalities to fetch data into a pandas DataFrame and update a sheet with processed data.

Functions:
- fetch_google_sheet_data: Fetches data from a specified Google Sheet into a pandas DataFrame.
- update_google_sheet: Updates a Google Sheet with data from a pandas DataFrame.
"""

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd


def fetch_google_sheet_data(credentials_file, sheet_id, sheet_name):
    """
    Fetches data from a specified Google Sheet and returns it as a pandas DataFrame.

    Args:
        credentials_file (str): Path to the Google Service Account credentials JSON file.
        sheet_id (str): The ID of the Google Sheet.
        sheet_name (str): The name of the worksheet (tab) within the Google Sheet.

    Returns:
        pd.DataFrame: A DataFrame containing the data from the Google Sheet.
                      Returns an empty DataFrame if no data is found.
    
    Raises:
        FileNotFoundError: If the credentials file is not found.
        google.auth.exceptions.GoogleAuthError: If authentication fails.
        Exception: For any other errors encountered during the API call.
    """
    try:
        # Authenticate using the Service Account credentials
        creds = Credentials.from_service_account_file(
            credentials_file, 
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Fetch data from the specified range
        result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
        data = result.get('values', [])

        if not data:
            return pd.DataFrame()  # Return an empty DataFrame if no data is found

        # Extract headers and rows
        headers = data[0]
        rows = data[1:]
        return pd.DataFrame(rows, columns=headers)
    except Exception as e:
        raise Exception(f"Error fetching data from Google Sheet: {str(e)}")


def update_google_sheet(credentials_file, sheet_id, sheet_name, df):
    """
    Updates a specified Google Sheet with data from a pandas DataFrame.

    Args:
        credentials_file (str): Path to the Google Service Account credentials JSON file.
        sheet_id (str): The ID of the Google Sheet.
        sheet_name (str): The name of the worksheet (tab) within the Google Sheet.
        df (pd.DataFrame): The DataFrame containing data to write into the sheet.

    Returns:
        str: Success message if the update is successful.
    
    Raises:
        FileNotFoundError: If the credentials file is not found.
        google.auth.exceptions.GoogleAuthError: If authentication fails.
        Exception: For any other errors encountered during the API call.
    """
    try:
        # Authenticate using the Service Account credentials
        creds = Credentials.from_service_account_file(
            credentials_file, 
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Convert DataFrame to list of lists (required format for Google Sheets API)
        data = [df.columns.tolist()] + df.values.tolist()

        # Prepare the request body for updating the sheet
        body = {'values': data}

        # Perform the update
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=sheet_name,
            valueInputOption="RAW",
            body=body
        ).execute()

        return "Google Sheet updated successfully."
    except Exception as e:
        raise Exception(f"Error updating Google Sheet: {str(e)}")
