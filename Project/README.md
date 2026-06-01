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
| **AI Backend** | **Ollama** (Model: **Qwen 2.5 7B**) |
| **Database** | **MySQL** (Vận hành thực tế), SQLite3 (Development) |
| **Payment Gateway** | **VNPay** (Tích hợp thực tế), Mock Payment |

---

## 4. Hướng dẫn cài đặt & Cấu hình Production

### 1. FILE CẤU HÌNH .ENV (Bắt buộc)
Tạo file `.env` tại thư mục gốc và cấu hình như sau:

```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database MySQL
DB_NAME=smart_bookstore
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306

# AI / Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# VNPay Settings
VNP_TMN_CODE=your-tmn-code
VNP_HASH_KEY=your-hash-key
VNP_URL=https://sandbox.vnpayment.vn/paymentv2/vpcpay.html
```

### 2. CÀI ĐẶT THƯ VIỆN
```bash
pip install django python-dotenv mysqlclient requests
```

### 3. KIẾN TRÚC CHATBOT MỚI
Chatbot Bookie đã được nâng cấp lên kiến trúc **RAG (Retrieval-Augmented Generation)**:
- **Streaming Response:** Hiển thị câu trả lời ngay lập tức theo thời gian thực (giống ChatGPT).
- **Database Access:** AI có khả năng tra cứu hơn 400 đầu sách trong kho dữ liệu thực tế để gợi ý chính xác cho khách hàng.

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
