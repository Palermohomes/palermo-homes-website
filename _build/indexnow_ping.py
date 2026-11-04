"""IndexNow protocol integration for Palermo Homes.

IndexNow is an open protocol that lets you instantly notify search engines
(Bing, Yandex, Seznam, Naver, Yep) when content on your site is new or
updated. Google does NOT currently consume IndexNow directly, but ChatGPT
and Perplexity read Bing's index, so this is a GEO (Generative Engine
Optimization) win on top of Bing SEO.

How it works:
1. Generate a secret API key (one-time) and host it as a text file at the
   site root under that key's filename. The file content must be the key.
   Search engines fetch that file to verify ownership before accepting
   submissions.
2. POST a JSON payload listing URLs to the IndexNow endpoint. Bing then
   crawls them within hours.

Run this script after any build that adds or updates content. It reads
sitemap.xml for the current URL list and submits the ones changed today.

Setup (one-time):
  - Key file lives at site/<KEY>.txt with content = <KEY>
  - Same key is referenced in this script and in the submission payload

Usage:
  python _build/indexnow_ping.py              # pings all URLs with today's lastmod
  python _build/indexnow_ping.py --all        # pings every URL in sitemap
  python _build/indexnow_ping.py --urls u1 u2 # pings specific URLs
"""
import sys
import json
import urllib.request
import urllib.error
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SITEMAP = SITE / "sitemap.xml"

# IndexNow key for palermohomes.com. 32-char hex string.
# This is NOT a secret in the traditional sense (it's hosted publicly at /KEY.txt)
# but it does prevent arbitrary third parties from submitting URLs on your behalf.
KEY = "a7f3c9e2d8b641578a4e9c3b2f6d8e1a"
HOST = "palermohomes.com"
KEY_FILE_URL = f"https://{HOST}/{KEY}.txt"

# IndexNow endpoint. Bing is the primary consumer. One submission to this
# endpoint propagates to all participating search engines.
ENDPOINT = "https://api.indexnow.org/IndexNow"


def ensure_key_file():
    """Create the verification key file at site root if missing. Idempotent."""
    key_path = SITE / f"{KEY}.txt"
    if not key_path.exists() or key_path.read_text().strip() != KEY:
        key_path.write_text(KEY, encoding="utf-8")
        print(f"  wrote {key_path.name} (IndexNow verification key)")


def urls_from_sitemap(today_only=True):
    """Parse sitemap.xml and return URLs. If today_only, filter to those with lastmod=today."""
    if not SITEMAP.exists():
        print("  ERROR: sitemap.xml not found. Run generate_sitemap.py first.")
        return []
    xml = SITEMAP.read_text(encoding="utf-8")
    urls = []
    today = date.today().isoformat()
    for match in re.finditer(r"<url>\s*<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml):
        loc, lastmod = match.group(1), match.group(2)
        if today_only and lastmod != today:
            continue
        urls.append(loc)
    return urls


def submit(urls):
    """POST URLs to IndexNow. Returns True on success (2xx)."""
    if not urls:
        print("  no URLs to submit")
        return True
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_FILE_URL,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")
            print(f"  IndexNow response: HTTP {status}")
            if body.strip():
                print(f"  body: {body[:300]}")
            return 200 <= status < 300
    except urllib.error.HTTPError as e:
        # IndexNow returns 202 (accepted) on success, 200 (ok). Others are informational.
        # 400 usually means malformed URL. 403 means key verification failed.
        # 422 means URLs don't belong to this host.
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        print(f"  IndexNow HTTPError: {e.code} {e.reason}")
        if body.strip():
            print(f"  body: {body[:300]}")
        return False
    except Exception as e:
        print(f"  IndexNow request failed: {e}")
        return False


def main():
    ensure_key_file()
    args = sys.argv[1:]
    if args and args[0] == "--urls":
        urls = args[1:]
    elif args and args[0] == "--all":
        urls = urls_from_sitemap(today_only=False)
    else:
        urls = urls_from_sitemap(today_only=True)
    print(f"IndexNow: submitting {len(urls)} URL(s) to Bing/Yandex/participating engines")
    for u in urls[:10]:
        print(f"  - {u}")
    if len(urls) > 10:
        print(f"  ... and {len(urls) - 10} more")
    ok = submit(urls)
    print(f"Done. {'OK' if ok else 'FAILED'}.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
