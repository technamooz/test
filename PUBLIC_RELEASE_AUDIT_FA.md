# گزارش ممیزی انتشار عمومی Technamooz

**نسخه بررسی‌شده:** 4.1.0  
**تاریخ ممیزی:** 2026-09-22  
**وضعیت:** آماده برای انتشار پس از تکمیل شناسه D1 توسط مالک Cloudflare

## دامنه بررسی

تمام 18 فایل اصلی پروژه، شامل Worker خوانا و encoded، صفحات `index.html`، `dashboard.html` و `subscription.html`، قالب‌های Clash و sing-box و v2ray، Wrangler، نصب‌کننده، converter پایتون و مستندات بررسی شدند. علاوه بر مرور ساختاری، syntax فایل‌های JavaScript و Python و Bash، ساختار صفحات HTML و Bundle واقعی Wrangler نیز تست شد.

## اصلاحات مهم

احراز هویت username/password با endpointهای مدیریتی هماهنگ شد تا ورود جدید فقط صفحه را باز نکند، بلکه endpointهای users، stats، update، API keys و sync را نیز به‌درستی مجاز کند. همچنین مقادیر `[PROTECTED]` دیگر هنگام ذخیره تنظیمات روی credential واقعی overwrite نمی‌شوند.

برای ورود پنل rate limit در سطح Worker اضافه شد؛ پس از پنج تلاش ناموفق از یک IP، پاسخ موقت `429` برگردانده می‌شود. نسخه encoded پس از هر اصلاح از Worker خوانا بازسازی شد تا دو نسخه از نظر رفتار همگام باشند.

صفحات `index.html`، `dashboard.html` و `subscription.html` داخل Worker جاسازی شدند. در نتیجه Deploy مستقل دیگر برای نمایش پنل و صفحه subscription به دریافت فایل از GitHub وابسته نیست. فقط اگر `DASHBOARD_URL` یا `SUBSCRIPTION_URL` تنظیم شود، منبع خارجی به‌صورت اختیاری استفاده خواهد شد. مسیر ریشه دامنه نیز اکنون صفحه اصلی Technamooz را نمایش می‌دهد.

## نتایج تست

| تست | نتیجه |
|---|---|
| `node --check _worker.js` | موفق |
| `node --check _worker.encode.js` | موفق |
| `python3 -m py_compile worker_converter.py` | موفق |
| `bash -n setup.sh` | موفق |
| syntax اسکریپت‌های داخلی هر سه صفحه | موفق |
| وجود Login، captcha و refresh captcha | تأیید شد |
| embed شدن index، dashboard و subscription | تأیید شد |
| rate limit و protected merge | تأیید شد |
| نبود ارجاع برند قدیمی در Worker و داشبورد | تأیید شد |
| `wrangler deploy --dry-run` | موفق |
| حجم Bundle نهایی | 1126.22 KiB؛ حجم gzip برابر 288.38 KiB |
| Binding موردنیاز | `IOT_DB` از نوع D1 |

## تنها مرحله وابسته به حساب مالک

فایل `wrangler.toml` به‌صورت عمدی شامل مقدار نمونه `YOUR_D1_DATABASE_ID_HERE` است؛ این مقدار secret نیست و باید با شناسه D1 حساب خودتان جایگزین شود. نصب‌کننده `setup.sh` این کار را با ساخت یا یافتن دیتابیس D1 انجام می‌دهد و سپس `wrangler.toml` تولیدشده را قبل از Deploy می‌نویسد. اگر Deploy دستی انجام می‌دهید، ابتدا دیتابیس را بسازید و مقدار `database_id` را جایگزین کنید.

برای محیط عمومی، بلافاصله بعد از نصب مقدار پیش‌فرض `technamooz` برای username/password و master key را در تنظیمات پنل تغییر دهید. این مقدار فقط default نصب اولیه است و نباید در سرویس عمومی بدون تغییر باقی بماند.

## یادداشت عملیاتی

این ممیزی خطاهای قابل‌اثبات کد و انتشار را اصلاح کرده است، اما صحت اتصال نهایی هر کانفیگ به IP، پورت، DNS، دامنه و تنظیمات واقعی همان Deploy وابسته است. پس از Deploy، یک کاربر آزمایشی با حداقل یک IP و پورت واقعی بسازید، لینک subscription را در یک کلاینت پشتیبانی‌شده import کنید و QR همان لینک را با گوشی آزمایش کنید.
