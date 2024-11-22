import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Pedido, Produto
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Outras configurações...

BOT_TOKEN = os.getenv('BOT_TOKEN')

def get_status_string(status_code):
    status_mapping = {
        0: "Aguardando",
        1: "Preparando",
        2: "Pronto",
        3: "Entregue",
        4: "Cancelado"
    }
    return status_mapping.get(status_code, "Desconhecido")

@login_required
def getPedidos(request):
    
    return render(request, 'pedidos.html', {'active_page': 'Pedidos'})

@csrf_exempt
def alterar_status(request, pedido_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            status = data.get('status')

            if status not in [0, 1, 2, 3]:
                return JsonResponse({'error': 'Status inválido'}, status=400)

            pedido = Pedido.objects.get(id=pedido_id)
            pedido.status = status
            pedido.save()

            # Enviar notificação ao bot
            send_status_update_to_bot(pedido.cliente, pedido.id, status)

            return JsonResponse({'status': pedido.get_status_display()}, status=200)

        except Pedido.DoesNotExist:
            return JsonResponse({'error': f'Pedido com ID {pedido_id} não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def send_status_update_to_bot(cliente, pedido_id, status):
    chat_id = get_chat_id_by_cliente(cliente)  # Função para obter o chat_id do cliente
    status_message = f"O status do seu pedido #{pedido_id} foi atualizado para: {get_status_string(status)}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': status_message
    }
    requests.post(url, json=payload)

def get_chat_id_by_cliente(cliente):
    # Implementar lógica para obter o chat_id do cliente com base no nome ou ID do cliente
    pass

@login_required
def search_pedidos(request):
    query = request.GET.get('query', '')

    if query.isdigit():
        pedidos = Pedido.objects.filter(id=int(query))
    else:
        pedidos = Pedido.objects.filter(cliente__icontains=query)

    pedidos_data = []
    for pedido in pedidos:
        pedidos_data.append({
            'id': pedido.id,
            'status': get_status_string(pedido.status),
            'valor': pedido.valor,
            'cliente': pedido.cliente,
            'produtos': [produto.nome for produto in pedido.produto.all()],
        })

    return JsonResponse({'pedidos': pedidos_data}, status=200)

@csrf_exempt
def listar_pedidos(request):
    if request.method == 'GET':
        try:
            # Buscar todos os pedidos
            pedidos = Pedido.objects.all()
            
            # Transformar os pedidos em um formato que possa ser retornado como JSON
            pedidos_data = []
            for pedido in pedidos:
                pedidos_data.append({
                    'id': pedido.id,
                    'status': get_status_string(pedido.status),
                    'valor': pedido.valor,
                    'cliente': pedido.cliente,
                   'produtos': [{
                        'id': produto.id,
                        'nome': produto.nome  # Adicionando o nome do produto
                    } for produto in pedido.produto.all()],
                })

            # Retornar os pedidos como JSON
            return JsonResponse({'pedidos': pedidos_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def pedido_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Inicializar o valor total
            valor_total = 0
            produtos_ids = data.get('produtos_ids', [])

            # Validar e buscar os produtos
            produtos = []
            for produto_id in produtos_ids:
                try:
                    produto = Produto.objects.get(id=produto_id)
                    produtos.append(produto)
                    valor_total += produto.preco  # Supondo que Produto tem um campo 'preco'
                except Produto.DoesNotExist:
                    return JsonResponse({'error': f'Produto com ID {produto_id} não encontrado'}, status=404)

            # Criar o pedido com o valor total e cliente
            pedido = Pedido.objects.create(
                status=data['status'],
                valor=valor_total,
                cliente=data['cliente'],
                endereco_entrega=data['endereco_entrega']
            )

            # Associar os produtos ao pedido
            pedido.produto.set(produtos)

            return JsonResponse({'message': 'Pedido criado com sucesso'}, status=201)

        except KeyError as e:
            return JsonResponse({'error': f'Campo {e} é necessário'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
    
@csrf_exempt
def deletar_pedido(request, pedido_id):
    if request.method == 'DELETE':
        try:

            pedido = Pedido.objects.get(id=pedido_id)
            pedido.delete()
            return JsonResponse({'message': f'Pedido com ID {pedido_id} deletado com sucesso.'}, status=200)

        except Pedido.DoesNotExist:
            return JsonResponse({'error': f'Pedido com ID {pedido_id} não encontrado.'}, status=404)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
