# config.py
import os

# Default values can be provided as a fallback
PORT = int(os.getenv("PORT", 5000))
TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "192.168.1.114")
TEMPORAL_PORT = os.getenv("TEMPORAL_PORT", "7233")
REDIS_HOST = os.getenv("REDIS_HOST", "192.168.1.110")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = os.getenv("REDIS_DB", "0")
AMAZON_USERNAME = os.getenv("AMAZON_USERNAME")
AMAZON_PASSWORD = os.getenv("AMAZON_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")