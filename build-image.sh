#!/bin/bash

# Generate a UUID for the image name
# IMAGE_NAME_SERVICE1="transparency-embedding-svc-$(uuidgen)"
IMAGE_NAME_SERVICE2="transparency-gst-llm-query-svc"

# Build the Docker image for Service 1
# docker build -t ttl.sh/${IMAGE_NAME_SERVICE1}:1h ./embedding_svc

# Build the Docker image for Service 2
docker build -t ghcr.io/ankith-genai/${IMAGE_NAME_SERVICE2}:latest ./query_svc

# Push the images to ttl.sh
# docker push ttl.sh/${IMAGE_NAME_SERVICE1}:1h
docker push ghcr.io/ankith-genai/${IMAGE_NAME_SERVICE2}:latest