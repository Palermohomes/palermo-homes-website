"""Scan every HTML file for broken asset references.
Checks src, href, srcset, data-src, data-lazy-src, poster, and inline url(...) refs.
Reports any local path that doesn't resolve on disk + any external URL that may fail.
Run after every build."""
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

SITE = Path(__file__).resolve().parent.parent / "site"

ATTR_RE = re.compile(r'\b(src|href|poster|data-src|data-lazy-src)="([^"]+)"')
SRCSET_RE = re.compile(r'\bsrcset="([^"]+)"')
CSS_URL_RE = re.compile(r'url\(\s*["\']?([^"\')\s]+)["\']?\s*\)')

# References we intentionally ignore
IGNORE_PREFIXES = ("mailto:", "tel:", "javascript:", "#", "data:")
# Domains we know are external + expected
EXTERNAL_OK = ("fonts.googleapis.com", "fonts.gstatic.com", "schema.org", "www.w3.org", "gmpg.org")


def resolve(page: Path, ref: str) -> Path | None:
    """Resolve an asset reference against a page to an absolute Path on disk.
    Returns None for external URLs, template fragments, or unsupported schemes."""
    if not ref or ref.startswith(IGNORE_PREFIXES):
        return None
    if ref.startswith(("http://", "https://", "//")):
        return None
    # JS/template fragments. Not real URLs (contain +, {, whitespace, etc.)
    if any(c in ref for c in ("+", "{", " ", "\t", "\n")):
        return None
    # strip query/fragment
    ref = ref.split("?", 1)[0].split("#", 1)[0]
    ref = unquote(ref)
    if not ref:
        return None
    if ref.startswith("/"):
        return SITE / ref.lstrip("/")
    return (page.parent / ref).resolve()


def check(page: Path, broken: list, externals: dict):
    try:
        html = page.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        broken.append((page, "READ_ERROR", str(e)))
        return
    seen: set = set()

    def note_ref(attr: str, ref: str):
        if not ref or ref.startswith(IGNORE_PREFIXES):
            return
        if ref.startswith(("http://", "https://", "//")):
            host = urlparse(("https:" + ref) if ref.startswith("//") else ref).hostname or ""
            if any(host.endswith(d) for d in EXTERNAL_OK):
                return
            externals.setdefault(host, []).append((page, attr, ref))
            return
        target = resolve(page, ref)
        if target is None:
            return
        key = (attr, str(target))
        if key in seen:
            return
        seen.add(key)
        if not target.exists():
            broken.append((page, attr, ref))

    for m in ATTR_RE.finditer(html):
        note_ref(m.group(1), m.group(2))

    for m in SRCSET_RE.finditer(html):
        for part in m.group(1).split(","):
            url = part.strip().split()[0] if part.strip() else ""
            note_ref("srcset", url)

    for m in CSS_URL_RE.finditer(html):
        note_ref("url()", m.group(1))


def main():
    broken: list[tuple[Path, str, str]] = []
    externals: dict[str, list] = {}
    pages = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"):
                continue
            pages += 1
            check(Path(root) / f, broken, externals)

    print(f"Scanned {pages} pages\n")

    if broken:
        print(f"BROKEN LOCAL REFS: {len(broken)}")
        # group by ref for readability
        by_ref: dict[str, list[Path]] = {}
        for p, attr, ref in broken:
            by_ref.setdefault(f"{attr}={ref}", []).append(p)
        for ref, pgs in sorted(by_ref.items(), key=lambda x: -len(x[1]))[:30]:
            print(f"  ({len(pgs):>3}x) {ref}")
            for pg in pgs[:3]:
                print(f"        on {pg.relative_to(SITE)}")
    else:
        print("BROKEN LOCAL REFS: 0  [OK]")

    print()
    if externals:
        print("EXTERNAL DEPENDENCIES (will fail offline):")
        for host, items in sorted(externals.items()):
            print(f"  {host}: {len(items)} refs (e.g. {items[0][2][:100]})")
    else:
        print("EXTERNAL DEPENDENCIES: 0")

    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
