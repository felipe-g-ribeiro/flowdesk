from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from products.models import Category, Product
from sales.models import Sale


class DashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="dashboard-user",
            password="test-password",
        )
        category = Category.objects.create(name="Dashboard")
        product = Product.objects.create(
            name="Produto do dashboard",
            category=category,
            price="25.00",
            stock=4,
        )
        customer = Customer.objects.create(name="Cliente do dashboard")
        Sale.objects.create(
            customer=customer,
            product=product,
            quantity=1,
            total="25.00",
        )

    def test_anonymous_user_is_redirected_from_dashboard(self):
        response = self.client.get(reverse("dashboard"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
        )

    def test_authenticated_user_can_access_dashboard(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/dashboard.html")
        self.assertEqual(response.context["total_products"], 1)
        self.assertEqual(response.context["total_categories"], 1)
        self.assertEqual(response.context["total_customers"], 1)
        self.assertEqual(response.context["total_sales"], 1)


class LoginTests(TestCase):
    def setUp(self):
        self.username = "login-user"
        self.password = "test-password"
        get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )

    def test_user_can_log_in(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.username,
                "password": self.password,
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_login_does_not_authenticate_user(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.username,
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_redirects_to_login(self):
        self.client.login(
            username=self.username,
            password=self.password,
        )

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
