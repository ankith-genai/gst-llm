from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain_redis import RedisVectorStore
from flask import Flask, request, jsonify
import redis
import openai
import json

# Define paths
gst_data_path = "/home/chai/Documents/gst-llm/gst_data_text"  # Update path
redis_url = "redis://127.0.0.1:6379"
redis_client = redis.Redis.from_url(redis_url)
index_name = "gst_index"

# Set OpenTextEmbeddings API
openai.api_base = "https://api.opentextembeddings.com/v1"

# Function to get embeddings
def get_embedding(text):
    response = openai.Embedding.create(
        model="bge-large-en",
        input=text
    )
    return response["data"][0]["embedding"]

# Create a wrapper class for the embedding function
class EmbeddingFunction:
    def embed_query(self, text):
        return get_embedding(text)

# Check if the index exists in Redis
try:
    redis_client.ft(index_name).info()
    db = RedisVectorStore(
        redis_url=redis_url,
        index_name=index_name,
        embeddings=EmbeddingFunction(),  # Use the wrapper class here
    )
    print(f"Index '{index_name}' found in Redis. Loading existing database.")

except redis.exceptions.ResponseError:
    print(f"Index '{index_name}' not found in Redis. Creating new index.")

    # Load and process documents
    loader = DirectoryLoader(gst_data_path, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Convert texts into embeddings and store in Redis
    embedded_texts = [
        {"text": text.page_content, "embedding": get_embedding(text.page_content)}
        for text in texts
    ]

    db = Redis(
        redis_url=redis_url,
        index_name=index_name,
        texts=[doc["text"] for doc in embedded_texts],
        embeddings=[doc["embedding"] for doc in embedded_texts],
    )

# Initialize LLM
llm = OllamaLLM(model="llama2")

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

app = Flask(__name__)

@app.route('/refresh_gst_data', methods=['POST'])
def refresh_gst_data():
    try:
        loader = DirectoryLoader(gst_data_path, glob="**/*.txt", loader_cls=TextLoader)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        embedded_texts = [
            {"text": text.page_content, "embedding": get_embedding(text.page_content)}
            for text in texts
        ]

        db = Redis(
            redis_url=redis_url,
            index_name=index_name,
            texts=[doc["text"] for doc in embedded_texts],
            embeddings=[doc["embedding"] for doc in embedded_texts],
        )

        return jsonify({"message": "Data refreshed and stored in Redis."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/gst_query/', methods=['POST'])
def gst_query():
    query = request.json.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    result = qa_chain.invoke({"query": query})

    output = {"result": result["result"]}
    return jsonify(output), 200

if __name__ == '__main__':
    app.run(debug=True)
