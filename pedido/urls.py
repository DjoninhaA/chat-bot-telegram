from django.urls import path
from pedido import views
from .views import pedido_create

urlpatterns = [
    path('ver/', views.pedido_create, name = 'pedidos.html'),
]
