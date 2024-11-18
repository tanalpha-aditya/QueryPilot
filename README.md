
# QueryPilot 

## Project Title: AI Agent for Automated Data Retrieval and Parsing

This project demonstrates an **AI-powered agent** designed to process datasets, conduct automated web searches, and extract specific information based on user-defined queries. A simple and intuitive dashboard facilitates user interactions, including file uploads, query definitions, and viewing/downloading results.

---

## Features

1. **File Upload and Preview**:
   - Supports uploading **CSV files** or linking **Google Sheets**.
   - Displays available columns for user selection.

2. **Dynamic Query Input**:
   - Custom prompt templates with placeholders (e.g., `{entity}`).
   - Automatically integrates user-defined queries for automated searches.

3. **Automated Web Search**:
   - Leverages APIs like SerpAPI for reliable and rate-limited web searches.
   - Processes and stores search results for further analysis.

4. **LLM Integration**:
   - Parses web search results using a Language Model (e.g., OpenAI GPT).
   - Extracts user-requested information with high accuracy.

5. **Data Presentation and Export**:
   - Displays results in a user-friendly table format.
   - Offers download options (e.g., CSV) or integration with Google Sheets.

6. **Error Handling**:
   - Includes mechanisms for API rate limits and query failures.
   - Notifies users of incomplete operations.

---

## Installation

### Prerequisites

1. **Python 3.8+**
2. Recommended environment: `virtualenv` or `conda`

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/tanalpha-aditya/QueryPilot.git
cd QueryPilot
```

---

### Step 2: Install Dependencies
Install required libraries using the provided `requirements.txt` file:
```bash
pip install -r requirements.txt
```

---

### Step 3: Set Up Environment Variables
Create a `.env` file in the project root with your API keys:
```dotenv
SERP_API_KEY=your_serp_api_key
OPENAI_API_KEY=your_openai_api_key
```

---

### Step 4: Run the Application
To start the application:
```bash
python3 app.py
```

The dashboard will be accessible at `http://127.0.0.1:7860`.

---

## Requirements

### File: `requirements.txt`
```txt

gradio
pandas
google-api-python-client
google-auth
gspread
langchain
langchain-openai
langchain-chroma
requests
python-dotenv

```

---

## Hosted Version ( Additional )

Try the application hosted on **Hugging Face Spaces**:  
Note : Do not input large excel files for testing or else my free monthly credits will finish :p. 
[Query-Pilot on Hugging Face Spaces](https://huggingface.co/spaces/raghuv-aditya/Query-Pilot)

---

## Usage Instructions

1. **Upload a CSV File or Connect it with Google service account**:
   - Click on "Upload File" and select your dataset.
   - Preview and select the target column for queries.

2. **Define a Query**:
   - Input a query using placeholders (e.g., `Get the email of {company}`).

3. **Process Data**:
   - Run the query to retrieve and extract data.

4. **Download Results**:
   - Save results locally as a CSV or update connected Google Sheets.

---

## Loom Video Walkthrough
Watch the walkthrough video: [Loom Video Link](https://loom.com/share/your-video-id)

---

## Optional Features Implemented

- **Advanced Query Templates**: Multiple fields in a single query. ( yet to implement )
- **Google Sheets Output**: Update extracted data directly to Sheets. 
- **Error Handling**: Comprehensive feedback for failed queries. 

---

## Contact and Support
For queries or feedback, contact me at [Aditya Raghuvanshi](mailto:tanalpha.aditya@gmail.com).

---

This project is part of the **BreakoutAI Assessment**.
