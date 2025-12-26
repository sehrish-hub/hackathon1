# Implementation Plan: RAG Ingestion

**Feature**: RAG Ingestion
**Feature Branch**: `001-rag-ingestion`
**Created**: 2025-12-25
**Status**: Draft
**Input**: User description: "RAG Spec-1: URL ingestion, embeddings, and vector storage

Planning goals:
- Build a minimal, reproducible backend ingestion pipeline for RAG

Execution plan:
- Create backend folder for the RAG pipeline
- Initialize project using UV package manager
- Create a single main.py file inside backend
- Implement all ingestion logic within main.py only
- Configure environment variables (Cohere, Qdrant)
- Fetch deployed Docusaurus website URLs
- Extract and clean textual content from URLs
- Chunk text with fixed size and overlap
- Generate embeddings using Cohere embedding models
- Create and configure Qdrant collection
- Store embeddings with metadata (URL, section, chunk id)
- Implement a single main() function to orchestrate:
  - URL fetching
  - Chunking
  - Embedding generation
  - Vector storage in Qdrant
- Verify ingestion via sample similarity query
- Add basic logging and error handling

Out of scope:
- Retrieval and ranking logic
- Agent orchestration
- API or frontend integration
- Multiple files or modular architecture"

## Technical Context

### Architecture Overview
- **Backend**: Python application using Cohere for embeddings and Qdrant for vector storage
- **Data Flow**: URLs → Content Extraction → Text Chunking → Embedding Generation → Vector Storage
- **Deployment**: Local execution with cloud-hosted Qdrant

### Technology Stack
- **Language**: Python 3.10+
- **Embedding Model**: Cohere embedding models
- **Vector Database**: Qdrant Cloud (Free Tier)
- **Package Manager**: UV
- **Web Scraping**: requests/BeautifulSoup or similar
- **Text Processing**: Standard Python libraries

### Known Unknowns
- **URL Source**: The specific Docusaurus website URLs to ingest will be configurable via environment variables or configuration file
- **Chunk Size**: Using 1000 characters with 200-character overlap based on research (research.md)
- **Qdrant Collection Name**: Using "book_content" as the collection name based on research (research.md)

## Constitution Check

### Alignment with Project Principles
- **Technical Accuracy**: Implementation will use proper error handling and validation
- **AI-Native Design**: Content will be structured for RAG retrieval
- **User-Centric Experience**: Pipeline will be reproducible and configurable

### Potential Violations
- None identified - plan aligns with project constitution

## Gates

### Entry Gates
- [x] Feature specification exists and is approved
- [x] Technical prerequisites identified
- [x] Architecture aligns with project constitution

### Exit Gates
- [ ] All clarifications resolved in research phase
- [ ] Implementation approach validated
- [ ] Dependencies properly documented

## Phase 0: Outline & Research

### Research Tasks

#### RT-001: URL Source Identification
- **Task**: Determine the specific Docusaurus website URLs to ingest
- **Status**: Pending
- **Dependencies**: User input required

#### RT-002: Chunking Parameters
- **Task**: Define optimal chunk size and overlap parameters
- **Status**: Pending
- **Dependencies**: Best practices research

#### RT-003: Qdrant Configuration
- **Task**: Determine appropriate Qdrant collection configuration
- **Status**: Pending
- **Dependencies**: Qdrant documentation review

### Dependencies

- **Cohere API**: For embedding generation
- **Qdrant Cloud**: For vector storage
- **Python libraries**: requests, beautifulsoup4, cohere, qdrant-client

## Phase 1: Design & Contracts

### Data Model

#### Content Document
- **Fields**:
  - source_url (string): The original URL of the content
  - content_text (string): The extracted text content
  - section_title (string): The section title from the page
  - chunk_id (string): Unique identifier for the chunk
  - metadata (object): Additional metadata about the content

#### Embedding Vector
- **Fields**:
  - vector_data (array[float]): The embedding vector
  - document_id (string): Reference to the source document
  - metadata (object): Associated metadata including URL and chunk info

#### Processing Job
- **Fields**:
  - job_id (string): Unique identifier for the processing job
  - urls (array[string]): List of URLs to process
  - status (string): Current status of the job
  - start_time (datetime): When the job started
  - end_time (datetime): When the job completed

### API Contracts

#### Ingestion Pipeline Interface
- **Function**: main()
- **Purpose**: Orchestrate the entire ingestion process
- **Parameters**: None (uses configuration from environment)
- **Returns**: Processing status and statistics

### Quickstart Guide

#### Prerequisites
- Python 3.10+
- UV package manager
- Cohere API key
- Qdrant Cloud endpoint and API key

#### Setup
1. Install dependencies with UV
2. Configure environment variables
3. Run the ingestion pipeline

## Phase 2: Implementation Plan

### Implementation Steps

#### Step 1: Project Setup
- Create backend directory
- Initialize project with UV
- Install required dependencies

#### Step 2: Configuration
- Set up environment variable handling
- Configure Cohere and Qdrant clients

#### Step 3: Content Extraction
- Implement URL crawling and content extraction
- Add text cleaning and preprocessing

#### Step 4: Text Chunking
- Implement chunking logic with fixed size and overlap
- Add chunk ID generation

#### Step 5: Embedding Generation
- Implement Cohere embedding generation
- Add error handling for API calls

#### Step 6: Vector Storage
- Create Qdrant collection
- Store embeddings with metadata
- Implement verification queries

#### Step 7: Orchestration
- Create main() function to coordinate all steps
- Add logging and error handling

### Success Criteria
- Content successfully extracted from all specified URLs
- Embeddings generated and stored in Qdrant
- Verification queries return expected results
- Pipeline is reproducible and configurable