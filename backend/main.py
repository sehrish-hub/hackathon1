"""
RAG Ingestion Pipeline
A backend data ingestion layer for a Docusaurus-based AI book with embedded RAG chatbot.
"""
import os
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import requests
from bs4 import BeautifulSoup
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
import time
import json
from urllib.parse import urljoin, urlparse
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ContentDocument:
    """
    Represents a chunk of extracted content with associated metadata
    """
    source_url: str
    content_text: str
    section_title: str
    chunk_id: str
    created_at: datetime = field(default_factory=datetime.now)

    def validate(self) -> bool:
        """Validate the content document"""
        if not self.source_url:
            raise ValueError("source_url must not be empty")
        if not self.content_text:
            raise ValueError("content_text must not be empty")
        if not self.chunk_id:
            raise ValueError("chunk_id must not be empty")
        return True


@dataclass
class EmbeddingVector:
    """
    Represents the semantic embedding of content chunk
    """
    vector_data: List[float]
    document_id: str
    metadata: Dict[str, Any]
    embedding_model: str

    def validate(self) -> bool:
        """Validate the embedding vector"""
        if not self.vector_data:
            raise ValueError("vector_data must not be empty")
        if len(self.vector_data) == 0:
            raise ValueError("vector_data must have correct dimensions")
        if not self.document_id:
            raise ValueError("document_id must not be empty")
        if not self.embedding_model:
            raise ValueError("embedding_model must not be empty")
        return True


@dataclass
class ProcessingJob:
    """
    Represents an ingestion pipeline execution
    """
    job_id: str
    urls: List[str]
    status: str = "pending"
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    processed_count: int = 0
    failed_count: int = 0
    error_details: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate the processing job"""
        if not self.job_id:
            raise ValueError("job_id must not be empty")
        if self.status not in ["pending", "in_progress", "completed", "failed"]:
            raise ValueError("status must be one of the defined values")
        if self.processed_count < 0 or self.failed_count < 0:
            raise ValueError("processed_count and failed_count must be non-negative")
        if self.end_time and self.start_time > self.end_time:
            raise ValueError("start_time must be before end_time if job is completed")
        return True


def load_config():
    """Load configuration from environment variables"""
    config = {
        'cohere_api_key': os.getenv('COHERE_API_KEY'),
        'qdrant_url': os.getenv('QDRANT_URL'),
        'qdrant_api_key': os.getenv('QDRANT_API_KEY'),
        'docusaurus_urls': os.getenv('DOCUSAURUS_URLS', '').split(','),
        'sitemap_url': os.getenv('SITEMAP_URL', 'https://ai-native-six.vercel.app/sitemap.xml'),
        'use_sitemap': os.getenv('USE_SITEMAP', 'false').lower() == 'true',
        'filter_docs_only': os.getenv('FILTER_DOCS_ONLY', 'true').lower() == 'true',  # Default to true for better RAG quality
        'chunk_size': int(os.getenv('CHUNK_SIZE', '1000')),
        'chunk_overlap': int(os.getenv('CHUNK_OVERLAP', '200')),
        'collection_name': os.getenv('QDRANT_COLLECTION_NAME', 'book_content')
    }

    # Validate required configuration
    required_fields = ['cohere_api_key', 'qdrant_url', 'qdrant_api_key']
    missing_fields = [field for field in required_fields if not config[field]]
    if missing_fields:
        raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")

    return config


def setup_cohere_client():
    """Set up Cohere API client with proper error handling"""
    try:
        config = load_config()
        cohere_client = cohere.Client(config['cohere_api_key'])
        return cohere_client
    except Exception as e:
        logger.error(f"Failed to set up Cohere client: {str(e)}")
        raise


def setup_qdrant_client():
    """Set up Qdrant client with proper error handling"""
    try:
        config = load_config()
        qdrant_client = QdrantClient(
            url=config['qdrant_url'],
            api_key=config['qdrant_api_key'],
            prefer_grpc=False  # Use HTTP for Qdrant Cloud
        )
        return qdrant_client
    except Exception as e:
        logger.error(f"Failed to set up Qdrant client: {str(e)}")
        raise


def validate_url(url: str) -> bool:
    """Validate if a string is a proper URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def extract_urls_from_sitemap(sitemap_url: str, max_retries: int = 3, filter_docs_only: bool = False) -> List[str]:
    """Extract URLs from a sitemap.xml file"""
    import xml.etree.ElementTree as ET

    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to fetch sitemap: {sitemap_url} (attempt {attempt + 1}/{max_retries})")
            response = requests.get(sitemap_url, timeout=30)
            response.raise_for_status()

            # Parse the XML content
            root = ET.fromstring(response.content)

            # Handle both regular sitemap and sitemap index files
            urls = []
            namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            # Find all <url><loc> elements (regular sitemap)
            for url_elem in root.findall('sitemap:url/sitemap:loc', namespace):
                url = url_elem.text.strip()
                if url:
                    # Replace placeholder domain with actual domain if needed
                    if 'your-docusaurus-site.example.com' in url:
                        url = url.replace('your-docusaurus-site.example.com', 'ai-native-six.vercel.app')
                    urls.append(url)

            # Also handle sitemap index files (if <sitemap> elements exist)
            if not urls:
                index_namespace = {
                    'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                    's': 'http://www.sitemaps.org/schemas/sitemap/0.9'
                }
                # Try with different namespace possibilities
                for sitemap_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                    sitemap_loc = sitemap_elem.text.strip()
                    if sitemap_loc and sitemap_loc.endswith('.xml'):
                        logger.info(f"Found nested sitemap: {sitemap_loc}")
                        nested_urls = extract_urls_from_sitemap(sitemap_loc)
                        urls.extend(nested_urls)

                # Fallback - try without namespace
                if not urls:
                    for url_elem in root.findall('.//loc'):
                        url = url_elem.text.strip()
                        if url:
                            # Replace placeholder domain with actual domain if needed
                            if 'your-docusaurus-site.example.com' in url:
                                url = url.replace('your-docusaurus-site.example.com', 'ai-native-six.vercel.app')
                            urls.append(url)

            # Filter URLs if requested to only include /docs/* pages
            if filter_docs_only:
                filtered_urls = []
                for url in urls:
                    if '/docs/' in url and not any(endpoint in url for endpoint in ['/login', '/logout', '/signup', '/markdown-page']):
                        filtered_urls.append(url)

                logger.info(f"Successfully extracted {len(filtered_urls)} /docs/* URLs from sitemap (original: {len(urls)} URLs)")
                return filtered_urls
            else:
                logger.info(f"Successfully extracted {len(urls)} URLs from sitemap: {sitemap_url}")
                return urls

        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for sitemap {sitemap_url}: {str(e)}")
            if attempt == max_retries - 1:
                logger.error(f"All {max_retries} attempts failed for sitemap {sitemap_url}")
                return []
        except ET.ParseError as e:
            logger.error(f"Failed to parse sitemap XML from {sitemap_url}: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error extracting URLs from sitemap {sitemap_url}: {str(e)}")
            return []

    return []


