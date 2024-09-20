from django.shortcuts import render

from django.http import HttpResponse


def ver_produtos(request):
    
    return render(request, 'ver_produtos.html')