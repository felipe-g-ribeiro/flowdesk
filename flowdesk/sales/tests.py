from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from products.models import Category, Product

from .models import Sale


class SaleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="sales-user",
            password="test-password",
        )
        cls.customer = Customer.objects.create(
            name="Daniel Costa",
            email="daniel@example.com",
        )
        cls.category = Category.objects.create(name="Casa")
        cls.product = Product.objects.create(
            name="Cadeira",
            category=cls.category,
            price="150.00",
            stock=10,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_sale_creation_preserves_relationships(self):
        sale = Sale.objects.create(
            customer=self.customer,
            product=self.product,
            quantity=2,
            total=Decimal("300.00"),
        )

        self.assertEqual(sale.customer, self.customer)
        self.assertEqual(sale.product, self.product)
        self.assertEqual(sale.total, Decimal("300.00"))

    def test_sale_creation_calculates_total_and_updates_stock(self):
        response = self.client.post(
            reverse("sale_create"),
            {
                "customer": self.customer.pk,
                "product": self.product.pk,
                "quantity": 3,
            },
        )

        self.assertRedirects(response, reverse("sale_list"))
        sale = Sale.objects.get()
        self.assertEqual(sale.total, Decimal("450.00"))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)

    def test_sale_creation_rejects_insufficient_stock(self):
        response = self.client.post(
            reverse("sale_create"),
            {
                "customer": self.customer.pk,
                "product": self.product.pk,
                "quantity": 11,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Estoque insuficiente.")
        self.assertFalse(Sale.objects.exists())
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)

    def test_sale_pages_require_login(self):
        self.client.logout()

        response = self.client.get(reverse("sale_list"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('sale_list')}",
        )