def clean_text(text: str) -> str:
    """Clean and preprocess text content"""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that might cause issues
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    return text.strip()


def crawl_url(url: str, max_retries: int = 3) -> Optional[str]:
    """Implement URL crawling function to fetch web page content"""
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to crawl URL: {url} (attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Raise an exception for bad status codes
            logger.info(f"Successfully crawled URL: {url}")
            return response.text
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for URL {url}: {str(e)}")
            if attempt == max_retries - 1:
                logger.error(f"All {max_retries} attempts failed for URL {url}")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff
    return None


def extract_content_with_bs(html_content: str) -> tuple[str, str]:
    """Implement content extraction using BeautifulSoup to get clean text and section title"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Try to extract the main content - prioritize main content areas
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article')) or soup

    # Extract text
    text = main_content.get_text()

    # Clean up the text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    # Extract section title (try multiple selectors)
    title_element = soup.find('title') or soup.find('h1') or soup.find('h2')
    section_title = title_element.get_text().strip() if title_element else "Unknown Section"

    return clean_text(text), section_title


def extract_section_title(html_content: str) -> str:
    """Implement function to extract section titles from pages"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Look for various title elements
    title_element = soup.find('title') or soup.find('h1') or soup.find('h2')
    if title_element:
        return clean_text(title_element.get_text())
    else:
        return "Unknown Section"


def process_single_url(url: str) -> Optional[ContentDocument]:
    """Process a single URL and return a ContentDocument"""
    html_content = crawl_url(url)
    if html_content is None:
        logger.error(f"Failed to crawl URL: {url}")
        return None

    content_text, section_title = extract_content_with_bs(html_content)

    if not content_text:
        logger.warning(f"No content extracted from URL: {url}")
        return None

    # Generate a unique base chunk ID for this URL
    base_chunk_id = url_hash(url)

    content_doc = ContentDocument(
        source_url=url,
        content_text=content_text,
        section_title=section_title,
        chunk_id=base_chunk_id  # This will be used as base for actual chunk IDs in embedding creation
    )

    # Validate the content document
    try:
        content_doc.validate()
        return content_doc
    except ValueError as e:
        logger.error(f"Validation failed for content document from {url}: {str(e)}")
        return None


def url_hash(url: str) -> str:
    """Generate a simple hash for URL to use in chunk ID"""
    import hashlib
    return hashlib.md5(url.encode()).hexdigest()[:8]


def process_multiple_urls(urls: List[str]) -> List[ContentDocument]:
    """Create function to process multiple URLs in sequence"""
    logger.info(f"Starting to process {len(urls)} URLs for content extraction")

    content_documents = []

    for i, url in enumerate(urls):
        logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

        if not validate_url(url):
            logger.error(f"Invalid URL format: {url}")
            continue

        content_doc = process_single_url(url)
        if content_doc:
            content_documents.append(content_doc)
            # Log content length to verify we're getting substantial content
            content_length = len(content_doc.content_text) if content_doc.content_text else 0
            logger.info(f"Successfully processed URL: {url} (content length: {content_length} chars)")
        else:
            logger.error(f"Failed to process URL: {url}")

    logger.info(f"Content extraction completed: {len(content_documents)} documents extracted from {len(urls)} URLs")
    return content_documents


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict]:
    """Implement text chunking function with 1000 char size and 200 char overlap"""
    if len(text) <= chunk_size:
        return [{"text": text, "start_idx": 0, "end_idx": len(text)}]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If this is not the last chunk, try to break at a sentence or word boundary
        if end < len(text):
            # Look for a good breaking point (space or sentence end)
            search_start = end - overlap if start != 0 else end  # Apply overlap except for first chunk
            for i in range(min(end, len(text)) - 1, search_start - 1, -1):
                if text[i] in ['.', '!', '?', ';', ':', ' ', '\n', '\t']:
                    end = i + 1
                    break

        # Ensure we don't exceed the text length
        end = min(end, len(text))

        chunk_text = text[start:end]
        chunks.append({
            "text": chunk_text,
            "start_idx": start,
            "end_idx": end
        })

        # Move start to after the overlap section
        if start == 0:
            start = end  # No overlap for the first chunk
        else:
            start = end - overlap if end - overlap > start else end  # Apply overlap for subsequent chunks

        # Prevent infinite loops
        if start >= len(text) or start <= 0:
            break

    # Handle any remaining text
    if start < len(text):
        chunks.append({
            "text": text[start:],
            "start_idx": start,
            "end_idx": len(text)
        })

    return chunks


