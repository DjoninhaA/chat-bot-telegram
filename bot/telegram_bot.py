import os
import json
import requests
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
API_KEY = os.getenv('BOT_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL')

USER_NAME = ""
ID_PRODUTOS_PEDIDO = []

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global USER_NAME
    USER_NAME = message.from_user.first_name
    welcome_message = "Bem-vindo ao nosso cardápio!"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Categorias", callback_data="navigate_to_categories"))
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "navigate_to_categories")
def navigate_to_categories(call):
    category_message(call.message)

def category_message(message):
    url = f"{API_BASE_URL}/produto/data/"
    response = requests.get(url)
    try:
        products = response.json().get('produtos', [])
    except json.JSONDecodeError:
        products = []
    categories = set(product['categoria__nome'] for product in products)
    markup = InlineKeyboardMarkup()
    for category in categories:
        markup.add(InlineKeyboardButton(category, callback_data=f"category_{category}"))
    markup.add(InlineKeyboardButton("Voltar", callback_data="start"))
    bot.send_message(message.chat.id, "Categorias disponíveis:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))
def show_category_products(call):
    category = call.data.split("_")[1]
    url = f"{API_BASE_URL}/produto/data/"
    response = requests.get(url)
    try:
        products = response.json().get('produtos', [])
    except json.JSONDecodeError:
        products = []
    category_products = [product for product in products if product['categoria__nome'] == category]
    message = f"Produtos na categoria {category}:\n\n"
    markup = InlineKeyboardMarkup()
    for product in category_products:
        markup.add(InlineKeyboardButton(product['nome'], callback_data=f"product_{product['nome']}"))
    markup.add(InlineKeyboardButton("Voltar", callback_data="navigate_to_categories"))
    bot.send_message(call.message.chat.id, message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("product_"))
def show_product_details(call):
    product_name = call.data.split("_")[1]
    url = f"{API_BASE_URL}/produto/data/"
    response = requests.get(url)
    try:
        products = response.json().get('produtos', [])
    except json.JSONDecodeError:
        products = []
    product = next((p for p in products if p['nome'] == product_name), None)
    if product:
        message = (
            f"Detalhes do Produto:\n\n"
            f"Nome: {product['nome']}\n"
            f"Descrição: {product['descricao']}\n"
            f"Preço: R$ {product['preco']}\n"
            f"Categoria: {product['categoria__nome']}\n\n"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Adicionar ao Carrinho", callback_data=f"add_to_cart_{product['nome']}"))
        markup.add(InlineKeyboardButton("Voltar", callback_data=f"category_{product['categoria__nome']}"))
        bot.send_message(call.message.chat.id, message, reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, f"Produto {product_name} não encontrado.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_to_cart_"))
def add_to_cart(call):
    """ print(call.data) """
    product_name = call.data.replace("add_to_cart_", "")
    print(product_name)
    global ID_PRODUTOS_PEDIDO
    product_id = get_product_id_by_name(product_name)
    if product_id:
        ID_PRODUTOS_PEDIDO.append(product_id)
        bot.send_message(call.message.chat.id, f"Produto {product_name} adicionado ao carrinho com sucesso!")
    else:
        bot.send_message(call.message.chat.id, f"Erro ao adicionar o produto {product_name} ao carrinho.")
        

def get_product_id_by_name(product_name):
    url = f"{API_BASE_URL}/produto/data/"
    response = requests.get(url)
    if response.status_code == 200:
        products = response.json().get('produtos', [])
        for product in products:
            if product['nome'] == product_name:
                return product['id']
    else:
        print(f"Erro ao buscar produtos: {response.status_code}")
    return None

if __name__ == "__main__":
    bot.polling()