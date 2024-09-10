import sys
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.readers.web import SimpleWebPageReader
from llama_index.embeddings.ollama import OllamaEmbedding
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def ingest_data(url):
    # Get database connection details from environment variables
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')

    # Check if all required environment variables are set
    if not all([db_name, db_user, db_password, db_host, db_port]):
        print("Error: One or more required environment variables are not set.")
        sys.exit(1)

    # Set up Ollama embedding
    embed_model = OllamaEmbedding(model_name="llama3.1:8b")
    Settings.embed_model = embed_model

    # Create a PGVectorStore instance
    vector_store = PGVectorStore.from_params(
        database=db_name,
        host=db_host,
        password=db_password,
        port=db_port,
        user=db_user,
        table_name="document_embeddings",
        embed_dim=4096,  # Llama 3.1 embedding dimension
    )

    # Create a storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Load documents from the provided URL
    documents = SimpleWebPageReader(html_to_text=True).load_data([url])

    # Add timestamp to each document
    for doc in documents:
        doc.metadata["timestamp"] = datetime.now().isoformat()

    # Create an index from the documents
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )

    print(f"Data from {url} has been successfully ingested and stored in the database.")
    print(f"Table name: {vector_store.table_name}")  # Add this line to print the actual table name

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ingest_data.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    ingest_data(url)