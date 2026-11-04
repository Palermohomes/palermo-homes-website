"""Insert Services menu item into every page's nav, right after Projects.
Idempotent. Safe to rerun."""
import os
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

SERVICES_LI_MARKER = 'menu-item-services-v2'

# Match the Projects <li>, capture href value so we can determine depth
PROJ_RE = re.compile(
    r'(<li class="menu-item[^"]*menu-item-818"><a href=")([^"]*projects/index\.html)("[^>]*>Projects</a></li>)'
)


def insert_services(html: str) -> tuple[str, bool]:
    if SERVICES_LI_MARKER in html:
        return html, False  # already inserted
    m = PROJ_RE.search(html)
    if not m:
        return html, False
    projects_href = m.group(2)
    # e.g. "projects/index.html" -> "" (root) ; "../projects/index.html" -> "../"
    prefix = projects_href[: projects_href.rfind("projects/")]
    services_href = f"{prefix}services/index.html"
    new_li = (
        f'<li class="menu-item menu-item-type-post_type menu-item-object-page {SERVICES_LI_MARKER}">'
        f'<a href="{services_href}">Services</a></li>'
    )
    inserted = m.group(0) + new_li
    return html[: m.start()] + inserted + html[m.end():], True


def main():
    count = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = Path(root) / f
            html = p.read_text(encoding="utf-8")
            new_html, changed = insert_services(html)
            if changed:
                p.write_text(new_html, encoding="utf-8")
                count += 1
                print(f"  + {p.relative_to(SITE)}")
    print(f"Updated {count} pages")


if __name__ == "__main__":
    main()
