# Temporal Review Analyzer

This project integrates OpenAI's ChatGPT for foundational natural language processing tasks. It explores a microservices architecture, utilizing Python's programming flexibility alongside Flask's HTTP request management. The system incorporates Temporal for workflow management and Redis for data storage, establishing a scalable framework for data processing. This MVP is designed to process and analyze Amazon review datasets on a manageable scale, aiming to provide basic sentiment analysis and insights.

The incorporation of ChatGPT's AI capabilities within a Python-based microservices framework marks the beginning of this project's journey. While the solution demonstrates a fundamental approach to navigating data workflows, it is cautious not to overstate its current capabilities. Instead, it presents an innovative, albeit initial, strategy for leveraging AI to begin understanding customer sentiments from sizable datasets. This effort aligns with the ongoing exploration within the field of data science, offering a starting point for more complex and scalable solutions in the future.


## Solution Overview

The pipeline is composed of several key components that work in unison:

**Scraping Module:** This component is responsible for systematically retrieving product reviews from Amazon. Utilizing Python with libraries such as requests and BeautifulSoup, it navigates product pages, extracts review data (including ratings, titles, and review text), and stores the information for further analysis.

**Sentiment Analysis Module:** Leveraging OpenAI's GPT model, and the TextBlob library, this module analyzes the sentiment of each review. The integration of OpenAI's GPT model allows for advanced sentiment analysis that can understand context and nuance in text far beyond traditional methods. Additionally, TextBlob provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, and sentiment analysis. Each review is assigned a sentiment score, indicating the review's overall positive, negative, or neutral tone.

**Data Storage and Management:** Redis, an in-memory data store, acts as the intermediary storage solution, holding the scraped reviews and their sentiment scores. Its fast read/write capabilities ensure efficient data handling throughout the analysis process.

**Aggregation and Scoring:** Once sentiment analysis is complete, the pipeline calculates the average sentiment score across all reviews, yielding an overall sentiment score for the product. This score is a float ranging from -1 (entirely negative) to 1 (entirely positive), providing a concise metric for assessing customer sentiment.

**Temporal Workflow Engine:** At the heart of the pipeline is Temporal, a workflow orchestration platform that manages the execution of tasks (scraping, analysis, aggregation). Temporal ensures fault tolerance, retries, and efficient execution, making the pipeline resilient and scalable.

**Flask Application:** A Flask-based web server acts as the interface for initiating the sentiment analysis pipeline. Users can trigger analysis through a simple HTTP request, specifying the product ID. The Flask application communicates with the Temporal workflow, which orchestrates the execution of the pipeline.


## Advanced OpenAI GPT Sentiment Analysis

The sentiment analysis module has been enhanced with the capability to use OpenAI's GPT model for an advanced analysis of review texts. This process includes:

**Preprocessing:** Each review text is preprocessed to remove unnecessary symbols, whitespace, and HTML tags. This step ensures the analysis focuses on the meaningful content of the review.

**OpenAI GPT Analysis:** For reviews that require a deeper understanding of context or contain nuanced expressions, the OpenAI GPT model is employed. This model can interpret the sentiment of complex sentences more accurately than traditional methods.

**Polarity Calculation:** For each cleaned review title, TextBlob evaluates the sentiment and assigns a polarity score. This score ranges from -1 to 1, where -1 represents a completely negative sentiment, 1 represents a completely positive sentiment, and 0 indicates neutrality.

**Hybrid Analysis Approach:** By combining the fast analysis from TextBlob with the depth of analysis provided by the GPT model, the system ensures efficient and comprehensive sentiment analysis across all reviews.

## Quantification and Aggregation
Once each review has been assigned a sentiment polarity score, the algorithm quantifies these scores to determine an overall sentiment score for the product.

**Weighting Reviews:** The algorithm can optionally weight reviews based on factors such as the review's helpfulness score, the recency of the review, or the reviewer's credibility. This step involves assigning more significance to certain reviews, although the initial implementation treats all reviews equally.

**Averaging Polarity Scores:** The core of the analysis algorithm is the calculation of the average sentiment polarity score across all reviews. This average represents the overall sentiment for the product, summarizing the collective opinion of all reviewers.

**Interpreting the Score:** The final average polarity score is interpreted to provide a qualitative understanding of the sentiment. For example, scores near 1 indicate overwhelmingly positive sentiment, scores near -1 indicate negative sentiment, and scores around 0 suggest mixed or neutral sentiment.

## Enhancements for Depth of Analysis
To further enhance the analysis algorithm, several improvements can be considered:

**Natural Language Understanding (NLU):** Integrating more advanced NLU capabilities can improve sentiment detection accuracy, especially for reviews with complex expressions, sarcasm, or nuanced opinions.

**Aspect-Based Sentiment Analysis:** By breaking down the sentiment analysis to specific aspects or features of the product (e.g., quality, value for money, customer service), the algorithm can provide more granular insights into customer opinions.

**Machine Learning Models:** Custom machine learning models trained on domain-specific datasets can outperform general-purpose libraries like TextBlob, especially when tailored to the nuances of product reviews in specific categories.


