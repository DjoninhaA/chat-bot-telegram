from django.contrib import admin
from django.urls import path, include
from produto import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('produto/', include('produto.urls')),
    path('pedido/', include('pedido.urls')),
    path('', include('bot.urls')),
    path('accounts/', include ('django.contrib.auth.urls')),
    path('usuario/', include ('usuario.urls'))
]
