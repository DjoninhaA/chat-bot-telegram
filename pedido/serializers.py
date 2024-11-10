from rest_framework import serializers
from .models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pedido
        fields = ['id', 'nome_produto', 'quantidade', 'observacoes', 'status']