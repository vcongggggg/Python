"""
Lấy dữ liệu sách mẫu từ Open Library API (API công khai, miễn phí) và lưu vào database.
Chạy: python manage.py seed_books
"""
import json
import random
import urllib.error
import urllib.request

from django.core.management.base import BaseCommand

from books.models import Book, Category


def fetch_url(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "SmartBookstore/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def get_cover_url(cover_id):
    if not cover_id:
        return ""
    return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"


class Command(BaseCommand):
    help = "Thêm sách mẫu từ Open Library API vào database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=24,
            help="Số sách tối đa mỗi thể loại (mặc định 24)",
        )
        parser.add_argument(
            "--subjects",
            type=str,
            default="fiction,programming,science,romance,mystery",
            help="Cac the loai cach nhau bo dau phay",
        )
        parser.add_argument(
            "--offset",
            type=int,
            default=0,
            help="Vi tri bat dau (de lay trang tiep theo, thu offset=30, 60...)",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        offset = max(0, options["offset"])
        subjects = [s.strip() for s in options["subjects"].split(",") if s.strip()]
        created_books = 0
        for subject in subjects:
            url = f"https://openlibrary.org/subjects/{subject}.json?limit={limit}&offset={offset}"
            self.stdout.write(f"Fetching: {subject}...")
            try:
                data = fetch_url(url)
            except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
                self.stdout.write(self.style.WARNING(f"  Skip {subject}: {e}"))
                continue
            name = data.get("name") or subject.replace("_", " ").title()
            category, _ = Category.objects.get_or_create(name=name)
            works = data.get("works") or []
            for w in works:
                title = (w.get("title") or "").strip()
                if not title or len(title) > 255:
                    continue
                authors = w.get("authors") or []
                author = (authors[0].get("name") or "Unknown").strip() if authors else "Unknown"
                if len(author) > 255:
                    author = author[:252] + "..."
                cover_id = w.get("cover_id")
                cover_image = get_cover_url(cover_id) if cover_id else ""
                year = w.get("first_publish_year")
                if year and (year < 1000 or year > 2100):
                    year = None
                if Book.objects.filter(title=title, author=author).exists():
                    continue
                price = random.randint(50, 250) * 1000  # 50k - 250k VND
                description = f"Sách hay về {name}. Tác giả: {author}."
                Book.objects.create(
                    title=title,
                    author=author,
                    description=description,
                    price=price,
                    category=category,
                    published_year=year,
                    cover_image=cover_image or "",
                )
                created_books += 1
        self.stdout.write(self.style.SUCCESS(f"Done. Added {created_books} books."))
