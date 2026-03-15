# Smart Bookstore — Website gợi ý sản phẩm thông minh

Đề tài môn Python: **Website bán sách trực tuyến** với hệ thống gợi ý sách dựa trên AI (content-based recommendation).

---

## 1. Tổng quan

- **Công nghệ:** Django (Python), SQLite, Bootstrap 5  
- **Loại đề tài:** Web (Django) + AI (thuật toán gợi ý)  
- **Mô tả:** Cửa hàng sách online giả lập: xem sách, giỏ hàng, đặt hàng, đánh giá, danh sách yêu thích và **gợi ý sách thông minh** theo thể loại/sở thích người dùng.

---

## 2. Công nghệ sử dụng

| Thành phần   | Công nghệ                    |
|-------------|------------------------------|
| Backend     | Django 6.x                    |
| Database    | SQLite3                       |
| Frontend    | HTML, Bootstrap 5, Django Template |
| Ngôn ngữ    | Python 3.12                   |

---

## 3. Chức năng chính

### 3.1 Khách (chưa đăng nhập)

- Xem **trang chủ**: sách mới, bán chạy, đánh giá cao, đã xem gần đây.
- **Tìm kiếm & lọc**: tìm theo tên sách/tác giả, lọc theo thể loại, sắp xếp (giá, tên, mới nhất, bán chạy, đánh giá).
- **Phân trang** danh sách sách (12 sách/trang).
- **Duyệt theo thể loại**: danh sách thể loại → trang sách theo từng thể loại.
- Xem **chi tiết sách**: mô tả, giá, sách cùng thể loại, cùng tác giả.
- **Giỏ hàng** (session): thêm/sửa số lượng; đặt hàng cần đăng nhập.

### 3.2 Người dùng (đã đăng nhập)

- Tất cả chức năng khách.
- **Đăng ký / Đăng nhập / Đăng xuất**.
- **Giỏ hàng & đặt hàng**: thanh toán (tạo đơn), xem **đơn hàng của tôi**.
- **Đánh giá sách**: 1–5 sao + nhận xét; xem đánh giá và điểm trung bình.
- **Danh sách yêu thích (Wishlist)**: thêm/bỏ sách, xem trang yêu thích.
- **Tài khoản**: xem thông tin, chỉnh sửa họ tên, email.

### 3.3 AI — Gợi ý sách thông minh

- **Sách bán chạy:** theo số lượng đã bán (`OrderItem`).
- **Sách được đánh giá cao:** theo điểm trung bình và số lượt đánh giá.
- **Gợi ý cho bạn (trang chủ):** dựa trên thể loại sách user đã mua hoặc đánh giá ≥ 4 sao → gợi ý sách cùng thể loại (content-based).
- **Sách tương tự (trang chi tiết):** cùng thể loại, sắp theo độ phổ biến.
- **Cùng tác giả:** sách cùng `author`.

---

## 4. Cấu trúc project

```
Project/
├── manage.py
├── README.md
├── bookstore/                 # Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── books/                     # App chính
│   ├── models.py              # Category, Book, Order, OrderItem, Rating, Wishlist
│   ├── views.py               # Toàn bộ view
│   ├── urls.py
│   ├── forms.py               # RegisterForm, RatingForm, ProfileEditForm
│   ├── admin.py               # Đăng ký model cho admin
│   ├── context_processors.py  # cart_count, recently_viewed_ids
│   └── migrations/
├── templates/
│   ├── base.html              # Layout chung, navbar, footer
│   ├── registration/
│   │   ├── login.html
│   │   └── register.html
│   └── books/
│       ├── home.html
│       ├── book_list.html     # Tìm kiếm, lọc, phân trang
│       ├── book_detail.html
│       ├── category_list.html
│       ├── category_detail.html
│       ├── cart.html
│       ├── order_list.html
│       ├── wishlist.html
│       ├── profile.html
│       ├── profile_edit.html
│       ├── rate_book.html
│       ├── about.html
│       └── contact.html
└── db.sqlite3                 # Database (tạo sau khi migrate)
```

