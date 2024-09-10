import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.llms.ollama import Ollama

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWORD')

# Connect to the database
vector_store = PGVectorStore.from_params(
    database=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASS,
    table_name="document_vectors"
)

# Create a storage context
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Initialize Ollama LLM
llm = Ollama(model="llama3.1:8b")

# Create a service context with the Ollama LLM
service_context = ServiceContext.from_defaults(llm=llm)

# Load the index from the vector store
index = VectorStoreIndex.from_vector_store(
    vector_store,
    storage_context=storage_context,
    service_context=service_context
)

# Create a query engine
query_engine = index.as_query_engine()

# Main loop for user queries
while True:
    user_query = input("Enter your question (or 'quit' to exit): ")
    
    if user_query.lower() == 'quit':
        break
    
    # Get the response from the query engine
    response = query_engine.query(user_query)
    
    print("\nResponse:")
    print(response)
    print("\n" + "-"*50 + "\n")

print("Thank you for using the query system!")