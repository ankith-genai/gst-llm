FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy application files for Service 1
COPY query_svc /app/
COPY start_app.sh /app/
COPY requirements.txt /app/
RUN chmod +x /app/start_app.sh

# Install dependencies
RUN pip install --no-cache-dir --trusted-host files.pythonhosted.org -r /app/requirements.txt

# Expose the port for Service 1
EXPOSE 5001

# Run the startup script for Service 1
CMD ["/app/start_app.sh"]