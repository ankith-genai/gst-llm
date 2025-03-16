#!/bin/bash

# Start Ollama in the background
# nohup ollama serve > /dev/null 2>&1 &

# Start redis server
# nohup redis-stack-server > /dev/null 2>&1 &
# Wait for a few seconds to ensure Ollama starts properly
# sleep 5

# Start Flask app with Gunicorn
exec gunicorn -b 0.0.0.0:5000 app:app --workers 4 --timeout 0
