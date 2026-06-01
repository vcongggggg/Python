# Bookie Project Status And Web Test Plan

## 1. Project Scope

Bookie is a Django bookstore web application. The active source code lives in `Project/`.

Main goal: provide a usable online bookstore experience with catalog browsing, cart/checkout, orders, user profile, admin dashboard, light AI assistance, and optional digital reading.

Current source layout:

- `Project/books/`: main app, models, views, URLs, forms, chatbot, tests, seed commands.
- `Project/bookstore/`: Django settings and root URL config.
- `Project/templates/`: HTML pages.
- `Project/static/`: CSS, JavaScript, and images.
- `Project/.env.example`: safe environment template.
- `Project/requirements.txt`: Python dependencies.

## 2. Main Data Models

- `Category`: book categories.
- `Book`: catalog item, stock, price, cover URL, digital book fields.
- `ReadingProgress`: per-user digital reading progress.
- `Wishlist`: user saved books.
- `Coupon`: discount code with validity rules.
- `Order`: checkout/order lifecycle and payment method.
- `OrderItem`: books purchased in an order, including digital-purchase flag.
- `Rating`: user rating and review.
- `AdminAuditLog`: staff/admin actions.

## 3. Current Features

### Public/User Features

- Home page with featured/popular/recommended book sections.
- Book listing with search, category filter, and sorting.
- Book detail page with description, stock state, ratings, related books, and wishlist/cart actions.
- Category list and category detail pages.
- User registration, login, logout.
- Cart add/update/remove.
- Checkout with shipping address, note, coupon, and payment method.
- Order list and order detail.
- Order cancellation while pending/confirmed.
- PDF invoice download for owned orders.
- Wishlist page and AJAX wishlist add/remove.
- Profile page and profile edit.
- Reading DNA page with stats, charts, milestones, and recommendations.
- Digital reader with preview/full access and reading-progress save.
- About and contact pages.

### Commerce/Admin Features

- Coupon validation endpoint.
- Mock payment confirmation.
- VNPay return/callback path and VNPay helper module.
- Admin dashboard summary: revenue, orders, users, books, charts/lists.
- Staff dashboard pages for users, books, coupons, orders, audit logs.
- CSV exports for books and orders.
- Order status update API for staff with permission.
- RBAC seed command for default staff groups.

### AI/Chatbot Features

The chatbot is intentionally kept "good enough" and not treated as the core system.

- Ollama-backed chatbot endpoint.
- Streaming chatbot endpoint.
- Database-grounded book lookup before model response.
- Order lookup / recommendation actions through chatbot response handling.
- Rate limit on chatbot sync and stream endpoints.
- Fallback response when the model fails.

## 4. Setup And Run

From repository root:

```powershell
cd Project
copy .env.example .env
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_books --limit 50
python manage.py seed_demo_user
python manage.py seed_rbac
python manage.py runserver
```

Useful demo account:

- Username: `demo`
- Password: `demo123`

Optional digital books:

```powershell
python manage.py seed_reader_content
```

Run commands from repository root if preferred:

```powershell
python Project\manage.py check
python Project\manage.py test books
python Project\manage.py runserver
```

## 5. Automated Test Status

Current automated test command:

```powershell
python Project\manage.py test books
```

Current baseline: `12 tests OK`.

Covered by automated tests:

- Home page loads.
- Book detail page loads.
- Digital reader loads for a free digital book.
- Reading progress API saves page/finished state.
- Non-digital books redirect away from reader.
- Paid digital books show preview before purchase and full access after digital purchase.
- Digital checkout marks `OrderItem.is_digital_purchase` and does not reduce stock.
- Dashboard route names reverse successfully.
- Reading DNA supplies chart data and insight context.
- Order detail links invoice PDF.
- Invoice PDF download requires owner and returns valid PDF response.
- Chatbot sync endpoint rate limits repeated requests.
- Chatbot stream endpoint shares chatbot rate limit.

Not fully covered yet:

- Full browser UI rendering and responsive visual checks.
- AJAX wishlist/cart DOM updates.
- Coupon edge cases such as expired/max-used coupons.
- Staff permission matrix for all dashboard actions.
- VNPay checksum success/failure paths.
- Real Ollama integration behavior.
- PDF visual layout quality.

## 6. Manual Web Test Checklist

Use this checklist after starting the server at `http://127.0.0.1:8000/`.

### Smoke Navigation

- Open `/`.
- Confirm header/nav render without broken layout.
- Click `Books`, `Categories`, `About`, `Contact`.
- Search from the header and confirm suggestions/results appear.
- Resize browser to mobile width and check nav/chatbot do not overlap core content.

### Catalog And Book Detail

- Open `/books/`.
- Test search by book title and author.
- Test category filter.
- Test sort options.
- Open a book detail page.
- Confirm cover/placeholder, price, stock, rating area, related books, and CTA buttons render.
- Try out-of-stock book if available and confirm add-to-cart is disabled or blocked.

### Cart And Checkout

