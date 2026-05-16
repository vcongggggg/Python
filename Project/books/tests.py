from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import Permission

from books.models import AdminAuditLog, Book, Category, Coupon, Order, OrderItem

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
        self.assertEqual(response.status_code, 302)

        view_user = Permission.objects.get(codename="view_user")
        self.staff_user.user_permissions.add(view_user)
        response = self.client.get(reverse("dashboard_users"))
        self.assertEqual(response.status_code, 200)

    def test_audit_log_requires_permission(self) -> None:
        response = self.client.get(reverse("dashboard_audit_logs"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("dashboard_audit_logs"))
        self.assertEqual(response.status_code, 302)

        view_log = Permission.objects.get(codename="view_adminauditlog")
        self.staff_user.user_permissions.add(view_log)
        response = self.client.get(reverse("dashboard_audit_logs"))
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

        change_user = Permission.objects.get(codename="change_user")
        self.staff_user.user_permissions.add(change_user)
        self.client.force_login(self.staff_user)
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

        change_user = Permission.objects.get(codename="change_user")
        self.staff_user.user_permissions.add(change_user)
        self.client.force_login(self.staff_user)
        response = self.client.post(
            reverse("dashboard_user_toggle_active", args=[target.pk])
        )
        self.assertEqual(response.status_code, 302)
        target.refresh_from_db()
        self.assertFalse(target.is_active)


class AdminCrudTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.category = Category.objects.create(name="IT")
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

    def test_admin_books_list_requires_staff(self) -> None:
        response = self.client.get(reverse("dashboard_books"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("dashboard_books"))
        self.assertEqual(response.status_code, 302)

        view_book = Permission.objects.get(codename="view_book")
        self.staff_user.user_permissions.add(view_book)
        response = self.client.get(reverse("dashboard_books"))
        self.assertEqual(response.status_code, 200)

    def test_admin_book_create_requires_superuser(self) -> None:
        payload = {
            "title": "New Book",
            "author": "Author",
            "description": "Desc",
            "price": "120000",
            "category": self.category.pk,
            "published_year": "2024",
            "num_pages": "100",
            "cover_image": "",
            "stock": "5",
            "is_digital": "on",
            "content_text": "Sample",
        }

        self.client.force_login(self.staff_user)
        response = self.client.post(reverse("dashboard_book_create"), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.filter(title="New Book").count(), 0)

        add_book = Permission.objects.get(codename="add_book")
        self.staff_user.user_permissions.add(add_book)
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse("dashboard_book_create"), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.filter(title="New Book").count(), 1)

    def test_admin_book_edit_requires_superuser(self) -> None:
        book = Book.objects.create(
            title="Old",
            author="A",
            price=100,
            category=self.category,
            stock=5,
        )
        payload = {
            "title": "Updated",
            "author": "A",
            "description": "",
            "price": "100",
            "category": self.category.pk,
            "published_year": "",
            "num_pages": "",
            "cover_image": "",
            "stock": "5",
            "is_digital": "",
            "content_text": "",
        }

        self.client.force_login(self.staff_user)
        response = self.client.post(reverse("dashboard_book_edit", args=[book.pk]), data=payload)
        self.assertEqual(response.status_code, 302)
        book.refresh_from_db()
        self.assertEqual(book.title, "Old")

        change_book = Permission.objects.get(codename="change_book")
        self.staff_user.user_permissions.add(change_book)
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse("dashboard_book_edit", args=[book.pk]), data=payload)
        self.assertEqual(response.status_code, 302)
        book.refresh_from_db()
        self.assertEqual(book.title, "Updated")

    def test_admin_book_delete_requires_superuser(self) -> None:
        book = Book.objects.create(
            title="Delete Me",
            author="A",
            price=100,
            category=self.category,
            stock=5,
        )

        self.client.force_login(self.staff_user)
        response = self.client.post(reverse("dashboard_book_delete", args=[book.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(pk=book.pk).exists())

        delete_book = Permission.objects.get(codename="delete_book")
        self.staff_user.user_permissions.add(delete_book)
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse("dashboard_book_delete", args=[book.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(pk=book.pk).exists())

    def test_admin_coupons_list_requires_staff(self) -> None:
        response = self.client.get(reverse("dashboard_coupons"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("dashboard_coupons"))
        self.assertEqual(response.status_code, 302)

        view_coupon = Permission.objects.get(codename="view_coupon")
        self.staff_user.user_permissions.add(view_coupon)
        response = self.client.get(reverse("dashboard_coupons"))
        self.assertEqual(response.status_code, 200)

    def test_admin_coupon_create_edit_delete_requires_superuser(self) -> None:
        now = timezone.now()
        payload = {
            "code": "SAVE10",
            "discount_type": "percent",
            "discount_value": "10",
            "min_order_amount": "0",
            "max_uses": "100",
            "used_count": "0",
            "active": "on",
            "valid_from": now.strftime("%Y-%m-%d %H:%M:%S"),
            "valid_to": (now + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.client.force_login(self.staff_user)
        response = self.client.post(reverse("dashboard_coupon_create"), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Coupon.objects.filter(code="SAVE10").exists())

        add_coupon = Permission.objects.get(codename="add_coupon")
        change_coupon = Permission.objects.get(codename="change_coupon")
        delete_coupon = Permission.objects.get(codename="delete_coupon")
        self.staff_user.user_permissions.add(add_coupon, change_coupon, delete_coupon)
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse("dashboard_coupon_create"), data=payload)
        self.assertEqual(response.status_code, 302)
        coupon = Coupon.objects.get(code="SAVE10")

        edit_payload = payload | {"discount_value": "15"}
        response = self.client.post(
            reverse("dashboard_coupon_edit", args=[coupon.pk]),
            data=edit_payload,
        )
        self.assertEqual(response.status_code, 302)
        coupon.refresh_from_db()
        self.assertEqual(float(coupon.discount_value), 15.0)

        self.client.force_login(self.staff_user)
        response = self.client.post(reverse("dashboard_coupon_delete", args=[coupon.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Coupon.objects.filter(pk=coupon.pk).exists())

    def test_admin_orders_list_requires_staff(self) -> None:
        order = Order.objects.create(user=self.regular_user)
        OrderItem.objects.create(order=order, book=Book.objects.create(
            title="Order Book",
            author="A",
            price=100,
            category=self.category,
            stock=5,
        ), quantity=1, price=100)

        response = self.client.get(reverse("dashboard_orders"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("dashboard_orders"))
        self.assertEqual(response.status_code, 302)

        view_order = Permission.objects.get(codename="view_order")
        self.staff_user.user_permissions.add(view_order)
        response = self.client.get(reverse("dashboard_orders"))
        self.assertEqual(response.status_code, 200)

    def test_export_requires_permission(self) -> None:
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("export_orders_csv"))
        self.assertEqual(response.status_code, 302)

        view_order = Permission.objects.get(codename="view_order")
        self.staff_user.user_permissions.add(view_order)
        response = self.client.get(reverse("export_orders_csv"))
        self.assertEqual(response.status_code, 200)

    def test_audit_log_created_on_actions(self) -> None:
        add_book = Permission.objects.get(codename="add_book")
        self.staff_user.user_permissions.add(add_book)
        self.client.force_login(self.staff_user)
        payload = {
            "title": "Audit Book",
            "author": "Author",
            "description": "Desc",
            "price": "120000",
            "category": self.category.pk,
            "published_year": "2024",
            "num_pages": "100",
            "cover_image": "",
            "stock": "5",
            "is_digital": "on",
            "content_text": "Sample",
        }
        response = self.client.post(reverse("dashboard_book_create"), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(AdminAuditLog.objects.filter(action="book_create").exists())
