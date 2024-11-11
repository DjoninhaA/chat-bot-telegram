from django.db import models
from .models import Produto

ORDER_STATUS = ((0, 'AGUARDANDO'), (1, 'PREPARANDO'), (2, 'PRONTO'))

class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.SmallIntegerField(choices=ORDER_STATUS)
    data = models.DateTimeField(auto_now=True)
    valor = models.FloatField(null=False)

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cliente = models.CharField(default=None)