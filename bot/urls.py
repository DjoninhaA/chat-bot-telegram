from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-bot'),  # Rota para o bot ou página inicial
]
