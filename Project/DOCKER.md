# Huong dan chay bang Docker

Stack Docker dev mac dinh gom:

- `web`: Django development server
- `db`: PostgreSQL 16

Chatbot dung Ollama dang chay tren may Windows cua ban qua `host.docker.internal`.
Cach nay tranh viec Docker tai lai image Ollama va model, tiet kiem nhieu dung luong o C.

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

Truoc khi chay chatbot, dam bao Ollama tren Windows dang co model:

```powershell
ollama list
```

Neu chua co model nhe mac dinh:

```powershell
ollama pull qwen2.5:3b
```

Trong Docker, Django goi Ollama tren host qua:

```env
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=qwen2.5:3b
```

Model `qwen2.5:3b` du nhe cho chatbot cua web. Neu muon dung model nang hon, sua `OLLAMA_MODEL`
trong `docker-compose.yml`.

## Neu o C bi day do Docker

Dung lenh dang pull truoc bang `Ctrl + C`, sau do chay:

```powershell
docker compose down --remove-orphans
docker system prune
```

Lenh prune se xoa image/container/build cache Docker khong con dung. Khong xoa source code project.
Neu muon chuyen toan bo Docker Desktop sang o D, vao Docker Desktop Settings va doi vi tri disk image/WSL data
sang o D, hoac dung tinh nang move disk image neu Docker Desktop cua ban co ho tro.
