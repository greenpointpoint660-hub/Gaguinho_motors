from django.contrib import admin
from .models import Carrinho, Carro, Cliente, ItemCarrinho, ItemPedido, Pedido

admin.site.register(Carro)
admin.site.register(Cliente)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
