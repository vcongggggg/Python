import random
from django.db.models import Q, Count
from .models import Book, Order, Wishlist

class BookieChatbot:
    """Hệ thống Trợ lý ảo AI Bookie cho Smart Bookstore."""

    def __init__(self, user=None):
        self.user = user

    def get_response(self, text: str):
        text = text.lower().strip()
        
        # 1. Chào hỏi
        if any(w in text for w in ["chào", "hi", "hello", "bạn ơi", "bookie"]):
            return self._handle_greeting()

        # 2. Tra cứu đơn hàng
        if any(w in text for w in ["đơn hàng", "mua", "vận chuyển", "đã giao", "trạng thái"]):
            return self._handle_order_lookup()

        # 3. Tìm kiếm sách
        if any(w in text for w in ["tìm", "sách", "có sách", "muốn mua", "quyển", "cuốn"]):
            return self._handle_book_search(text)

        # 4. Tư vấn DNA / Gợi ý
        if any(w in text for w in ["gợi ý", "dna", "hợp", "thích"]):
            return self._handle_dna_recommendation()

        # 5. FAQ cơ bản
        if any(w in text for w in ["ship", "vận chuyển", "bao lâu", "giá"]):
            return {
                "text": "Bookie hỗ trợ giao hàng toàn quốc nhé! Thường mất 2-3 ngày thôi nè. Phí ship đồng giá 30k, nhưng đơn trên 500k là được FREESHIP luôn đó!",
                "type": "text"
            }

        if "đổi trả" in text:
            return {
                "text": "Bạn có thể đổi trả sách trong vòng 7 ngày nếu có lỗi từ nhà sản xuất nha. Bookie luôn đặt quyền lợi của bạn lên hàng đầu!",
                "type": "text"
            }

        # 6. Mặc định
        return {
            "text": "Xin lỗi, Bookie chưa hiểu ý bạn lắm. Bạn có thể hỏi về 'Tìm sách', 'Trạng thái đơn hàng' hoặc 'Gợi ý sách' được không?",
            "type": "text",
            "quick_replies": ["Tìm sách hay", "Đơn hàng của tôi", "Gợi ý cho tôi"]
        }

    def _handle_greeting(self):
        name = self.user.username if self.user and self.user.is_authenticated else "bạn"
        greetings = [
            f"Chào {name}! Bookie rất vui được gặp bạn. Hôm nay bạn muốn tìm cuốn sách nào?",
            f"Hế lô {name}! Có Bookie đây. Bạn cần mình giúp gì cho hành trình đọc sách hôm nay không?",
            f"Chào {name}, mình là Bookie. Rất nhiều sách mới vừa về kho, bạn có muốn mình giới thiệu không?"
        ]
        return {
            "text": random.choice(greetings),
            "type": "text",
            "quick_replies": ["Tìm sách mới", "Gợi ý theo DNA", "Tra cứu đơn hàng"]
        }

    def _handle_order_lookup(self):
        if not self.user or not self.user.is_authenticated:
            return {
                "text": "Bạn vui lòng đăng nhập để Bookie có thể tra cứu đơn hàng giúp bạn nhé!",
                "type": "text",
                "quick_replies": ["Đăng nhập"]
            }
        
        last_order = Order.objects.filter(user=self.user).order_by("-created_at").first()
        if not last_order:
            return {
                "text": "Bạn chưa có đơn hàng nào tại Smart Bookstore. Mau mau chốt đơn để được Bookie phục vụ tận tình nhé!",
                "type": "text",
                "quick_replies": ["Mua sách ngay"]
            }
        
        return {
            "text": f"Đơn hàng gần nhất của bạn là **#{last_order.pk}**. Trạng thái hiện tại: **{last_order.status_display_vi}**. Cảm ơn bạn đã tin tưởng Bookie!",
            "type": "text",
            "quick_replies": ["Chi tiết đơn hàng", "Mua thêm sách"]
        }

    def _handle_book_search(self, text):
        # Extract keywords (Simple way: remove common stop words or action words)
        ignore_words = ["tìm", "sách", "có", "không", "về", "của", "tác giả", "muốn", "quyển", "cuốn", "giá", "rẻ"]
        query = text
        for w in ignore_words:
            query = query.replace(w, "")
        query = query.strip()

        if not query:
            return {
                "text": "Bạn muốn tìm sách về chủ đề gì nè? Ví dụ: 'Sách Python' hay 'Tác giả Nguyễn Nhật Ánh'.",
                "type": "text"
            }

        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(category__name__icontains=query)
        ).annotate(sales=Count("order_items")).order_by("-sales")[:3]

        if not books:
            return {
                "text": f"Tiếc quá, Bookie chưa thấy cuốn nào liên quan tới '{query}'. Bạn thử tìm với từ khóa khác xem sao?",
                "type": "text"
            }

        results = []
        for b in books:
            results.append({
                "id": b.pk,
                "title": b.title,
                "price": f"{b.price:,.0f}₫",
                "url": f"/books/{b.pk}/",
                "image": b.cover_image or None
            })

        return {
            "text": f"Đã tìm thấy vài cuốn hay ho cho bạn về '{query}' đây:",
            "type": "books",
            "books": results
        }

    def _handle_dna_recommendation(self):
        if not self.user or not self.user.is_authenticated:
            return {
                "text": "Đăng nhập ngay để Bookie phân tích DNA đọc sách và gợi ý 'chuẩn gu' nhất cho bạn nhé!",
                "type": "text"
            }
        
        # Pull from the same logic used in the Reading DNA page
        from .views import _get_explainable_recommendations
        recs = _get_explainable_recommendations(self.user, limit=3)
        
        if not recs:
            return {
                "text": "Bookie đang nghiên cứu thêm gu của bạn. Hãy mua và đánh giá thêm vài cuốn để mình hiểu bạn hơn nhé!",
                "type": "text",
                "quick_replies": ["Xem sách bán chạy"]
            }
        
        results = []
        for r in recs:
            b = r["book"]
            results.append({
                "id": b.pk,
                "title": b.title,
                "price": f"{b.price:,.0f}₫",
                "url": f"/books/{b.pk}/",
                "image": b.cover_image or None,
                "reason": r["reason"]
            })

        return {
            "text": "Dựa trên DNA của bạn, Bookie cá là bạn sẽ thích những cuốn này:",
            "type": "books",
            "books": results
        }
