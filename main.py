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

def process_query_with_dynamic_column(file_path, query_template):
    # Extract the column name from the query template
    column_name = extract_column_name(query_template)
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    if column_name not in df.columns:
        raise ValueError(f"The specified column '{column_name}' is missing in the provided CSV file.")
    
    # Extract unique values from the column
    values = df[column_name].unique()
    
    # Iterate through values and replace placeholders
    results = []
    for value in values:
        query = query_template.replace(f"{{{column_name}}}", str(value))
        print("Processing query:", query)
        raw_data = get_raw_data(file_path, query)
        # print("Raw data:", raw_data)
        vector_store = process_safety_with_chroma(raw_data)
        qa_system = create_chatbot(vector_store)

        # Create a prompt
        prompt = f"Give me the answer for this below query '{query}' from the content provided. The content always contains the answer."
        answer = ask_question(qa_system, prompt)
        
        results.append({column_name: value, "Answer": answer})
    
    return results

# Input parameters
file_path = "example_input.csv"
query_template = "Get me the customer care phone number of {Company}"  # Template with placeholder

# Process and display results
answers = process_query_with_dynamic_column(file_path, query_template)
for result in answers:
    # print(f"{list(result.keys())[0].capitalize()}: {result[list(result.keys())[0]]}")
    print(f"{result['Answer']}")
    print("-" * 40)
