from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class ProductAndCategoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="products-user",
            password="test-password",
        )
        cls.category = Category.objects.create(name="Eletrônicos")
        cls.product = Product.objects.create(
            name="Notebook",
            category=cls.category,
            price="2500.00",
            stock=5,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_product_creation_and_category_relationship(self):
        product = Product.objects.create(
            name="Mouse",
            category=self.category,
            price="80.00",
            stock=10,
        )

        self.assertEqual(product.category, self.category)
        self.assertIn(product, self.category.products.all())
        self.assertEqual(product.stock, 10)

    def test_product_list_displays_products(self):
        response = self.client.get(reverse("product_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_creation_view_creates_product(self):
        response = self.client.post(
            reverse("product_create"),
            {
                "name": "Teclado",
                "category": self.category.pk,
                "price": "120.00",
                "stock": 8,
            },
        )

        self.assertRedirects(response, reverse("product_list"))
        self.assertTrue(Product.objects.filter(name="Teclado").exists())

    def test_category_creation_view_creates_category(self):
        response = self.client.post(
            reverse("category_create"),
            {"name": "Acessórios"},
        )

        self.assertRedirects(response, reverse("category_list"))
        self.assertTrue(
            Category.objects.filter(name="Acessórios").exists()
        )

    def test_category_update_view_updates_category(self):
        response = self.client.post(
            reverse("category_update", args=[self.category.pk]),
            {"name": "Informática"},
        )

        self.assertRedirects(response, reverse("category_list"))
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Informática")

    def test_product_update_and_delete_views(self):
        update_response = self.client.post(
            reverse("product_update", args=[self.product.pk]),
            {
                "name": "Notebook atualizado",
                "category": self.category.pk,
                "price": "2700.00",
                "stock": 7,
            },
        )

        self.assertRedirects(update_response, reverse("product_list"))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Notebook atualizado")
        self.assertEqual(self.product.stock, 7)

        delete_response = self.client.get(
            reverse("product_delete", args=[self.product.pk])
        )

        self.assertRedirects(delete_response, reverse("product_list"))
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_category_pages_require_login(self):
        self.client.logout()

        response = self.client.get(reverse("category_list"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('category_list')}",
        )
