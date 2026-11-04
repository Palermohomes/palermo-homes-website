"""One-off verification table: URL | status | canonical OK | title OK | desc OK | H1 | schema OK."""
import re, json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

rows = []
for p in sorted(SITE.rglob("index.html")):
    url_path = str(p.relative_to(SITE)).replace("\\", "/").replace("index.html", "")
    url = "https://palermohomes.com/" + url_path
    html = p.read_text(encoding="utf-8", errors="ignore")
    cm = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"', html) or \
         re.search(r'<link[^>]*href="([^"]*)"[^>]*rel="canonical"', html)
    canon_ok = "yes" if cm and cm.group(1) == url else "NO"
    tm = re.search(r"<title>([^<]*)</title>", html)
    title_ok = "yes" if tm and tm.group(1).strip() else "NO"
    dm = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html) or \
         re.search(r'<meta[^>]*content="([^"]*)"[^>]*name="description"', html)
    desc_ok = "yes" if dm and dm.group(1).strip() else "NO"
    body = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.DOTALL)
    h1c = len(re.findall(r"<h1\b", body))
    h1_ok = "yes" if h1c == 1 else f"NO({h1c})"
    schema_ok = "yes"
    for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, flags=re.DOTALL):
        try:
            json.loads(m.group(1))
        except Exception:
            schema_ok = "NO"
            break
    rows.append(("/" + url_path, canon_ok, title_ok, desc_ok, h1_ok, schema_ok))

print(f"{'URL':<60} | {'status':<6} | {'canon':<5} | {'title':<5} | {'desc':<5} | {'H1':<6} | schema")
print("-" * 60 + "-+-" + "-" * 6 + "-+-" + "-" * 5 + "-+-" + "-" * 5 + "-+-" + "-" * 5 + "-+-" + "-" * 6 + "-+-------")
all_ok = 0
for url, c, t, d, h, s in rows:
    status = "OK" if (c == "yes" and t == "yes" and d == "yes" and h == "yes" and s == "yes") else "ISSUE"
    if status == "OK":
        all_ok += 1
    print(f"{url:<60} | {status:<6} | {c:<5} | {t:<5} | {d:<5} | {h:<6} | {s}")

print()
print(f"Total: {len(rows)} pages. OK on every check: {all_ok} / {len(rows)}")
