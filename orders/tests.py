from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import Category, Product
from .models import Order, OrderItem

User = get_user_model()


class OrderModelTests(TestCase):
    def test_order_item_total(self):
        category = Category.objects.create(name="Торти", slug="torty")
        product = Product.objects.create(
            category=category,
            name="Торт",
            slug="tort",
            description="Опис",
            price="200.00",
            is_available=True,
        )
        order = Order.objects.create(
            first_name="Імʼя",
            last_name="Прізвище",
            email="test@example.com",
            phone="+380000000000",
            address="Адреса",
            total="400.00",
        )
        item = OrderItem.objects.create(
            order=order, product=product, name="Торт", price="200.00", quantity=2
        )
        self.assertEqual(item.get_total(), Decimal("400.00"))


class OrderViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )

    def test_order_history_requires_authentication(self):
        url = reverse("orders:history")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response["Location"])

    def test_order_history_for_authenticated_user(self):
        self.client.login(email="user@example.com", password="password123")
        url = reverse("orders:history")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order_history.html")
