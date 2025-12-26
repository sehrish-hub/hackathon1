# RAG Ingestion Pipeline

A backend data ingestion pipeline for extracting content from Docusaurus websites, generating embeddings using Cohere, and storing them in Qdrant vector database for RAG applications.

## Features

- Crawls and extracts clean text content from Docusaurus websites
- Chunks text with configurable size and overlap
- Generates semantic embeddings using Cohere embedding models
- Stores embeddings with metadata in Qdrant Cloud
- Includes verification queries to test stored vectors
- Comprehensive error handling and logging
- Command-line interface for easy execution

## Prerequisites

- Python 3.10+
- UV package manager
- Cohere API key
- Qdrant Cloud endpoint and API key

## Installation

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies using UV:

```bash
uv venv  # Create virtual environment
source .venv/bin/activate  # Activate virtual environment (Linux/Mac)
# OR
.venv\Scripts\activate  # Activate virtual environment (Windows)
uv pip install cohere qdrant-client requests beautifulsoup4 python-dotenv
```

## Configuration

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

## Usage

### Command Line Interface

```bash
# Run with default configuration
python main.py

# Run with specific URLs
python main.py --urls "https://example.com/page1,https://example.com/page2"

# Enable verbose logging
python main.py --verbose
```

### As a Module

```python
from main import main

success = main()
```

## Architecture

The pipeline follows these steps:

1. **Content Extraction**: Crawls provided URLs and extracts clean text content
2. **Text Chunking**: Splits content into configurable chunks with overlap
3. **Embedding Generation**: Creates semantic embeddings using Cohere
4. **Vector Storage**: Stores embeddings in Qdrant with metadata
5. **Verification**: Tests stored vectors with sample queries

## Data Models

### ContentDocument
- `source_url`: Original URL of the content
- `content_text`: Extracted text content
- `section_title`: Section title from the page
- `chunk_id`: Unique identifier for the chunk

### EmbeddingVector
- `vector_data`: The embedding vector from Cohere
- `document_id`: Reference to the source document
- `metadata`: Associated metadata including URL, chunk_id, section_title
- `embedding_model`: The model used to generate the embedding

### ProcessingJob
- `job_id`: Unique identifier for the processing job
- `urls`: List of URLs to process
- `status`: Current status (pending, in_progress, completed, failed)
- `start_time`: When the job started
- `end_time`: When the job completed
- `processed_count`: Number of URLs successfully processed
- `failed_count`: Number of URLs that failed to process

## Error Handling

The pipeline includes comprehensive error handling:

- Retry mechanisms for URL requests (up to 3 attempts)
- Retry mechanisms for embedding generation (up to 3 attempts)
- Retry mechanisms for Qdrant operations (up to 3 attempts)
- Detailed logging for debugging
- Graceful degradation when individual components fail

## Verification

After ingestion, the pipeline runs a verification query to ensure vectors were stored correctly. You can also manually test vector retrieval using the Qdrant client.

## Performance Considerations

- Text chunking preserves sentence boundaries where possible
- Overlap between chunks maintains context
- Memory usage is optimized for large content sets
- Parallel processing is used where appropriate