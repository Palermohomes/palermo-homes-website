"""Verify injected business schema is valid JSON on every page."""
import re
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
PATTERN = re.compile(r'SITE-BUSINESS-SCHEMA START -->\s*<script type="application/ld\+json">(.+?)</script>', re.DOTALL)

ok = 0
fail = 0
missing = 0

for html_file in SITE.rglob("*.html"):
    html = html_file.read_text(encoding="utf-8")
    m = PATTERN.search(html)
    if not m:
        missing += 1
        print(f"MISSING: {html_file.relative_to(SITE)}")
        continue
    try:
        data = json.loads(m.group(1))
        types = [item["@type"] for item in data["@graph"]]
        assert "Organization" in types and "HomeAndConstructionBusiness" in types
        ok += 1
    except (json.JSONDecodeError, AssertionError, KeyError) as e:
        fail += 1
        print(f"INVALID: {html_file.relative_to(SITE)} ,  {e}")

print(f"\n=== RESULT ===")
print(f"Valid: {ok}")
print(f"Invalid: {fail}")
print(f"Missing block: {missing}")
