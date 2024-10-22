from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_bot, name = 'home-bot'),
    path('config', views.config_bot, name = 'config_bot')
]