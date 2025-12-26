# Research: RAG Ingestion

## Decision Log

### Decision: URL Source Identification
**Rationale**: Based on the project constitution, the Docusaurus website URLs should be the deployed textbook website that contains the book content. Since the project is about creating a Physical AI & Humanoid Robotics textbook with Docusaurus, we'll assume the URLs are the deployed GitHub Pages site.

**Resolution**: The URLs will be determined by the deployed Docusaurus site containing the textbook content. For testing purposes, we'll implement the system to accept a configurable list of URLs.

**Alternatives considered**:
- Hardcoding specific URLs - rejected as it reduces flexibility
- Auto-discovering URLs through sitemap - adds complexity beyond requirements

### Decision: Chunk Size and Overlap Parameters
**Rationale**: Based on common RAG practices and the project constitution's reference to "semantic chunking with 512-token chunks, 50-token overlap", we'll use similar parameters but adapted to character count for simplicity.

**Resolution**:
- Chunk size: 1000 characters
- Overlap: 200 characters
- This provides a good balance between context preservation and retrieval efficiency

**Alternatives considered**:
- Token-based chunking - more accurate but requires additional tokenization libraries
- Sentence-based chunking - good for context but potentially inconsistent sizes
- Fixed character count chunking - simple and effective for this implementation

### Decision: Qdrant Collection Configuration
**Rationale**: Need to create an appropriate collection in Qdrant to store the embeddings with proper metadata structure.

**Resolution**:
- Collection name: "book_content"
- Vector size: Determined by Cohere embedding model (typically 1024 for medium model)
- Payload schema: Include source_url, chunk_id, section_title, and content_text in metadata

**Alternatives considered**:
- Different collection names - "book_content" is descriptive and clear
- Different vector sizes - determined by embedding model, not configurable
- Different metadata schema - current schema covers all required metadata from spec

## Technology Research

### Cohere Embedding Models
- **Model**: Cohere's embed-multilingual-v3.0 (recommended for text)
- **Dimensions**: 1024 (for medium variant)
- **Usage**: Best for semantic search and RAG applications
- **Rate Limits**: Need to handle appropriately with retry logic

### Text Chunking Best Practices
- **Fixed-size chunking**: Split content into fixed-length chunks
- **Overlap**: Include overlapping content to preserve context
- **Boundary preservation**: Try to split at sentence or paragraph boundaries when possible
- **Metadata retention**: Preserve source information with each chunk

### Qdrant Vector Database
- **Cloud Free Tier**: Sufficient for development and testing
- **Collection creation**: Simple API for creating collections with vector dimensions
- **Metadata storage**: Rich payload support for storing document metadata
- **Similarity search**: Built-in vector similarity search capabilities

## Implementation Patterns

### Error Handling Strategy
- **Retry mechanisms**: For API calls to Cohere and Qdrant
- **Graceful degradation**: Continue processing when individual URLs fail
- **Comprehensive logging**: Track progress and errors for debugging
- **Validation**: Verify content extraction and embedding generation

### Configuration Management
- **Environment variables**: Store API keys and endpoints securely
- **Configuration file**: Store chunking parameters and other settings
- **Default values**: Provide sensible defaults for all configurable parameters