"""Rewrite footer image/link paths from page-relative to root-relative so they
resolve correctly at any depth. Idempotent."""
import os
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

# Site-root paths that should be absolute (never depth-relative)
ROOT_PATHS = ("wp-content", "wp-includes", "fonts", "projects", "services",
              "about", "awards", "media", "contact", "project")

# `../` chain followed by one of the root paths. Inside quoted attributes
PATTERN = re.compile(
    r'(src|href)="((?:\.\./)+)(' + "|".join(ROOT_PATHS) + r')/'
)

# Same but for use in srcset lists / url() (no quote before the ../)
BARE = re.compile(r'((?:\.\./)+)(' + "|".join(ROOT_PATHS) + r')/')


def fix(html: str) -> tuple[str, int]:
    count = 0

    # 1) src=/href= attributes
    def attr_sub(m):
        nonlocal count
        count += 1
        return f'{m.group(1)}="/{m.group(3)}/'
    html = PATTERN.sub(attr_sub, html)

    # 2) srcset="...". Each URL rewritten independently
    def srcset_sub(m):
        nonlocal count
        def url_sub(u):
            nonlocal count
            count += 1
            return f'/{u.group(2)}/'
        return f'srcset="{BARE.sub(url_sub, m.group(1))}"'
    html = re.sub(r'srcset="([^"]+)"', srcset_sub, html)

    # 3) CSS url(...) refs. Inside <style> blocks and style="" attributes
    def css_sub(m):
        nonlocal count
        quote, raw = m.group(1), m.group(2)
        if raw.startswith(("http://", "https://", "//", "data:", "/")):
            return m.group(0)
        new = BARE.sub(lambda u: f'/{u.group(2)}/', raw)
        if new != raw:
            count += 1
        return f'url({quote}{new}{quote})'
    html = re.sub(r'url\(\s*(["\']?)([^"\')\s]+)\1\s*\)', css_sub, html)

    # 4) Cleanup: collapse any accidentally doubled paths (e.g. from a prior bad run)
    # Matches "/foo/bar.ext/foo/bar.ext" and reduces to "/foo/bar.ext"
    def dedupe(m):
        nonlocal count
        count += 1
        return m.group(1)
    html = re.sub(
        r'(/(?:' + "|".join(ROOT_PATHS) + r')/[^"\')\s]+?)\1',
        dedupe,
        html,
    )

    return html, count


def main():
    total_files = 0
    total_fixes = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = Path(root) / f
            html = p.read_text(encoding="utf-8")
            new_html, n = fix(html)
            if n > 0:
                p.write_text(new_html, encoding="utf-8")
                total_files += 1
                total_fixes += n
    print(f"Fixed {total_fixes} paths across {total_files} pages")


if __name__ == "__main__":
    main()
