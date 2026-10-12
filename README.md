# Technamooz Control Plane v2

پنل جدید modular برای Railway با FastAPI backend، frontend مستقل RTL و state store اتمیک روی Volume.

## اجرا

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD='change-this-password'
export SECRET_KEY='long-random-secret'
export DATA_DIR=./data
uvicorn app.main:app --reload --port 8000
```

## Railway

- Volume را روی `/data` mount کنید.
- `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `SECRET_KEY` را تنظیم کنید.
- `PORT` را دستی تنظیم نکنید.
- healthcheck: `/api/health`
- یک replica و یک worker استفاده کنید تا PostgreSQL adapter اضافه شود.

## معماری

```text
app/main.py                 composition root
app/api/router.py           version-one HTTP API
app/core/config.py          environment configuration
app/core/security.py        bcrypt and sessions
app/core/store.py           atomic persistent state + legacy state compatibility
app/services/configs.py     protocol URI and subscription domain service
frontend/                   independent RTL dashboard
```

نسخه‌ی فعلی عمداً کنار نسخه‌ی stable قبلی ساخته شده است. migration از `technamooz_state.json` به‌صورت backward-compatible انجام می‌شود و حذف داده ندارد.
