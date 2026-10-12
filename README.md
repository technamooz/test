# Technamooz Control Plane v2.1 Premium

پنل مدیریتی ماژولار V2Ray برای Railway با FastAPI، frontend مستقل RTL، state پایدار روی Volume و API تفکیک‌شده.

## گزارش شناخت نسخه‌ی فعلی

این پروژه پنل مدیریت و تولید URI است، نه binary مستقل Xray/V2Ray. داده‌ها شامل credential مدیر و کانفیگ‌ها در state store ذخیره می‌شوند. Railway فقط HTTP/HTTPS عمومی می‌دهد؛ اجرای node خام TCP/UDP باید روی VPS یا سرویس شبکه‌ای جدا باشد.

## ساختار

```text
app/main.py                 composition root, lifespan, security headers
app/api/router.py           HTTP endpoints and backward-compatible API
app/api/schemas.py          strict Pydantic request models
app/api/deps.py             auth, proxy-aware client IP, same-origin guard
app/core/config.py          fail-fast environment settings
app/core/security.py        bcrypt, session expiry
app/core/rate_limit.py      login sliding-window limiter
app/core/store.py           atomic Volume persistence and CRUD
app/core/logging.py         stdout logging
app/services/config_manager.py domain CRUD service
app/services/configs.py     URI and Base64 subscription domain service
frontend/                   responsive RTL Premium dashboard
tests/                      API and regression tests
```

## Local run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD='change-this-password'
export SECRET_KEY='long-random-secret'
export DATA_DIR=./data
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Health:

```text
GET /health
GET /api/health
```

## Railway deployment

1. Repository را به Railway متصل کنید.
2. یک Volume با mount path `/data` بسازید.
3. Variables زیر را تنظیم کنید؛ `PORT` را دستی نسازید:

```text
ADMIN_USERNAME=<unique username>
ADMIN_PASSWORD=<long random password>
SECRET_KEY=<long stable secret>
DATA_DIR=/data
RAILWAY_PUBLIC_DOMAIN=<domain without https://>
ALLOWED_PUBLIC_HOSTS=<same domain>
TRUST_PROXY_HEADERS=true
SECURE_COOKIES=true
LOG_LEVEL=INFO
```

Healthcheck روی `/health` تنظیم شده است. یک replica و یک worker استفاده کنید؛ sessionها و state فعلی process-local/file-based هستند. برای scale افقی، adapter رسمی PostgreSQL/Redis باید اضافه شود.

## تست

```bash
python -m compileall -q app tests
python -m unittest discover -s tests -v
```

## محدودیت‌های شفاف

- این نسخه برای پنل و generator آماده است و Xray binary را روی Railway اجرا نمی‌کند.
- relay کامل، Telegram Bot و خروجی Clash/Sing-box نسخه‌ی stable قبلی هنوز در این شاخه‌ی بازطراحی‌شده migrate نشده‌اند؛ نسخه‌ی stable قبلی را تا پایان migration حذف نکنید.
- state روی Volume پایدار است، اما برای چند replica کافی نیست؛ PostgreSQL + Redis فاز بعدی production scale است.
