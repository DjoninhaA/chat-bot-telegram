from django.urls import path
from . import views

urlpatterns = [
    path('ver/', views.get_order, name = 'pedidos.html'),
]
