"""
Embedding Storage Module

This module processes structured JSON data into a Chroma vector store using LangChain's OpenAI embeddings.
It handles data formatting, text splitting, and metadata extraction before creating embeddings.

Functions:
- process_safety_with_chroma: Converts JSON data into a Chroma vector store for efficient query handling.
"""

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from config import PERSIST_DIRECTORY


def process_safety_with_chroma(data):
    """
    Processes and stores the given structured JSON data into ChromaDB.

    Args:
        data (list): A list of dictionaries containing structured JSON data. 
            Each dictionary should include keys like 'snippet', 'snippet_highlighted_words', 'title', 'link', etc.

    Returns:
        Chroma: The Chroma vector store object containing the processed embeddings.

    Raises:
        ValueError: If the data list is empty or invalid.
    """
    if not data or not isinstance(data, list):
        raise ValueError("Invalid data provided. Expected a non-empty list of structured JSON dictionaries.")

    documents = []

    for item in data:
        # Extract content and highlighted words
        content = item.get("snippet", "")
        highlighted_words = item.get("snippet_highlighted_words", [])
        highlighted_words_str = ", ".join(highlighted_words) if isinstance(highlighted_words, list) else str(highlighted_words)

        # Create metadata dictionary for the document
        metadata = {
            "position": item.get("position"),
            "title": item.get("title"),
            "link": item.get("link"),
            "source": item.get("source"),
            "displayed_link": item.get("displayed_link"),
            "highlighted_words": highlighted_words_str,
        }

        # Append highlighted words to content if available
        if content:
            content += f" Highlighted words: {highlighted_words_str}" if highlighted_words_str else ""
            documents.append(Document(page_content=content, metadata=metadata))

    # Validate document creation
    if not documents:
        raise ValueError("No valid documents were created from the provided data.")

    # Initialize embeddings and Chroma store
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(documents, embeddings, persist_directory=PERSIST_DIRECTORY)

    return vector_store
