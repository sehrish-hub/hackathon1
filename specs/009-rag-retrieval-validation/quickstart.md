# Quickstart: RAG Retrieval and Pipeline Validation

## Overview
This guide helps you quickly set up and run the RAG retrieval validation system to test similarity search against stored book content embeddings in Qdrant.

## Prerequisites
- Python 3.10+
- pip package manager
- Access to Qdrant Cloud instance with stored embeddings
- Cohere API key
- Environment with stored embeddings from the ingestion pipeline

## Setup

### 1. Install Dependencies
```bash
pip install cohere qdrant-client python-dotenv requests
```

### 2. Configure Environment Variables
Create a `.env` file in the backend directory with the following:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=book_content
```

### 3. Verify Qdrant Collection
Ensure the Qdrant collection exists and contains stored embeddings from the ingestion pipeline.

## Usage

### Run the Retrieval Validation
```bash
cd backend
python retrieve.py
```

### Or Run with a Specific Query
```bash
cd backend
python retrieve.py --query "What are the applications of humanoid robotics?"
```

## Configuration Options

### Environment Variables
- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_URL`: Qdrant Cloud instance URL
- `QDRANT_API_KEY`: Qdrant API key for authentication
- `QDRANT_COLLECTION_NAME`: Name of the collection containing stored embeddings (default: book_content)
- `TOP_K_RESULTS`: Number of results to retrieve (default: 5)
- `SIMILARITY_THRESHOLD`: Minimum similarity score for results (default: 0.0)

### Command Line Options
- `--query`: Specific query text to test (default: sample query)
- `--top-k`: Number of results to retrieve (default: 5)
- `--collection`: Qdrant collection name (default: book_content)
- `--verbose`: Enable detailed logging

## Expected Output
The system will:
1. Connect to Qdrant Cloud
2. Generate embeddings for the query
3. Execute similarity search against stored vectors
4. Return top-k results with metadata
5. Validate metadata completeness
6. Log results for inspection

Example output:
```
Connecting to Qdrant Cloud...
Query: "What are the applications of humanoid robotics?"
Generated embeddings for query
Executing similarity search in collection: book_content
Retrieved 5 results:
1. Score: 0.842, URL: https://ai-native-six.vercel.app/docs/chapter-1/why-humanoids
   Content: "Applications of humanoid robotics span multiple domains: - Healthcare and assisted living - Manufacturing and industrial automation - Education and research..."
2. Score: 0.798, URL: https://ai-native-six.vercel.app/docs/chapter-2/evolution-from-ros1
   Content: "Humanoid robotics represents a unique intersection of multiple disciplines..."
...
Validation: All results contain required metadata fields ✓
```

## Troubleshooting

### Common Issues
- **Connection errors**: Verify Qdrant URL and API key in environment
- **No results found**: Check that the collection contains stored embeddings
- **Embedding errors**: Verify Cohere API key and model access
- **Missing metadata**: Confirm ingestion pipeline stored complete metadata

### Validation Checks
- Qdrant connection established ✓
- Collection exists and contains vectors ✓
- Cohere API accessible ✓
- Results contain all required metadata fields ✓