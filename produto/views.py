from django.shortcuts import render

from django.http import HttpResponse


def get_products(request):
    
    return render(request, 'produtos.html', {'active_page': 'Produtos'})