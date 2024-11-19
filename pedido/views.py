import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Pedido, Produto
from django.views.decorators.csrf import csrf_exempt

# View para renderizar pedidos (exemplo de visualização, se necessário)
def get_status_string(status_code):
    status_mapping = {
        0: "Pendente",
        1: "Em andamento",
        2: "Concluído",
        # Adicione outros status se necessário
    }
    return status_mapping.get(status_code, "Desconhecido")

def renderizar(request):
    if request.method =="GET":
        return(request, 'pedido.html')

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
                cliente=data['cliente']
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
