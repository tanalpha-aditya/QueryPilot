"""
App for processing data from CSV files or Google Sheets using query templates.
Features:
1. Preview data from CSV/Google Sheets.
2. Process data based on query templates.
3. Download processed CSV or update Google Sheets.
"""

import gradio as gr
from modules.data_processor import (
    process_query_and_update_csv,
    extract_column_name,
    process_query_and_update_sheets,
)
from modules.gsheet_handler import fetch_google_sheet_data, update_google_sheet
import pandas as pd
import tempfile


def preview_columns(file=None, credentials=None, sheet_id=None, sheet_name=None):
    """
    Preview the first few rows and column names of a CSV file or Google Sheet.
    
    Args:
        file: The uploaded CSV file object.
        credentials: The uploaded Google Service Account credentials file.
        sheet_id: The Google Sheet ID.
        sheet_name: The name of the specific worksheet/tab in the Google Sheet.

    Returns:
        A tuple containing:
        - DataFrame preview (or error message as string).
        - List of column names (or empty list if an error occurs).
    """
    try:
        if file:
            df = pd.read_csv(file.name)
        elif credentials and sheet_id and sheet_name:
            df = fetch_google_sheet_data(credentials.name, sheet_id, sheet_name)
        else:
            return "No data source provided", []

        return df.head(), list(df.columns)
    except Exception as e:
        return str(e), []


def process_data(file=None, credentials=None, sheet_id=None, sheet_name=None, query_template=None):
    """
    Process data from a CSV file or Google Sheet using a query template.
    
    Args:
        file: The uploaded CSV file object.
        credentials: The uploaded Google Service Account credentials file.
        sheet_id: The Google Sheet ID.
        sheet_name: The name of the specific worksheet/tab in the Google Sheet.
        query_template: A template query string for processing data.

    Returns:
        A tuple containing:
        - Processed DataFrame (or empty DataFrame on error).
        - Path to the temporary CSV file (or error message as string).
    """
    try:
        if file:
            updated_df = process_query_and_update_csv(file.name, query_template)
        elif credentials and sheet_id and sheet_name:
            df = fetch_google_sheet_data(credentials.name, sheet_id, sheet_name)
            updated_df = process_query_and_update_sheets(credentials.name, df, query_template)
        else:
            return pd.DataFrame(), "No data source provided"
        
        # Write DataFrame to a temporary file for download
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        updated_df.to_csv(temp_file.name, index=False)
        return updated_df, temp_file.name
    except Exception as e:
        return pd.DataFrame(), str(e)


def update_sheet(credentials, sheet_id, sheet_name, processed_df):
    """
    Update the specified Google Sheet with processed data.
    
    Args:
        credentials: The uploaded Google Service Account credentials file.
        sheet_id: The Google Sheet ID.
        sheet_name: The name of the specific worksheet/tab in the Google Sheet.
        processed_df: The DataFrame containing processed data.

    Returns:
        A success message or error message as a string.
    """
    try:
        update_google_sheet(credentials.name, sheet_id, sheet_name, processed_df)
        return "Google Sheet updated successfully!"
    except Exception as e:
        return str(e)


def build_csv_tab():
    """
    Build the CSV File tab UI in Gradio.

    Returns:
        A Gradio TabItem for CSV File operations.
    """
    with gr.TabItem("CSV File"):
        gr.Markdown("""
                ## **CSV File Operations**
                1. Upload a CSV file to preview its columns and structure.
                2. Enter a query template using placeholders like `{ColumnName}` to extract or modify data.
                3. Process the CSV and download the updated file.
                **Sample Query Template**:  
                `Get me the name of the CEO of {Company}`  
                Replace `{Company}` with the column name containing company names.
                """)

        csv_file = gr.File(label="Upload CSV File")
        query_template_csv = gr.Textbox(label="CSV Query Template (e.g., 'Get me the name of CEO of {Company}')")
        with gr.Row():
            preview_button_csv = gr.Button("Preview Columns")
            process_button_csv = gr.Button("Process Queries")

        preview_output_csv = gr.Dataframe(label="CSV Data Preview")
        processed_output_csv = gr.Dataframe(label="Processed CSV Data")
        download_button_csv = gr.File(label="Download Processed CSV")

        preview_button_csv.click(
            preview_columns,
            inputs=[csv_file, gr.State(None), gr.State(None), gr.State(None)],
            outputs=[preview_output_csv, gr.State(None)],
        )
        process_button_csv.click(
            process_data,
            inputs=[csv_file, gr.State(None), gr.State(None), gr.State(None), query_template_csv],
            outputs=[processed_output_csv, download_button_csv],
        )


