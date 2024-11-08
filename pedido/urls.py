<<<<<<< Updated upstream
from django.urls import path, include

from . import views

urlpatterns = [
    
]
=======
# pedido/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),  # Página de listagem de pedidos
    path('novo/', views.novo_pedido, name='novo_pedido'),  # Página para criar um novo pedido
]
>>>>>>> Stashed changes
