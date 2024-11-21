import os
import json
import requests
from dotenv import load_dotenv
from telegram_menu import BaseMessage, TelegramMenuSession, NavigationHandler

load_dotenv()
API_KEY = os.getenv('BOT_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL')

USER_NAME = ""
ID_PRODUTOS_PEDIDO = []

class StartMessage(BaseMessage):
    LABEL = "start"

    def __init__(self, navigation: NavigationHandler) -> None:
        super().__init__(navigation, StartMessage.LABEL)

    def update(self) -> str:
        welcomeMessage = "Bem-vindo ao nosso cardápio!"
        global USER_NAME
        USER_NAME = self.navigation.user_name
        self.add_button(label="Categorias", callback=self.navigate_to_categories)
        return welcomeMessage

    async def navigate_to_categories(self) -> None:
        category_message = CategoryMessage(self.navigation)
        await self.navigation.goto_menu(category_message)

class CategoryMessage(BaseMessage):
    LABEL = "Categorias"

    def __init__(self, navigation: NavigationHandler) -> None:
        super().__init__(navigation, CategoryMessage.LABEL)
        self.category = None

    def update(self) -> str:
        url = f"{API_BASE_URL}/produto/data/"
        response = requests.get(url)
        try:
            products = response.json().get('produtos', [])
        except json.JSONDecodeError as e:
            products = []
        categories = set(product['categoria__nome'] for product in products)
        for category in categories:
            self.add_button(label=category, callback=ProductMessage(self.navigation, category=category))
        return "Categorias disponíveis:\n\n"

class ProductMessage(BaseMessage):
    LABEL = "product"

    def __init__(self, navigation: NavigationHandler, product_name: str = None, category: str = None) -> None:
        super().__init__(navigation, ProductMessage.LABEL)
        self.product_name = product_name
        self.category = category

    def update(self) -> str:
        if self.product_name:
            return self.get_product_details()
        else:
            return self.get_category_products()

    def get_category_products(self) -> str:
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
            self.add_button(label=product['nome'], callback=ProductMessage(self.navigation, product_name=product['nome']))
        return message

    def get_product_details(self) -> str:
        print(f"update called for product: {self.product_name}")  # Log para depuração
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
        
        product = next((p for p in products if p['nome'] == self.product_name), None)
        if product:
            message = (
                f"Detalhes do Produto:\n\n"
                f"Nome: {product['nome']}\n"
                f"Descrição: {product['descricao']}\n"
                f"Preço: R$ {product['preco']}\n"
                #f"Tempo de Preparo: {product['tempoDePreparo']} minutos\n"
                #f"Subcategoria: {product['subcategoria']}\n"
                f"Categoria: {product['categoria__nome']}\n\n"
            )
            self.add_button(label="Adicionar ao Carrinho", callback=AddToCartMessage(self.navigation, [self.product_name]))
            return message
        else:
            return f"Produto {self.product_name} não encontrado."

    def get_keyboard(self):
        print(f"get_keyboard called for category: {self.category}")  # Log para depuração
        return [{"text": "Voltar", "callback_data": "start"}]

class AddToCartMessage(BaseMessage):
    LABEL = "add_to_cart"

    def __init__(self, navigation: NavigationHandler, product_names: list) -> None:
        super().__init__(navigation, AddToCartMessage.LABEL)
        self.product_names = product_names
        print(f"Nome: {USER_NAME}")  # Log para depuração

    def update(self) -> str:
        urlPostPedido = f"{API_BASE_URL}/pedido/criar/"
        
        # Obter os IDs dos produtos a partir dos nomes dos produtos
        global ID_PRODUTOS_PEDIDO
        ID_PRODUTOS_PEDIDO = [self.get_product_id_by_name(product_name) for product_name in self.product_names]

        payload = {
            "produtos_ids": ID_PRODUTOS_PEDIDO, 
            "status": 0,
            "cliente": USER_NAME,  # Usar o nome da conversa
            "quantidade": 1  # Você pode ajustar a quantidade conforme necessário
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(urlPostPedido, json=payload, headers=headers)
        
        if response.status_code == 201:
            return f"Produtos {', '.join(self.product_names)} adicionados ao carrinho com sucesso!"
        else:
            print(f"Erro: {response.content}, status code: {response.status_code}")
            return f"Erro ao adicionar os produtos ao carrinho."

    def get_product_id_by_name(self, product_name: str) -> int:
        url = f"{API_BASE_URL}/produto/data/"
        response = requests.get(url)
        if response.status_code == 200:
            products = response.json().get('produtos', [])
            for product in products:
                if product['nome'] == product_name:
                    return product['id']
        return None

def start_bot():
    print("Starting bot...")  # Log para depuração
    menu_session = TelegramMenuSession(API_KEY)
    menu_session.start(StartMessage)

if __name__ == "__main__":
    start_bot()