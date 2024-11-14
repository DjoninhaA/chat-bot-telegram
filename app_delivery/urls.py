from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from produto import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('produto/', include('produto.urls')),
    path('pedido/', include('pedido.urls')),
    path('bot', include('bot.urls')),
     path('', lambda request: redirect('login')),
    path('usuario/', include ('usuario.urls'))
]
