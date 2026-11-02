# Project Technamooz (پروژه تکناموز)

### The Ultimate Serverless Gateway on Cloudflare Workers

**Technamooz** (Persian for *Hidden/Concealed*) is a secure, lightweight, and highly customizable reverse proxy that runs entirely on the edge. It transforms your Cloudflare Worker into a powerful, obfuscated gateway using **VLESS** or **Trojan** protocols, managed via a beautiful, self-contained Web UI.

[![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white)](https://workers.cloudflare.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](./LICENSE)
[![JavaScript](https://img.shields.io/badge/JavaScript-100%25-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://github.com/technamooz/technamooz/blob/main/_worker.js)

> 🇮🇷 [نسخه فارسی / Persian Version](./README_FA.md)

---

## 📖 Table of Contents

- [Why Technamooz?](#-why-technamooz)
- [Key Features](#-key-features)
- [Prerequisites](#-prerequisites)
- [Quick Install Options](#-quick-install-options)
- [Step-by-Step Deployment Guide](#-step-by-step-deployment-guide)
- [Dashboard Guide](#-dashboard-guide)
- [Advanced Configuration](#-advanced-configuration)
- [Useful Resources](#-useful-resources)
- [Applying Configuration Changes](#-applying-configuration-changes)
- [FAQ & Troubleshooting](#-faq--troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Why Technamooz?

Technamooz isn't just a proxy script — it's a complete management solution designed for **stealth**, **speed**, and **ease of use**.

- 🛡️ **Hidden in Plain Sight:** Unauthorized access attempts are proxied to legitimate sites (e.g., `ubuntu.com` or `docker.com`), making your gateway look like a regular website to network scanners.
- ⚡ **Zero Server Cost:** Runs entirely on Cloudflare's free plan. No VPS, no server maintenance.
- 🎨 **Modern Dashboard:** A fully embedded, mobile-friendly dashboard with Dark/Light modes and dual-language support (English / فارسی).
- 🤖 **Telegram Bot Integration:** Manage your gateway, check usage, and receive login alerts directly via Telegram.
- 📡 **Multi-User & Multi-IP:** Generate dedicated subscription links for different users and automatically combine them with clean IP lists.
- 💾 **D1 SQLite Storage:** Configuration persists in Cloudflare D1 database, eliminating KV write limitations.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔐 **Dual Protocol** | Switch instantly between **VLESS** (Alpha), **Trojan** (Beta), or **Both** simultaneously |
| 📱 **QR Code Generation** | Modal-based QR codes for instant mobile client configuration |
| 👥 **Multi-User Profiles** | Create separate profiles with unique subscription links, per-user nodes, and per-user NAT64 |
| 🌍 **Clean IP Multiplexer** | Input a list of clean Cloudflare IPs — Technamooz auto-generates configs for all of them |
| 🌐 **NAT64 Support** | Automatic IPv4-to-NAT64-mapped IPv6 conversion with multiple prefix support |
| ⚙️ **Real-Time Metrics** | View Origin IP, Edge Node location, and run browser-side latency diagnostics |
| 💾 **D1 SQLite Storage** | All configuration persists in Cloudflare D1 even after code updates |
| 🚨 **Kill Switch** | Immediately pause all proxy traffic with one click from the dashboard or Telegram |
| 📊 **Bandwidth Management** | Track per-user upload/download with TB/GB limits and pause/resume controls |
| 📋 **Activity Logs** | Full history of login attempts and configuration changes |
| 🔒 **ECH Support** | Toggle Encrypted Client Hello (ECH) parameters in generated client configs |
| 📦 **Backup & Restore** | Export/import your full configuration as a `.json` file |
| 🔄 **Auto Update** | Automatic deployment of new versions from GitHub with format and obfuscation options |
| 🎭 **Configurable Fake Configs** | Customizable fake subscription entries with `{usage}` and `{expiry}` template variables |
| 🖥️ **Per-User Nodes** | Define custom hostnames per subscriber for multi-region deployments |
| 🏷️ **Rich Name Strategy** | Config naming with `{FLAG}`, `{COUNTRY}`, `{CITY}`, `{ISP}`, `{HOST}`, `{DATE}`, `{WORKER}` tags |
| 🌐 **Bilingual Subscription Page** | Subscription info page with full **Persian/Farsi** and **English** support, RTL layout, and dark/light mode toggle |
| 🤖 **Telegram Bot Management** | Full gateway management via inline Telegram buttons — users, settings, logs, and advanced config |
| 🔗 **Linked Panels (Other Nodes)** | Connect multiple Technamooz panels securely with API Keys for cross-panel management and update propagation |

---

## 🔧 Prerequisites

- A **Cloudflare account** (free tier is sufficient) — [sign up here](https://dash.cloudflare.com/sign-up)
- Access to **Workers & Pages** and **D1 SQLite Database** in your Cloudflare Dashboard
- A modern web browser
- *(Optional)* A Telegram Bot Token and Chat ID for bot integration

---

## 🚀 Quick Install Options

For easier deployment you can use:

- **Telegram Install Bot:** [@technamoozbot](https://t.me/technamoozbot)
- **Web Installer:** [https://technamooz.github.io/technamooz-installer/](https://technamooz.github.io/technamooz-installer/)

Or follow the manual steps below.

---

## 🚀 Step-by-Step Deployment Guide

### Step 1: Create a D1 Database

1. Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Go to **Storage and databases** → **D1 SQLite Database**.
3. Click **Create database**.
4. Enter a name (e.g. `iot_db`) and click **Create**.

### Step 2: Deploy the Worker

1. Go to **Workers & Pages** → **Create application** → **Create Worker**.
2. Name it (e.g. `technamooz-core`) and click **Deploy**.
3. Click **Edit code**, delete the placeholder, and paste the full content of [`_worker.js`](https://github.com/technamooz/technamooz/blob/main/_worker.js).
4. Click **Save and Deploy**.

### Step 3: Bind the D1 Database

1. Open your Worker → **Settings** → **Bindings** → **Add binding**.
2. Type: **D1 database**
3. Variable name: **`IOT_DB`** (must be exact)
4. Select the database you created → **Save** → **Deploy**.

### Step 4: Access the Dashboard

Open:

```
https://<your-worker-domain>/sync/dash
```

> Visiting `/` or `/sync` without `/dash` shows a camouflage page (Ubuntu/Docker). This is intentional.

### Step 5: First-Time Configuration

1. Login with the default master key: `admin`
2. Immediately go to **System** tab and:
   - Change **Master Key**
   - Change **API Route** to a secret path (bookmark the new URL!)
   - Set or auto-generate **Device UUID**
3. Click **Update Config**.

---

## 🖥️ Dashboard Guide

The dashboard includes these main sections:

| Tab | Purpose |
|---|---|
| **Overview** | User summary cards, traffic stats, and update banner |
| **Endpoints** | Connection URIs, QR codes, and subscription links |
| **Metrics** | Live usage, Origin IP, Edge Node (Colo), latency diagnostics |
| **System** | Core settings (protocol, UUID, API Route, Master Key, ports, Auto-Update, Panel API Keys, Backup) |
| **Advanced** | Clean IPs, Linked Panels, Multi-User, Telegram, Kill Switch, ECH, NAT64, etc. |
| **Logs** | Login attempts and configuration change history |
| **Clients** | Visual multi-user management |
| **Help** | Built-in help and FAQ |

---

## 🔩 Advanced Configuration

### Clean IP Multiplexer

In **Advanced** → **Clean IPs**, enter one IP (or `IP#Name`) per line. The subscription will contain a separate config for each IP.

**Recommended tools for finding Clean IPs:**
- GitHub: [technamooz](https://github.com/technamooz)
- Telegram: [@itsZetaBot](https://t.me/itsZetaBot)

### Relay IP

Recommended bot: [@technamoozproxyipbot](https://t.me/technamoozproxyipbot)

### Linked Panels (Other Nodes)

Connect external Technamooz panels using **URL + API Key** for cross-panel management and update propagation.  
(Legacy `slaveNodes` / Cascade fields are automatically migrated to `linkedPanels`.)

### Multi-User Profiles

Format (one per line):

```
<uuid>:Username
```

Access: `https://<worker>/sync/sub?sub=Username`

### Telegram Bot

1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get Chat ID from [@userinfobot](https://t.me/userinfobot)
3. Enter Token + Chat ID in Advanced tab and save

Commands: `/status`, `/pause` (Kill Switch)

### Kill Switch

Toggle in Advanced (or send `/pause` via Telegram) to immediately stop all proxy traffic while keeping the worker alive.

---

## 🔗 Useful Resources

| Purpose | Resource |
|---|---|
| Clean IP finder | [technamooz](https://github.com/technamooz) · [@itsZetaBot](https://t.me/itsZetaBot) |
| Relay IP | [@technamoozproxyipbot](https://t.me/technamoozproxyipbot) |
| Easy Install (Telegram) | [@technamoozbot](https://t.me/technamoozbot) |
| Web Installer | [technamooz.github.io/technamooz-installer](https://technamooz.github.io/technamooz-installer/) |

---

## 💾 Applying Configuration Changes

After changing anything in **System** or **Advanced**:

1. Click **Update Config** at the bottom.
2. Wait for “Syncing…” then the page reloads.

If you changed the API Route, the page redirects to the new path — bookmark it.

---

## ❓ FAQ & Troubleshooting

**`⚠️ IOT_DB namespace missing!`**  
→ D1 binding is missing or the variable name is not exactly `IOT_DB`. Fix in Worker Settings → Bindings and redeploy.

**Root URL shows Ubuntu/Docker**  
→ Expected behavior. Always use `/sync/dash` (or your custom API Route + `/dash`).

**Forgot Master Key or API Route**  
→ Check values in the D1 Console (`sys_config` key).

**Free plan limits**  
→ 100,000 requests/day. Monitor via Cloudflare Analytics integration in Advanced.

---

## 🤝 Contributing

1. Fork the repository
2. Create a branch
3. Make your changes
4. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](./LICENSE)

---

<div align="center">

Made with ❤️ by the Open Source Community

[⭐ Star this repo](https://github.com/technamooz/technamooz) · [🐛 Report a bug](https://github.com/technamooz/technamooz/issues) · [🇮🇷 نسخه فارسی](./README_FA.md)

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