def build_google_sheets_tab():
    """
    Build the Google Sheets tab UI in Gradio.

    Returns:
        A Gradio TabItem for Google Sheets operations.
    """
    with gr.TabItem("Google Sheets"):
        gr.Markdown("""
                    ## **Google Sheets Operations**  
                    This section allows you to connect to a Google Sheet and perform data queries.
                    **Steps to Use**:
                    1. **Provide Google Service Account Credentials**:
                        - Create a Service Account in Google Cloud Console.
                        - Download the Service Account credentials as a JSON file.
                        - Share the Google Sheet with the Service Account's email (found in the JSON file under `client_email`).
                    2. **Enter the Google Sheet ID**:
                        - The Google Sheet ID is the part of the URL between `/d/` and `/edit`, for example:  
                        `https://docs.google.com/spreadsheets/d/<SheetID>/edit`
                    3. **Enter the Sheet Name**:
                        - This is the name of the specific worksheet (tab) within the Google Sheet, e.g., `Sheet1`.
                    **Example Input**:  
                    - Google Sheet ID: `1aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789`  
                    - Sheet Name: `SalesData`
                    **Sample Query Template**:  
                    `Get me the revenue of {Product}`  
                    Replace `{Product}` with the column name containing product names.
                    """)

        credentials = gr.File(label="Google Service Account Credentials (JSON)")
        sheet_id = gr.Textbox(label="Google Sheet ID")
        sheet_name = gr.Textbox(label="Google Sheet Name (e.g., Sheet1)")
        query_template_sheet = gr.Textbox(label="Query Template (e.g., 'Get me the name of CEO of {Company}')")
        with gr.Row():
            preview_button_sheet = gr.Button("Preview Columns")
            process_button_sheet = gr.Button("Process Queries")
            update_button = gr.Button("Update Google Sheet")

        preview_output_sheet = gr.Dataframe(label="Google Sheet Data Preview")
        processed_output_sheet = gr.Dataframe(label="Processed Google Sheet Data")
        download_button_sheet = gr.File(label="Download Processed CSV")
        update_status = gr.Textbox(label="Update Status", interactive=False)

        preview_button_sheet.click(
            preview_columns,
            inputs=[gr.State(None), credentials, sheet_id, sheet_name],
            outputs=[preview_output_sheet, gr.State(None)],
        )
        process_button_sheet.click(
            process_data,
            inputs=[gr.State(None), credentials, sheet_id, sheet_name, query_template_sheet],
            outputs=[processed_output_sheet, download_button_sheet],
        )
        update_button.click(
            update_sheet,
            inputs=[credentials, sheet_id, sheet_name, processed_output_sheet],
            outputs=[update_status],
        )


def gradio_app():
    """
    Build and launch the Gradio application.
    
    Returns:
        A Gradio app instance.
    """
    with gr.Blocks(theme=gr.themes.Citrus()) as app:
        gr.Markdown("""
        # CSV/Google Sheets Query Processor Agent
        This application allows you to:
        - Upload a CSV file or connect to a Google Sheet.
        - Preview the data to understand the structure and available columns.
        - Process the data by executing query templates that extract or manipulate information.
        - Download the processed data as a CSV file or update the Google Sheet directly.
                    
         **Note**:  
        This app uses my personal OpenAI API key and SERP API key, which have limited free API calls.  
        If the app does not work due to API limits, you can:
        1. Visit the [GitHub Repository](https://github.com/tanalpha-aditya/QueryPilot).
        2. Download the project.
        3. Use your own API keys to run it locally.
        For help setting up, refer to the documentation in the GitHub repository.
        """)

        with gr.Tabs():
            build_csv_tab()
            build_google_sheets_tab()

    return app


if __name__ == "__main__":
    app = gradio_app()
    app.launch()
