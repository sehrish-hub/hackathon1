# API Contract: RAG Ingestion Pipeline

## Main Ingestion Function

### Function: main()
- **Purpose**: Orchestrate the entire RAG ingestion process
- **Input**: None (reads configuration from environment variables)
- **Output**: Processing status and statistics
- **Side Effects**: Content extracted, embeddings generated, vectors stored in Qdrant

### Process Flow
1. **Configuration Loading**: Read environment variables and settings
2. **URL Processing**: Iterate through provided Docusaurus URLs
3. **Content Extraction**: Extract and clean text content from each URL
4. **Text Chunking**: Split content into fixed-size chunks with overlap
5. **Embedding Generation**: Generate semantic embeddings using Cohere
6. **Vector Storage**: Store embeddings in Qdrant with metadata
7. **Verification**: Run sample similarity queries to verify storage
8. **Reporting**: Output processing statistics and status

## Supporting Functions

### Function: extract_content_from_url(url: str) -> str
- **Purpose**: Extract clean text content from a given URL
- **Input**: URL string
- **Output**: Clean text content as string
- **Errors**: Returns empty string if URL is inaccessible

### Function: chunk_text(text: str, chunk_size: int, overlap: int) -> List[Dict]
- **Purpose**: Split text into overlapping chunks with metadata
- **Input**: Text string, chunk size, overlap size
- **Output**: List of chunk dictionaries with content and metadata
- **Errors**: Raises exception if chunk_size <= overlap

### Function: generate_embeddings(texts: List[str]) -> List[List[float]]
- **Purpose**: Generate embeddings for a list of text chunks
- **Input**: List of text strings
- **Output**: List of embedding vectors
- **Errors**: Handles API rate limits and retry logic

### Function: store_vectors(vectors: List[Dict]) -> bool
- **Purpose**: Store embedding vectors in Qdrant with metadata
- **Input**: List of vector dictionaries with embeddings and metadata
- **Output**: Success status (true/false)
- **Errors**: Handles Qdrant connection issues