---

## 5. Mô hình dữ liệu (Models)

| Model      | Mô tả ngắn |
|-----------|-------------|
| **Category** | Thể loại sách (tên). |
| **Book**     | Sách: title, author, description, price, category, published_year, num_pages, cover_image, created_at. |
| **Order**    | Đơn hàng: user, created_at. Có `total` (property). |
| **OrderItem**| Chi tiết đơn: order, book, quantity, price. Có `subtotal` (property). |
| **Rating**   | Đánh giá: user, book, score (1–5), comment, created_at. Unique (user, book). |
| **Wishlist** | Yêu thích: user, book, added_at. Unique (user, book). |

Quan hệ chính: `Book` → `Category` (FK); `Order` → `User`, `OrderItem` → `Order` & `Book`; `Rating`, `Wishlist` → `User` & `Book`.

---

## 6. URL chính

| URL | Chức năng |
|-----|------------|
| `/` | Trang chủ |
| `/books/` | Tất cả sách (tìm, lọc, sắp xếp, phân trang) |
| `/books/<id>/` | Chi tiết sách |
| `/categories/` | Danh sách thể loại |
| `/categories/<id>/` | Sách theo thể loại |
| `/register/`, `/login/`, `/logout/` | Đăng ký, đăng nhập, đăng xuất |
| `/cart/` | Giỏ hàng |
| `/cart/add/<book_id>/` | Thêm vào giỏ |
| `/cart/checkout/` | Thanh toán (đặt hàng) |
| `/orders/` | Đơn hàng của tôi |
| `/wishlist/` | Danh sách yêu thích |
| `/wishlist/add/<book_id>/`, `/wishlist/remove/<book_id>/` | Thêm/bỏ yêu thích |
| `/profile/`, `/profile/edit/` | Tài khoản, chỉnh sửa |
| `/rate/<book_id>/` | Gửi/sửa đánh giá |
| `/about/`, `/contact/` | Giới thiệu, liên hệ |
| `/admin/` | Django Admin |

---

## 7. Cách chạy project

### Yêu cầu

- Python 3.10+
- Django 6.x (`pip install django`)
- MySQL (hoặc đổi lại SQLite trong `settings.py`)

### Các bước

```bash
# 1. Vào thư mục project
cd Project

# 2. Tạo database và áp dụng migrations
python manage.py migrate

# 3. (Khuyến nghị) Thêm sách mẫu từ Open Library API
python manage.py seed_books
# Tùy chọn: python manage.py seed_books --limit 24 --subjects fiction,programming,science

# 4. (Tùy chọn) Tạo tài khoản admin
python manage.py createsuperuser

# 5. Chạy server
python manage.py runserver
```

Mở trình duyệt: **http://127.0.0.1:8000/**

- Lệnh **seed_books** lấy dữ liệu từ [Open Library](https://openlibrary.org) (API công khai), tạo thể loại và sách kèm ảnh bìa, giá mẫu.
- Có thể thêm/sửa **Category**, **Book** qua **http://127.0.0.1:8000/admin/** (sau khi tạo superuser).

---

## 8. Phần AI trong báo cáo

Hệ thống gợi ý sử dụng:

1. **Content-based:** Gợi ý theo thể loại sách user đã mua/đánh giá cao.
2. **Thống kê:** Sách bán chạy (số lượng bán), sách đánh giá cao (rating trung bình).
3. **Quan hệ nội dung:** Sách cùng thể loại, cùng tác giả.

Code gợi ý nằm trong `books/views.py`: `_get_popular_books`, `_get_top_rated_books`, `_get_recommended_for_user`, và phần “sách tương tự” / “cùng tác giả” trong `book_detail`.

---

## 9. Tác giả / Nhóm

- Đề tài: **Website gợi ý sản phẩm thông minh** (Smart Bookstore)  
- Môn: Python  
- Số nhóm: 13 (theo đăng ký đề tài)

---

*Tài liệu tổng hợp cho project Smart Bookstore — Django + AI gợi ý.*
