# Use an Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Flask application files into the container
COPY src/*.py ./

ENV AMAZON_USERNAME changeme
ENV AMAZON_PASSWORD changeme

# Expose the port that the Flask application runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["python3", "main.py"]
