import os
api_key = os.getenv("SERPAPI_KEY")

# Directory to persist embeddings with ChromaDB
PERSIST_DIRECTORY = "./chroma_db"
