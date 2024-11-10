from uuid import uuid4
from django.db import models
from produto.models import Produto 


from django.db import models

class Pedido(models.Model):
    nome_produto = models.CharField(max_length=100, default='Nome Padrão')
    quantidade = models.IntegerField()
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Pendente")

    def __str__(self):
        return f"{self.nome_produto} - {self.quantidade}"
