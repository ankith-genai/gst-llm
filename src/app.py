# app.py (Flask application)

from flask import Flask, request, jsonify
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

app = Flask(__name__)

# Define paths (adjust as needed if not using Google Drive directly)
persist_directory = "./rag_db"  # Store the database in the current directory (deploy to Railway)

# Load the existing database
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# Initialize the language model
llm = Ollama(model="llama2")

# Create the QA chain
qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

@app.route('/query', methods=['POST'])
def query_rag():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    try:
        result = qa_chain({"query": query})
        return jsonify({"result": result["result"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)