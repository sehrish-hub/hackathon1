# Quickstart Guide: RAG Ingestion

## Overview
This guide will help you set up and run the RAG ingestion pipeline to extract content from Docusaurus websites, generate embeddings, and store them in Qdrant.

## Prerequisites
- Python 3.10 or higher
- UV package manager
- Cohere API key
- Qdrant Cloud endpoint and API key

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Navigate to Backend Directory
```bash
cd backend
```

### 3. Install Dependencies with UV
```bash
uv venv  # Create virtual environment
source .venv/bin/activate  # Activate virtual environment (Linux/Mac)
# OR
.venv\Scripts\activate  # Activate virtual environment (Windows)
uv pip install cohere qdrant-client requests beautifulsoup4 python-dotenv
```

### 4. Configure Environment Variables
Create a `.env` file in the backend directory with the following content:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
DOCUSAURUS_URLS=https://your-docusaurus-site.com/docs/intro,https://your-docusaurus-site.com/docs/setup
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
QDRANT_COLLECTION_NAME=book_content
```

### 5. Run the Ingestion Pipeline
```bash
python main.py
```

## Configuration Options

### Environment Variables
- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: Your Qdrant Cloud endpoint URL
- `QDRANT_API_KEY`: Your Qdrant Cloud API key
- `DOCUSAURUS_URLS`: Comma-separated list of Docusaurus URLs to process
- `CHUNK_SIZE`: Size of text chunks in characters (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks in characters (default: 200)
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: book_content)

## Expected Output
When the pipeline runs successfully, you should see:
1. Content extracted from each URL
2. Text chunks created with specified size and overlap
3. Embeddings generated for each chunk
4. Vectors stored in Qdrant with metadata
5. Verification query results showing successful storage

## Troubleshooting

### Common Issues
1. **API Key Errors**: Verify your Cohere and Qdrant API keys are correct
2. **URL Access Issues**: Ensure the Docusaurus URLs are publicly accessible
3. **Qdrant Connection**: Check that your Qdrant endpoint and credentials are correct

### Logging
The pipeline logs progress and errors to help with debugging. Check the console output for detailed information.