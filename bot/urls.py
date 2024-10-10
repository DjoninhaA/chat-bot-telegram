from django.urls import path
from . import views

urlpatterns = [
    path('config', views.config_bot, name = 'config_bot'),
]