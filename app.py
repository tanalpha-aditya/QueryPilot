import gradio as gr
from modules.data_processor import process_query_and_update_csv, extract_column_name, process_query_and_update_sheets
from modules.gsheet_handler import fetch_google_sheet_data, update_google_sheet
import pandas as pd
import tempfile
from google.oauth2.service_account import Credentials
import json
import gspread

def preview_columns(file=None, credentials=None, sheet_id=None, sheet_name=None):
    """
    Preview columns from the uploaded CSV file or Google Sheet.
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
    Process data using the provided query template and return the updated DataFrame and CSV file path.
    """
    try:
        if file:
            print(file.name)
            updated_df = process_query_and_update_csv(file.name, query_template)
        elif credentials and sheet_id and sheet_name:
            # credentials_path = credentials.name  # The file path for the credentials JSON
            
            # # Use gspread to authenticate and fetch the data
            # gc = gspread.service_account(credentials_path)  # Pass the path of the credentials file
            # print("Dddddddddd")
            # sh = gc.open_by_url(sheet_id)  # Open the Google Sheet by URL
            # worksheet = sh.worksheet(sheet_name)  # Access the specified worksheet
            
            # # Extract all values from the sheet
            # values = worksheet.get_all_values()
            # df = pd.DataFrame(values[1:], columns=values[0])
            # print(df)
            df = fetch_google_sheet_data(credentials.name, sheet_id, sheet_name)
            # Process the data with the query template
            # print(df)
            # print("krsghvkrgsnker")
            updated_df = process_query_and_update_sheets(credentials.name, df, query_template)
            # update_google_sheet(credentials.name, sheet_id, sheet_name, updated_df)
        else:
            return None, "No data source provided"
        
        # Write DataFrame to a temporary file for download
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        updated_df.to_csv(temp_file.name, index=False)
        return updated_df, temp_file.name  # Return DataFrame and file path
    except Exception as e:
        return pd.DataFrame(), str(e)
    
def update_sheet(credentials, sheet_id, sheet_name, processed_df):
    """
    Update the Google Sheet with the processed data.
    """
    try:
        update_google_sheet(credentials.name, sheet_id, sheet_name, processed_df)
        return "Google Sheet updated successfully!"
    except Exception as e:
        return str(e)
    
# Gradio Interface
def gradio_app():
    with gr.Blocks(theme=gr.themes.Citrus()) as app:
        gr.Markdown("### CSV/Google Sheets Query Processor Dashboard")

        # States to store independent data for CSV and Google Sheets
        csv_data_state = gr.State(None)  # To store CSV data
        sheet_data_state = gr.State(None)  # To store Google Sheets data

        with gr.Tabs():
            with gr.TabItem("CSV File"):
                csv_file = gr.File(label="Upload CSV File")
                query_template_csv = gr.Textbox(label="CSV Query Template (e.g., 'Get me the name of CEO of {Company}')")
                with gr.Row():
                    preview_button_csv = gr.Button("Preview Columns")
                    process_button_csv = gr.Button("Process Queries")

                preview_output_csv = gr.Dataframe(label="CSV Data Preview")
                processed_output_csv = gr.Dataframe(label="Processed CSV Data")
                download_button_csv = gr.File(label="Download Processed CSV")

            with gr.TabItem("Google Sheets"):
                credentials = gr.File(label="Google Service Account Credentials (JSON)")
                sheet_id = gr.Textbox(label="Google Sheet ID")
                sheet_name = gr.Textbox(label="Google Sheet Name (e.g., Sheet1)")
                query_template_sheet = gr.Textbox(label="Google Sheets Query Template (e.g., 'Get me the name of CEO of {Company}')")
                with gr.Row():
                    preview_button_sheet = gr.Button("Preview Columns")
                    process_button_sheet = gr.Button("Process Queries")
                    update_button = gr.Button("Update Google Sheet")

                preview_output_sheet = gr.Dataframe(label="Google Sheet Data Preview")
                processed_output_sheet = gr.Dataframe(label="Processed Google Sheet Data")
                download_button_sheet = gr.File(label="Download Processed CSV")
                update_status = gr.Textbox(label="Update Status", interactive=False)

        # Button Interactions for CSV
        preview_button_csv.click(
            preview_columns,
            inputs=[csv_file, gr.State(None), gr.State(None), gr.State(None)],  # Pass placeholders for unused inputs
            outputs=[preview_output_csv, csv_data_state],
        )
        process_button_csv.click(
            process_data,
            inputs=[csv_file, gr.State(None), gr.State(None), gr.State(None), query_template_csv],
            outputs=[processed_output_csv, download_button_csv],
        )

        # Button Interactions for Google Sheets
        preview_button_sheet.click(
            preview_columns,
            inputs=[gr.State(None), credentials, sheet_id, sheet_name],
            outputs=[preview_output_sheet, sheet_data_state],
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

    return app


if __name__ == "__main__":
    app = gradio_app()
    app.launch()
