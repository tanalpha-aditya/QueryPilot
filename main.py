import re
import pandas as pd
from scraper import get_raw_data
from embedding_storage import process_safety_with_chroma
from qa_chatbot import create_chatbot, ask_question

def extract_column_name(query_template):
    # Use regex to extract the column name inside curly braces
    match = re.search(r"\{(.*?)\}", query_template)
    if not match:
        raise ValueError("No placeholder found in the query template. Ensure the query contains a placeholder like {column_name}.")
    return match.group(1)

def process_query_and_update_csv(file_path, query_template):
    # Extract the column name from the query template
    column_name = extract_column_name(query_template)
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    if column_name not in df.columns:
        raise ValueError(f"The specified column '{column_name}' is missing in the provided CSV file.")
    
    # Ensure an "Answer" column exists or create it
    if "Answer" not in df.columns:
        df["Answer"] = ""

    # Iterate through rows to process queries
    for index, row in df.iterrows():
        value = row[column_name]
        query = query_template.replace(f"{{{column_name}}}", str(value))
        
        # Process the query
        raw_data = get_raw_data(file_path, query)
        vector_store = process_safety_with_chroma(raw_data)
        qa_system = create_chatbot(vector_store)

        # Create a prompt
        prompt = f"Give me the exact answer for this below query '{query}' in a structured format with a link from the content provided only."
        answer = ask_question(qa_system, prompt)

        # Update the "Answer" column
        df.at[index, "Answer"] = answer

    # Save the updated DataFrame back to the same CSV file
    df.to_csv(file_path, index=False)
    print(f"CSV file updated successfully with answers in the 'Answer' column.")

# Input parameters
file_path = "example_input.csv"
query_template = "Get me the name of CEO of {Company}"  # Template with placeholder

# Process and update the CSV file
process_query_and_update_csv(file_path, query_template)
