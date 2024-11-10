from django.contrib import admin
from django.urls import include, path

from produto import views

urlpatterns = [
    path('', views.get_products, name = 'ver_produtos'),
    path('data/', views.produtos_data, name = 'produtos_data'),
    path('delete/<int:id>', views.produto_detete, name = 'produto_delete'),
]