def generate_chunk_id(source_url: str, chunk_index: int) -> str:
    """Generate unique chunk IDs based on source URL and sequence number"""
    url_hash_part = url_hash(source_url)
    return f"{url_hash_part}_{chunk_index:03d}"


def generate_embeddings_for_texts(texts: List[str], cohere_client) -> Optional[List[List[float]]]:
    """Implement Cohere embedding generation for text chunks"""
    try:
        logger.info(f"Generating embeddings for {len(texts)} text chunks")
        response = cohere_client.embed(
            texts=texts,
            model="embed-multilingual-v3.0",  # Using multilingual model for broader compatibility
            input_type="search_document"  # Required parameter for Cohere API
        )
        embeddings = response.embeddings
        logger.info(f"Successfully generated embeddings for {len(embeddings)} text chunks")
        return embeddings
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {str(e)}")
        return None


def add_error_handling_for_cohere_rate_limits():
    """Placeholder for Cohere API rate limit handling - implemented in generate_embeddings_with_retry"""
    pass


def generate_embeddings_with_retry(texts: List[str], cohere_client, max_retries: int = 3) -> Optional[List[List[float]]]:
    """Implement retry logic for embedding generation failures"""
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempt {attempt + 1} to generate embeddings for {len(texts)} texts")
            embeddings = generate_embeddings_for_texts(texts, cohere_client)
            if embeddings is not None and len(embeddings) == len(texts):
                logger.info(f"Successfully generated embeddings on attempt {attempt + 1}")
                return embeddings
            else:
                logger.warning(f"Embedding generation returned unexpected result on attempt {attempt + 1}")
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                logger.error(f"All {max_retries} attempts failed for embedding generation")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff

    return None


