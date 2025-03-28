from flask import Flask, request, jsonify
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.vectorstores import Redis
from langchain.embeddings import HuggingFaceEmbeddings
import redis
import os
import json

# Define Redis URL
redis_url = "redis://127.0.0.1:6379"
redis_client = redis.Redis.from_url(redis_url)
index_name = "gst_index"

base_url = "http://localhost:8080"
# Initialize the language model
llm = Ollama(model="llama2",  base_url=base_url)  # Replace with your chosen Ollama model

# Create the Redis vectorstore
db = Redis(
    redis_url=redis_url,
    index_name=index_name,
    embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"),
)

# Create the QA chain
qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

app = Flask(__name__)

@app.route('/gst_query/', methods=['POST'])
def gst_query():
    query = request.json.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    result = qa_chain({"query": query})

    output = {"result": result["result"]}
    return jsonify(output), 200

if __name__ == '__main__':
    app.run(debug=True) 