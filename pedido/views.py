import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Pedido, Produto
from django.views.decorators.csrf import csrf_exempt

# View para renderizar pedidos (exemplo de visualização, se necessário)
def get_order(request):
    return render(request, 'pedidos.html')

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
    