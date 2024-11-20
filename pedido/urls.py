from django.urls import path
from pedido import views
from .views import pedido_create

urlpatterns = [
    path('', views.getPedidos, name = 'pedidos'),
    path('data/', views.listar_pedidos, name= 'data'),
    path('criar/', views.pedido_create, name=  'criar'),
    path('deletar/<int:pedido_id>/', views.deletar_pedido, name = 'deletar'),
    path('alterarStatus/<int:pedido_id>/', views.alterar_status, name = 'alterarStatus'),
    path('search/', views.search_pedidos, name = 'search'),
]