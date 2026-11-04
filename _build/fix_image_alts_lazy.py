"""Post-build pass: fill empty img alt attributes with context-derived alt text,
and add loading="lazy" to below-the-fold images. Idempotent. Safe to rerun.

Rules for alt generation (strictly from filename + path context, no inventing):
- /project/<slug>/ gallery image -> "<Project name> custom home by Palermo Homes in <city>"
- Other img with alt="" where filename is palermo project photo -> similar derived
- Logos / brand marks -> "Palermo Homes" or "Palermo Homes logo"
- First img on a page (likely LCP/hero) gets loading="eager" fetchpriority="high"
- All subsequent images get loading="lazy" if not already set
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

# Map project slug -> (display name, city/area). From build_service_areas.py context
# and project_communities data. Only slugs we can verify from the directory listing.
PROJECT_META = {
    "1252":                ("Modern Lakeview Custom Home on Cabernet Way",      "West Kelowna"),
    "713":                 ("Custom Home on Eagle Summit Drive",                "Abbotsford"),
    "cabernet-2":          ("Luxury Modern Custom Home on Cabernet Way",        "West Kelowna"),
    "cabernet-3":          ("Modern Hillside Custom Home on Cabernet Way",      "West Kelowna"),
    "eagle-mountain-1":    ("Modern Custom Home on Mahogany Drive",             "Eagle Mountain, Abbotsford"),
    "eagle-mountain-2":    ("Luxury Mountain View Custom Home on Mahogany Drive","Eagle Mountain, Abbotsford"),
    "eagle-mountain-3":    ("Custom Home on Aquila Drive",                      "Eagle Mountain, Abbotsford"),
    "eagle-mountain-4":    ("Executive Modern Custom Home on Montana Place",    "Eagle Mountain, Abbotsford"),
    "eagle-mountain-5":    ("Hillside Walkout Custom Home on Eagle Peak Drive", "Eagle Mountain, Abbotsford"),
    "eagle-mountain-6":    ("Modern Family Custom Home on Eagle Summit Drive",  "Abbotsford"),
    "eagle-mountain-9":    ("Modern Valley View Custom Home on Verado Court",   "Eagle Mountain, Abbotsford"),
    "lakestone":           ("Custom Home on Ledgestone Road",                   "Lake Country"),
    "malbec-2":            ("Luxury Modern Custom Home on Malbec Place",        "West Kelowna"),
    "malbec-place-1":      ("Modern Lakeview Custom Home on Malbec Place",      "West Kelowna"),
    "touriga-place-1":     ("Modern Lakeview Custom Home on Touriga Place",     "West Kelowna"),
    "verado-court":        ("Custom Home on Verado Court",                      "Eagle Mountain, Abbotsford"),
    "vineyard-estates-3":  ("Luxury Custom Home in Vineyard Estates",           "West Kelowna"),
    "vineyard-estates-4":  ("Modern Hillside Custom Home in Vineyard Estates",  "West Kelowna"),
    "west-abbotsford":     ("Custom Home in West Abbotsford",                   "Abbotsford"),
}


def derive_alt_for(img_tag: str, project_slug: str | None) -> str | None:
    """Return a safe, context-derived alt string, or None if we can't."""
    src_m = re.search(r'src="([^"]*)"', img_tag)
    if not src_m:
        return None
    src = src_m.group(1).lower()
    # Logo variants
    if "palermo-logo" in src or "logolockup" in src or "pal_logo" in src:
        return "Palermo Homes"
    # Project gallery image (we have slug context)
    if project_slug and project_slug in PROJECT_META:
        name, city = PROJECT_META[project_slug]
        return f"{name} by Palermo Homes in {city}"
    # Awards / media / about page known assets by filename
    if "awards" in src or "award" in src:
        return "Palermo Homes award recognition"
    if "cabernet" in src:
        return "Palermo Homes custom build on Cabernet Way, West Kelowna"
    if "malbec" in src:
        return "Palermo Homes custom build on Malbec Place, West Kelowna"
    if "touriga" in src:
        return "Palermo Homes custom build on Touriga Place, West Kelowna"
    if "ledgestone" in src or "lakestone" in src:
        return "Palermo Homes custom build on Ledgestone Road, Lake Country"
    if "eagle" in src or "mahogany" in src or "verado" in src:
        return "Palermo Homes custom build on Eagle Mountain, Abbotsford"
    if "tcp_" in src:
        # Early project photos. Not always possible to attribute
        return "Palermo Homes custom home portfolio"
    return None


def process_file(path: Path) -> tuple[int, int]:
    """Returns (alts_filled, lazy_added)."""
    html = path.read_text(encoding="utf-8")
    orig = html
    # Derive project slug from path if under /project/<slug>/
    parts = path.relative_to(SITE).parts
    project_slug = parts[1] if len(parts) >= 2 and parts[0] == "project" else None

    alts_filled = 0
    lazy_added = 0
    first_img_seen = False

    def fix_img(m):
        nonlocal alts_filled, lazy_added, first_img_seen
        tag = m.group(0)
        # Skip images inside <head> / <script> / <noscript>. We only touch body-visible ones.
        # (regex context handles via outer sub, assume body for perf)
        # Alt handling
        if 'alt=""' in tag or 'alt=' not in tag:
            new_alt = derive_alt_for(tag, project_slug)
            if new_alt:
                if 'alt=""' in tag:
                    tag = tag.replace('alt=""', f'alt="{new_alt}"', 1)
                else:
                    tag = tag.replace("<img", f'<img alt="{new_alt}"', 1)
                alts_filled += 1
        # Lazy loading / fetchpriority
        if 'loading=' not in tag:
            if not first_img_seen:
                # Hero / LCP candidate. Eager + high priority
                tag = tag.replace("<img", '<img loading="eager" fetchpriority="high"', 1)
                first_img_seen = True
            else:
                tag = tag.replace("<img", '<img loading="lazy" decoding="async"', 1)
                lazy_added += 1
        elif not first_img_seen:
            first_img_seen = True
        return tag

    # Only process images in body (skip anything before <body>)
    body_m = re.search(r"<body[^>]*>", html)
    if not body_m:
        return (0, 0)
    body_start = body_m.end()
    body = html[body_start:]
    body_new = re.sub(r"<img\b[^>]*>", fix_img, body)
    html = html[:body_start] + body_new

    if html != orig:
        path.write_text(html, encoding="utf-8")
    return (alts_filled, lazy_added)


def main():
    total_alts = 0
    total_lazy = 0
    files = 0
    for p in SITE.rglob("index.html"):
        a, l = process_file(p)
        if a or l:
            files += 1
            total_alts += a
            total_lazy += l
    print(f"Processed {files} pages. Alts filled: {total_alts}. Lazy added: {total_lazy}.")


if __name__ == "__main__":
    main()
