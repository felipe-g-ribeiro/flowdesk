from django import forms

from .models import Categoria, Cliente, ItemVenda, Produto, Venda


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome", "descricao"]


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["categoria", "nome", "sku", "preco", "estoque", "ativo"]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "email", "telefone"]


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ["cliente", "observacoes"]


class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ["produto", "quantidade", "preco_unitario"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["produto"].queryset = Produto.objects.filter(ativo=True).order_by("nome")
