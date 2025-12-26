# Data Model: RAG Retrieval and Pipeline Validation

## Entity: Retrieval Result
**Description**: Contains the result of a similarity search operation with text content and metadata

**Fields**:
- `text_content` (string): The retrieved text chunk content
- `similarity_score` (float): Cosine similarity score between query and result
- `source_url` (string): Original URL of the document containing the text chunk
- `section_title` (string): Title of the section where the text chunk appears
- `chunk_id` (string): Unique identifier for the text chunk
- `chunk_index` (int): Sequential index of the chunk within the original document
- `original_text` (string): The original text content before processing

**Validation Rules**:
- All fields must be present (not null/empty)
- similarity_score must be between 0 and 1
- source_url must be a valid URL format
- chunk_index must be non-negative integer

## Entity: Query Embedding
**Description**: Vector representation of user query text for similarity search

**Fields**:
- `vector_data` (list[float]): The embedding vector (1024-dimensional)
- `query_text` (string): Original query text that was embedded
- `embedding_model` (string): Model used for embedding generation

**Validation Rules**:
- vector_data must have correct dimensions (1024 for Cohere medium model)
- query_text must not be empty
- embedding_model must match ingestion model for compatibility

## Entity: Stored Embedding
**Description**: Vector representation of book content chunks stored in Qdrant with associated metadata

**Fields**:
- `vector_data` (list[float]): The embedding vector (1024-dimensional)
- `document_id` (string): Identifier for the original document
- `source_url` (string): URL of the original document
- `section_title` (string): Title of the section
- `chunk_id` (string): Unique identifier for the text chunk
- `chunk_index` (int): Sequential index of the chunk within document
- `original_text` (string): Original text content

**Validation Rules**:
- All metadata fields must be present
- vector_data must have correct dimensions
- document_id must be consistent across chunks from same document

## Entity: Qdrant Collection
**Description**: Vector database collection containing book content embeddings with metadata

**Fields**:
- `collection_name` (string): Name of the Qdrant collection
- `vector_size` (int): Dimension of the stored vectors (1024)
- `distance_metric` (string): Distance metric used (cosine similarity)
- `total_vectors` (int): Count of vectors in the collection

**Validation Rules**:
- Collection must exist and be accessible
- Vector size must match embedding model output
- Distance metric must be compatible with embedding vectors