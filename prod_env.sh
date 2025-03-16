#!/bin/bash

# Export environment variables
# prod_env.sh
export OLLAMA_HOST=http://localhost:11434  # Use localhost for Ollama server
export REDIS_HOST=localhost                  # Use localhost for Redis server
export REDIS_PORT=6379                       # Default Redis port

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "Docker is not installed. Please install Docker first."
        exit 1
    fi
}

# Function to check if Redis container is running
check_redis_container() {
    if [ "$(docker ps -q -f name=redis-stack-server)" ]; then
        echo "Redis container is already running."
    else
        echo "Starting Redis container with RediSearch..."
        docker run --name redis-stack-server -d -p $REDIS_PORT:$REDIS_PORT redis/redis-stack-server
        echo "Redis container with RediSearch started."
    fi
}

# Function to check if Ollama container is running
check_ollama_container() {
    if [ "$(docker ps -q -f name=ollama-server)" ]; then
        echo "Ollama server is already running."
    else
        echo "Starting Ollama server..."
        docker run --name ollama-server -d -p 11434:11434 ollama/ollama
        echo "Ollama server started."
    fi
}

# Main script execution
check_docker
check_redis_container
# check_ollama_container

echo "Environment variables set and services checked/started."