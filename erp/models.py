from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import DecimalField, ExpressionWrapper, F, Sum


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nome


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="produtos")
    nome = models.CharField(max_length=120)
    sku = models.CharField(max_length=50, unique=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.sku})"


class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=25, blank=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="vendas")
    observacoes = models.TextField(blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criada_em"]

    def __str__(self):
        return f"Venda #{self.pk} - {self.cliente.nome}"

    @property
    def total(self):
        total = self.itens.aggregate(
            valor=Sum(
                ExpressionWrapper(
                    F("quantidade") * F("preco_unitario"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )
        )["valor"]
        return total or Decimal("0.00")


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="itens_venda")
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "item de venda"
        verbose_name_plural = "itens de venda"

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def clean(self):
        if self.quantidade <= 0:
            raise ValidationError({"quantidade": "A quantidade deve ser maior que zero."})

        estoque_disponivel = self.produto.estoque
        if self.pk:
            original = ItemVenda.objects.select_related("produto").get(pk=self.pk)
            if original.produto_id == self.produto_id:
                estoque_disponivel += original.quantidade

        if self.quantidade > estoque_disponivel:
            raise ValidationError({"quantidade": "Estoque insuficiente para o produto selecionado."})

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.preco_unitario = self.preco_unitario or self.produto.preco
        self.full_clean()

        original = None
        if self.pk:
            original = ItemVenda.objects.select_related("produto").get(pk=self.pk)

        super().save(*args, **kwargs)

        if original and original.produto_id != self.produto_id:
            original.produto.estoque += original.quantidade
            original.produto.save(update_fields=["estoque"])
            self.produto.estoque -= self.quantidade
            self.produto.save(update_fields=["estoque"])
            return

        delta = self.quantidade
        if original:
            delta -= original.quantidade

        if delta:
            self.produto.estoque -= delta
            self.produto.save(update_fields=["estoque"])

    @transaction.atomic
    def delete(self, *args, **kwargs):
        produto = self.produto
        quantidade = self.quantidade
        super().delete(*args, **kwargs)
        produto.estoque += quantidade
        produto.save(update_fields=["estoque"])
