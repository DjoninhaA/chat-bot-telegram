# produto/views.py
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from produto.models import Produto


def get_products(request):
    
    return render(request, 'produtos.html', {'active_page': 'Produtos'})

def produtos_data(request):
    produtos = Produto.objects.all().values()

    pageNumber = int(request.GET.get('page', 1))
    pageSize = 10
    startIndex = (pageNumber - 1) * pageSize
    endIndex = pageNumber + pageSize

    produtosLista = list(produtos[startIndex:endIndex])

    totalPages = (len(produtos) + pageSize -1 ) // pageSize

    return JsonResponse({'produtos': produtosLista, 'totalPages': totalPages, 'currentPage': pageNumber})

@csrf_exempt
@require_http_methods(['DELETE'])
def produto_detete(request, id):
    print('Rota acessada')
    try:
        print(Produto.objects.all())
        produto = Produto.objects.get(id=id)
        print(produto)
        produto.delete()
        return JsonResponse({'message': 'Produto deletado com sucesso!'})
    except Produto.DoesNotExist:
        return JsonResponse({'message': 'Produto não encontrado!'}, status=404)