from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Pedido
from .serializers import PedidoSerializer

# Create your views here.
def get_order(request):
    
    return render(request, 'pedidos.html')


class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    