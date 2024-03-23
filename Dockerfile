FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application files into the container
COPY src/*.py ./

ENV TEMPORAL_HOST 192.168.1.114
ENV TEMPORAL_PORT 7233
ENV AMAZON_USERNAME changeme
ENV AMAZON_PASSWORD changeme
ENV REDIS_HOST 192.168.1.110 
ENV REDIS_PORT 6379
ENV REDIS_DB "0"
ENV PORT 5000
ENV OPENAI_API_KEY changeme

# Expose the port that the Flask application runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "main.py"]
