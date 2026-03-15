from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password123"
        )

    def test_register_page_renders(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_login_page_renders(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_profile_requires_login(self):
        url = reverse("accounts:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response["Location"])

    def test_profile_page_for_authenticated_user(self):
        self.client.login(email="user@example.com", password="password123")
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
