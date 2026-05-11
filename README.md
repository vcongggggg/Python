# Bookie — Midnight Cosmic Library ✦

**Bookie** là hệ thống thương mại điện tử bán sách hiện đại, được tái định nghĩa với trải nghiệm **Midnight Cosmic** (Vũ trụ nửa đêm). Website tích hợp Trí tuệ nhân tạo (AI) để cá nhân hóa hành trình đọc sách, phân tích cảm xúc và mang đến một giao diện điện ảnh, cao cấp.

---

## 1. Tầm nhìn dự án (Phase 3: Midnight Cosmic Redesign)

Dự án đã trải qua đợt lột xác toàn diện về UI/UX để chuyển mình từ một nhà sách trực tuyến thông thường thành một **Thư viện số cao cấp**:
- **Branding:** Tên thương hiệu mới **Bookie** với Logo tối giản phong cách Gold-on-Dark.
- **Aesthetic:** Concept "Midnight Cosmic" sử dụng dải màu Aurora Mesh, các hạt tinh thể chuyển động và hiệu ứng kính mờ (Glassmorphism).
- **Technology:** Tích hợp **GSAP (GreenSock)** cho các hiệu ứng cuộn trang mượt mà và ScrollTriggers sinh động.

---

## 2. Các tính năng đột phá (Core Features)

### 2.1 Trải nghiệm người dùng (UX Design)
- **Bento Grid Categories:** Hệ thống danh mục được sắp xếp theo bố cục Bento hiện đại, sử dụng hình ảnh minh họa 3D phong cách Abstract chuyên sâu.
- **Infinite Cosmic Ticker:** Thanh chạy thông tin vô tận (Looping Marquee) ở Header, cung cấp các thông tin khuyến mãi và tính năng AI theo thời gian thực.
- **AI Showcase:** Khu vực giới thiệu công nghệ AI với các thẻ tính năng (Content-based Filtering, Sentiment Analysis, Reading DNA) được thiết kế với Background AI-generated 3D nghệ thuật.
- **Cinematic Book Cards:** Thẻ sách 3D với hiệu ứng Glare (phản chiếu ánh sáng) và tương tác vật lý khi di chuột.

### 2.2 Trí tuệ nhân tạo (AI Engine)
- **Content-based Filtering:** Gợi ý sách thông minh dựa trên "Dấu vân tay sở thích" của người dùng.
- **Sentiment Analysis:** Phân tích cảm xúc nhận xét tự động (Tích cực/Tiêu cực) để xếp hạng chất lượng sách.
- **Reading DNA:** Bản đồ hóa nhóm tính cách đọc sách (Explorer, Scholar, Critic...) qua đồ thị trực quan.
- **Bookie Chatbot:** Trợ lý ảo AI có khả năng kéo thả, hỗ trợ giải đáp và tìm kiếm sách 24/7.

### 2.3 Hệ thống nghiệp vụ chuyên nghiệp
- **Thanh toán QR:** Hệ thống Mock Payment tích hợp tạo mã QR động cho Momo/VNPay.
- **Dashboard Admin:** Quản lý doanh thu, đơn hàng và kho sách qua các biểu đồ trực quan (Chart.js).
- **Real-time Interaction:** Toàn bộ hành động Thêm vào giỏ/Yêu thích đều sử dụng AJAX không tải lại trang.

---

## 3. Stack Công nghệ (Technology Stack)

| Thành phần | Công nghệ |
| :--- | :--- |
| **Core Backend** | Django 6.1 (Python 3.12) |
| **Frontend Foundation** | HTML5, Vanilla JS (ES6+), CSS3 Variables |
| **Animation Engine** | **GSAP (GreenSock)** + ScrollTrigger |
| **UI Kit** | Custom CSS (Midnight System), Bootstrap Icons |
| **Database** | SQLite3 (Cấu trúc quan hệ tối ưu) |
| **Visual Assets** | AI-Generated 3D Illustrations |

---

## 4. Hướng dẫn cài đặt nhanh

```bash
# 1. Cài đặt môi trường
pip install django

# 2. Khởi tạo dữ liệu
python manage.py makemigrations
python manage.py migrate

# 3. Import dữ liệu sách mẫu (Chuyên sâu)
python manage.py seed_books --limit 50

# 4. Chạy server
python manage.py runserver
```

---

## 5. Thông tin thực hiện

- **Dự án:** Bookie — Midnight Cosmic Bookstore
- **Nhóm thực hiện:** Nhóm 13 (PBL Python)
- **Trạng thái:** Hoàn thiện 100% (Gold Master Version)

---
*Giao diện Bookie được tối ưu hóa cho trải nghiệm cao cấp trên trình duyệt hiện đại.*

---

## 6. Hướng dẫn cài đặt

```bash
# 1. Cài đặt thư viện
pip install django

# 2. Khởi tạo Database
python manage.py makemigrations
python manage.py migrate

# 3. Seed dữ liệu thực tế (Hàng chục đầu sách từ Open Library)
python manage.py seed_books --limit 50

# 4. Tạo quản trị viên
python manage.py createsuperuser

# 5. Khởi chạy
python manage.py runserver
```

---

## 7. Thông tin nhóm thực hiện

- **Đề tài:** Website gợi ý sản phẩm thông minh (Smart Bookstore)
- **Môn học:** Lập trình Python
- **Nhóm:** 13
- **Tính năng đặc biệt:** Mock Payment, Draggable AI Chatbot, Reading DNA, Sentiment Analysis.

---
*Dự án hoàn thiện 100% các yêu cầu về nghiệp vụ và tích hợp công nghệ AI.*
