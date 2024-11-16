import os
# from dotenv import load_dotenv


# load_dotenv()
# Ensure your OpenAI API key is set in the environment variables.
# open_api_key = os.getenv("OPENAI_API_KEY")
# os.environ["OPENAI_API_KEY"] = api_key

api_key = os.getenv("SERPAPI_KEY")

# Directory to persist embeddings with ChromaDB
PERSIST_DIRECTORY = "./chroma_db"
