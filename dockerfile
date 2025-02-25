# Use an official lightweight Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# # Install Ollama
# RUN curl -fsSL https://ollama.com/install.sh | sh

# RUN ollama serve &; ollama pull llama2

# Install Redis Stack Server
# RUN apt-get update && apt-get install -y wget && \
#     wget https://download.redis.io/releases/redis-stack-server-7.2.0.tar.gz && \
#     tar -xvzf redis-stack-server-7.2.0.tar.gz && \
#     mv redis-stack-server-7.2.0 /usr/local/bin/redis-stack && \
#     rm redis-stack-server-7.2.0.tar.gz

# Install Gunicorn
RUN pip install gunicorn

# Copy the startup script
COPY start.sh /start_app.sh
RUN chmod +x /start_app.sh

# Expose ports for Flask (8000) and Redis Stack (6379)
EXPOSE 8000 6379

# Run the startup script
CMD ["/start_app.sh"]
