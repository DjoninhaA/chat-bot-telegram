from uuid import uuid4
from django.db import models
from produto.models import Produto 

<<<<<<< Updated upstream
class Pedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    #cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    

    def __str__(self):
        return f'ID:{self.id} | Produto: {self.produto.nome} | Quantidade {self.quantidade}'
=======
# Create your models here.
# pedido/models.py
from django.db import models

class Pedido(models.Model):
    nome_produto = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Pendente")

    def __str__(self):
        return f"{self.nome_produto} - {self.quantidade}"
>>>>>>> Stashed changes
