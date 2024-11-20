# accounts/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.get_user, name='usuarios'),
    path('data/', views.user_data, name='usuarios_data'),
]
