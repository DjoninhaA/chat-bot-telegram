from uuid import uuid4
from django.db import models
from produto.models import Produto 

class Pedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    #cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    

    def __str__(self):
        return f'ID:{self.id} | Produto: {self.produto.nome} | Quantidade {self.quantidade}'