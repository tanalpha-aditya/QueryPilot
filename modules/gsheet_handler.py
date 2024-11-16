from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

def fetch_google_sheet_data(credentials_file, sheet_id, sheet_name):
    """
    Fetch data from Google Sheets.
    """
    try:
        creds = Credentials.from_service_account_file(credentials_file, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
        data = result.get('values', [])
        headers = data[0]
        rows = data[1:]
        return pd.DataFrame(rows, columns=headers)
    except Exception as e:
        return str(e)

def update_google_sheet(credentials_file, sheet_id, sheet_name, df):
    """
    Update Google Sheets with the processed data.
    """
    try:
        creds = Credentials.from_service_account_file(credentials_file, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Convert DataFrame to list of lists
        data = [df.columns.tolist()] + df.values.tolist()

        # Update the sheet
        body = {'values': data}
        sheet.values().update(
            spreadsheetId=sheet_id,
            range=sheet_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        return "Google Sheet updated successfully."
    except Exception as e:
        return str(e)
