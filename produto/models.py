# pedido/models.py
from django.db import models

<<<<<<< Updated upstream
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tempoDePreparo = models.IntegerField()
    subcategoria = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
=======
class Pedido(models.Model):
    nome_produto = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome_produto
>>>>>>> Stashed changes
