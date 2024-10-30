from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_products, name = 'ver_produtos'),
    path('data/', views.produtos_data, name = 'produtos_data'),
]