- Add a physical book to cart.
- Update quantity in `/cart/`.
- Remove item from cart.
- Add a digital book to cart and confirm quantity stays `1`.
- Checkout as logged-in user.
- Enter shipping address and COD payment.
- Confirm order is created and cart clears.
- Confirm physical stock decreases after physical checkout.
- Confirm digital checkout does not decrease stock.

### Coupons

- Create a coupon in admin/dashboard or Django admin.
- Apply valid coupon during checkout.
- Try invalid coupon code and confirm friendly error.
- Try coupon below minimum order if configured.
- Confirm order total reflects discount.

### Orders And Invoice

- Open `/orders/`.
- Open an order detail page.
- Confirm status timeline, items, address, totals.
- Download invoice PDF.
- Confirm browser downloads/opens a PDF.
- Try accessing another user's invoice URL and confirm access is denied.
- Cancel a pending/confirmed order and confirm stock is restored for physical items.

### Payment

- Checkout with Momo mock.
- Confirm payment page renders QR/mock instructions.
- Click confirm payment and verify order status becomes confirmed.
- Checkout with VNPay sandbox only if env vars are configured.
- Test VNPay failure/success callback separately when sandbox credentials are valid.

### Wishlist

- Add a book to wishlist from detail/list if button exists.
- Confirm wishlist badge/count changes.
- Open `/wishlist/`.
- Remove item and confirm it disappears.
- Confirm unauthenticated wishlist actions redirect or show login requirement.

### Ratings And Sentiment

- Open a purchased/read book if rating is allowed by current UI.
- Submit a 1-5 star rating and comment.
- Confirm rating displays on book detail.
- Confirm sentiment summary percentages do not break layout.

### Profile And Reading DNA

- Open `/profile/`.
- Edit first name, last name, email.
- Open `/profile/reading-dna/`.
- Confirm stats cards render.
- Confirm radar and trend charts render.
- Confirm milestones/recommendations render if enough data exists.
- Confirm empty-state renders for a new user with no orders/ratings.

### Digital Reader

- Open a digital book detail page.
- Click read/reader button.
- For a free digital book, confirm full content opens.
- For a paid digital book before purchase, confirm preview mode.
- Purchase digital format and confirm full reader access.
- Use next/previous page buttons.
- Refresh reader and confirm progress resumes.
- Confirm font-size slider and theme button work.
- Confirm "Ask AI" opens/sends page context without breaking reader.

### Chatbot

- Open chatbot bubble.
- Ask for a broad recommendation, e.g. "goi y sach lap trinh".
- Confirm response is friendly and does not invent irrelevant products too aggressively.
- Ask for order status while logged out and logged in.
- Confirm fallback message appears if Ollama is unavailable.
- Send many requests quickly and confirm rate limit message appears.
- Check chatbot does not cover critical mobile controls.

### Admin Dashboard

- Create staff/admin user or assign groups with `seed_rbac`.
- Open `/dashboard/`.
- Confirm staff-only access.
- Check dashboard stats and charts.
- Open user, book, coupon, order, audit pages.
- Test book create/edit/delete with correct permission.
- Test coupon create/edit/delete with correct permission.
- Test order status update.
- Export orders CSV.
- Export books CSV.
- Confirm audit logs are recorded for admin actions.

## 7. UX/UI Review Notes

Current strengths:

- Rich visual identity with Midnight Cosmic styling.
- Main flows are discoverable: catalog, detail, cart, checkout, orders.
- Dashboard covers core admin operations.
- Reader mode is present and test-covered.
- Chatbot is present but scoped as helper, not the main product.

Known improvement areas:

- Many templates still use inline styles, making consistency harder to maintain.
- Some Vietnamese text appears without full accents in admin/dashboard areas.
- Chatbot frontend renders limited HTML formatting and should avoid unsafe text rendering patterns.
- Some AJAX flows need browser-level tests, not only Django unit tests.
- Payment sandbox should be tested with real sandbox credentials before demo.
- PDF invoice is functional but visually simple.

## 8. Code Quality Notes

Current good points:

- `.env` is ignored; `.env.example` is committed.
- Root duplicate Django tree was removed; `Project/` is the source of truth.
- Test database uses SQLite automatically for tests.
- Core hardening checks pass with `python Project\manage.py check`.
- Feature work has been committed on separate branches and merged after tests pass.

Known code smells/risk areas:

- `Project/books/views.py` is large and should eventually be split by domain.
- A legacy `api_chatbot_sync_unused` function remains and can be removed in a cleanup commit.
- Some endpoints use `csrf_exempt`; review whether frontend can use normal CSRF protection.
- Broad `except Exception` blocks should be narrowed where possible.
- Dashboard permission tests should be expanded.

## 9. Recommended Next Work

Do not add major new features until these are improved:

1. Add tests for coupon validity and checkout totals.
2. Add tests for dashboard permissions and admin actions.
3. Remove dead chatbot fallback code.
4. Harden chatbot frontend rendering.
5. Review CSRF exemptions and remove unnecessary ones.
6. Polish key templates for mobile layout and text consistency.
7. Run a manual browser pass through the checklist above.

