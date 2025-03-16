from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
import redis
from langchain.vectorstores import Redis
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Load GST data and initialize the application.')
parser.add_argument('--gst_data_path', type=str, required=True, help='Path to the GST data directory')
args = parser.parse_args()

# Use the provided gst_data_path
gst_data_path = args.gst_data_path

# Mount Google Drive
# drive.mount('/content/drive')

# Define paths
# persist_directory = "/content/drive/MyDrive/rag_db" # Store the database on Google Drive

# redis_url = os.getenv("REDIS_URL") # Replace with your Redis URL
redis_url="redis://127.0.0.1:6379"
redis_client = redis.Redis.from_url(redis_url)
index_name = "gst_index"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Check if the index exists in Redis
try:
    redis_client.ft(index_name).info()  # This will raise an error if the index doesn't exist
    # If no error, the index exists, so load it
    db = Redis(
        redis_url=redis_url,
        index_name=index_name,
        embedding=embeddings,
    )
    print(f"Index '{index_name}' found in Redis. Loading existing database.")

except redis.exceptions.ResponseError:
    # If error, the index doesn't exist, so create it
    print(f"Index '{index_name}' not found in Redis. Creating new index.")

    # Load documents
    loader = DirectoryLoader(gst_data_path, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Create the Redis vectorstore
    db = Redis.from_documents(
        texts,
        embeddings,
        redis_url=redis_url,
        index_name=index_name,
    )

# Initialize the language model
llm = Ollama(model="llama2") # Replace with your chosen Ollama model

# Create the QA chain
qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())


# Example query
query = "what is the taxatbility provision for road construction under annuity model in GST give all the legal provisions, classifcation, ciruclars and notifcations also"
result = qa_chain({"query": query})
print(result["result"])