# pedido/views.py
from django.shortcuts import render
<<<<<<< Updated upstream
from rest_framework.viewsets import ModelViewSet
from .models import Pedido
from .serializers import PedidoSerializer

# Create your views here.

class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
=======
from .models import Pedido

# View para listar os pedidos
def lista_pedidos(request):
    pedidos = Pedido.objects.all()  # Aqui você pega todos os pedidos no banco de dados
    return render(request, 'pedido/pedidos.html', {'pedidos': pedidos})
>>>>>>> Stashed changes
