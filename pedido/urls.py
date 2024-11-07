from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet

router = DefaultRouter()
router.register(r'ver', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),
]