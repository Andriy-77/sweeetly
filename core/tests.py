from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from catalog.models import Category, Product


class HomeViewTests(TestCase):
    def setUp(self):
        cache.clear()
        self.category = Category.objects.create(name="Торти", slug="torty")
        self.product = Product.objects.create(
            category=self.category,
            name="Ягідний торт",
            slug="yagidnyi-tort",
            description="Смачний торт",
            price="350.00",
            is_available=True,
            is_popular=True,
        )

    def test_home_page_renders(self):
        url = reverse("core:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertIn("popular", response.context)
        self.assertIn("categories", response.context)

    def test_home_uses_cache_for_popular_products(self):
        url = reverse("core:home")
        self.client.get(url)
        cached_popular = cache.get("popular_products")
        self.assertIsNotNone(cached_popular)
        self.assertTrue(any(p.id == self.product.id for p in cached_popular))


class StaticPagesTests(TestCase):
    def test_about_page_renders(self):
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/about.html")

    def test_delivery_page_renders(self):
        response = self.client.get(reverse("core:delivery"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/delivery.html")