## Implementation Overview

- **Flask Application (`routes.py`)**: Serves as the entry point for the application, handling HTTP requests and triggering Temporal workflows.
- **Temporal Workflow (`main.py`)**: Orchestrates the review scraping and analysis tasks, ensuring reliable execution and fault tolerance.
- **Scraper Activity (`scrape.py`)**: Scrapes review data from Amazon product pages and stores it in Redis.
- **Analysis Activity (`analyze.py`)**: Analyzes the scraped review data using both TextBlob and OpenAI's GPT model to determine overall sentiment.
- **Configuration (`config.py`)**: Manages environment variables and application configuration settings, including the OpenAI API key.
- **Redis** Acts as a temporary data store for the scraped reviews, facilitating distributed processing.

### Key Features

- Scalable review scraping and analysis.
- Fault-tolerant workflow execution with Temporal.
- Simple HTTP interface for triggering analysis jobs.
- Configurable for different Amazon products.

## Getting Started

### Prerequisites

- Access to OpenAI API with a valid API key.
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
python3 src/main.py
```

### Configuration

Configure the application by setting the following environment variables in `config.py` or through your deployment environment:

- `AMAZON_USERNAME` and `AMAZON_PASSWORD` for Amazon login (optional).
- `TEMPORAL_HOST` and `TEMPORAL_PORT` for connecting to the Temporal server.
- `REDIS_HOST`, `REDIS_PORT`, and `REDIS_DB` for Redis connection details.
-  `OPENAI_API_KEY` for OpenAI API access.



# Building and Running the Temporal Review Analyzer

## 1. Building the Docker Image (Optional)

The application can be packaged into a Docker container. Two build scripts are provided for different architectures:

- `build.sh` for standard x86_64 architectures.
- `build-arm64.sh` for ARM64 architectures, such as a Rasberry Pi K3s environment.

### Standard Build (x86_64)

Run the following command in your terminal:

```bash
./build.sh
```

### ARM64 Build

Be sure to run this on the same arch node you plan to ultimately execute your pods on.

```bash
./build-arm64.sh
```

These scripts will build the Docker image and push it to Docker Hub. Make sure you are logged into Docker Hub with `docker login` before running the scripts.

## 2. Running Locally with Docker Compose

To run the application locally using Docker Compose, ensure you have `docker-compose.yml` file configured. Then, execute:

```bash
docker-compose up
```

This command will start the Review Analyzer application.

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

- **`items1.txt`**: Contains a list of Amazon product IDs to be analyzed.
- **`test1.sh`**: A shell script that reads `items1.txt` and sends HTTP requests to the application for each product ID.

### Running the Tests

1. Ensure the Temporal Review Analyzer application is running and accessible at the specified URL within the `test1.sh` script.
2. Open a terminal and navigate to the directory containing `test1.sh` and `items1.txt`.
3. Make `test1.sh` executable by running:

```bash
chmod +x test1.sh
```

4. Execute the test script:

```bash
./test1.sh
```

The script will read each Amazon product ID from `items1.txt`, URL encode the product ID, and send an HTTP GET request to the application. The application's response, including the sentiment analysis result for each product, will be printed to the terminal.

```bash
(env) Bens-MacBook-Pro:temporal-review-analyzer bbertka$ ./test1.sh
{"item":"B0CJVL51V9","result":82.664,"verdict":"B-"}
{"item":"B07CJV9H25","result":92.67128712871293,"verdict":"A-"}
{"item":"B0CL38TZ3L","result":68.2,"verdict":"D+"}
{"item":"B0CF1VZ5H4","result":70.65714285714286,"verdict":"C-"}
{"item":"B0CF1ZVLKS","result":80.84444444444445,"verdict":"B-"}
{"item":"B0CF1TFM39","result":79.10000000000001,"verdict":"C+"}
{"item":"B0CVX5RTZJ","result":0.0,"verdict":"F"}
{"item":"B0BN1K7ZLZ","result":58.228571428571435,"verdict":"F"}
{"item":"B0CR8KY6G5","result":0.0,"verdict":"F"}
{"item":"B0B6148YKN","result":92.580198019802,"verdict":"A-"}
{"item":"B09WB2NL8W","result":90.98019801980203,"verdict":"A-"}
{"item":"B07BPKL2D2","result":92.53267326732676,"verdict":"A-"}
{"item":"B07Q5HMXTN","result":86.52277227722779,"verdict":"B"}
```

### Understanding `test1.sh`

The script performs the following steps:

- Reads each line (product ID) from `items1.txt`.
- Uses `jq` to URL encode the product ID to ensure it is properly formatted for inclusion in the query string of the HTTP request.
- Sends an HTTP GET request to the application for each product ID, using `curl`.
- Prints the application's response to the terminal.

By following these instructions, you can easily run automated tests against the Temporal Review Analyzer application to validate its functionality with various Amazon products.


# Contributing

Contributions to enhance the Temporal Review Analyzer, such as improving the analysis algorithms, extending the functionality, or optimizing the architecture, are welcome. Please submit pull requests or open issues for any bugs or feature suggestions.