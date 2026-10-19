from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Cliente, ItemVenda, Produto, Venda


class VendaItemTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Bebidas")
        self.produto = Produto.objects.create(
            categoria=self.categoria,
            nome="Café",
            sku="CAF-1",
            preco=Decimal("12.50"),
            estoque=10,
        )
        self.cliente = Cliente.objects.create(nome="Cliente Teste")
        self.venda = Venda.objects.create(cliente=self.cliente)

    def test_adicionar_item_baixa_estoque_e_soma_total(self):
        ItemVenda.objects.create(venda=self.venda, produto=self.produto, quantidade=2)

        self.produto.refresh_from_db()
        self.venda.refresh_from_db()

        self.assertEqual(self.produto.estoque, 8)
        self.assertEqual(self.venda.total, Decimal("25.00"))

    def test_nao_permite_item_com_estoque_insuficiente(self):
        item = ItemVenda(venda=self.venda, produto=self.produto, quantidade=99)
        with self.assertRaises(ValidationError):
            item.full_clean()


class HtmxViewTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Eletrônicos")

    def test_formulario_htmx_retorna_partial(self):
        response = self.client.get(
            reverse("erp:categoria_create"),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "modal-title")
        self.assertNotContains(response, "<html")

    def test_submit_htmx_retorna_redirect_header(self):
        response = self.client.post(
            reverse("erp:categoria_create"),
            {"nome": "Limpeza", "descricao": "Produtos de limpeza"},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.headers.get("HX-Redirect"), reverse("erp:categoria_list"))
