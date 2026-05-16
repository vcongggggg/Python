from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from books.models import Book, Category

User = get_user_model()

class BasicFlowTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.category = Category.objects.create(name="IT")
        self.book = Book.objects.create(
            title="Django Pro",
            author="Copilot",
            price=100.0,
            category=self.category,
            stock=10
        )
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_home_page(self) -> None:
        """Kiểm tra trang chủ có hoạt động không."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_book_detail(self) -> None:
        """Kiểm tra xem trang chi tiết sách có hiển thị đúng không."""
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Pro")


class AdminPermissionsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="password123",
            is_staff=True,
        )
        self.super_user = User.objects.create_superuser(
            username="superuser",
            password="password123",
            email="superuser@example.com",
        )
        self.regular_user = User.objects.create_user(
            username="regular",
            password="password123",
        )

    def test_dashboard_requires_staff(self) -> None:
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_user_management_requires_staff(self) -> None:
        response = self.client.get(reverse("dashboard_users"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("dashboard_users"))
        self.assertEqual(response.status_code, 200)

    def test_toggle_staff_requires_superuser(self) -> None:
        target = self.regular_user
        self.client.force_login(self.staff_user)
        response = self.client.post(
            reverse("dashboard_user_toggle_staff", args=[target.pk])
        )
        self.assertEqual(response.status_code, 302)
        target.refresh_from_db()
        self.assertFalse(target.is_staff)

        self.client.force_login(self.super_user)
        response = self.client.post(
            reverse("dashboard_user_toggle_staff", args=[target.pk])
        )
        self.assertEqual(response.status_code, 302)
        target.refresh_from_db()
        self.assertTrue(target.is_staff)

    def test_toggle_active_requires_superuser(self) -> None:
        target = self.regular_user
        self.client.force_login(self.staff_user)
        response = self.client.post(
            reverse("dashboard_user_toggle_active", args=[target.pk])
        )
        self.assertEqual(response.status_code, 302)
        target.refresh_from_db()
        self.assertTrue(target.is_active)

        self.client.force_login(self.super_user)
        response = self.client.post(
            reverse("dashboard_user_toggle_active", args=[target.pk])
        )
        self.assertEqual(response.status_code, 302)
        target.refresh_from_db()
        self.assertFalse(target.is_active)
