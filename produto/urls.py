from django.contrib import admin
from django.urls import include, path

urlpatterns = [
<<<<<<< Updated upstream
    path('', views.get_products, name = 'ver_produtos'),
    path('data/', views.produtos_data, name = 'produtos_data'),
    path('delete/<int:id>', views.produto_detete, name = 'produto_delete'),
=======
    path('admin/', admin.site.urls),
    path('produto/', include('app_name.urls')),  # ou a URL que você usa para o produto
    path('pedido/', include('app_name.urls')),  # Aqui, inclui a URL do pedido
>>>>>>> Stashed changes
]
