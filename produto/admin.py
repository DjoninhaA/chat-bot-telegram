from django.contrib import admin

from produto.models import Categoria, Produto

# Register your models here.
admin.site.register(Produto)
admin.site.register(Categoria)