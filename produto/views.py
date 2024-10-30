from django.shortcuts import render

from django.http import JsonResponse

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