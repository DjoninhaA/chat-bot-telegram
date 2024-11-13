import os
import telebot
from telebot.util import quick_markup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, MenuButtonWebApp, WebAppInfo
import json
from dotenv import load_dotenv

from .adminPanelRequests import showProducts, showCart
from .cart import add_to_cart, get_cart

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
botToken = os.getenv('BOT_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL')

bot = telebot.TeleBot(botToken)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '<b>Bem vindo ao nosso restaurante!</b>', parse_mode='HTML', reply_markup=gen_markup_menu())

def gen_markup_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Catálogo", web_app=WebAppInfo(url=f"{API_BASE_URL}/catalog/")),
        InlineKeyboardButton("Sacola", web_app=WebAppInfo(url=f"{API_BASE_URL}/cart/")),
    )
    return markup

def gen_markup_cart():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Finalizar Compra", callback_data="/checkout"),
        InlineKeyboardButton("Voltar ao Catálogo", callback_data="/catalog"),
    )
    return markup

def gen_markup_checkout():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Pagar", callback_data="/pay"),
        InlineKeyboardButton("Cancelar", callback_data="/cancel"),
    )
    return markup

def gen_markup_payment():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Cartão de Crédito", callback_data="/credit_card"),
        InlineKeyboardButton("Boleto", callback_data="/boleto"),
    )
    return markup

def gen_markup_confirmation():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Confirmar", callback_data="/confirm"),
        InlineKeyboardButton("Cancelar", callback_data="/cancel"),
    )
    return markup

def gen_markup_catalog_products():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    products_json = showProducts()
    for product in json.loads(products_json)["products"]:
        markup.add(InlineKeyboardButton(product["name"], callback_data=f"/add_{product['name']}"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.message.chat.id
    if call.data == "/catalog":
        bot.send_message(user_id, '<b>Catálogo:</b>', parse_mode='HTML', reply_markup=gen_markup_catalog_products())
    elif call.data == "/cart":
        cart_items = get_cart(user_id)
        formatted_message = format_cart_message(cart_items)
        bot.send_message(user_id, formatted_message, parse_mode='HTML')
    elif call.data.startswith("/add_"):
        product_name = call.data.split("_")[1]
        products_json = showProducts()
        products = json.loads(products_json)["products"]
        product = next((p for p in products if p["name"] == product_name), None)
        if product:
            add_to_cart(user_id, product)
            bot.send_message(user_id, f"{product_name} foi adicionado ao seu carrinho.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def format_cart_message(cart_items):
    if not cart_items:
        return "Seu carrinho está vazio."
    message = "<b>Seu Carrinho:</b>\n"
    for item in cart_items:
        message += f"\n<b>{item['name']}</b>\n"
        message += f"Preço: {item['price']}\n"
    return message

def start_bot():
    bot.polling()

def set_webhook():
    webhook_url = f"https://your-domain.com/bot/telegram-webhook/"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    #set_webhook()
    start_bot()