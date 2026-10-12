# Panel Technamooz v1.0.0.0 Stable

نسخهٔ stable اختصاصی Technamooz با کپچای سروری، username/password، تغییر credential، localization دو‌زبانه، تم‌های dark/light، لوگوی رسمی، مرکز کنترل ربات Telegram و تنظیمات Railway آماده شد.

## Railway-ready hardening — 2026-10-11
- secure cookie قابل تنظیم با پشتیبانی از HTTPS پشت reverse proxy.
- هدرهای امنیتی مرورگر و flush/fsync برای state file.
- hashهای جدید رمز عبور با bcrypt با حفظ سازگاری PBKDF2 قدیمی.
- `.python-version`، `.env.example`، `.gitignore` و تست‌های واحد.
- مستندسازی Volume، single-worker و محدودیت TCP/UDP Railway.

## Single-container Xray Core — 2026-10-12

- اضافه‌شدن `xray_manager.py` برای تولید، validation، اجرا، reload و shutdown واقعی Xray Core.
- اضافه‌شدن Dockerfile با Xray Core نسخه pin شده `1.8.24`.
- اجرای Xray روی loopback و نگه‌داشتن Railway `PORT` برای FastAPI.
- bridge داخلی WebSocket برای VLESS و Trojan.
- همگام‌سازی خودکار تغییرات کانفیگ با Xray.
- endpointهای احراز‌شدهٔ `/api/xray/status` و `/api/xray/reload`.
- تست واقعی binary Xray و اعتبارسنجی config موفق شد.
- تست process start/stop و تست واحد تولید کانفیگ اضافه شد.

## Deep audit and ping fix — 2026-10-12

در تست end-to-end واقعی مشخص شد که routeهای WebSocket wrapper بدون type annotation صحیح FastAPI ممکن است با 403 رد شوند. annotation صحیح `WebSocket` اضافه شد و مسیر VLESS از کلاینت Xray تا اینترنت با موفقیت تست شد. همچنین reload مبتنی بر SIGHUP حذف و با restart کنترل‌شده جایگزین شد؛ watcher دیگر بلافاصله بعد از startup هسته را reload نمی‌کند و در صورت crash آن را recover می‌کند. credentialهای hardcode شده از login و settings frontend حذف شدند. کانفیگ‌های منقضی از inbound Xray حذف می‌شوند و کانفیگ‌هایی که quota، IP limit یا speed limit دارند از bridge مستقیم Xray عبور نمی‌کنند و به relay policy-aware قبلی سپرده می‌شوند.
