
# Evolução do Chat-Bot-Telegram

Este projeto é um sistema de gerenciamento de produtos, categorias, usuários e pedidos, integrado a um chatbot para facilitar a interação com os usuários. O sistema inclui funcionalidades de cadastro, edição, exclusão e visualização de produtos e categorias, além de alertas de novos pedidos e suporte a pagamentos e rastreamento via chatbot.

## Funcionalidades Principais

- Cadastro e gerenciamento de produtos e categorias  
- Menu de usuários com níveis de acesso e autenticação segura  
- Painel de controle para gerenciar pedidos e status  
- Integração com Telegram para catálogo de produtos e suporte a clientes  
- Processamento de pagamentos via chatbot  

## Pré-Requisitos

1. Instale os seguintes softwares:  
   - Python 3.x  
   - Telegram (para configurar e testar o bot)  

2. Clone o repositório:  
   ```bash
   git clone <https://github.com/DjoninhaA/chat-bot-telegram.git>
   ```

3. Acesse o diretório do projeto:  
   ```bash
   cd chat-bot-telegram
   ```

4. Crie um ambiente virtual:  
   ```bash
   python -m venv venv
   ```

5. Ative o ambiente virtual:  
   - No Windows:  
     ```bash
     .\venv\Scripts\activate
     ```
   - No Mac/Linux:  
     ```bash
     source venv/bin/activate
     ```

6. Instale as dependências:  
   ```bash
   pip install -r requirements.txt
   ```

## Configuração e Instalação

1. **Configuração do Banco de Dados**  
   - Certifique-se de ter um banco de dados PostgreSQL, MySQL ou SQLite configurado.  
   - No arquivo `settings.py`, atualize as credenciais na seção `DATABASES` para conectar ao banco.  

2. **Migrações do Banco de Dados**  
   Aplique as migrações para criar as tabelas no banco de dados:  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Criação do Superusuário**  
   Crie um superusuário para acessar o painel administrativo:  
   ```bash
   python manage.py createsuperuser
   ```

4. **Iniciar o Servidor**  
   Inicie o servidor Django para acessar a aplicação:  
   ```bash
   python manage.py runserver
   ```

5. **Iniciar o Bot do Telegram**  
   Execute o arquivo que gerencia o bot para integrá-lo ao Telegram:  
   ```bash
   python manage.py startbot
   ```

## Rotas Principais

### Produtos
- `GET /api/products/` - Listar produtos  
- `POST /api/products/` - Criar um produto  
- `PUT /api/products/<id>/` - Atualizar um produto  
- `DELETE /api/products/<id>/` - Deletar um produto  

### Pedidos
- `GET /pedidos/` - Listar pedidos  
- `POST /pedidos/` - Criar um pedido  
- `PATCH /pedidos/`/<id>/` - Atualizar status de um pedido  

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias e correções.
