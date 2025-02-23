# README.md

This project provides a Retrieval Augmented Generation (RAG) based chat API using Ollama and local text documents.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Ollama:**
    * Ensure Ollama is installed and running on your system.
    * Pull the `llama2` model (or your preferred Ollama model): `ollama pull llama2`
3.  **Prepare Data:**
    * Place your text files in the `gst_data` folder.
    * Run the initial Colab notebook code (or a similar script) to generate the Chroma database in the `rag_db` folder. This only needs to be run once.
    * If using Google drive, download the rag\_db folder into your project folder.
4.  **Run the Flask Application:**
    ```bash
    python app.py
    ```

## API Usage

Send a POST request to `/query` with a JSON payload containing the `query` parameter.

Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "what is the taxatbility provision for road construction under annuity model in GST give all the legal provisions, classifcation, ciruclars and notifcations also"}' http://localhost:5000/query