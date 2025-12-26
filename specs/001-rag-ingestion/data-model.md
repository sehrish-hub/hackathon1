# Data Model: RAG Ingestion

## Entities

### Content Document
- **Description**: Represents a chunk of extracted content with associated metadata
- **Fields**:
  - source_url (string): The original URL of the content
  - content_text (string): The extracted text content
  - section_title (string): The section title from the page
  - chunk_id (string): Unique identifier for the chunk (URL + sequential number)
  - created_at (datetime): Timestamp when the chunk was created

### Embedding Vector
- **Description**: Represents the semantic embedding of content chunk
- **Fields**:
  - vector_data (array[float]): The embedding vector from Cohere
  - document_id (string): Reference to the source document
  - metadata (object): Associated metadata including URL, chunk_id, section_title
  - embedding_model (string): The model used to generate the embedding

### Processing Job
- **Description**: Represents an ingestion pipeline execution
- **Fields**:
  - job_id (string): Unique identifier for the processing job (UUID)
  - urls (array[string]): List of URLs to process
  - status (string): Current status (pending, in_progress, completed, failed)
  - start_time (datetime): When the job started
  - end_time (datetime): When the job completed
  - processed_count (integer): Number of URLs successfully processed
  - failed_count (integer): Number of URLs that failed to process
  - error_details (object): Details about any errors that occurred

## Relationships

- One Processing Job contains many Content Documents (1:M)
- One Content Document maps to one Embedding Vector (1:1)

## Validation Rules

### Content Document
- source_url must be a valid URL format
- content_text must not be empty
- chunk_id must be unique within the system
- created_at must be a valid timestamp

### Embedding Vector
- vector_data must have the correct dimension (1024 for Cohere medium model)
- document_id must reference an existing Content Document
- embedding_model must be a valid Cohere model identifier

### Processing Job
- status must be one of the defined values
- start_time must be before end_time if job is completed
- processed_count and failed_count must be non-negative integers