def create_embedding_vectors(content_docs: List[ContentDocument], cohere_client) -> List[EmbeddingVector]:
    """Create function to generate embedding vectors with metadata"""
    embedding_vectors = []
    config = load_config()
    chunk_size = config['chunk_size']
    chunk_overlap = config['chunk_overlap']

    logger.info(f"Starting to create embedding vectors for {len(content_docs)} content documents")

    for i, content_doc in enumerate(content_docs):
        logger.info(f"Processing document {i+1}/{len(content_docs)} from {content_doc.source_url}")

        # Chunk the content text
        text_chunks = chunk_text(content_doc.content_text, chunk_size, chunk_overlap)
        logger.info(f"Document from {content_doc.source_url} was chunked into {len(text_chunks)} chunks")

        # Prepare texts for embedding
        texts_for_embedding = [chunk["text"] for chunk in text_chunks]

        if not texts_for_embedding:
            logger.warning(f"No text chunks generated for document from {content_doc.source_url}")
            continue

        # Generate embeddings with retry logic
        embeddings = generate_embeddings_with_retry(texts_for_embedding, cohere_client)

        if embeddings is None:
            logger.error(f"Failed to generate embeddings for document from {content_doc.source_url}")
            continue

        # Create embedding vectors with metadata
        for j, (chunk, embedding) in enumerate(zip(texts_for_embedding, embeddings)):
            chunk_id = generate_chunk_id(content_doc.source_url, j + 1)

            metadata = {
                "source_url": content_doc.source_url,
                "section_title": content_doc.section_title,
                "chunk_id": chunk_id,
                "chunk_index": j,
                "original_text": chunk
            }

            embedding_vector = EmbeddingVector(
                vector_data=embedding,
                document_id=content_doc.chunk_id,
                metadata=metadata,
                embedding_model="embed-multilingual-v3.0"
            )

            try:
                embedding_vector.validate()
                embedding_vectors.append(embedding_vector)
            except ValueError as e:
                logger.error(f"Validation failed for embedding vector: {str(e)}")
                continue

    logger.info(f"Created {len(embedding_vectors)} embedding vectors from {len(content_docs)} content documents")
    return embedding_vectors


def create_qdrant_collection(collection_name: str, vector_size: int = 1024):
    """Create Qdrant collection named "book_content" with appropriate vector dimensions"""
    qdrant_client = setup_qdrant_client()

    try:
        # Check if collection already exists
        collections = qdrant_client.get_collections()
        collection_exists = any(col.name == collection_name for col in collections.collections)

        if not collection_exists:
            # Create the collection with specified vector size
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created Qdrant collection: {collection_name} with vector size {vector_size}")
        else:
            logger.info(f"Qdrant collection {collection_name} already exists")
    except Exception as e:
        logger.error(f"Failed to create Qdrant collection {collection_name}: {str(e)}")
        raise


def store_embeddings_in_qdrant(embedding_vectors: List[EmbeddingVector], collection_name: str):
    """Implement function to store embedding vectors in Qdrant with metadata"""
    qdrant_client = setup_qdrant_client()

    try:
        points = []
        for i, emb_vec in enumerate(embedding_vectors):
            point = models.PointStruct(
                id=i,  # Using index as ID, in production you'd want UUIDs
                vector=emb_vec.vector_data,
                payload=emb_vec.metadata
            )
            points.append(point)

        # Upload points to Qdrant
        qdrant_client.upsert(
            collection_name=collection_name,
            points=points
        )
        logger.info(f"Successfully stored {len(embedding_vectors)} vectors in Qdrant collection: {collection_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to store embeddings in Qdrant: {str(e)}")
        return False


def add_metadata_storage_for_fields():
    """Placeholder - metadata fields are already implemented in the store_embeddings_in_qdrant function"""
    pass


def run_verification_query(collection_name: str, query_text: str, cohere_client, limit: int = 5):
    """Implement verification query function to test stored vectors"""
    try:
        # Generate embedding for the query text
        query_embedding = generate_embeddings_with_retry([query_text], cohere_client, max_retries=3)

        if query_embedding is None or len(query_embedding) == 0:
            logger.error("Failed to generate query embedding")
            return []

        # Perform similarity search in Qdrant
        qdrant_client = setup_qdrant_client()
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding[0],
            limit=limit
        )

        logger.info(f"Verification query returned {len(search_results)} results")
        return search_results
    except Exception as e:
        logger.error(f"Verification query failed: {str(e)}")
        return []


