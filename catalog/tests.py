from django.test import TestCase
from django.urls import reverse
from .models import Category, Product


class CategoryModelTests(TestCase):
    def test_get_absolute_url_uses_slug(self):
        category = Category.objects.create(name="Торти", slug="torty")
        self.assertEqual(
            category.get_absolute_url(),
            reverse("catalog:category", kwargs={"slug": "torty"}),
        )


class ProductModelTests(TestCase):
    def test_get_absolute_url_uses_slug(self):
        category = Category.objects.create(name="Торти", slug="torty")
        product = Product.objects.create(
            category=category,
            name="Ягідний торт",
            slug="yagidnyi-tort",
            description="Смачний торт",
            price="350.00",
            is_available=True,
        )
        self.assertEqual(
            product.get_absolute_url(),
            reverse("catalog:product", kwargs={"slug": "yagidnyi-tort"}),
        )


class CatalogViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Торти", slug="torty")
        self.product = Product.objects.create(
            category=self.category,
            name="Шоколадний торт",
            slug="shokoladnyi-tort",
            description="Опис",
            price="300.00",
            is_available=True,
        )

    def test_product_list_view(self):
        response = self.client.get(reverse("catalog:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/product_list.html")
        self.assertIn("page_obj", response.context)

    def test_category_detail_view(self):
        url = reverse("catalog:category", kwargs={"slug": self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/category_detail.html")

    def test_product_detail_view_updates_recently_viewed(self):
        url = reverse("catalog:product", kwargs={"slug": self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/product_detail.html")
        self.assertIn("recently_viewed", self.client.session)
        self.assertIn(self.product.id, self.client.session["recently_viewed"])

    def test_search_autocomplete_min_length(self):
        url = reverse("catalog:search_autocomplete")
        response = self.client.get(url, {"q": "a"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"], [])

    def test_search_autocomplete_returns_results(self):
        url = reverse("catalog:search_autocomplete")
        response = self.client.get(url, {"q": "Шоколад"})
        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        self.assertTrue(any(item["slug"] == self.product.slug for item in results))
