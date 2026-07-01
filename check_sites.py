"""
Website Change Checker (GitHub Actions version)
-------------------------------------------------
Runs automatically on a schedule via GitHub Actions — no server or VM needed.

What it does each run:
1. Reads links.json
2. Fetches each site's text content
3. Compares it to the previously saved hash
4. If different -> sends a Telegram message with the link
5. Saves the new hash back into links.json (committed back to the repo
   by the GitHub Actions workflow)
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

LINKS_FILE = Path(__file__).parent / "links.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def load_links():
    if LINKS_FILE.exists():
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_links(links):
    with open(LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)


def send_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("BOT_TOKEN/CHAT_ID সেট নেই, Telegram মেসেজ পাঠানো বাদ দেওয়া হলো।")
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text},
            timeout=15,
        )
    except Exception as e:
        print(f"[telegram] send failed: {e}")


def fetch_page_text(url):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())


def hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    links = load_links()
    if not links:
        print("links.json খালি — কোনো লিংক যোগ করা নেই।")
        return

    for name, info in links.items():
        url = info["url"]
        try:
            text = fetch_page_text(url)
        except Exception as e:
            print(f"[check] failed for {url}: {e}")
            continue

        new_hash = hash_text(text)
        old_hash = info.get("hash")

        if old_hash is not None and new_hash != old_hash:
            msg = (
                "🔔 পরিবর্তন শনাক্ত হয়েছে!\n\n"
                f"নাম: {name}\n"
                f"লিংক: {url}\n"
                f"সময়: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )
            send_message(msg)
            print(f"CHANGED: {name}")
        else:
            print(f"no change: {name}")

        links[name]["hash"] = new_hash
        links[name]["last_checked"] = datetime.now(timezone.utc).isoformat()

    save_links(links)


if __name__ == "__main__":
    main()
