# OpenAI GPT Review Analyzer 

This project integrates OpenAI's ChatGPT for foundational natural language processing tasks. It explores a microservices architecture, utilizing Python's programming flexibility alongside Flask's HTTP request management. The system incorporates Temporal for workflow management and Redis for data storage, establishing a scalable framework for data processing. This MVP is designed to process and analyze Amazon review datasets on a manageable scale, aiming to provide basic sentiment analysis and insights.

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
- Temporal Server
- Redis instance
- Kubernetes
- GitLab 

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

