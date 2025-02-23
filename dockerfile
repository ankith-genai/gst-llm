# Use an official lightweight Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama (Linux)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama in the background
RUN ollama pull llama2

# Expose a port for Flask
EXPOSE 8000

# Run the startup script
CMD ["./start_app.sh"]