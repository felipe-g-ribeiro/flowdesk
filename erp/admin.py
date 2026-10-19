from django.contrib import admin

from .models import Categoria, Cliente, ItemVenda, Produto, Venda


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "sku", "categoria", "preco", "estoque", "ativo")
    list_filter = ("categoria", "ativo")
    search_fields = ("nome", "sku")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "telefone")
    search_fields = ("nome", "email", "telefone")


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 0


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "criada_em", "total")
    search_fields = ("cliente__nome",)
    inlines = [ItemVendaInline]
