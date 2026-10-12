# راهنمای استقرار امن Panel Technamooz روی Railway

## معماری واقعی

این برنامه یک پنل مدیریتی، تولیدکننده‌ی subscription و relay مبتنی بر HTTP/WebSocket/XHTTP است. داخل پروژه binary مستقل Xray/V2Ray وجود ندارد. Railway برای nodeهای خام TCP/UDP عمومی مناسب نیست؛ برای سرویس واقعی Xray، nodeها را روی VPS نگه دارید و این پنل را جداگانه روی Railway اجرا کنید.

## تنظیمات لازم

1. یک سرویس جدید از repository بسازید.
2. یک **Volume** به همان سرویس متصل کنید و Mount Path را `/data` بگذارید.
3. فقط یک replica و یک worker اجرا کنید؛ state و sessionهای فعلی process-local هستند.
4. این Variables را تعریف کنید:

```text
ADMIN_USERNAME=<نام کاربری یکتا>
ADMIN_PASSWORD=<رمز طولانی و تصادفی>
SECRET_KEY=<secret ثابت و طولانی>
ADMIN_RESET_CREDENTIALS=false
DATA_DIR=/data
SECURE_COOKIES=true
RAILWAY_PUBLIC_DOMAIN=<دامنه واقعی بدون https://>
ALLOWED_PUBLIC_HOSTS=<همان دامنه، در صورت داشتن دامنه سفارشی با کاما جدا کنید>
TRUST_PROXY_HEADERS=true
ALLOW_PRIVATE_TARGETS=false
```

`PORT` را دستی override نکنید؛ Railway آن را تزریق می‌کند.

## اگر login با Variables جدید رد شد

فایل state روی Volume، username و password hash قبلی را حفظ می‌کند و به‌صورت عمدی روی مقادیر جدید environment اولویت دارد. برای reset یک‌باره، این متغیر را موقتاً `true` کنید:

```text
ADMIN_RESET_CREDENTIALS=true
```

بعد از یک deploy موفق، با همان `ADMIN_USERNAME` و `ADMIN_PASSWORD` وارد شوید، سپس این متغیر را حذف کنید یا به `false` برگردانید و دوباره deploy کنید. این کار کانفیگ‌ها و subscriptionها را حذف نمی‌کند؛ فقط credential مدیر را جایگزین می‌کند.

## Telegram اختیاری

```text
TELEGRAM_BOT_TOKEN=<توکن ربات>
TELEGRAM_ADMIN_IDS=<شناسه‌ها با کاما>
```

توکن در فایل state ذخیره نمی‌شود و در backup هم export نمی‌شود.

## بررسی پس از deploy

```bash
curl -fsS https://YOUR_DOMAIN/health
```

باید JSON با `status: ok` دریافت شود. سپس login، ساخت یک کانفیگ آزمایشی، restart سرویس و حفظ state را بررسی کنید.

## ریسک‌ها و محدودیت‌ها

- بدون Volume، فایل JSON موقتی است و داده‌ها بعد از restart/redeploy از بین می‌روند.
- اجرای چند replica یا چند worker با state فعلی توصیه نمی‌شود.
- relay عمومی می‌تواند resource-intensive باشد؛ سقف منابع و لاگ‌ها را پایش کنید.
- `ALLOW_PRIVATE_TARGETS` را در production فعال نکنید؛ فعال‌کردن آن می‌تواند SSRF ایجاد کند.
- هیچ تضمینی برای «بن نشدن حساب» وجود ندارد؛ استفاده باید با قوانین Railway، قوانین نود مقصد و قوانین سرویس‌های ثالث سازگار باشد.
