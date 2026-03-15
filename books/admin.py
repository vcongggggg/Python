from django.contrib import admin

from .models import Book, Category, Order, OrderItem, Rating, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "book_count")
    search_fields = ("name",)

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = "Số sách"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ("book",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "item_count", "total_amount")
    list_filter = ("created_at",)
    search_fields = ("user__username",)
    inlines = (OrderItemInline,)

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Số mục"

    def total_amount(self, obj):
        total = sum((item.price * item.quantity) for item in obj.items.all())
        return f"{total:,.0f}₫"
    total_amount.short_description = "Tổng tiền"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "price", "published_year", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "author")
    list_editable = ("price",)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "added_at")
    list_filter = ("added_at",)
    raw_id_fields = ("user", "book")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "book", "quantity", "price", "subtotal")
    list_filter = ("order",)
    raw_id_fields = ("order", "book")

    def subtotal(self, obj):
        return obj.price * obj.quantity
    subtotal.short_description = "Thành tiền"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "score", "created_at")
    list_filter = ("score",)
    search_fields = ("user__username", "book__title")
