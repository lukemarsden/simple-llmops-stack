import sys
import os
from dotenv import load_dotenv
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores import PGVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.readers import SimpleWebPageReader
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

def ingest_data(url):
    # Get database connection details from environment variables
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_string)

    # Create a PGVectorStore instance
    vector_store = PGVectorStore.from_engine(engine, table_name="document_embeddings")

    # Create a storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Load documents from the provided URL
    documents = SimpleWebPageReader(html_to_text=True).load_data([url])

    # Create an index from the documents
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )

    print(f"Data from {url} has been successfully ingested and stored in the database.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ingest_data.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    ingest_data(url)