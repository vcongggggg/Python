# Smart Bookstore — Hệ thống gợi ý sách thông minh (Phase 2 Enhanced)

Đề tài môn Python: **Website bán sách trực tuyến** tích hợp AI (Content-based Recommendation, Sentiment Analysis & User Profiling).

---

## 1. Tổng quan dự án

Dự án đã hoàn thành **Phase 2** với các nâng cấp mạnh mẽ về trải nghiệm người dùng (UX), tính năng tương tác thời gian thực (AJAX) và ứng dụng AI chuyên sâu hơn.

- **Công nghệ:** Django 6.x, SQLite, Bootstrap 5, Chart.js.
- **Tính năng nổi bật:** Gợi ý sách thông minh, Phân tích cảm nhận người dùng (AI Sentiment), Reading DNA, và Quản lý đơn hàng thời gian thực.

---

## 2. Các chức năng mới (Phase 2 Update)

### 2.1 Trải nghiệm người dùng (UX) & AJAX
- **Real-time Wishlist & Cart:** Thêm/xóa sản phẩm khỏi yêu thích và giỏ hàng ngay lập tức mà không cần tải lại trang. Cập nhật Badge số lượng ở Navbar theo thời gian thực.
- **Thanh toán thông minh:** Áp dụng mã giảm giá (Coupon) và xem trước số tiền được giảm bằng AJAX trước khi đặt hàng.
- **Giao diện hiện đại:** Navbar được tái cấu trúc thông minh, hỗ trợ Dark Mode hoàn chỉnh, hình ảnh bìa sách hiển thị trọn vẹn (Aspect-ratio fix).

### 2.2 AI & Dữ liệu chuyên sâu
- **Reading DNA:** Phân tích phong cách đọc sách của người dùng (Explorer, Dreamer, Critic...) dựa trên lịch sử mua hàng và đánh giá.
- **AI Sentiment Analysis:** Tự động phân tích sắc thái nhận xét của khách hàng (Tích cực, Tiêu cực, Trung lập) để tóm tắt chất lượng sách.
- **Explainable Recommendations:** Gợi ý sách kèm lý do cụ thể (Ví dụ: "Vì bạn đã mua sách của tác giả X", "Cùng thể loại Y mà bạn yêu thích").
- **Reading Milestones:** Hệ thống thành tựu (Gamification) tặng huy hiệu dựa trên hoạt động đọc sách (Đại tuyển thủ, Bác học đa tài, Nhà phê bình ưu tú...).

### 2.3 Dashboard Quản lý (Dành cho Staff)
- **Thống kê trực quan:** Biểu đồ doanh thu theo tháng, phân bổ thể loại và top sách bán chạy (sử dụng Chart.js).
- **Quản lý đơn hàng AJAX:** Cập nhật trạng thái đơn hàng (Chờ xác nhận, Đang giao, Đã giao...) trực tiếp từ bảng thống kê.
- **Báo cáo dữ liệu:** Xuất dữ liệu Sách và Đơn hàng ra file CSV (UTF-8-SIG hỗ trợ Excel).
- **Cảnh báo tồn kho:** Tự động liệt kê các đầu sách sắp hết hàng (tồn kho < 10).

---

## 3. Cấu trúc Project (Cập nhật)

```
Project/
├── bookstore/                 # Cấu hình dự án Django
├── books/                     # App chính
│   ├── context_processors.py  # Xử lý dữ liệu toàn cục (Cart, Wishlist, Reading DNA)
│   ├── models.py              # Category, Book, Order, Rating, Wishlist, Coupon
│   ├── views.py               # Chứa logic AI, AJAX API và Staff Dashboard
│   ├── seed_books.py          # Lệnh import dữ liệu mẫu từ Open Library
│   └── ...
├── templates/
│   ├── base.html              # Navbar (Redesigned), Footer, Theme Engine
│   └── books/
│       ├── dashboard.html     # Staff Dashboard với biểu đồ
│       ├── reading_dna.html   # Trang phân tích AI cá nhân
│       ├── checkout.html      # Trang thanh toán tích hợp AJAX Coupon
│       └── ...
└── static/                    # Assets, CSS, JS
```

---

## 4. Công nghệ & Thư viện

| Thành phần | Công nghệ |
| :--- | :--- |
| **Backend** | Django 6.1 (Python 3.12) |
| **Frontend UI** | Bootstrap 5.3, Bootstrap Icons |
| **Visualization** | Chart.js 4.4 (Polar Area, Line, Bar, Doughnut) |
| **AI Logic** | Rule-based Sentiment, Content-based Filtering, User DNA Profiling |
| **Database** | SQLite3 |

---

## 5. Hướng dẫn cài đặt & Chạy nhanh

```bash
# 1. Cài đặt Django
pip install django

# 2. Migrate Database
python manage.py migrate

# 3. Seed dữ liệu mẫu (Sách & Thể loại thực tế)
python manage.py seed_books --limit 50 --subjects fiction,programming,business

# 4. Tạo tài khoản Admin (Để vào Dashboard)
python manage.py createsuperuser

# 5. Khởi động server
python manage.py runserver
```

Truy cập: `http://127.0.0.1:8000/`

---

## 6. AI Features trong báo cáo

1. **Phân tích cảm xúc:** Sử dụng thuật toán so khớp từ khóa (Rule-based) hỗ trợ song ngữ (Việt - Anh) để gán nhãn sentiment cho review.
2. **Gợi ý dựa trên nội dung:** Xây dựng Profile người dùng từ dữ liệu mua sắm thực tế để gợi ý những sản phẩm có tương quan cao nhất.
3. **Reading DNA Mapping:** Thuật toán phân loại người dùng vào các nhóm tính cách đọc sách dựa trên trọng số của các thể loại đã tương tác.

---

*Dự án được thực hiện cho mục đích học tập môn Lập trình Python — Nhóm 13.*
