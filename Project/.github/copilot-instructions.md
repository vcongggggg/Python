# Copilot Instructions — Django Bookstore

Tuan theo [./AGENTS.md](AGENTS.md) cho agent roster, quy tac van hanh, va runbook.

## Quick Reference

**Stack:** Django · MySQL · Ollama (local LLM)
**UI language:** Tieng Viet (tat ca string hien thi ra UI)
**Code language:** English (variable names, function names, comments trong code)

## Onboarding Checklist
- Use Python 3.x and a virtual environment (e.g., `.venv`).
- Install dependencies from `requirements.txt`.
- Configure environment variables used in `bookstore/settings.py` (DB, Ollama, DEBUG).
- Run migrations before first run.
- Optional: seed sample data with `python manage.py seed_books`.
 - Verify Ollama is running and model is available before testing chatbot.

## Local Run (Development)
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Environment Variables
- `DEBUG` (True/False)
- `ALLOWED_HOSTS` (comma-separated)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT`, `OLLAMA_MAX_TOKENS`, `OLLAMA_TEMPERATURE`, `OLLAMA_NUM_CTX`

## Scope
- Applies to AI-assisted development for the Django bookstore + Ollama chatbot.
- Use for onboarding and consistent collaboration.

## Agent Roster
1. **Planner**
	- Turns product requirements into an implementation plan.
	- Outputs a task list and identifies risks/dependencies.

2. **Research**
	- Checks docs/specs and existing code patterns before changes.
	- Summarizes findings with links to files and decisions.

3. **Implementation**
	- Makes code changes following project conventions.
	- Keeps edits minimal and testable.

4. **QA / Testing**
	- Defines test strategy (unit/integration/e2e where relevant).
	- Runs tests and reports results with clear reproduction steps.

5. **Security**
	- Reviews input validation, auth, secrets, and data handling.
	- Flags risks and proposes safer alternatives.

6. **UI/UX**
	- Ensures templates and styles match the design direction.
	- Checks responsive behavior and accessibility basics.

## Khi sinh code, luon tuan theo:

1. **Models** — phai co `__str__`, `class Meta`, `verbose_name` tieng Viet
2. **Views** — CBV uu tien, `LoginRequiredMixin` cho protected routes
3. **Templates** — extend `base.html`, dung `{% url %}` va `{% static %}`, khong inline style/script
4. **Ollama calls** — luon co timeout, luon handle `ConnectError`, khong render output bang `|safe`
5. **Khong hardcode** — URL dung `reverse()`, secret dung env var, khong raw SQL

## File layout
- Django apps: `books/`, `bookstore/`
- Templates: `templates/`
- Ollama wrapper: `books/ollama_client.py`
- Settings: `bookstore/settings.py`

## Truoc khi suggest code
- Kiem tra pattern da co trong codebase
- Khong tu y them migration neu chua duoc yeu cau
- Neu thay doi anh huong auth hoac data → hoi truoc
- Neu co thay doi lien quan DB schema, phai neu ro rollback/forward plan

## Test Workflow
- Unit: `python manage.py test`
- Khi them route API, test duong dan va status code.
- Neu co thay doi logic quan trong, dua ra buoc test thu cong ro rang.
- Moi khi hoan thanh chuc nang moi, phai viet test va chay test.

## Review Checklist
- Khong hardcode secret, token, URL noi bo.
- Xu ly loi ro rang (message than thien voi UI, log chi tiet ben server).
- Kiem tra input boundary (form, query, JSON body).
- Khong dung raw SQL; su dung ORM va filter an toan.
- Cap nhat template co su dung `url` va `static` dung quy dinh.

## API Conventions
- Khong dung Django REST Framework.
- Su dung `JsonResponse` va status code dung nguyen tac HTTP.
- Tra ve thong tin loi ro rang, khong leak stacktrace cho client.
- Giu format phan hoi nhat quan theo pattern hien co trong `books/views.py`.

## Logging & Error Handling
- Log phia server du thong tin (context, error type, request id neu co).
- Khong log thong tin nhay cam (password, token, PII).
- UI chi hien thong bao than thien; chi tiet loi de trong log.

## Database & Migrations
- Khong sua migration cu; tao migration moi neu can.
- Neu thay doi schema, can cap nhat fixtures/seed neu co.
- Tranh query nang trong template; dua logic vao view.

## Performance
- Tranh N+1: dung `select_related`/`prefetch_related` khi can.
- Gioi han so luong record va pagination khi tra ve danh sach.
- Gioi han context length/tokens khi goi Ollama.

## Git Workflow
- Khong sua file khong lien quan.
- Khong reformat toan bo file neu khong can.
- Neu tao commit, dung format: `type: mo ta` (feat/fix/refactor/docs/test/chore/perf/ci).

## CI/CD Checklist (GitHub Actions)
- Chay test truoc khi merge (`python manage.py test`).
- Kiem tra lint/format neu pipeline co bat.
- Neu thay doi env vars, cap nhat docs va secrets trong repo.
- Neu thay doi Dockerfile/compose, xac nhan build thanh cong.
- Khong dua secrets vao log hoac artifact.

## Deployment Rules (Docker/Gunicorn/Nginx)
- Docker image phai cai dependencies tu `requirements.txt`.
- Gunicorn phai bind dung port va set worker hop ly.
- Nginx (neu co) can proxy dung `/` va static files.
- Khong dung `DEBUG=True` tren production.
- Dam bao `ALLOWED_HOSTS` va DB settings phu hop moi truong.

## Security Checklist (API/LLM)
- Validate input (query, form, JSON) truoc khi xu ly.
- Sanitize/escape output neu co noi dung nguoi dung nhap.
- Khong log noi dung nhay cam hoac PII.
- Rate limit cho endpoints nhay cam neu can.
- LLM prompt phai co guardrails, khong leak secret.
- LLM output khong duoc render bang `|safe`.

## Operating Rules
- Prefer small, reviewable changes over large refactors.
- Avoid destructive commands (e.g., hard reset) unless explicitly approved.
- Do not modify production data or credentials.
- Validate user input at system boundaries.
- Keep prompts and outputs in Vietnamese where the UI is Vietnamese.

## Runbook (Typical Flow)
1. **Planner** creates a plan and identifies files to touch.
2. **Research** checks docs and existing code paths.
3. **Implementation** applies changes and updates templates/views as needed.
4. **QA / Testing** runs tests or provides manual test steps.
5. **Security** reviews any changes involving user input, auth, or external calls.

## File Conventions
- Django code in `books/` and `bookstore/`.
- Templates under `templates/`.
- Static assets under `static/`.
- Ollama settings live in `bookstore/settings.py`.

## Output Expectations
- Provide concise change summaries.
- Include file references and line ranges when applicable.
- Offer test commands or verification steps.

## Escalation
- If requirements are unclear, ask for clarification before coding.
- If a change impacts data or security, request approval first.