def create_similarity_search_function(collection_name: str, query_embedding: List[float], limit: int = 5):
    """Create similarity search function for verification purposes"""
    try:
        qdrant_client = setup_qdrant_client()
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=limit
        )

        logger.info(f"Similarity search returned {len(search_results)} results")
        return search_results
    except Exception as e:
        logger.error(f"Similarity search failed: {str(e)}")
        return []


def add_error_handling_for_qdrant_connection():
    """Placeholder for Qdrant connection error handling - implemented in setup_qdrant_client"""
    pass


def implement_retry_logic_for_qdrant_operations(collection_name: str, operation_func, *args, max_retries: int = 3):
    """Implement retry logic for Qdrant storage operations"""
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempt {attempt + 1} for Qdrant operation")
            result = operation_func(collection_name, *args)
            logger.info(f"Qdrant operation successful on attempt {attempt + 1}")
            return result
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                logger.error(f"All {max_retries} attempts failed for Qdrant operation")
                raise
            time.sleep(2 ** attempt)  # Exponential backoff


def main():
    """Create main() function to coordinate the entire ingestion process"""
    logger.info("Starting RAG Ingestion Pipeline")

    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")

        # Validate configuration
        required_fields = ['cohere_api_key', 'qdrant_url', 'qdrant_api_key']
        missing_fields = [field for field in required_fields if not config[field]]

        # If using sitemap, validate that sitemap URL is provided
        if config['use_sitemap'] and not config['sitemap_url']:
            missing_fields.append('sitemap_url')

        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")
        logger.info("Configuration validation passed")

        # Extract URLs based on configuration
        if config['use_sitemap']:
            logger.info(f"Using sitemap to extract URLs: {config['sitemap_url']}")
            # Use filter_docs_only to only include /docs/* pages and exclude login/signup/logout based on config
            extracted_urls = extract_urls_from_sitemap(config['sitemap_url'], filter_docs_only=config['filter_docs_only'])
            if not extracted_urls:
                logger.error("No URLs extracted from sitemap, stopping pipeline")
                processing_job = ProcessingJob(
                    job_id=str(uuid.uuid4()),
                    urls=[]
                )
                processing_job.status = "failed"
                processing_job.end_time = datetime.now()
                processing_job.error_details = {"error": "No URLs extracted from sitemap"}
                return False
            urls_to_process = extracted_urls
            filter_msg = " /docs/*" if config['filter_docs_only'] else ""
            logger.info(f"Extracted {len(urls_to_process)}{filter_msg} URLs from sitemap:")
            for i, url in enumerate(urls_to_process[:10]):  # Log first 10 URLs
                logger.info(f"  {i+1:2d}. {url}")
            if len(urls_to_process) > 10:
                logger.info(f"  ... and {len(urls_to_process) - 10} more URLs")
        else:
            # Filter out empty strings from the URL list
            urls_to_process = [url.strip() for url in config['docusaurus_urls'] if url.strip()]
            logger.info(f"Using configured URLs: {len(urls_to_process)} URLs")
            for i, url in enumerate(urls_to_process):
                logger.info(f"  {i+1}. {url}")

        # Create processing job
        job_id = str(uuid.uuid4())
        processing_job = ProcessingJob(
            job_id=job_id,
            urls=urls_to_process
        )
        processing_job.status = "in_progress"
        processing_job.start_time = datetime.now()
        logger.info(f"Started processing job {job_id} for {len(urls_to_process)} URLs")

        # Set up clients
        cohere_client = setup_cohere_client()
        qdrant_client = setup_qdrant_client()
        logger.info("Clients initialized successfully")

        # Step 1: Content Extraction
        logger.info("Starting content extraction phase")
        content_docs = process_multiple_urls(urls_to_process)
        processing_job.processed_count = len([doc for doc in content_docs if doc.content_text])
        processing_job.failed_count = len(urls_to_process) - processing_job.processed_count
        logger.info(f"Content extraction completed: {len(content_docs)} documents extracted")

        if not content_docs:
            logger.error("No content documents extracted, stopping pipeline")
            processing_job.status = "failed"
            processing_job.end_time = datetime.now()
            return False

        # Step 2: Chunking and Embedding Generation
        logger.info("Starting chunking and embedding generation phase")
        embedding_vectors = create_embedding_vectors(content_docs, cohere_client)
        logger.info(f"Embedding generation completed: {len(embedding_vectors)} vectors created")

        if not embedding_vectors:
            logger.error("No embedding vectors created, stopping pipeline")
            processing_job.status = "failed"
            processing_job.end_time = datetime.now()
            return False

        # Step 3: Vector Storage
        logger.info("Starting vector storage phase")
        create_qdrant_collection(config['collection_name'])
        storage_success = store_embeddings_in_qdrant(embedding_vectors, config['collection_name'])

        if not storage_success:
            logger.error("Failed to store embeddings in Qdrant, stopping pipeline")
            processing_job.status = "failed"
            processing_job.end_time = datetime.now()
            return False

        logger.info("Vector storage completed successfully")

        # Step 4: Verification
        logger.info("Starting verification phase")
        if content_docs:
            sample_text = content_docs[0].content_text[:100]  # Use first 100 chars of first document
            verification_results = run_verification_query(config['collection_name'], sample_text, cohere_client)
            logger.info(f"Verification query returned {len(verification_results)} results")

        # Update job status
        processing_job.status = "completed"
        processing_job.end_time = datetime.now()
        logger.info(f"Pipeline completed successfully. Job {job_id} finished in {processing_job.end_time - processing_job.start_time}")

        # Print summary statistics
        print(f"\n--- Pipeline Summary ---")
        print(f"Job ID: {processing_job.job_id}")
        print(f"Status: {processing_job.status}")
        print(f"Processed URLs: {processing_job.processed_count}")
        print(f"Failed URLs: {processing_job.failed_count}")
        print(f"Content Documents: {len(content_docs)}")
        print(f"Embedding Vectors: {len(embedding_vectors)}")
        print(f"Start Time: {processing_job.start_time}")
        print(f"End Time: {processing_job.end_time}")
        print(f"Duration: {processing_job.end_time - processing_job.start_time}")

        return True

    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        # If we have a processing job, update its status
        try:
            if 'processing_job' in locals():
                processing_job.status = "failed"
                processing_job.end_time = datetime.now()
                if not processing_job.error_details:
                    processing_job.error_details = {"error": str(e)}
        except:
            pass  # If processing_job wasn't created yet, ignore
        return False


