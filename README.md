# simple-llmops-stack

This guide will walk you through setting up a simple LLMOps stack on an Ubuntu machine.

<!-- TODO: re-add TOC when done -->

## Prerequisites
- Ubuntu machine with an NVIDIA GPU
- Sudo access
- [Docker setup](https://docs.docker.com/engine/install/ubuntu/) completed

## Clone this repo

```
git clone https://github.com/lukemarsden/simple-llmops-stack
cd simple-llmops-stack
```

## Installing Ollama
1. Run the Ollama installation one-liner:
   ```
   curl https://ollama.ai/install.sh | sh
   ```
2. Pull the Llama 3.1 model:
   ```
   ollama pull llama3.1:8b
   ```
3. Check that you can talk to the model interactively:
   ```
   ollama run llama3.1:8b
   ```
   This will start an interactive session with the Llama 3.1 model. Say hi, then exit.

## Setting up Environment Variables
1. Create a `.env` file in the project root directory:
   ```bash
   touch .env
   ```

2. Add the following content to the `.env` file:
   ```
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=mysecretpassword
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. Source the `.env` file to make the environment variables available in your shell:
   ```bash
   source .env
   ```

## Adding pgvector
2. Pull the pgvector Docker image:
   ```
   docker pull ankane/pgvector
   ```

3. Start a pgvector container:
   ```
   docker run --name pgvector -e POSTGRES_PASSWORD=$DB_PASSWORD -p $DB_PORT:5432 -d ankane/pgvector
   ```
   Warning: data will be ephemeral.

4. Verify the container is running:
   ```
   docker ps
   ```

## Using LlamaIndex to Ingest Data
1. Set up a Python environment and install dependencies:
   ```bash
   # Create a virtual environment
   python3 -m venv llmops_env

   # Activate the virtual environment
   source llmops_env/bin/activate
   ```

   Install dependencies
   ```
   pip install -r requirements.txt
   ```

2. Run the ingestion script:
   ```
   python ingest_data.py <URL>
   ```

## Demo: Querying the Ingested Data
1. Run the demo script:
   ```
   python query_data.py
   ```

## Starting the Embedding Explorer Application
1. Ensure you're in the project root directory and your virtual environment is activated.

2. Start the Flask web application in a separate terminal:
   ```bash
   source llmops_env/bin/activate
   python app.py
   ```

3. Open a web browser and navigate to `http://localhost:5000` to view the web interface.

The web application provides a simple interface to view the ingested data stored in the pgvector database. It displays a list of the most recent documents, including their text content and metadata. This allows you to easily verify that your data ingestion process is working correctly and explore the stored information.

Want a production-ready stack? Check out [helix.ml](https://helix.ml)
