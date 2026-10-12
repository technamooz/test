# Panel Technamooz `v1.0.0.0` <span style="color:#10b981;font-weight:bold;font-size:0.7em;">STABLE</span>

> پنل فوق‌حرفه‌ای و یکپارچه ساخت، توزیع و مدیریت کانفیگ‌های ابری VPN بر پایهٔ پایتون و FastAPI  
> توسعه‌یافته توسط **تیم Technamooz** با مدیریت **amirparsa**  
> نسخه: `technamooz-version-1.0.0.0 stable`

---

## 🌟 معرفی پروژه (Overview)
**Panel Technamooz** یک سیستم مدرن، پرسرعت و کم‌مصرف برای ساخت و کنترل ترافیک کانفیگ‌های امن ضد فیلترینگ است که به صورت ۱۰۰٪ به زبان **Python** و با فریم‌ورک قدرتمند **FastAPI** توسعه داده شده است. این نسخه برای استقرار پایدار و مقیاس‌پذیر بر روی سرورهای ابری و به‌ویژه پلتفرم **Railway** بهینه‌سازی شده است.

---

## 🚀 قابلیت‌های کلیدی نسخه Ultra 3.0 Stable

### 🛡️ پروتکل‌های پشتیبانی‌شده
- **VLESS WebSocket (WS)** با پشتیبانی از TLS / Reality
- **Trojan WebSocket (WS)** با احراز هویت SHA-224 و بازپخش مستقیم به هسته
- **XHTTP Packet-Up** (فناوری عبور از شدیدترین محدودیت‌ها)
- **XHTTP Stream-Up** با مدیریت بهینه جریان داده و مالتی‌پلکسینگ

### 📡 فرمت‌های اشتراک نوین و هوشمند
- **Clash Meta / Mihomo (YAML)**: خروجی کامل و استاندارد پروکسی با Ruleها و تنظیمات DNS
- **Sing-box (JSON)**: سازگار با نسخه 1.8+ برای کلاینت‌های Android، iOS، Windows و Linux
- **V2Ray / Xray URI**: لینک‌های استاندارد سازگار با v2rayNG, Streisand, FoXray, Nekobox, Shadowrocket
- **صفحات سابسکریپشن وب**: پنل عمومی زیبا برای هر مشترک با QR Code و نمایش حجم/انقضا

### 🎯 مسیریابی با آی‌پی تمیز (Clean IP / CDN Domain)
- پشتیبانی مستقیم از درج Clean IP مخصوص اپراتورهای ایرانسل، همراه‌اول، رایتل و مخابرات
- امکان تعیین دامنه CDN مجزا برای Host و SNI به منظور دور زدن مسدودسازی‌های SNI-based

### 🎨 رابط کاربری گلاسمورفیسم نوین (Glassmorphism UI/UX)
- **دو زبانه کامل**: انگلیسی (پیش‌فرض) و فارسی با سوئیچ آنی بدون رفرش
- **دو تم رنگی اختصاصی**:
  - **تم تاریک (Dark Mode)**: مشکی متالیک و قرمز آتشین (`#07070a` + `#ef233c`)
  - **تم روشن (Light Mode)**: سفید ابریشمی، بنفش نئونی و قرمز (`#f8fafc` + `#7209b7` + `#ef233c`)
- **لوگوی اختصاصی Technamooz**: تعبیه‌شده به‌صورت وکتور و پایدار در تمام صفحات
- **ویترین شبکه‌های اجتماعی تکناموز**: دسترسی ۱-کلیک به یوتیوب، تلگرام، اینستاگرام، توییتر، گیت‌هاب، وبسایت رسمی و پشتیبانی

### ⚙️ امنیت و کنترل ترافیک سازمانی
- **محدودیت تعداد کاربر همزمان (IP Limiter)**: جلوگیری از اشتراک‌گذاری اکانت‌ها با TTL دقیق
- **محدودکننده نرخ سرعت (Token Bucket Limiter)**: اعمال سقف پهنای باند بر حسب مگابیت (Mbps)
- **تمدید ۱-کلیک (+۳۰ روز)** و **ریست ترافیک مصرفی**
- **ورود دو مرحله‌ای با کد امنیتی (CAPTCHA)** جهت محافظت در برابر حملات Brute-Force
- **امکان تغییر نام کاربری و رمز عبور** از درون پنل با bcrypt؛ hashهای قدیمی PBKDF2 نیز برای سازگاری پذیرفته می‌شوند

