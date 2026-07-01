# 🔔 Website Change Monitor Bot

কোনো website-এ নতুন কিছু আসলে বা পরিবর্তন হলে সাথে সাথে **Telegram**-এ নোটিফিকেশন পাবেন।

**সম্পূর্ণ ফ্রি। কোনো সার্ভার নেই। কোনো VM নেই। কোনো লিমিট নেই।**
GitHub নিজেই প্রতি ৩০ মিনিটে সব চেক করে নেবে।

---

## যা যা লাগবে

- একটা **GitHub account** (ফ্রি, কার্ড লাগে না)
- একটা **Telegram account**
- ব্যস।

---

## ধাপ ১ — Telegram Bot তৈরি করুন (৩ মিনিট)

1. Telegram-এ `@BotFather` সার্চ করে open করুন
2. `/newbot` পাঠান
3. বটের একটা নাম দিন — যেমন: `My Site Monitor`
4. একটা username দিন, শেষে `bot` থাকতে হবে — যেমন: `usman_site_monitor_bot`
5. BotFather একটা **token** দেবে, এরকম দেখতে:
   ```
   7123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   এটা কপি করে কোথাও রেখে দিন — এটাই `BOT_TOKEN`

---

## ধাপ ২ — আপনার Telegram Chat ID বের করুন (১ মিনিট)

1. Telegram-এ `@userinfobot` সার্চ করুন
2. `/start` পাঠান
3. একটা সংখ্যা দেবে — যেমন: `712345678`
   এটাই আপনার `CHAT_ID`

---

## ধাপ ৩ — GitHub Repository তৈরি করুন

1. github.com-এ লগিন করুন
2. উপরে ডানে `+` বোতাম → `New repository`
3. Repository name: `site-monitor` (যেকোনো নাম দিন)
4. **Public** রাখুন (Public repo-তে Actions ফ্রি ও আনলিমিটেড)
5. `Create repository` চাপুন

---

## ধাপ ৪ — ফাইলগুলো Repository-তে আপলোড করুন

Repository-তে ঢুকে `Add file → Upload files` চাপুন।
নিচের ফাইলগুলো আপলোড করুন এবং **folder structure** ঠিক রাখুন:

```
site-monitor/
├── .github/
│   └── workflows/
│       └── monitor.yml       ← এটা subfolder-সহ বানাতে হবে (নিচে দেখুন)
├── check_sites.py
├── links.json
└── requirements.txt
```

> **.github/workflows/monitor.yml** আপলোড করার সময়:
> `Add file → Create new file` চাপুন, filename-এ লিখুন:
> `.github/workflows/monitor.yml`
> তারপর monitor.yml-এর কনটেন্ট পেস্ট করুন।

বাকি তিনটা ফাইল সরাসরি আপলোড করতে পারবেন।

---

## ধাপ ৫ — BOT_TOKEN ও CHAT_ID সিক্রেট হিসেবে সেভ করুন

Repository-তে:
1. **Settings** ট্যাবে যান
2. বামে **Secrets and variables → Actions** ক্লিক করুন
3. **New repository secret** বোতাম চাপুন

প্রথম secret:
- Name: `BOT_TOKEN`
- Secret: BotFather থেকে পাওয়া token পেস্ট করুন
- `Add secret` চাপুন

দ্বিতীয় secret:
- Name: `CHAT_ID`
- Secret: আপনার Chat ID পেস্ট করুন
- `Add secret` চাপুন

---

## ধাপ ৬ — প্রথমবার টেস্ট করুন

1. Repository-তে **Actions** ট্যাবে যান
2. বামে `Website Change Monitor` দেখতে পাবেন
3. **Run workflow → Run workflow** চাপুন
4. ৩০ সেকেন্ড অপেক্ষা করুন, সবুজ টিক দেখাবে
5. প্রথম রানে শুধু hash সেভ হবে, কোনো Telegram মেসেজ আসবে না (এটাই স্বাভাবিক)
6. এখন `links.json`-এ একটা সাইটের কনটেন্ট পরিবর্তন করে (যেমন url ঠিক রেখে hash বদলে দিন) আবার `Run workflow` চাপলে Telegram-এ মেসেজ আসবে

---

## নতুন website যোগ করবেন কীভাবে

`links.json` ফাইলটা GitHub-এ সরাসরি Edit করুন:

```json
{
  "oxoke-shop": {
    "url": "https://shop.oxoke.com",
    "hash": null,
    "added": "2026-01-01T00:00:00"
  },
  "suno": {
    "url": "https://suno.com",
    "hash": null,
    "added": "2026-01-01T00:00:00"
  },
  "আমার-যেকোনো-নাম": {
    "url": "https://example.com",
    "hash": null,
    "added": "2026-01-01T00:00:00"
  }
}
```

`hash: null` রাখলে প্রথম রানে baseline নেবে, পরের রান থেকে পরিবর্তন ধরবে।

---

## কত মিনিট পরপর চেক হবে সেটা বদলাবেন কীভাবে

`monitor.yml` ফাইলে এই লাইনটা:
```
- cron: "*/30 * * * *"
```
`*/30` মানে ৩০ মিনিট। `*/15` করলে ১৫ মিনিট, `*/60` করলে ১ ঘণ্টা।

> ⚠️ GitHub Actions-এর cron সর্বনিম্ন ৫ মিনিট পরপর চলতে পারে।

---

## এটা সত্যিই ফ্রি থাকবে তো?

হ্যাঁ।
- GitHub Actions: Public repo-তে **আনলিমিটেড মিনিট**, কোনো বিল নেই
- Telegram Bot API: **সম্পূর্ণ ফ্রি**, ব্যক্তিগত ব্যবহারে কোনো লিমিট নেই
- কোনো সার্ভার, কোনো hosting, কোনো database লাগছে না

---

## পরিবর্তন শনাক্ত হলে Telegram-এ যা দেখাবে

```
🔔 পরিবর্তন শনাক্ত হয়েছে!

নাম: oxoke-shop
লিংক: https://shop.oxoke.com
সময়: 2026-07-01 14:30:00 UTC
```
