from django.urls import include, path

from rest_framework import routers
from pedido import views as pedido_views

router = routers.DefaultRouter()
router.register(r'pedido', pedido_views.PedidoViewSet  ,basename='pedido')


urlpatterns =  [
    path('', include(router.urls))
]