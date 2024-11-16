import re
import pandas as pd
from modules.scraper import get_raw_data
from modules.embedding_storage import process_safety_with_chroma
from modules.qa_chatbot import create_chatbot, ask_question

def extract_column_name(query_template):
    """
    Extract the column name from the query template enclosed in curly braces.
    """
    match = re.search(r"\{(.*?)\}", query_template)
    if not match:
        raise ValueError("No placeholder found in the query template. Ensure the query contains a placeholder like {column_name}.")
    return match.group(1)

def process_query_and_update_csv(file_path, query_template):
    """
    Processes the queries based on the specified column, updates the CSV file, 
    and adds an 'Answer' column with responses.
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