### 🤖 ربات تلگرام پیشرفته Technamooz
- نظارت لحظه‌ای بر سلامت سرور، مصرف پردازنده، رم و ترافیک (`/status`)
- ساخت و صدور سریع کانفیگ‌های VLESS و Trojan
- ارسال لینک‌های مستقیم اشتراک Clash و Sing-box به کاربران
- دستورات تمدید و ریست اکانت برای ادمین

---

## 🔑 مشخصات ورود (Credentials)

- **نام کاربری**: از `ADMIN_USERNAME` خوانده می‌شود؛ مقدار پیش‌فرض فقط برای توسعه‌ی محلی است.
- **رمز عبور**: در production فقط از `ADMIN_PASSWORD` خوانده می‌شود و مقدار پیش‌فرض ناامن مجاز نیست.
- **کد امنیتی (کپچا)**: کد تصادفی ۵ رقمی نمایش داده‌شده در صفحه

*(پس از ورود می‌توانید از منوی تنظیمات نام کاربری و رمز عبور را تغییر دهید.)*

---

## ☁️ راهنمای استقرار روی Railway (Deployment Guide)

این پروژه دارای فایل‌های استاندارد `railway.json` و `Procfile` است و برای اجرای مستقیم روی Railway طراحی شده است.

### مراحل نصب:
1. مخزن گیت‌هاب پروژه را در حساب Railway خود **Import** کنید:
   ```
   https://github.com/technamooz/Panel_Technamooz_VPN
   ```
2. در تنظیمات سرویس Railway، یک **Volume** ایجاد کرده و مسیر Mount آن را برابر با `/data` قرار دهید (جهت ذخیره دائمی دیتابیس کانفیگ‌ها و ساب‌ها).
3. متغیرهای محیطی (Environment Variables):
   - `ADMIN_USERNAME`: نام کاربری ادمین (پیش‌فرض: `Amirparsa`)
   - `ADMIN_PASSWORD`: رمز عبور ادمین (در محیط production الزامی و بدون مقدار پیش‌فرض امن)
   - `DATA_DIR`: مسیر ذخیره داده‌ها (پیش‌فرض: `/data` در Railway و `./data` در محیط محلی)
   - `TELEGRAM_BOT_TOKEN`: توکن ربات تلگرام (اختیاری)
   - `TELEGRAM_ADMIN_IDS`: شناسه‌های عددی تلگرام ادمین‌ها با کاما (اختیاری)
   - `SECRET_KEY`: secret ثابت و طولانی برای سازگاری restart (الزامی در production)
   - `SECURE_COOKIES=true`: cookie امن برای HTTPS
   - `TRUST_PROXY_HEADERS=true`: فقط هنگام عبور درخواست‌ها از proxy مورد اعتماد Railway
4. پلتفرم Railway به صورت خودکار متغیر `PORT` را تزریق کرده و سرویس از طریق دستور زیر راه‌اندازی می‌شود:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. هلث‌چک پروژه روی آدرس `/health` به صورت فعال نظارت می‌کند.

### الزامات امنیتی نسخهٔ hardened

- در محیط Railway، متغیر `ADMIN_PASSWORD` اجباری است و برنامه بدون آن اجرا نمی‌شود؛ رمز توسعهٔ `Technamooz` فقط برای اجرای محلی است.
- برای تولید URL صحیح، `RAILWAY_PUBLIC_DOMAIN` یا `ALLOWED_PUBLIC_HOSTS` را تنظیم کنید. مقدار `TRUST_PROXY_HEADERS` فقط زمانی فعال شود که برنامه پشت reverse proxy مورد اعتماد است.
- CORS به‌صورت پیش‌فرض غیرفعال است؛ در صورت نیاز، originهای دقیق را در `CORS_ORIGINS` با کاما جدا کنید و از wildcard استفاده نکنید.
- relay به مقصدهای private/loopback/link-local متصل نمی‌شود. فقط در شبکهٔ کاملاً کنترل‌شده و با آگاهی از ریسک، `ALLOW_PRIVATE_TARGETS=true` را فعال کنید.
- اجرای چند replica یا چند worker با state فعلی پشتیبانی نمی‌شود؛ یک replica و یک worker اجرا کنید.
- راهنمای کامل در [`RAILWAY_DEPLOYMENT_FA.md`](RAILWAY_DEPLOYMENT_FA.md) قرار دارد.

