# Temporal Review Analyzer

The Temporal Review Analyzer pipeline is an Minimum Viable Product (MVP) distributed system designed to automate the collection, analysis, and aggregation of online product reviews to derive an overall customer sentiment score. Utilizing Temporal for workflow orchestration, Flask for HTTP request handling, and Redis for data storage, the solution offers a scalable and fault-tolerant architecture for processing vast amounts of review data from Amazon.

## Solution Overview

The system comprises several components working together to enable the scraping and analysis of product reviews:

- **Flask Application (`routes.py`)**: Serves as the entry point for the application, handling HTTP requests and triggering Temporal workflows.
- **Temporal Workflow (`main.py`)**: Orchestrates the review scraping and analysis tasks, ensuring reliable execution and fault tolerance.
- **Scraper Activity (`scrape.py`)**: Scrapes review data from Amazon product pages and stores it in Redis.
- **Analysis Activity (`analyze.py`)**: Analyzes the scraped review data to determine overall sentiment.
- **Configuration (`config.py`)**: Manages environment variables and application configuration settings.
- **Redis** Acts as a temporary data store for the scraped reviews, facilitating distributed processing.

### Key Features

- Scalable review scraping and analysis.
- Fault-tolerant workflow execution with Temporal.
- Simple HTTP interface for triggering analysis jobs.
- Configurable for different Amazon products.

### Sentiment Analysis Methodology
The sentiment analysis module is a critical component, utilizing TextBlob to assign polarity scores to review texts, ranging from -1 (entirely negative) to 1 (entirely positive). This process includes:

- Preprocessing: Cleaning the review text to focus on relevant content.
- Polarity Calculation: Using TextBlob to determine the sentiment polarity of each review.
- Review Weighting (optional): Applying weights to reviews based on helpfulness, recency, or credibility to influence their impact on the overall sentiment score.
- Averaging Scores: Computing the average of all polarity scores to obtain a single metric representing the overall product sentiment.

### Enhancements and Depth of Analysis
To enhance the sentiment analysis algorithm, several strategies can be considered:

- Advanced NLU Techniques: Integrating NLU capabilities for better context understanding, especially for nuanced expressions.
- Aspect-Based Analysis: Segmenting sentiment by product features to provide more detailed insights.
C- ustom Machine Learning Models: Developing domain-specific models trained on relevant datasets for improved accuracy.

### Conclusion
The Temporal Review Analyzer pipeline offers a sophisticated solution for businesses to gauge customer sentiment through automated review analysis. By streamlining the process from data collection to sentiment aggregation, the pipeline provides valuable insights into customer perceptions, enabling informed decision-making and targeted improvements to products and services. Through continuous refinement and incorporation of advanced analysis techniques, the solution stands as a robust tool for harnessing the power of customer feedback in shaping product strategies.

## Getting Started

### Prerequisites

- Python 3.8+
- Temporal Server
- Redis instance
- Docker and Docker Compose (optional)
- Kubernetes (optional)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/temporal-review-analyzer.git
cd temporal-review-analyzer
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Start the Temporal server (if running locally):

```bash
docker-compose up -d
```

4. Run the Flask application:

```bash
python routes.py
```

### Configuration

Configure the application by setting the following environment variables in `config.py` or through your deployment environment:

- `AMAZON_USERNAME` and `AMAZON_PASSWORD` for Amazon login.
- `TEMPORAL_HOST` and `TEMPORAL_PORT` for connecting to the Temporal server.
- `REDIS_HOST`, `REDIS_PORT`, and `REDIS_DB` for Redis connection details.

# Building and Running the Temporal Review Analyzer

## 1. Building the Docker Image

The application can be packaged into a Docker container. Two build scripts are provided for different architectures:

- `build.sh` for standard x86_64 architectures.
- `build-arm64.sh` for ARM64 architectures, suitable for newer Macs and some Linux distributions.

### Standard Build (x86_64)

Run the following command in your terminal:

```bash
./build.sh
```

### ARM64 Build

Run the following command in your terminal:

```bash
./build-arm64.sh
```

These scripts will build the Docker image and push it to Docker Hub. Make sure you are logged into Docker Hub with `docker login` before running the scripts.

## 2. Running Locally with Docker Compose

To run the application locally using Docker Compose, ensure you have `docker-compose.yml` file configured. Then, execute:

```bash
docker-compose up
```

This command will start all necessary services, including Temporal, Redis, and the Temporal Review Analyzer application.

## 3. Deploying to Kubernetes

To deploy the application to a Kubernetes cluster, follow these steps:

### Step 1: Create a Kubernetes Deployment

Make sure your `deployment.yml` file is correctly configured with the Docker image you built and pushed to Docker Hub. This file should define the deployment and any necessary services (like Redis and Temporal, if not already running in your cluster).

Apply the deployment to your cluster:

```bash
kubectl apply -f deployment.yml
```

### Step 2: Access the Application

If your deployment includes a LoadBalancer service type (as recommended for cloud deployments), you can obtain the external IP address using:

```bash
kubectl get svc
```

Look for the `temporal-review-analyzer-service` service and note the external IP. You can access the application via `http://EXTERNAL_IP:5000`.

For local Kubernetes clusters (e.g., Minikube), you might need to use port forwarding to access the service:

```bash
kubectl port-forward svc/temporal-review-analyzer-service 5000:5000
```

Now, you can access the application at `http://localhost:5000`.

## Next Steps

Explore the application's functionality by making HTTP requests to trigger review analyses. For example:

```bash
curl http://localhost:5000/sentiment?item=<ITEM_ID>
```

Replace `<ITEM_ID>` with the actual Amazon product ID.

## Testing Guide

This guide provides instructions on how to run automated tests for the Temporal Review Analyzer application. The tests are designed to send HTTP requests to the application for a list of predefined Amazon product IDs to analyze sentiment.

### Prerequisites

Before running the tests, ensure you have the following:

- The Temporal Review Analyzer application is running and accessible.
- `curl` installed on your system for sending HTTP requests.
- `jq` utility installed on your system for URL encoding of query parameters.

### Test Files

- **`items.txt`**: Contains a list of Amazon product IDs to be analyzed.
- **`test.sh`**: A shell script that reads `items.txt` and sends HTTP requests to the application for each product ID.

### Running the Tests

1. Ensure the Temporal Review Analyzer application is running and accessible at the specified URL within the `test.sh` script.
2. Open a terminal and navigate to the directory containing `test.sh` and `items.txt`.
3. Make `test.sh` executable by running:

```bash
chmod +x test.sh
```

4. Execute the test script:

```bash
./test.sh
```

The script will read each Amazon product ID from `items.txt`, URL encode the product ID, and send an HTTP GET request to the application. The application's response, including the sentiment analysis result for each product, will be printed to the terminal.

### Understanding `test.sh`

The script performs the following steps:

- Reads each line (product ID) from `items.txt`.
- Uses `jq` to URL encode the product ID to ensure it is properly formatted for inclusion in the query string of the HTTP request.
- Sends an HTTP GET request to the application for each product ID, using `curl`.
- Prints the application's response to the terminal.

By following these instructions, you can easily run automated tests against the Temporal Review Analyzer application to validate its functionality with various Amazon products.


# Contributing

Feel free to contribute to the project by submitting pull requests or opening issues for bugs or enhancements.
