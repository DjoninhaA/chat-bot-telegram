from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

import json

from produto.models import Produto, Categoria

@login_required
def get_products(request):
    
    return render(request, 'produtos.html', {'active_page': 'Produtos'})

@login_required
def produto_detail(request, id=None):
    categorias = Categoria.objects.all().values()
    if id:
        produto = Produto.objects.get(id=id)
    else: 
        produto = None
    return render(request, 'produtoDetalhes.html', {'active_page': 'Produtos', 'produto': produto, 'categorias': categorias})

@login_required
def produtos_data(request):
    produtos = Produto.objects.all().values(
        'id', 'nome', 'descricao', 'preco', 'categoria__nome', 'imagem'
    )

    produtos_lista = []
    for produto in produtos:
        produto['imagem'] = request.build_absolute_uri(settings.MEDIA_URL + produto['imagem'])
        produtos_lista.append(produto)

    page_number = int(request.GET.get('page', 1))
    page_size = 10
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size

    total_pages = (len(produtos_lista) + page_size - 1) // page_size
    return JsonResponse({'produtos': produtos_lista[start_index:end_index], 'totalPages': total_pages, 'currentPage': page_number})

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def produto_create(request):
    try:
        imagem = request.FILES.get('imagem')
        print(imagem)
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        categoria_id = request.POST.get('categoria')
        subcategoria = request.POST.get('subcategoria')
        tempoDePreparo = request.POST.get('tempoDePreparo')

        produto = Produto.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            categoria_id=categoria_id,
            subcategoria=subcategoria,
            tempoDePreparo=tempoDePreparo,
            imagem=imagem
        )
        return JsonResponse({'message': 'Produto criado com sucesso!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(['POST'])
def categoria_create(request):
    try:
        data = json.loads(request.body)
        categoria = Categoria.objects.create(
            nome=data['nome'],
        )

        return JsonResponse({'message': 'Categoria criada com sucesso!', 'success':'true', 'categoriaNome': categoria.nome, 'categoriaId': categoria.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(['DELETE'])
def produto_detete(request, id):
    try:
        produto = Produto.objects.get(id=id)
        produto.delete()
        return JsonResponse({'message': 'Produto deletado com sucesso!'})
    except Produto.DoesNotExist:
        return JsonResponse({'message': 'Produto não encontrado!'}, status=404)

@login_required   
@csrf_exempt
@require_http_methods(['PUT'])
def produto_edit(request, id):
    try:
        produto = Produto.objects.get(id=id)
        data = json.loads(request.body)
        produto.nome = data['nome']
        produto.descricao = data['descricao']
        produto.preco = data['preco']
        produto.categoria_id = data['categoria']
        produto.subcategoria = data['subcategoria']
        produto.tempoDePreparo = data['tempoDePreparo']
        produto.save()
        return JsonResponse({'message': 'Produto editado com sucesso!'})
    except Produto.DoesNotExist:
        return JsonResponse({'message': 'Produto não encontrado!'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def produto_search(request):
    query = request.GET.get('query', '')
    produtos = Produto.objects.filter(nome__icontains=query).values(
        'nome', 'descricao', 'preco', 'tempoDePreparo', 'subcategoria', 'categoria__nome'
    )

    pageNumber = int(request.GET.get('page', 1))
    pageSize = 10
    startIndex = (pageNumber - 1) * pageSize
    endIndex = startIndex + pageSize

    produtosLista = list(produtos[startIndex:endIndex])

    totalPages = (len(produtos) + pageSize -1 ) // pageSize

    return JsonResponse({'Produtos': produtosLista, 'totalPages': totalPages, 'currentPage': pageNumber})