#!/bin/bash

# Define variables
DOCKER_IMAGE_NAME="bbertka/temporal-review-analyzer:latest"
DOCKER_FILE="Dockerfile"

# Build Docker image
docker build -t $DOCKER_IMAGE_NAME -f $DOCKER_FILE .

# Push Docker image to Docker Hub
docker push $DOCKER_IMAGE_NAME
