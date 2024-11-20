from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_products),
    path('adicionar/', views.produto_detail),
    path('detalhes/<int:id>', views.produto_detail),
    path('data/', views.produtos_data, name='produtos_data'),
    path('criar/', views.produto_create),
    path('deletar/<int:id>', views.produto_detete),
    path('editar/<int:id>', views.produto_edit),
    path('search/', views.produto_search),
    path('categoria', views.get_categorias),
    path('categoria/criar/', views.categoria_create),
    path('categoria/deletar/<int:id>', views.categoria_delete),
    path('categoria/editar/<int:id>', views.categoria_edit),
    path('categoria/data/', views.categoria_data),
]
