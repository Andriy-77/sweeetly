from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from cart.cart import Cart
from catalog.models import Category, Product
from orders.models import Order

User = get_user_model()


class PaymentViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )
        category = Category.objects.create(name="Торти", slug="torty")
        product = Product.objects.create(
            category=category,
            name="Торт",
            slug="tort",
            description="Опис",
            price="200.00",
            is_available=True,
        )
        self.order = Order.objects.create(
            user=self.user,
            first_name="Імʼя",
            last_name="Прізвище",
            email="test@example.com",
            phone="+380000000000",
            address="Адреса",
            total="200.00",
        )
        cart = Cart(self.client.request().wsgi_request)
        cart.add(product, quantity=1)

    def test_success_view_clears_cart_and_renders(self):
        url = reverse("payments:success", kwargs={"order_id": self.order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payments/success.html")
