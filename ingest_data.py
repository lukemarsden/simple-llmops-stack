import sys
import os
import logging
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.readers.web import SimpleWebPageReader
from llama_index.embeddings.ollama import OllamaEmbedding
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()
logging.info("Environment variables loaded from .env file")

def ingest_data(url):
    logging.info(f"Starting data ingestion for URL: {url}")

    # Get database connection details from environment variables
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')

    # Check if all required environment variables are set
    if not all([db_name, db_user, db_password, db_host, db_port]):
        logging.error("One or more required environment variables are not set.")
        sys.exit(1)
    logging.info("All required environment variables are set")

    # Set up Ollama embedding
    logging.info("Setting up Ollama embedding model")
    embed_model = OllamaEmbedding(model_name="llama3.1:8b")
    Settings.embed_model = embed_model

    # Create a PGVectorStore instance
    logging.info("Creating PGVectorStore instance")
    vector_store = PGVectorStore.from_params(
        database=db_name,
        host=db_host,
        password=db_password,
        port=db_port,
        user=db_user,
        table_name="document_embeddings",
        embed_dim=4096,  # Llama 3.1 embedding dimension
    )
    logging.info(f"PGVectorStore created with table name: {vector_store.table_name}")

    # Create a storage context
    logging.info("Creating storage context")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Load documents from the provided URL
    logging.info(f"Loading documents from URL: {url}")
    documents = SimpleWebPageReader(html_to_text=True).load_data([url])
    logging.info(f"Loaded {len(documents)} documents from the URL")

    # Add timestamp to each document
    logging.info("Adding timestamps to documents")
    for doc in documents:
        doc.metadata["timestamp"] = datetime.now().isoformat()

    # Create an index from the documents
    logging.info("Creating VectorStoreIndex from documents")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )
    logging.info("VectorStoreIndex created successfully")

    logging.info(f"Data from {url} has been successfully ingested and stored in the database.")
    logging.info(f"Table name: {vector_store.table_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Incorrect number of arguments provided")
        print("Usage: python ingest_data.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    logging.info(f"Script started with URL: {url}")
    ingest_data(url)
    logging.info("Script completed successfully")