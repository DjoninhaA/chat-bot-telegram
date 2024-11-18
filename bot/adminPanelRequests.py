import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')

def showProducts():
    response = requests.get(f"{API_BASE_URL}/produto/data/")
    products = response.json()
    return products['produtos']