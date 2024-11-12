from django.db import models
from produto.models import Produto

ORDER_STATUS = ((0, 'AGUARDANDO'), (1, 'PREPARANDO'), (2, 'PRONTO'))

class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.SmallIntegerField(choices=ORDER_STATUS)
    data = models.DateTimeField(auto_now=True)
    valor = models.FloatField(null=False)

    produto = models.ManyToManyField(Produto)
    cliente = models.CharField(max_length=255, default=None)