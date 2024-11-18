from django.urls import path
from pedido import views
from .views import pedido_create

urlpatterns = [
    path('ver/', views.listar_pedidos, name = 'pedidos'),
    path('criar/', views.pedido_create, name=  'criar'),
    path('deletar/<int:pedido_id>/', views.deletar_pedido, name = 'deletar')
]