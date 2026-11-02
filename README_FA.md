<div dir="rtl">

# پروژه تکناموز (Project Technamooz)

### قدرتمندترین دروازه بدون سرور روی Cloudflare Workers

**تکناموز** (به معنای *پتکناموز/مخفی*) یک پروکسی معکوس امن، سبک و قابل سفارشی‌سازی است که به طور کامل روی Edge اجرا می‌شود. این پروژه Worker کلودفلر شما را به یک دروازه قدرتمند و مبهم با پشتیبانی از پروتکل‌های **VLESS** و **Trojan** تبدیل می‌کند که از طریق یک داشبورد زیبا و خودکفا مدیریت می‌شود.

[![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white)](https://workers.cloudflare.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](./LICENSE)
[![JavaScript](https://img.shields.io/badge/JavaScript-100%25-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://github.com/technamooz/technamooz/blob/main/_worker.js)

> 🌐 [English Version / نسخه انگلیسی](./README.md)

---

## 📖 فهرست مطالب

- [چرا تکناموز؟](#-چرا-تکناموز)
- [ویژگی‌های کلیدی](#-ویژگیهای-کلیدی)
- [پیش‌نیازها](#-پیشنیازها)
- [گزینه‌های نصب سریع](#-گزینههای-نصب-سریع)
- [راهنمای نصب گام‌به‌گام](#-راهنمای-نصب-گامبهگام)
- [راهنمای داشبورد](#-راهنمای-داشبورد)
- [تنظیمات پیشرفته](#-تنظیمات-پیشرفته)
- [منابع مفید](#-منابع-مفید)
- [ذخیره تغییرات](#-ذخیره-تغییرات)
- [سوالات متداول و رفع اشکال](#-سوالات-متداول-و-رفع-اشکال)
- [مشارکت در پروژه](#-مشارکت-در-پروژه)
- [مجوز](#-مجوز)

---

## 🌟 چرا تکناموز؟

تکناموز فقط یک اسکریپت پروکسی نیست — یک راه‌حل مدیریت کامل است که برای **مخفی‌کاری**، **سرعت** و **سادگی** طراحی شده.

- 🛡️ **پتکناموز در دید عموم:** درخواست‌های غیرمجاز به طور خودکار به سایت‌های معتبر (مثل `ubuntu.com` یا `docker.com`) هدایت می‌شوند.
- ⚡ **بدون هزینه سرور:** کاملاً روی پلن رایگان Cloudflare اجرا می‌شود.
- 🎨 **داشبورد مدرن:** رابط کاربری واکنش‌گرا با پشتیبانی از حالت تاریک/روشن و دو زبانه (انگلیسی/فارسی).
- 🤖 **ربات تلگرام:** مدیریت دروازه، بررسی مصرف و دریافت هشدارهای ورود.
- 📡 **چند کاربر و چند IP:** لینک اشتراک اختصاصی + ترکیب با لیست IP پاک.
- 💾 **ذخیره‌سازی D1 SQLite:** تنظیمات در دیتابیس Cloudflare D1 ذخیره می‌شوند.

---

## ✨ ویژگی‌های کلیدی

| ویژگی | توضیح |
|---|---|
| 🔐 **پروتکل دوگانه** | سوئیچ فوری بین **VLESS** (آلفا)، **Trojan** (بتا) یا هر دو |
| 📱 **تولید QR Code** | کد QR برای پیکربندی سریع کلاینت موبایل |
| 👥 **پروفایل چند کاربره** | لینک اشتراک اختصاصی، نود و NAT64 جداگانه برای هر کاربر |
| 🌍 **مولتی‌پلکسر IP پاک** | تولید خودکار کانفیگ برای هر IP پاک |
| 🌐 **پشتیبانی NAT64** | تبدیل خودکار IPv4 به NAT64-mapped IPv6 |
| ⚙️ **متریک‌های آنی** | IP اصلی، Edge Node و تشخیص تأخیر |
| 💾 **ذخیره‌سازی D1** | حفظ تنظیمات حتی پس از بروزرسانی کد |
| 🚨 **کلید قطع اضطراری** | توقف فوری ترافیک پروکسی از داشبورد یا تلگرام |
| 📊 **مدیریت پهنای باند** | محدودیت GB/TB و pause/resume برای هر کاربر |
| 📋 **لاگ فعالیت‌ها** | تاریخچه ورودها و تغییرات |
| 🔒 **پشتیبانی ECH** | Encrypted Client Hello در کانفیگ‌ها |
| 📦 **پشتیبان‌گیری و بازیابی** | خروجی/ورودی تنظیمات به صورت `.json` |
| 🔄 **بروزرسانی خودکار** | استقرار نسخه جدید با گزینه مبهم‌سازی |
| 🎭 **کانفیگ‌های جعلی** | ورودی‌های جعلی با `{usage}` و `{expiry}` |
| 🖥️ **نودهای اختصاصی کاربر** | هاست اختصاصی برای هر مشترک |
| 🏷️ **استراتژی نام غنی** | تگ‌های `{FLAG}`، `{COUNTRY}`، `{CITY}` و ... |
| 🌐 **صفحه اشتراک دوزبانه** | پشتیبانی کامل فارسی و انگلیسی + RTL |
| 🤖 **مدیریت ربات تلگرام** | مدیریت کامل از طریق دکمه‌های اینلاین |
| 🔗 **پنل‌های لینک‌شده (Other Nodes)** | اتصال امن چند پنل با API Key برای مدیریت متمرکز و انتشار بروزرسانی |

---

## 🔧 پیش‌نیازها

- یک **حساب Cloudflare** (پلن رایگان کافی است)
- دسترسی به **Workers & Pages** و **D1 SQLite Database**
- یک مرورگر مدرن
- *(اختیاری)* توکن ربات تلگرام و Chat ID

---

## 🚀 گزینه‌های نصب سریع

- **ربات تلگرام نصب:** [@technamoozbot](https://t.me/technamoozbot)
- **نصب‌کننده تحت وب:** [https://technamooz.github.io/technamooz-installer/](https://technamooz.github.io/technamooz-installer/)

یا مراحل دستی زیر را دنبال کنید.

---

## 🚀 راهنمای نصب گام‌به‌گام

### گام ۱: ساخت دیتابیس D1

1. وارد [داشبورد Cloudflare](https://dash.cloudflare.com/) شوید.
2. به **Storage and databases** → **D1 SQLite Database** بروید.
3. **Create database** را بزنید و نامی انتخاب کنید (مثلاً `iot_db`).

### گام ۲: استقرار Worker

1. به **Workers & Pages** → **Create application** → **Create Worker** بروید.
2. نامی بگذارید (مثلاً `technamooz-core`) و Deploy کنید.
3. **Edit code** را باز کنید، کد placeholder را پاک کنید و محتوای کامل [`_worker.js`](https://github.com/technamooz/technamooz/blob/main/_worker.js) را پیست کنید.
4. **Save and Deploy** بزنید.

### گام ۳: اتصال دیتابیس D1

1. Worker → **Settings** → **Bindings** → **Add binding**
2. نوع: **D1 database**
3. Variable name: **`IOT_DB`** (باید دقیق همین باشد)
4. دیتابیس را انتخاب کنید → Save → Deploy

### گام ۴: ورود به داشبورد

```
https://<آدرس-ورکر-شما>/sync/dash
```

> مراجعه به `/` یا `/sync` بدون `/dash` عمداً صفحه استتار نشان می‌دهد.

### گام ۵: پیکربندی اولیه

1. با کلید پیش‌فرض `admin` وارد شوید.
2. فوراً به تب **System** بروید و:
   - **Master Key** را تغییر دهید
   - **API Route** را به یک مسیر مخفی تغییر دهید (آدرس جدید را بوکمارک کنید!)
   - **Device UUID** را تنظیم یا خالی بگذارید
3. **Update Config** را بزنید.

---

## 🖥️ راهنمای داشبورد

| تب | کاربرد |
|---|---|
| **Overview** | خلاصه کاربران، ترافیک و بنر بروزرسانی |
| **Endpoints** | لینک اتصال، QR و اشتراک |
| **Metrics** | مصرف زنده، Origin IP، Edge Node و تست تأخیر |
| **System** | تنظیمات اصلی (پروتکل، UUID، مسیر API، کلید، پورت، Auto-Update، Panel API Keys، Backup) |
| **Advanced** | Clean IP، پنل‌های لینک‌شده، چند کاربره، تلگرام، Kill Switch، ECH، NAT64 و ... |
| **Logs** | تاریخچه ورود و تغییرات |
| **Clients** | مدیریت بصری کاربران |
| **Help** | راهنما و سوالات متداول |

---

## 🔩 تنظیمات پیشرفته

### مولتی‌پلکسر IP پاک

در تب **Advanced** لیست IP پاک را وارد کنید (یک IP در هر خط یا فرمت `IP#Name`). اشتراک برای هر IP یک کانفیگ جداگانه می‌سازد.

**ابزارهای پیشنهادی Clean IP:**
- GitHub: [technamooz](https://github.com/technamooz)
- تلگرام: [@itsZetaBot](https://t.me/itsZetaBot)

### Relay IP

ربات پیشنهادی: [@technamoozproxyipbot](https://t.me/technamoozproxyipbot)

### پنل‌های لینک‌شده (Other Nodes)

اتصال پنل‌های تکناموز دیگر با **URL + API Key** برای مدیریت متمرکز و انتشار بروزرسانی.  
(فیلدهای قدیمی `slaveNodes` / Cascade به‌طور خودکار به `linkedPanels` مهاجرت می‌شوند.)

### پروفایل چند کاربره

فرمت (یک خط برای هر کاربر):

```
<uuid>:نام‌کاربری
```

دسترسی: `https://<ورکر>/sync/sub?sub=نام‌کاربری`

### ربات تلگرام

1. ربات را از [@BotFather](https://t.me/botfather) بسازید
2. Chat ID را از [@userinfobot](https://t.me/userinfobot) بگیرید
3. در تب Advanced وارد کنید و ذخیره کنید

دستورات: `/status` و `/pause` (Kill Switch)

### کلید قطع اضطراری (Kill Switch)

از تب Advanced یا دستور `/pause` در تلگرام برای توقف فوری ترافیک پروکسی استفاده کنید.

---

## 🔗 منابع مفید

| کاربرد | منبع |
|---|---|
| پیدا کردن Clean IP | [technamooz](https://github.com/technamooz) · [@itsZetaBot](https://t.me/itsZetaBot) |
| Relay IP | [@technamoozproxyipbot](https://t.me/technamoozproxyipbot) |
| نصب آسان (تلگرام) | [@technamoozbot](https://t.me/technamoozbot) |
| نصب‌کننده وب | [technamooz.github.io/technamooz-installer](https://technamooz.github.io/technamooz-installer/) |

---

## 💾 ذخیره تغییرات

پس از هر تغییر در تب‌های **System** یا **Advanced**:

1. روی **Update Config** کلیک کنید.
2. منتظر «Syncing...» بمانید تا صفحه بارگذاری مجدد شود.

اگر API Route را تغییر دادید، صفحه به مسیر جدید هدایت می‌شود — آن را بوکمارک کنید.

---

## ❓ سوالات متداول و رفع اشکال

**پیام `⚠️ IOT_DB namespace missing!`**  
→ Binding دیتابیس D1 وجود ندارد یا نام متغیر دقیقاً `IOT_DB` نیست. در Settings → Bindings اصلاح و Redeploy کنید.

**آدرس اصلی سایت Ubuntu/Docker نشان می‌دهد**  
→ رفتار عمدی است. همیشه از `/sync/dash` (یا مسیر سفارشی + `/dash`) استفاده کنید.

**Master Key یا API Route را فراموش کرده‌ام**  
→ مقادیر را از D1 Console (کلید `sys_config`) بازیابی کنید.

**محدودیت پلن رایگان**  
→ ۱۰۰٬۰۰۰ درخواست در روز. از بخش Cloudflare Analytics در Advanced مصرف را مانیتور کنید.

---

## 🤝 مشارکت در پروژه

1. مخزن را Fork کنید
2. شاخه بسازید
3. تغییرات را اعمال کنید
4. Pull Request باز کنید

---

## 📄 مجوز

تحت مجوز MIT — فایل [LICENSE](./LICENSE) را ببینید.

---

<div align="center">

ساخته شده با ❤️ توسط جامعه متن‌باز

[⭐ ستاره بدهید](https://github.com/technamooz/technamooz) · [🐛 گزارش خطا](https://github.com/technamooz/technamooz/issues) · [🌐 نسخه انگلیسی](./README.md)

</div>

</div>

## Technamooz 4.1 — رفع مشکل کانفیگ

در نسخه 4.1 تولید رکوردهای نمایشی `127.0.0.1:1080` به‌صورت پیش‌فرض غیرفعال شده است. این رکوردها قبلاً در ابتدای بعضی subscriptionها قرار می‌گرفتند و در برخی کلاینت‌ها به‌عنوان کانفیگ واقعی نمایش داده می‌شدند. خروجی پیش‌فرض اکنون فقط شامل کانفیگ‌های واقعی Worker است.

### مسیرهای خروجی واقعی

- خروجی خام و Base64: `https://YOUR-DOMAIN/<apiRoute>`
- Clash/Mihomo: `https://YOUR-DOMAIN/<apiRoute>?format=clash`
- sing-box: `https://YOUR-DOMAIN/<apiRoute>?format=singbox`
- v2rayN JSON: `https://YOUR-DOMAIN/<apiRoute>?format=vjson`
- اشتراک کاربر: `https://YOUR-DOMAIN/<apiRoute>?sub=USER_ID`

مقدار پیش‌فرض `apiRoute` در این نسخه `sync` است. اگر در پنل تغییرش دهید، لینک‌های قدیمی دیگر معتبر نیستند و باید subscription را دوباره در کلاینت وارد کنید.

### چک‌لیست بعد از Deploy

1. در Cloudflare، Worker باید binding به D1 با نام `IOT_DB` داشته باشد.
2. در `wrangler.toml` مقدار `database_id` باید شناسه واقعی D1 باشد، نه `YOUR_D1_DATABASE_ID_HERE`.
3. در داشبورد، حداقل یک پورت فعال مانند `443` و حالت `VLESS` انتخاب کنید.
4. برای تست خام، پاسخ مسیر `/sync` باید یک متن Base64 چندخطی باشد؛ پاسخ HTML به معنی استفاده از User-Agent مرورگر یا بازکردن مسیر بدون کلاینت است.
5. کانفیگ باید با دامنه‌ای که Worker روی آن منتشر شده و مسیر `/<apiRoute>` ساخته شود؛ دامنه سرور مقصد را در فیلدهای اشتباه جایگزین نکنید.
6. اگر دامنه اختصاصی دارید، SSL آن باید فعال باشد و رکورد از نوع Worker Route یا Custom Domain باشد.

برای پشتیبانی رسمی: [Telegram: @technamooz_support](https://t.me/technamooz_support)

