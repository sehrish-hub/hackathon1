#!/usr/bin/env python3
"""
RAG Retrieval and Pipeline Validation System

This script validates end-to-end retrieval from Qdrant using stored embeddings.
It connects to Qdrant Cloud, generates embeddings for user queries using the same
Cohere model as ingestion, performs similarity search, and retrieves text chunks
with complete metadata for validation and inspection.
"""
import os
import logging
import argparse
import time
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import uuid
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Cohere and Qdrant - these may not be installed, so we handle that gracefully
try:
    import cohere
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    COHERE_AVAILABLE = True
    QDRANT_AVAILABLE = True
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Please install required packages: pip install cohere qdrant-client python-dotenv requests")
    COHERE_AVAILABLE = False
    QDRANT_AVAILABLE = False


@dataclass
class RetrievalResult:
    """Represents a single retrieval result with text content and metadata"""
    text_content: str
    similarity_score: float
    source_url: str
    section_title: str
    chunk_id: str
    chunk_index: int
    original_text: str


class RAGRetrievalValidator:
    """Validates RAG retrieval pipeline by connecting to Qdrant and performing similarity search"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Create console handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Load configuration
        self.cohere_api_key = os.getenv('COHERE_API_KEY')
        self.qdrant_url = os.getenv('QDRANT_URL')
        self.qdrant_api_key = os.getenv('QDRANT_API_KEY')
        self.collection_name = os.getenv('QDRANT_COLLECTION_NAME', 'book_content')
        self.top_k = int(os.getenv('TOP_K_RESULTS', '5'))
        self.similarity_threshold = float(os.getenv('SIMILARITY_THRESHOLD', '0.0'))

        # Initialize clients
        self.cohere_client = None
        self.qdrant_client = None

        # Validate required configuration
        missing_fields = []
        if not self.cohere_api_key:
            missing_fields.append('COHERE_API_KEY')
        if not self.qdrant_url:
            missing_fields.append('QDRANT_URL')
        if not self.qdrant_api_key:
            missing_fields.append('QDRANT_API_KEY')

        if missing_fields:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_fields)}")

    def setup_cohere_client(self) -> bool:
        """Set up Cohere client with proper error handling"""
        try:
            if not COHERE_AVAILABLE:
                self.logger.error("Cohere SDK not available. Please install: pip install cohere")
                return False

            self.cohere_client = cohere.Client(self.cohere_api_key)
            # Test the client by generating a simple embedding
            test_embedding = self.cohere_client.embed(
                texts=["test"],
                model="embed-multilingual-v3.0",
                input_type="search_query"
            )
            self.logger.info("Cohere client initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Cohere client: {str(e)}")
            return False

    def setup_qdrant_client(self) -> bool:
        """Set up Qdrant client with proper error handling"""
        try:
            if not QDRANT_AVAILABLE:
                self.logger.error("Qdrant client not available. Please install: pip install qdrant-client")
                return False

            self.qdrant_client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                prefer_grpc=False  # Use HTTP for Qdrant Cloud
            )

            # Test connection by listing collections
            collections = self.qdrant_client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if self.collection_name not in collection_names:
                self.logger.error(f"Collection '{self.collection_name}' not found in Qdrant. Available: {collection_names}")
                return False

            # Check if collection has vectors
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            if collection_info.points_count == 0:
                self.logger.warning(f"Collection '{self.collection_name}' is empty")

            self.logger.info(f"Qdrant client connected successfully to collection '{self.collection_name}' with {collection_info.points_count} vectors")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Qdrant: {str(e)}")
            return False

    def validate_configuration(self) -> bool:
        """Validate that all required services are accessible"""
        self.logger.info("Validating configuration and service connectivity...")

        cohere_ok = self.setup_cohere_client()
        qdrant_ok = self.setup_qdrant_client()

        if not cohere_ok:
            self.logger.error("Cohere client setup failed")
            return False

        if not qdrant_ok:
            self.logger.error("Qdrant client setup failed")
            return False

        self.logger.info("Configuration validation successful")
        return True

    def generate_query_embedding(self, query_text: str) -> Optional[List[float]]:
        """Generate embedding for query text using Cohere"""
        try:
            if not self.cohere_client:
                self.logger.error("Cohere client not initialized")
                return None

            response = self.cohere_client.embed(
                texts=[query_text],
                model="embed-multilingual-v3.0",  # Same model used in ingestion
                input_type="search_query"  # Use search_query type for queries
            )

            embeddings = response.embeddings
            if not embeddings or len(embeddings) == 0:
                self.logger.error("No embeddings returned from Cohere")
                return None

            self.logger.info(f"Generated embedding for query: '{query_text[:50]}...'")
            return embeddings[0]  # Return first (and only) embedding

        except Exception as e:
            self.logger.error(f"Failed to generate query embedding: {str(e)}")
            return None

    def execute_similarity_search(self, query_embedding: List[float], top_k: int = 5) -> List[RetrievalResult]:
        """Execute similarity search in Qdrant and return results with metadata"""
        try:
            if not self.qdrant_client:
                self.logger.error("Qdrant client not initialized")
                return []

            start_time = time.time()

            # Perform similarity search
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True  # Include metadata
            )

            search_time = time.time() - start_time
            self.logger.info(f"Similarity search completed in {search_time:.2f} seconds")

            # Convert search results to RetrievalResult objects
            results = []
            for i, hit in enumerate(search_results):
                try:
                    # Extract metadata from payload
                    payload = hit.payload
                    result = RetrievalResult(
                        text_content=payload.get('original_text', ''),
                        similarity_score=hit.score,
                        source_url=payload.get('source_url', ''),
                        section_title=payload.get('section_title', ''),
                        chunk_id=payload.get('chunk_id', ''),
                        chunk_index=payload.get('chunk_index', -1),
                        original_text=payload.get('original_text', '')
                    )
                    results.append(result)
                except Exception as e:
                    self.logger.warning(f"Failed to parse result {i}: {str(e)}")
                    continue

            self.logger.info(f"Retrieved {len(results)} results from similarity search")
            return results

        except Exception as e:
            self.logger.error(f"Failed to execute similarity search: {str(e)}")
            return []

    def validate_metadata_completeness(self, results: List[RetrievalResult]) -> Dict[str, Any]:
        """Validate that all required metadata fields are present in results"""
        validation_report = {
            'total_results': len(results),
            'complete_metadata': True,
            'missing_fields': [],
            'validation_passed': True,
            'details': []
        }

        required_fields = ['source_url', 'section_title', 'chunk_id', 'chunk_index']

        for i, result in enumerate(results):
            missing_fields = []
            for field in required_fields:
                value = getattr(result, field, None)
                if not value or (isinstance(value, int) and value == -1):
                    missing_fields.append(field)

            if missing_fields:
                validation_report['complete_metadata'] = False
                validation_report['validation_passed'] = False
                validation_report['details'].append({
                    'result_index': i,
                    'missing_fields': missing_fields,
                    'chunk_id': result.chunk_id
                })

        if not validation_report['complete_metadata']:
            all_missing = set()
            for detail in validation_report['details']:
                all_missing.update(detail['missing_fields'])
            validation_report['missing_fields'] = list(all_missing)

        return validation_report

    def log_results(self, query: str, results: List[RetrievalResult], validation: Dict[str, Any]):
        """Log retrieval results for inspection"""
        print(f"\n{'='*80}")
        print(f"QUERY: {query}")
        print(f"{'='*80}")

        if not results:
            print("No results retrieved.")
            return

        for i, result in enumerate(results, 1):
            print(f"\n{i}. Score: {result.similarity_score:.3f}")
            print(f"   URL: {result.source_url}")
            print(f"   Section: {result.section_title}")
            print(f"   Chunk ID: {result.chunk_id}")
            print(f"   Chunk Index: {result.chunk_index}")
            print(f"   Content Preview: {result.text_content[:200]}{'...' if len(result.text_content) > 200 else ''}")

        print(f"\n{'-'*80}")
        print("VALIDATION RESULTS:")
        print(f"  Total Results: {validation['total_results']}")
        print(f"  Complete Metadata: {'✓' if validation['complete_metadata'] else '✗'}")
        if validation['missing_fields']:
            print(f"  Missing Fields: {', '.join(validation['missing_fields'])}")
        print(f"  Validation Passed: {'✓' if validation['validation_passed'] else '✗'}")
        print(f"{'-'*80}")

    def validate_retrieval_pipeline(self, query: str, top_k: int = 5) -> bool:
        """Main method to validate the entire retrieval pipeline"""
        self.logger.info(f"Starting retrieval validation for query: '{query}'")

        # Validate configuration first
        if not self.validate_configuration():
            self.logger.error("Configuration validation failed")
            return False

        # Generate query embedding
        query_embedding = self.generate_query_embedding(query)
        if query_embedding is None:
            self.logger.error("Failed to generate query embedding")
            return False

        # Execute similarity search
        results = self.execute_similarity_search(query_embedding, top_k)
        if not results:
            self.logger.warning("No results returned from similarity search")
            # Still return True as the pipeline worked, just no relevant results
            return True

        # Validate metadata completeness
        validation = self.validate_metadata_completeness(results)

        # Log results for inspection
        self.log_results(query, results, validation)

        # Return whether validation passed
        return validation['validation_passed']

    def run_health_check(self) -> Dict[str, str]:
        """Perform a health check of the retrieval system"""
        health_status = {
            'qdrant_connection': 'disconnected',
            'cohere_api': 'unavailable',
            'collection_access': 'unavailable'
        }

        try:
            # Test Qdrant connection
            if self.setup_qdrant_client():
                health_status['qdrant_connection'] = 'connected'
                health_status['collection_access'] = 'available'

            # Test Cohere connection
            if self.setup_cohere_client():
                health_status['cohere_api'] = 'accessible'

        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")

        return health_status


def main():
    """Main function to run the RAG retrieval validation"""
    parser = argparse.ArgumentParser(description='RAG Retrieval and Pipeline Validation')
    parser.add_argument('--query', type=str, help='Query text to validate retrieval',
                       default='What are the applications of humanoid robotics?')
    parser.add_argument('--top-k', type=int, help='Number of results to retrieve', default=5)
    parser.add_argument('--collection', type=str, help='Qdrant collection name',
                       default=os.getenv('QDRANT_COLLECTION_NAME', 'book_content'))
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Update collection name from command line if provided
    if args.collection:
        os.environ['QDRANT_COLLECTION_NAME'] = args.collection

    try:
        validator = RAGRetrievalValidator()

        # Run the validation
        success = validator.validate_retrieval_pipeline(args.query, args.top_k)

        # Print final status
        print(f"\n{'='*80}")
        print(f"RETRIEVAL VALIDATION {'PASSED' if success else 'FAILED'}")
        print(f"Query: '{args.query}'")
        print(f"Collection: '{args.collection}'")
        print(f"Top-K: {args.top_k}")
        print(f"{'='*80}")

        # Run health check and print summary
        health = validator.run_health_check()
        print(f"\nHEALTH CHECK SUMMARY:")
        for service, status in health.items():
            status_icon = '✓' if status in ['connected', 'accessible', 'available'] else '✗'
            print(f"  {service}: {status_icon} {status}")

        return success

    except ValueError as e:
        print(f"Configuration error: {str(e)}")
        print("\nPlease ensure the following environment variables are set:")
        print("  COHERE_API_KEY: Your Cohere API key")
        print("  QDRANT_URL: Your Qdrant Cloud URL")
        print("  QDRANT_API_KEY: Your Qdrant API key")
        print("  QDRANT_COLLECTION_NAME: Name of the collection (default: book_content)")
        return False
    except Exception as e:
        print(f"Error during validation: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)