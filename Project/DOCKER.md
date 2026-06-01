# Huong dan chay bang Docker

Stack Docker dev gom:

- `web`: Django development server
- `db`: PostgreSQL 16
- `ollama`: Ollama local server
- `ollama-pull`: tu dong tai model `qwen2.5:3b` vao Docker volume

Lan dau chay co the mat lau vi Docker phai tai image va model Ollama.

## Chay toan bo stack

Tu thu muc `Project`:

```powershell
docker compose up --build
```

Mo web tai:

```text
http://127.0.0.1:8000/
```

## Dung stack

```powershell
docker compose down
```

Lenh nay khong xoa database PostgreSQL va model Ollama vi data dang nam trong Docker volumes.

## Xoa sach data Docker neu can lam lai tu dau

```powershell
docker compose down -v
```

## Chay command Django trong container

```powershell
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_books --limit 20
docker compose exec web python manage.py normalize_categories
```

## Luu y ve database

Khi chay Docker, project dung PostgreSQL trong service `db`, khac voi file SQLite local `db.sqlite3`.
Vi vay du lieu local hien co se khong tu dong xuat hien trong Docker. Neu can demo nhanh voi du lieu mau,
hay chay seed trong container sau khi stack da bat.

## Luu y ve chatbot

Trong Docker, Django goi Ollama qua:

```env
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=qwen2.5:3b
```

Model `qwen2.5:3b` du nhe cho chatbot cua web. Neu muon dung model nang hon, sua `OLLAMA_MODEL`
trong `docker-compose.yml` va doi command cua service `ollama-pull`.
