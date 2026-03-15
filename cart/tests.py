from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.urls import reverse
from catalog.models import Category, Product
from .cart import Cart


class CartModelTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        category = Category.objects.create(name="Торти", slug="torty")
        self.product = Product.objects.create(
            category=category,
            name="Торт тестовий",
            slug="test-tort",
            description="Опис",
            price="100.00",
            is_available=True,
        )

    def _get_request(self):
        request = self.factory.get("/")
        request.session = self.client.session
        return request

    def test_add_and_total(self):
        cart = Cart(self._get_request())
        cart.add(self.product, quantity=2)
        self.assertEqual(len(cart), 2)
        self.assertEqual(cart.get_total(), Decimal("200.00"))

    def test_remove(self):
        cart = Cart(self._get_request())
        cart.add(self.product, quantity=1)
        cart.remove(self.product)
        self.assertEqual(len(cart), 0)


class CartViewsTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Торти", slug="torty")
        self.product = Product.objects.create(
            category=category,
            name="Торт тестовий",
            slug="test-tort",
            description="Опис",
            price="150.00",
            is_available=True,
        )

    def test_cart_detail_page_renders(self):
        response = self.client.get(reverse("cart:detail"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart.html")

    def test_cart_add_endpoint(self):
        url = reverse("cart:add", kwargs={"product_id": self.product.id})
        response = self.client.post(url, {"quantity": 1})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 1)

    def test_cart_update_endpoint(self):
        add_url = reverse("cart:add", kwargs={"product_id": self.product.id})
        self.client.post(add_url, {"quantity": 1})
        update_url = reverse("cart:update", kwargs={"product_id": self.product.id})
        response = self.client.post(update_url, {"quantity": 3})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 3)

    def test_cart_remove_endpoint(self):
        add_url = reverse("cart:add", kwargs={"product_id": self.product.id})
        self.client.post(add_url, {"quantity": 1})
        remove_url = reverse("cart:remove", kwargs={"product_id": self.product.id})
        response = self.client.post(remove_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 0)
