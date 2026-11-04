"""Validate ALL JSON-LD schema blocks on every page (not just injected)."""
import re
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
PATTERN = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.+?)</script>', re.DOTALL)

files_with_errors = []
total_blocks = 0
total_pages = 0

for html_file in SITE.rglob("*.html"):
    total_pages += 1
    html = html_file.read_text(encoding="utf-8")
    matches = PATTERN.findall(html)
    for i, block in enumerate(matches):
        total_blocks += 1
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            files_with_errors.append(f"{html_file.relative_to(SITE)} (block {i+1}) ,  {e}")

print(f"Total pages scanned: {total_pages}")
print(f"Total schema blocks: {total_blocks}")
print(f"Errors: {len(files_with_errors)}")
if files_with_errors:
    for e in files_with_errors[:20]:
        print(f"  {e}")
else:
    print("All schema blocks valid.")
