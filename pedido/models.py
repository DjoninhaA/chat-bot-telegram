from django.db import models
from produto.models import Produto

ORDER_STATUS = ((0, 'Aguardando'), (1, 'Preparando'), (2, 'Pronto'), (3, 'Entregue'), (4, 'Cancelado'))

class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.SmallIntegerField(choices=ORDER_STATUS)
    data = models.DateTimeField(auto_now=True)
    valor = models.FloatField(null=False)
    produto = models.ManyToManyField(Produto)
    cliente = models.CharField(max_length=255, default=None)
    endereco_entrega = models.CharField(max_length=255, default='')
    chat_id = models.CharField(max_length=255, default='')  # Novo campo
    username = models.CharField(max_length=255, default='', null=True)  # Novo campo

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"