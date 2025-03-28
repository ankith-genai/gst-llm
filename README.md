# README.md

This project provides a Retrieval Augmented Generation (RAG) based chat API using Ollama and local text documents.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Redis Stack Server:**
    To set up the Redis Stack Server, follow these steps:
    
    1. Pull the Redis Stack Docker image:
        ```bash
        docker pull redis/redis-stack-server
        ```
    
    2. Run the Redis Stack Server:
        ```bash
        docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server
        ```
    
    3. Verify that the Redis Stack Server is running:
        ```bash
        docker ps
        ```

3.  **Run Ollama:**
    To set up the Ollama Docker image and pull the Llama2 model, follow these steps:
    
    1. Pull the Ollama Docker image:
        ```bash
        docker pull ollama/ollama
        ```
    
    2. Run the Ollama container:
        ```bash
        docker run -d --name ollama -p 11434:11434 ollama/ollama
        ```
    
    3. Pull the Llama2 model:
        ```bash
        docker exec -it ollama ollama pull llama2
        ```
    
    4. Verify that the Ollama container is running and the Llama2 model is available:
        ```bash
        docker logs ollama
        ```

4.  **Prepare Data:**
    * Place your text files in the `gst_data` folder.
    * Run the initial Colab notebook code (or a similar script) to generate the Chroma database in the `rag_db` folder. This only needs to be run once.
    * If using Google Drive, download the rag_db folder into your project folder.

5.  **Run the Flask Application:**
    ```bash
    python query_svc/app.py
    ```

## API Usage

Send a POST request to `/query` with a JSON payload containing the `query` parameter.

Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "what is the taxatbility provision for road construction under annuity model in GST give all the legal provisions, classifcation, ciruclars and notifcations also"}' http://localhost:5000/gst_query