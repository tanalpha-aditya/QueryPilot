from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_chroma import Chroma

def create_chatbot(vector_store):
    """
    Creates a chatbot for querying the Chroma vector store.
    Args:
        vector_store (Chroma): The vector store to use.
    Returns:
        RetrievalQA: The QA chatbot object.
    """
    llm = OpenAI(temperature=0.5)
    retriever = vector_store.as_retriever(search_type="mmr", k=5)
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", 
        retriever=retriever,
        return_source_documents=True
    )
    return qa


def ask_question(qa, query):
    """
    Asks a question to the chatbot and returns the response.
    Args:
        qa (RetrievalQA): The QA chatbot object.
        query (str): The question to ask.
    Returns:
        str: The answer from the chatbot.
    """
    try:
        response = qa.invoke({"query": query})
        answer = response.get('result', 'No answer found.')
        return f"Answer: {answer}\n"
    except Exception as e:
        return f"Error: {e}"