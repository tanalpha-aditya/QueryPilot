from scraper import get_raw_data
from embedding_storage import process_safety_with_chroma
from qa_chatbot import create_chatbot, ask_question

query = "give me the name of director of IIIT Hyderabad"
raw_data = get_raw_data()
vector_store = process_safety_with_chroma(raw_data)
qa_system = create_chatbot(vector_store)

prompt = "Give me the exact answer for this below query " + query + " in a structured format with a link from the content provided only."
answer = ask_question(qa_system, prompt)

print( answer )