---

## 💻 راه‌اندازی محلی (Local Development)

```bash
# کلون پروژه
git clone https://github.com/technamooz/Panel_Technamooz_VPN.git
cd Panel_Technamooz_VPN

# ساخت و فعال‌سازی محیط مجازی
python3 -m venv venv
source venv/bin/activate  # در ویندوز: venv\Scripts\activate

# نصب پیش‌نیازها
pip install -r requirements.txt

# اجرای سرور
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

سپس مرورگر خود را باز کرده و به آدرس زیر مراجعه نمایید:
```
http://localhost:8000/login
```

---

## 🌐 شبکه‌های اجتماعی و جامعه کاربری Technamooz

- 📺 **YouTube**: [@technamooz](https://youtube.com/@technamooz)
- 📢 **Telegram Channel**: [@technamooz](https://t.me/technamooz)
- 📸 **Instagram**: [@technamooz](https://instagram.com/technamooz)
- 🐦 **Twitter / X**: [@technamooz](https://twitter.com/technamooz)
- 🐙 **GitHub**: [github.com/technamooz](https://github.com/technamooz)
- 🌍 **Official Website**: [technamooz.ir](https://technamooz.ir)
- 💬 **Telegram Support**: [@technamooz_support](https://t.me/technamooz_support)

---

## 📄 لایسنس و حقوق نشر
این پروژه تحت لایسنس MIT منتشر شده است.  
توسعه‌یافته با افتخار توسط **تیم Technamooz** با مدیریت **amirparsa**.


## Managed Xray Core — Single Container

این نسخه علاوه بر relay سازگار قبلی، یک **Xray Core واقعی** را داخل همان Container اجرا می‌کند. FastAPI تنها پردازشی است که روی `PORT` عمومی Railway گوش می‌دهد و Xray روی loopback اجرا می‌شود؛ bridge داخلی WebSocket ترافیک VLESS/Trojan را به inboundهای Xray منتقل می‌کند.

### رفتار عملیاتی

- کانفیگ Xray در `/data/xray-config.json` به‌صورت atomic نوشته می‌شود.
- فقط کاربران فعال و منقضی‌نشده وارد inboundهای Xray می‌شوند.
- تغییرات CRUD حداکثر بعد از `XRAY_RELOAD_INTERVAL` ثانیه با Xray همگام می‌شوند.
- `GET /api/xray/status` وضعیت Core را نشان می‌دهد.
- `POST /api/xray/reload` برای reload دستی مدیر است.
- اگر binary یا validation در محیط محلی موجود نباشد، برنامه بالا می‌آید و relay سازگار قبلی fallback می‌شود؛ در Docker production، binary توسط Dockerfile نصب می‌شود.

### استقرار Docker روی Railway

وجود `Dockerfile` باعث می‌شود Railway از image production پروژه استفاده کند. در سرویس Railway:

1. یک Volume با mount path `/data` بسازید.
2. `ADMIN_PASSWORD` و `SECRET_KEY` را مقداردهی کنید.
3. `XRAY_ENABLED=true` را تنظیم کنید.
4. دامنه‌ی عمومی را در `RAILWAY_PUBLIC_DOMAIN` قرار دهید.
5. Deploy را اجرا کنید و در لاگ‌ها پیام `Xray Core started` را بررسی کنید.
6. ابتدا `/health` و سپس بعد از ورود `/api/xray/status` را بررسی کنید.

### محدودیت شبکه Railway

همان‌طور که در معماری Railway آمده است، این پیاده‌سازی برای VLESS/Trojan روی WebSocket و XHTTPهای HTTP-compatible مناسب است. اجرای UDP عمومی، WireGuard، TUIC، Hysteria2 و پورت‌های TCP خام به قابلیت شبکه‌ی سرویس Railway و TCP Proxy وابسته است و از داخل کد قابل تضمین نیست. پنل وضعیت `running` هسته را صادقانه نشان می‌دهد و عدد ping ساختگی تولید نمی‌کند.
