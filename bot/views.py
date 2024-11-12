import os
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import telebot
from .telegram_bot import bot
from django.shortcuts import render
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')

# Simulação de um banco de dados em memória para o carrinho
cart_db = {}

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)

def catalog_view(request):
    return render(request, 'catalog.html')

def products_api(request):
    response = requests.get(f'{API_BASE_URL}/products')  # Substitua pela URL da sua API externa
    if response.status_code == 200:
        products = response.json()
        return JsonResponse({"products": products})
    else:
        return JsonResponse({"error": "Não foi possível obter os produtos"}, status=response.status_code)

@csrf_exempt
def add_to_cart_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        product_name = data.get('product_name')

        # Obter a lista de produtos da API
        response = requests.get(f'{API_BASE_URL}/products')  # Substitua pela URL da sua API externa
        if response.status_code == 200:
            products = response.json()
            product = next((p for p in products if p["name"] == product_name), None)
            if product:
                if user_id not in cart_db:
                    cart_db[user_id] = []
                cart_db[user_id].append(product)
                return JsonResponse({"message": f"{product_name} foi adicionado ao carrinho"})
            return JsonResponse({"message": "Produto não encontrado"}, status=404)
        else:
            return JsonResponse({"message": "Não foi possível obter os produtos"}, status=response.status_code)
    return JsonResponse({"message": "Método não permitido"}, status=405)

def cart_view(request):
    return render(request, 'cart.html')

def cart_api(request):
    user_id = request.GET.get('user_id')
    cart = cart_db.get(user_id, [])
    return JsonResponse({"cart": cart})

@csrf_exempt
def finalize_order_api(request):
    if request.method == 'POST':
        # Adicione a lógica para finalizar o pedido
        return JsonResponse({"message": "Pedido finalizado com sucesso"})
    return JsonResponse({"message": "Método não permitido"}, status=405)

""" from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status

from rest_framework.decorators import api_view


from  .serializers import UserSerializer



def config_bot(request):
    return render(request, 'configuracao.html')

def home_bot(request):
    return render(request, 'login.html')
    
@api_view(['POST'])   
def create_bot(request):
    if request.method == 'POST':
        new_bot = request.data

        serializer = UserSerializer(data=new_bot)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
     """