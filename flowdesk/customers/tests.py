from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Customer


class CustomerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="customers-user",
            password="test-password",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_customer_creation(self):
        customer = Customer.objects.create(
            name="Ana Souza",
            email="ana@example.com",
            phone="11999999999",
        )

        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(str(customer), "Ana Souza")
        self.assertEqual(customer.email, "ana@example.com")

    def test_customer_creation_view_creates_customer(self):
        response = self.client.post(
            reverse("customer_create"),
            {
                "name": "Bruno Lima",
                "email": "bruno@example.com",
                "phone": "11888888888",
            },
        )

        self.assertRedirects(response, reverse("customer_list"))
        self.assertTrue(
            Customer.objects.filter(name="Bruno Lima").exists()
        )

    def test_customer_update_and_delete_views(self):
        customer = Customer.objects.create(
            name="Carla Mendes",
            email="carla@example.com",
            phone="11777777777",
        )

        update_response = self.client.post(
            reverse("customer_update", args=[customer.pk]),
            {
                "name": "Carla Santos",
                "email": "carla.santos@example.com",
                "phone": "11666666666",
            },
        )

        self.assertRedirects(update_response, reverse("customer_list"))
        customer.refresh_from_db()
        self.assertEqual(customer.name, "Carla Santos")
        self.assertEqual(customer.email, "carla.santos@example.com")

        delete_response = self.client.get(
            reverse("customer_delete", args=[customer.pk])
        )

        self.assertRedirects(delete_response, reverse("customer_list"))
        self.assertFalse(Customer.objects.filter(pk=customer.pk).exists())

    def test_customer_pages_require_login(self):
        self.client.logout()

        response = self.client.get(reverse("customer_list"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('customer_list')}",
        )
