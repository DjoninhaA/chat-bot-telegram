import os
import requests
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')

def add_to_cart(user_id, product):
    url = f"{API_BASE_URL}/add_to_cart/"
    payload = {
        "user_id": user_id,
        "product_name": product["name"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

def get_cart(user_id):
    url = f"{API_BASE_URL}/cart/"
    params = {
        "user_id": user_id
    }
    response = requests.get(url, params=params)
    return response.json().get("cart", [])

def products_api(request):
    response = requests.get('https://api.example.com/products')  # Substitua pela URL da sua API externa
    if response.status_code == 200:
        products = response.json()
        categories = set(product['category'] for product in products)
        categorized_products = {category: [] for category in categories}
        for product in products:
            categorized_products[product['category']].append(product)
        return JsonResponse({"categories": list(categories), "products": categorized_products})
    else:
        return JsonResponse({"error": "Não foi possível obter os produtos"}, status=response.status_code)