def run_pipeline_flow():
    """Implement pipeline flow: URLs → Content Extraction → Chunking → Embeddings → Storage"""
    return main()


def add_comprehensive_error_handling():
    """Placeholder - error handling is implemented throughout the pipeline"""
    pass


def add_processing_statistics():
    """Placeholder - statistics are included in the main function output"""
    pass


def implement_verification_step():
    """Placeholder - verification is implemented in the main function"""
    pass


def add_configuration_validation():
    """Placeholder - configuration validation is implemented in the main function"""
    pass


def create_command_line_interface():
    """Create command-line interface for the ingestion pipeline"""
    import argparse

    parser = argparse.ArgumentParser(description='RAG Ingestion Pipeline')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--urls', type=str, help='Comma-separated list of URLs to process')
    parser.add_argument('--sitemap', type=str, help='Sitemap URL to extract URLs from')
    parser.add_argument('--use-sitemap', action='store_true', help='Use sitemap to extract URLs instead of providing them directly')
    parser.add_argument('--filter-docs-only', action='store_true', help='Filter to only include /docs/* pages (default: true)')
    parser.add_argument('--all-pages', action='store_true', help='Include all pages (not just /docs/*) - overrides --filter-docs-only')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Override configuration if provided via command line
    if args.urls:
        os.environ['DOCUSAURUS_URLS'] = args.urls
    if args.sitemap:
        os.environ['SITEMAP_URL'] = args.sitemap
    if args.use_sitemap:
        os.environ['USE_SITEMAP'] = 'true'
    if args.filter_docs_only:
        os.environ['FILTER_DOCS_ONLY'] = 'true'
    elif args.all_pages:
        os.environ['FILTER_DOCS_ONLY'] = 'false'

    success = main()
    return success


# Add entry point for command line execution
if __name__ == "__main__":
    success = create_command_line_interface()
    if success:
        print("Pipeline completed successfully!")
        exit(0)
    else:
        print("Pipeline failed!")
        exit(1)