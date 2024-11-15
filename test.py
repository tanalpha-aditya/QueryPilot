# Load environment variables from .env file
import os
from dotenv import load_dotenv
# load_dotenv()

# Check if the variables are loaded
file_path = os.getenv("FILE_PATH")
api_key = os.getenv("SERPAPI_KEY")

print(f"File path: {file_path}")  # Check if the file path is correctly loaded
print(f"API key: {api_key}") 