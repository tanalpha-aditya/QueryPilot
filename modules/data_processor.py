"""
Data Processor Module

This module provides functions to process data from CSV files or Google Sheets based on 
a query template. The processed data includes adding an 'Answer' column with responses 
generated from a query-answering system.

Functions:
- extract_column_name: Extracts column names from a query template.
- process_query_and_update_csv: Processes queries in a CSV file and updates it.
- process_query_and_update_sheets: Processes queries in a Google Sheet and returns the updated DataFrame.
"""

import re
import pandas as pd
from modules.scraper import get_raw_data, get_raw_data_sheets
from modules.embedding_storage import process_safety_with_chroma
from modules.qa_chatbot import create_chatbot, ask_question


def extract_column_name(query_template):
    """
    Extract the column name from the query template enclosed in curly braces.

    Args:
        query_template (str): The query template containing a placeholder like {column_name}.

    Returns:
        str: The extracted column name.

    Raises:
        ValueError: If no placeholder is found in the query template.
    """
    match = re.search(r"\{(.*?)\}", query_template)
    if not match:
        raise ValueError("No placeholder found in the query template. Ensure the query contains a placeholder like {column_name}.")
    return match.group(1)


def process_query_and_update_csv(file_path, query_template):
    """
    Process queries in a CSV file and update it by adding an 'Answer' column.

    Args:
        file_path (str): Path to the CSV file to be processed.
        query_template (str): The query template containing a placeholder for column names.

    Returns:
        pd.DataFrame: The updated DataFrame with the 'Answer' column.

    Raises:
        ValueError: If the specified column is missing from the CSV file.
    """
    column_name = extract_column_name(query_template)
    df = pd.read_csv(file_path)
    
    if column_name not in df.columns:
        raise ValueError(f"The specified column '{column_name}' is missing in the provided CSV file.")
    
    if "Answer" not in df.columns:
        df["Answer"] = ""

    for index, row in df.iterrows():
        value = row[column_name]
        query = query_template.replace(f"{{{column_name}}}", str(value))
        
        # Process the query using provided functions
        raw_data = get_raw_data(file_path, query)
        vector_store = process_safety_with_chroma(raw_data)
        qa_system = create_chatbot(vector_store)
        prompt = f"Give me the exact answer for this below query '{query}' in a structured format with a link from the content provided only."
        answer = ask_question(qa_system, prompt)
        df.at[index, "Answer"] = answer

    df.to_csv(file_path, index=False)
    return df


def process_query_and_update_sheets(file_path, df, query_template):
    """
    Process queries in a Google Sheet and update the DataFrame by adding an 'Answer' column.

    Args:
        file_path (str): Path to the temporary file (not used directly here).
        df (pd.DataFrame): The DataFrame representing Google Sheet data.
        query_template (str): The query template containing a placeholder for column names.

    Returns:
        pd.DataFrame: The updated DataFrame with the 'Answer' column.

    Raises:
        ValueError: If the specified column is missing from the DataFrame.
    """
    column_name = extract_column_name(query_template)
    
    if column_name not in df.columns:
        raise ValueError(f"The specified column '{column_name}' is missing in the provided Google Sheet data.")
    
    if "Answer" not in df.columns:
        df["Answer"] = ""

    for index, row in df.iterrows():
        value = row[column_name]
        query = query_template.replace(f"{{{column_name}}}", str(value))
        
        # Process the query using provided functions
        raw_data = get_raw_data_sheets(query)
        vector_store = process_safety_with_chroma(raw_data)
        qa_system = create_chatbot(vector_store)
        prompt = f"Give me the exact answer for this below query '{query}' in a structured format with a link from the content provided only."
        answer = ask_question(qa_system, prompt)
        df.at[index, "Answer"] = answer
    
    return df
