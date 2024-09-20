from django.urls import path
from . import views

urlpatterns = [
    path('ver/', views.ver_produtos, name = 'ver_produtos'),
]
