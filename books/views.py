from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileEditForm, RatingForm, RegisterForm
from .models import Book, Category, Order, OrderItem, Rating, Wishlist

# ---------- Cart helpers (session: { "cart": { "book_id": quantity } }) ----------


def _get_cart(request):
    cart = request.session.get("cart")
    if not isinstance(cart, dict):
        cart = {}
    return cart


def _set_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True


def _cart_items(request):
    cart = _get_cart(request)
    if not cart:
        return []
    books = Book.objects.filter(pk__in=cart.keys())
    return [
        {"book": b, "quantity": cart[str(b.pk)], "subtotal": b.price * cart[str(b.pk)]}
        for b in books
    ]


# ---------- Recently viewed (session: list of book ids, newest last) ----------


def _push_recently_viewed(request, book_id: int):
    ids = request.session.get("recently_viewed")
    if not isinstance(ids, list):
        ids = []
    book_id = int(book_id)
    if book_id in ids:
        ids.remove(book_id)
    ids.append(book_id)
    request.session["recently_viewed"] = ids[-20:]
    request.session.modified = True


def _recently_viewed_books(request, limit: int = 6):
    ids = request.session.get("recently_viewed")
    if not isinstance(ids, list) or not ids:
        return []
    ids = ids[-limit:][::-1]
    books = list(Book.objects.filter(pk__in=ids))
    return _order_books_by_ids(books, ids)


def _order_books_by_ids(queryset, ids):
    """Return list of books in same order as ids (ids not in queryset skipped)."""
    by_id = {b.pk: b for b in queryset}
    return [by_id[i] for i in ids if i in by_id]


# ---------- Recommendation helpers ----------


def _get_popular_books(limit: int = 8):
    return (
        Book.objects.annotate(total_sold=Count("order_items"))
        .order_by("-total_sold", "title")[:limit]
    )


def _get_top_rated_books(limit: int = 8):
    return (
        Book.objects.annotate(avg_rating=Avg("ratings__score"), rating_count=Count("ratings"))
        .filter(rating_count__gt=0)
        .order_by("-avg_rating", "-rating_count", "title")[:limit]
    )


def _get_recommended_for_user(user, limit: int = 8):
    user_orders = OrderItem.objects.filter(order__user=user)
    user_ratings = Rating.objects.filter(user=user, score__gte=4)
    category_ids = (
        Category.objects.filter(books__order_items__in=user_orders)
        .union(Category.objects.filter(books__ratings__in=user_ratings))
        .values_list("id", flat=True)
    )
    if not category_ids:
        return _get_popular_books(limit=limit)
    return (
        Book.objects.filter(category_id__in=category_ids)
        .annotate(total_sold=Count("order_items"), avg_rating=Avg("ratings__score"))
        .order_by("-avg_rating", "-total_sold", "title")
        .distinct()[:limit]
    )


def _books_queryset(search=None, category_id=None, sort="title"):
    qs = Book.objects.all()
    if search and search.strip():
        q = Q(title__icontains=search.strip()) | Q(author__icontains=search.strip())
        qs = qs.filter(q)
    if category_id:
        qs = qs.filter(category_id=category_id)
    if sort == "price_asc":
        qs = qs.order_by("price", "title")
    elif sort == "price_desc":
        qs = qs.order_by("-price", "title")
    elif sort == "newest":
        qs = qs.order_by("-created_at", "title")
    elif sort == "popular":
        qs = qs.annotate(total_sold=Count("order_items")).order_by("-total_sold", "title")
    elif sort == "top_rated":
        qs = (
            qs.annotate(avg_rating=Avg("ratings__score"), rating_count=Count("ratings"))
            .filter(rating_count__gt=0)
            .order_by("-avg_rating", "-rating_count", "title")
        )
    else:
        qs = qs.order_by("title")
    return qs


# ---------- Views ----------


def home(request):
    books = Book.objects.all().order_by("-created_at")[:12]
    popular_books = _get_popular_books()
    top_rated_books = _get_top_rated_books()
    recommended_books = None
    if request.user.is_authenticated:
        recommended_books = _get_recommended_for_user(request.user)
    recently_viewed = _recently_viewed_books(request)
    context = {
        "books": books,
        "popular_books": popular_books,
        "top_rated_books": top_rated_books,
        "recommended_books": recommended_books,
        "recently_viewed": recently_viewed,
    }
    return render(request, "books/home.html", context)


def book_list(request):
    search = request.GET.get("q", "").strip()
    category_id = request.GET.get("category")
    try:
        current_category_id = int(category_id) if category_id else None
    except (TypeError, ValueError):
        current_category_id = None
    sort = request.GET.get("sort", "title")
    qs = _books_queryset(search=search or None, category_id=current_category_id, sort=sort)
    paginator = Paginator(qs, 12)
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)
    categories = Category.objects.all().order_by("name")
    context = {
        "page": page,
        "books": page.object_list,
        "categories": categories,
        "search": search,
        "current_category_id": current_category_id,
        "current_sort": sort,
    }
    return render(request, "books/book_list.html", context)


def category_list(request):
    categories = Category.objects.annotate(book_count=Count("books")).order_by("name")
    return render(request, "books/category_list.html", {"categories": categories})


def category_detail(request, pk: int):
    category = get_object_or_404(Category, pk=pk)
    sort = request.GET.get("sort", "title")
    qs = _books_queryset(category_id=pk, sort=sort)
    paginator = Paginator(qs, 12)
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)
    context = {"category": category, "page": page, "books": page.object_list, "current_sort": sort}
    return render(request, "books/category_detail.html", context)


