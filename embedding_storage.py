from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os

from config import PERSIST_DIRECTORY

def process_safety_with_chroma(data):
    """
    Processes and stores the given structured JSON data into ChromaDB.
    Args:
        data (list): A list of dictionaries containing structured JSON data.
    Returns:
        Chroma: The Chroma vector store object.
    """
    if os.path.exists(PERSIST_DIRECTORY):
        vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=OpenAIEmbeddings())
    else:
        documents = []
        
        for item in data:
            # Extract fields from the JSON structure
            content = item.get("snippet", "")
            highlighted_words = item.get("snippet_highlighted_words", [])
            metadata = {
                "position": item.get("position"),
                "title": item.get("title"),
                "link": item.get("link"),
                "source": item.get("source"),
                "displayed_link": item.get("displayed_link"),
                # Flatten highlighted_words list into a comma-separated string
                "highlighted_words": ", ".join(highlighted_words) if isinstance(highlighted_words, list) else highlighted_words
            }
            # Create a document for each snippet
            if content:
                documents.append(Document(page_content=content, metadata=metadata))
        # Initialize embeddings and Chroma store
        embeddings = OpenAIEmbeddings()
        vector_store = Chroma.from_documents(documents, embeddings, persist_directory=PERSIST_DIRECTORY)

    return vector_store
