import requests
from django.core.management.base import BaseCommand
from books.models import Book, Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds digital books from Project Gutenberg'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Đang bắt đầu kéo sách từ Project Gutenberg...'))
        
        # 1. Đảm bảo có Category "Kinh điển"
        category, _ = Category.objects.get_or_create(name='Kinh điển')
        
        # 2. Gọi API Gutendex để lấy danh sách sách phổ biến
        # Chúng ta lọc lấy sách tiếng Anh và có định dạng text/plain
        api_url = "https://gutendex.com/books/?languages=en&topic=fiction"
        
        try:
            response = requests.get(api_url, timeout=20)
            data = response.json()
            books_data = data.get('results', [])[:10]  # Lấy 10 cuốn đầu tiên
            
            for b_data in books_data:
                title = b_data.get('title')
                author = b_data['authors'][0]['name'] if b_data['authors'] else 'Unknown'
                gutenberg_id = b_data.get('id')
                
                self.stdout.write(f"Đang xử lý: {title}...")
                
                # Kiểm tra xem sách đã tồn tại chưa
                if Book.objects.filter(title=title, author=author).exists():
                    self.stdout.write(self.style.WARNING(f"Sách '{title}' đã tồn tại. Bỏ qua."))
                    continue
                
                # Tìm link text/plain
                text_url = b_data['formats'].get('text/plain; charset=utf-8') or b_data['formats'].get('text/plain')
                
                if not text_url:
                    self.stdout.write(self.style.ERROR(f"Không tìm thấy bản text cho {title}"))
                    continue
                
                # Tải nội dung sách
                try:
                    content_res = requests.get(text_url, timeout=15)
                    content_text = content_res.text
                    
                    # Lấy ảnh bìa (Open Library thường có ảnh dựa trên ID Gutenberg hoặc ID khác)
                    cover_url = b_data['formats'].get('image/jpeg') # Gutendex thường có link ảnh bìa sẵn
                    
                    # Tạo sách trong DB
                    Book.objects.create(
                        title=title,
                        author=author,
                        description=f"Một tác phẩm kinh điển từ Project Gutenberg (ID: {gutenberg_id}).",
                        price=0.00, # Sách kinh điển thường miễn phí hoặc rẻ
                        category=category,
                        is_digital=True,
                        content_text=content_text,
                        cover_image=cover_url or "",
                        stock=999
                    )
                    self.stdout.write(self.style.SUCCESS(f"Đã thêm thành công: {title}"))
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Lỗi khi tải nội dung {title}: {str(e)}"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Lỗi khi gọi API Gutendex: {str(e)}"))

        self.stdout.write(self.style.SUCCESS('--- Hoàn tất quá trình seed dữ liệu ---'))
