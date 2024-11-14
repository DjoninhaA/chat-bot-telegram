import os
import requests
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')

def showProducts():
    response = requests.get(f"{API_BASE_URL}/produto/data/")
    products = response.json()
    products_json = json.dumps(products)
    return products_json

def showCart():
    response = requests.get(f"{API_BASE_URL}/cart")
    cart = response.json()
    return cart