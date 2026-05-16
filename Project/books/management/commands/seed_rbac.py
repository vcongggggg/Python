from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


GROUP_PERMS = {
    "Staff": [
        "auth.view_user",
        "books.view_book",
        "books.view_coupon",
        "books.view_order",
        "books.view_orderitem",
    ],
    "Manager": [
        "books.view_book",
        "books.add_book",
        "books.change_book",
        "books.delete_book",
    ],
    "Accountant": [
        "books.view_order",
        "books.view_orderitem",
        "books.view_coupon",
    ],
    "Support": [
        "books.view_order",
        "books.change_order",
    ],
    "Admin": [
        "auth.view_user",
        "auth.change_user",
        "books.view_book",
        "books.add_book",
        "books.change_book",
        "books.delete_book",
        "books.view_coupon",
        "books.add_coupon",
        "books.change_coupon",
        "books.delete_coupon",
        "books.view_order",
        "books.change_order",
        "books.view_orderitem",
        "books.view_adminauditlog",
    ],
}


class Command(BaseCommand):
    help = "Create default RBAC groups and assign permissions."

    def handle(self, *args, **options):
        for group_name, perms in GROUP_PERMS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            permissions = Permission.objects.filter(
                content_type__app_label__in={p.split(".")[0] for p in perms},
                codename__in=[p.split(".")[1] for p in perms],
            )
            group.permissions.set(permissions)
            status = "created" if created else "updated"
            self.stdout.write(self.style.SUCCESS(f"{status} group: {group_name}"))
