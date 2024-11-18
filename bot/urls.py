from django.urls import path
from .views import telegram_webhook, catalog_view, products_api

urlpatterns = [
    path('telegram-webhook/', telegram_webhook, name='telegram_webhook'),
    path('produto/data/', catalog_view, name='catalog'),
    path('api/products/', products_api, name='products_api'),
]