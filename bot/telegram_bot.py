import os
import json
import requests
from dotenv import load_dotenv
from telegram_menu import BaseMessage, TelegramMenuSession, NavigationHandler

load_dotenv()
API_KEY = os.getenv('BOT_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL')

class StartMessage(BaseMessage):
    LABEL = "start"

    def __init__(self, navigation: NavigationHandler) -> None:
        super().__init__(navigation, StartMessage.LABEL)

    def update(self, navigation) -> str:
        print("update called")  # Log para depuração
        welcomeMessage = "Bem-vindo ao nosso cardápio!"
        category_message = CategoryMessage(navigation, "Categorias")
        self.add_button(label="Categorias", callback=category_message)
        return welcomeMessage

    def get_keyboard(self):
        print("get_keyboard called")  # Log para depuração
        url = f"{API_BASE_URL}/produto/data/"
        print(f"Requesting URL: {url}")  # Log para depuração
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")  # Log para depuração
        print(f"Response content: {response.content}")  # Log para depuração
        try:
            products = response.json().get('produtos', [])
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")  # Log para depuração
            products = []
        categories = set(product['categoria__nome'] for product in products)
        buttons = [{"text": category, "callback_data": category} for category in categories]
        print("Categories:", categories)  # Log para depuração
        print("Buttons:", buttons)  # Log para depuração
        return buttons

class CategoryMessage(BaseMessage):
    LABEL = "Categorias"

    def __init__(self, navigation: NavigationHandler, category: str) -> None:
        super().__init__(navigation, CategoryMessage.LABEL)
        self.category = category

    def update(self) -> str:
        print(f"update called for category: {self.category}")  # Log para depuração
        url = f"{API_BASE_URL}/produto/data/"
        print(f"Requesting URL: {url}")  # Log para depuração
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")  # Log para depuração
        print(f"Response content: {response.content}")  # Log para depuração
        try:
            products = response.json().get('produtos', [])
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")  # Log para depuração
            products = []
        categories = set(product['categoria__nome'] for product in products)
        for category in categories:
            self.add_button(label=category, callback=ProductMessage(self.navigation, category))
        return f"Produtos na categoria {self.category}:\n\n"

    def get_keyboard(self):
        print(f"get_keyboard called for category: {self.category}")  # Log para depuração
        return [{"text": "Voltar", "callback_data": "start"}]

class ProductMessage(BaseMessage):
    LABEL = "product"

    def __init__(self, navigation: NavigationHandler, category: str) -> None:
        super().__init__(navigation, ProductMessage.LABEL)
        self.category = category

    def update(self) -> str:
        print(f"update called for category: {self.category}")  # Log para depuração
        url = f"{API_BASE_URL}/produto/data/"
        print(f"Requesting URL: {url}")  # Log para depuração
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")  # Log para depuração
        print(f"Response content: {response.content}")  # Log para depuração
        try:
            products = response.json().get('produtos', [])
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")  # Log para depuração
            products = []
        message = f"Produtos na categoria {self.category}:\n\n"
        category_products = [product for product in products if product['categoria__nome'] == self.category]
        for product in category_products:
            self.add_button(label=product['nome'], callback=ProductMessage(self.navigation, product['nome']))
        return message

    def get_keyboard(self):
        print(f"get_keyboard called for category: {self.category}")  # Log para depuração
        return [{"text": "Voltar", "callback_data": "start"}]

def start_bot():
    print("Starting bot...")  # Log para depuração
    menu_session = TelegramMenuSession(API_KEY)
    menu_session.start(StartMessage)

if __name__ == "__main__":
    start_bot()