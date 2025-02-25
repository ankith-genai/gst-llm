from flask import Flask, request, jsonify
import os
import redis
from langchain.vectorstores import Redis as RedisVectorStore
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

app = Flask(__name__)

# Load environment variables for Railway deployment
OLLAMA_HOST = "http://ollama.railway.internal:11434"  # Internal hostname for Ollama
REDIS_HOST = "redis.railway.internal"  # Internal hostname for Redis
REDIS_PORT = 6379  # Default Redis port

# Connect to Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Initialize embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Initialize Redis as a vector database
db = RedisVectorStore(redis_url=f"redis://{REDIS_HOST}:{REDIS_PORT}", embedding=embeddings)

# Initialize Ollama with Railway's internal service URL
llm = Ollama(model="llama2", base_url=OLLAMA_HOST)

# Create the QA chain
qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

@app.route('/query', methods=['POST'])
def query_rag():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    try:
        # Perform retrieval-augmented generation (RAG)
        result = qa_chain({"query": query})
        return jsonify({"result": result["result"]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
