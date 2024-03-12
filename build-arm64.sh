#!/bin/bash

# Define variables
DOCKER_IMAGE_NAME="bbertka/temporal-review-analyzer-arm64:latest"
DOCKER_FILE="Dockerfile"

# Build Docker image
sudo docker build -t $DOCKER_IMAGE_NAME -f $DOCKER_FILE .

# Push Docker image to Docker Hub
sudo docker push $DOCKER_IMAGE_NAME
