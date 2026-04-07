from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:pk>/", views.category_detail, name="category_detail"),
    path("register/", views.register, name="register"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:book_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("rate/<int:book_id>/", views.rate_book, name="rate_book"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/add/<int:book_id>/", views.wishlist_add, name="wishlist_add"),
    path("wishlist/remove/<int:book_id>/", views.wishlist_remove, name="wishlist_remove"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("api/search/", views.api_search, name="api_search"),
]
