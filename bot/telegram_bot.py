import os
import json
import requests
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from bot.pagamento import enviar_pix_qr_code

load_dotenv()
API_KEY = os.getenv('BOT_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL')

USER_NAME = ""
ID_PRODUTOS_PEDIDO = []
ENDERECO_ENTREGA = ""

bot = telebot.TeleBot(API_KEY)

# Certifique-se de que o caminho da pasta de mídia está correto
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media', 'images')

# Variável global para armazenar os IDs das mensagens enviadas
global MENSAGENS_ENVIADAS
MENSAGENS_ENVIADAS = []

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
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Categorias disponíveis:", reply_markup=markup)

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
    
    # Apagar a mensagem do menu de categorias
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    
    for product in category_products:
        message = (
            f"Nome: {product['nome']}\n"
            f"Descrição: {product['descricao']}\n"
            f"Preço: R$ {product['preco']}\n"
        )
        
        # Remover a parte 'http://127.0.0.1:8000' da URL da imagem
        image_url = product["imagem"].replace("http://127.0.0.1:8000/", "")
        with open(image_url, 'rb') as image_file:
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=image_file,
                caption=message,
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("Adicionar ao Carrinho", callback_data=f"add_to_cart_{product['nome']}")
                )
            )
    
    # Adicionar botão de voltar ao final
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Voltar", callback_data="navigate_to_categories"))
    bot.send_message(call.message.chat.id, "Deseja voltar ao menu de categorias?", reply_markup=markup)

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
        markup.add(InlineKeyboardButton("Voltar", callback_data="navigate_to_categories"))
        
        image_url = product["imagem"].replace("http://127.0.0.1:8000/", "")
        with open(image_url, 'rb') as image_file:
            sent_message = bot.send_photo(
                chat_id=call.message.chat.id,
                photo=image_file,
                caption=message,
                reply_markup=markup
            )
            MENSAGENS_ENVIADAS.append(sent_message.message_id)
    else:
        sent_message = bot.send_message(call.message.chat.id,
                         f"Produto {product_name} não encontrado.")
        MENSAGENS_ENVIADAS.append(sent_message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_to_cart_"))
def add_to_cart(call):
    product_name = call.data.replace("add_to_cart_", "")
    global ID_PRODUTOS_PEDIDO
    product_id = get_product_id_by_name(product_name)
    if product_id:
        ID_PRODUTOS_PEDIDO.append(product_id)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Voltar", callback_data="navigate_to_categories"))
        markup.add(InlineKeyboardButton("Finalizar pedido", callback_data="finalizar_pedido"))
        bot.send_message(chat_id=call.message.chat.id, text="Produto adicionado ao carrinho! \nDeseja comprar outros produtos?", reply_markup=markup)
    else:
        bot.send_message(chat_id=call.message.chat.id, text=f"Erro ao adicionar o produto {product_name} ao carrinho.")
    
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

def calcular_valor_total(produtos_ids):
    url = f"{API_BASE_URL}/produto/data/"
    response = requests.get(url)
    try:
        products = response.json().get('produtos', [])
    except json.JSONDecodeError:
        products = []
    total = 0
    for product_id in produtos_ids:
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            total += float(product['preco'])
    return total

@bot.callback_query_handler(func=lambda call: call.data == "finalizar_pedido")
def finalizar_pedido(call):
    bot.send_message(call.message.chat.id, "Por favor, informe o endereço de entrega:")
    bot.register_next_step_handler(call.message, receber_endereco_entrega)

def receber_endereco_entrega(message):
    global ENDERECO_ENTREGA
    ENDERECO_ENTREGA = message.text
    valor_total = calcular_valor_total(ID_PRODUTOS_PEDIDO)
    chave_pix = "45998240404"
    descricao = "Pagamento do pedido:" + " + ".join(get_product_names(ID_PRODUTOS_PEDIDO))
    
    enviar_pix_qr_code(message.chat.id, valor_total, chave_pix, descricao, bot)
    bot.send_message(message.chat.id, f"Pedido finalizado! Use o QR Code acima para realizar o pagamento via Pix.\n\nEndereço de entrega: {ENDERECO_ENTREGA}")

def get_product_names(produtos_ids):
    url = f"{API_BASE_URL}/produto/data/"
    response = requests.get(url)
    try:
        products = response.json().get('produtos', [])
    except json.JSONDecodeError:
        products = []
    product_names = []
    for product_id in produtos_ids:
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            product_names.append(product['nome'])
    return product_names

if __name__ == "__main__":
    bot.polling()