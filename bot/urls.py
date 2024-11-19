from django.urls import path
from .views import catalog_view, cart_view, products_api, cart_api, add_to_cart_api, finalize_order_api, telegram_webhook

urlpatterns = [
    path('telegram-webhook/', telegram_webhook, name='telegram_webhook'),
    path('catalog/', catalog_view, name='catalog'),
    path('cart/', cart_view, name='cart'),
    path('api/products/', products_api, name='products_api'),
    path('api/cart/', cart_api, name='cart_api'),
    path('api/add_to_cart/', add_to_cart_api, name='add_to_cart_api'),
    path('api/finalize_order/', finalize_order_api, name='finalize_order_api'),
]