def book_detail(request, pk: int):
    book = get_object_or_404(Book, pk=pk)
    _push_recently_viewed(request, book.pk)
    similar_books = (
        Book.objects.filter(category=book.category)
        .exclude(pk=book.pk)
        .annotate(total_sold=Count("order_items"))
        .order_by("-total_sold", "title")[:8]
    )
    same_author_books = (
        Book.objects.filter(author=book.author)
        .exclude(pk=book.pk)
        .order_by("title")[:6]
    )
    avg_rating = book.ratings.aggregate(avg=Avg("score"), cnt=Count("id"))
    book_ratings = book.ratings.select_related("user").order_by("-created_at")[:10]
    user_rating = None
    rating_form = None
    is_in_wishlist = False
    if request.user.is_authenticated:
        user_rating = book.ratings.filter(user=request.user).first()
        rating_form = RatingForm(instance=user_rating)
        is_in_wishlist = Wishlist.objects.filter(user=request.user, book=book).exists()
    context = {
        "book": book,
        "similar_books": similar_books,
        "same_author_books": same_author_books,
        "avg_rating": avg_rating,
        "book_ratings": book_ratings,
        "user_rating": user_rating,
        "rating_form": rating_form,
        "is_in_wishlist": is_in_wishlist,
    }
    return render(request, "books/book_detail.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Đăng ký thành công.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def rate_book(request, book_id: int):
    book = get_object_or_404(Book, pk=book_id)
    user_rating = book.ratings.filter(user=request.user).first()
    if request.method == "POST":
        form = RatingForm(request.POST, instance=user_rating)
        if form.is_valid():
            r = form.save(commit=False)
            r.user = request.user
            r.book = book
            r.save()
            messages.success(request, "Đã lưu đánh giá.")
            return redirect("book_detail", pk=book.pk)
    else:
        form = RatingForm(instance=user_rating)
    return render(request, "books/rate_book.html", {"book": book, "form": form})


def cart_view(request):
    items = _cart_items(request)
    total = sum(x["subtotal"] for x in items)
    context = {"cart_items": items, "cart_total": total}
    return render(request, "books/cart.html", context)


def add_to_cart(request, book_id: int):
    book = get_object_or_404(Book, pk=book_id)
    cart = _get_cart(request)
    key = str(book.pk)
    qty = request.POST.get("quantity") or request.GET.get("quantity") or 1
    try:
        qty = max(1, int(qty))
    except (TypeError, ValueError):
        qty = 1
    cart[key] = cart.get(key, 0) + qty
    _set_cart(request, cart)
    messages.success(request, f"Đã thêm '{book.title}' vào giỏ.")
    next_url = request.GET.get("next") or request.POST.get("next") or "book_detail"
    if next_url == "book_detail":
        return redirect("book_detail", pk=book.pk)
    return redirect("cart")


def update_cart(request):
    if request.method != "POST":
        return redirect("cart")
    cart = _get_cart(request)
    for key in list(cart.keys()):
        qty = request.POST.get(f"qty_{key}")
        if qty is not None:
            try:
                n = int(qty)
                if n <= 0:
                    del cart[key]
                else:
                    cart[key] = n
            except (TypeError, ValueError):
                pass
    _set_cart(request, cart)
    messages.info(request, "Đã cập nhật giỏ hàng.")
    return redirect("cart")


@login_required
def checkout(request):
    items = _cart_items(request)
    if not items:
        messages.warning(request, "Giỏ hàng trống.")
        return redirect("cart")
    order = Order.objects.create(user=request.user)
    for row in items:
        OrderItem.objects.create(
            order=order,
            book=row["book"],
            quantity=row["quantity"],
            price=row["book"].price,
        )
    _set_cart(request, {})
    messages.success(request, f"Đặt hàng thành công. Mã đơn: #{order.pk}")
    return redirect("order_list")


@login_required
def order_list(request):
    orders = request.user.orders.prefetch_related("items__book").order_by("-created_at")
    return render(request, "books/order_list.html", {"orders": orders})


# ---------- Wishlist ----------


@login_required
def wishlist_add(request, book_id: int):
    book = get_object_or_404(Book, pk=book_id)
    Wishlist.objects.get_or_create(user=request.user, book=book)
    messages.success(request, f"Đã thêm '{book.title}' vào danh sách yêu thích.")
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "book_detail"
    if "book_detail" in str(next_url) or not next_url:
        return redirect("book_detail", pk=book.pk)
    return redirect(next_url)


@login_required
def wishlist_remove(request, book_id: int):
    book = get_object_or_404(Book, pk=book_id)
    Wishlist.objects.filter(user=request.user, book=book).delete()
    messages.info(request, "Đã bỏ khỏi danh sách yêu thích.")
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER")
    if next_url and "wishlist" in next_url:
        return redirect("wishlist")
    return redirect("book_detail", pk=book.pk)


@login_required
def wishlist_view(request):
    items = request.user.wishlist_items.select_related("book").order_by("-added_at")
    return render(request, "books/wishlist.html", {"wishlist_items": items})


# ---------- Profile ----------


@login_required
def profile(request):
    return render(request, "books/profile.html", {"profile_user": request.user})


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Đã cập nhật thông tin.")
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "books/profile_edit.html", {"form": form})


# ---------- Static ----------


def about(request):
    return render(request, "books/about.html")


def contact(request):
    return render(request, "books/contact.html")
