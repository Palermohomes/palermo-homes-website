"""Ensure every page's hero image loads eagerly (not lazy) for best LCP.

Rules:
- "Hero" = the first large content image at the top of the page.
  * If it's an <img>: force loading="eager" fetchpriority="high", strip loading="lazy".
  * If the hero is a CSS background-image (inline style on a .*-hero wrapper):
    add <link rel="preload" as="image" href="..." fetchpriority="high"> in <head>.
- Skip brand logos (palermo-logo, logoLockup, pal_logo). They are small, not heroes.
- Non-hero images: ensure loading="lazy", strip fetchpriority="high".
- Also strip any contradictory attribute pairs left behind by earlier runs
  (e.g. loading="lazy" and fetchpriority="high" on the same tag).

Also removes title="..." when the title value is just the image file name or "default".
Idempotent.
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

LOGO_PATTERNS = ("palermo-logo", "logolockup", "pal_logo")


def is_logo(src: str) -> bool:
    low = src.lower()
    return any(p in low for p in LOGO_PATTERNS)


def strip_attr(tag: str, name: str) -> str:
    """Remove attribute from tag, idempotent."""
    return re.sub(r'\s+' + re.escape(name) + r'="[^"]*"', '', tag)


def set_attr(tag: str, name: str, value: str) -> str:
    """Set attribute to value, replacing if present."""
    if re.search(r'\s' + re.escape(name) + r'="', tag):
        return re.sub(r'\s' + re.escape(name) + r'="[^"]*"', f' {name}="{value}"', tag, count=1)
    return tag.replace("<img", f'<img {name}="{value}"', 1)


def dedupe_attr(tag: str, name: str) -> str:
    """Collapse duplicate attribute occurrences to the first."""
    attrs = re.findall(r'\s' + re.escape(name) + r'="([^"]*)"', tag)
    if len(attrs) <= 1:
        return tag
    # Keep first, strip the rest
    first = attrs[0]
    tag = re.sub(r'\s' + re.escape(name) + r'="[^"]*"', '', tag)
    return tag.replace("<img", f'<img {name}="{first}"', 1)


def clean_title(tag: str) -> str:
    """Remove title="..." when value is a filename or 'default'."""
    m = re.search(r'\stitle="([^"]*)"', tag)
    if not m:
        return tag
    title = m.group(1).strip().lower()
    if title == "default" or re.search(r"\.(jpe?g|png|webp|gif|svg)$", title) or (title.count(" ") == 0 and len(title) < 60):
        # looks like a filename or short slug. Strip it
        if re.search(r"\.(jpe?g|png|webp|gif|svg)$", title) or title == "default":
            return re.sub(r'\stitle="[^"]*"', '', tag, count=1)
    return tag


def find_hero_in_body(body: str) -> tuple[str, str, str] | None:
    """Returns (full_tag, src, kind) for the hero image.
    kind: 'img' (first non-logo <img>) or ('bg', url) if first visible section has an inline background-image.
    Returns None if nothing identifiable."""
    # Look for inline background-image: url('...') in a hero section (within first ~3000 chars of body).
    bg_m = re.search(r"background-image:\s*url\(['\"]?([^'\")]+)['\"]?\)", body[:5000])
    img_m = None
    for m in re.finditer(r"<img[^>]*>", body):
        tag = m.group(0)
        src_m = re.search(r'src="([^"]+)"', tag)
        if not src_m:
            continue
        if is_logo(src_m.group(1)):
            continue
        img_m = (tag, src_m.group(1), m.start())
        break
    # Decide which comes first in document order
    bg_pos = bg_m.start() if bg_m else 10**9
    img_pos = img_m[2] if img_m else 10**9
    if img_pos < bg_pos and img_m:
        return (img_m[0], img_m[1], "img")
    if bg_m:
        return ("", bg_m.group(1), "bg")
    if img_m:
        return (img_m[0], img_m[1], "img")
    return None


def ensure_preload(head: str, href: str) -> tuple[str, bool]:
    """Add <link rel="preload" as="image"> for href if not already in head. Returns (new_head, added)."""
    if f'rel="preload"' in head and f'href="{href}"' in head:
        return (head, False)
    tag = f'<link rel="preload" as="image" href="{href}" fetchpriority="high">\n'
    new_head = head.replace("</head>", tag + "</head>", 1)
    return (new_head, True)


def process(page: Path) -> dict:
    html = page.read_text(encoding="utf-8")
    orig = html
    body_m = re.search(r"<body[^>]*>", html)
    if not body_m:
        return {"url": "", "err": "no body"}
    body_start = body_m.end()
    head = html[:body_start]
    body = html[body_start:]

    hero = find_hero_in_body(body)
    if not hero:
        return {"url": "", "err": "no hero"}
    _, hero_src, hero_kind = hero

    # Rewrite every <img> in the body
    def rewrite_img(m):
        tag = m.group(0)
        tag = clean_title(tag)
        src_m = re.search(r'src="([^"]+)"', tag)
        if not src_m:
            return tag
        src = src_m.group(1)
        # Deduplicate possibly-duplicated attributes
        for attr in ("decoding", "loading", "fetchpriority"):
            tag = dedupe_attr(tag, attr)
        if is_logo(src):
            # Logos: no eager/preload, no fetchpriority. Allow lazy (nav logo in head is usually above fold but is tiny)
            tag = strip_attr(tag, "fetchpriority")
            tag = strip_attr(tag, "loading")
            # Nav logo stays as-is without loading hint (browser default eager, fine for small file)
            return tag
        if hero_kind == "img" and src == hero_src:
            # This is the hero: eager + high priority, no lazy
            tag = strip_attr(tag, "loading")
            tag = strip_attr(tag, "fetchpriority")
            tag = set_attr(tag, "loading", "eager")
            tag = set_attr(tag, "fetchpriority", "high")
            # Keep/set decoding
            if "decoding=" not in tag:
                tag = set_attr(tag, "decoding", "async")
            return tag
        # Non-hero content image: lazy, no fetchpriority
        tag = strip_attr(tag, "fetchpriority")
        if "loading=" not in tag:
            tag = set_attr(tag, "loading", "lazy")
        if "decoding=" not in tag:
            tag = set_attr(tag, "decoding", "async")
        return tag

    new_body = re.sub(r"<img\b[^>]*>", rewrite_img, body)

    # If the hero is a CSS background, ensure a preload link exists in head
    preload_added = False
    if hero_kind == "bg":
        head, preload_added = ensure_preload(head, hero_src)

    new_html = head + new_body
    if new_html != orig:
        page.write_text(new_html, encoding="utf-8")

    return {
        "page": page,
        "hero_src": hero_src,
        "hero_kind": hero_kind,
        "preload_added": preload_added,
    }


def main():
    rows = []
    for p in sorted(SITE.rglob("index.html")):
        r = process(p)
        if "err" in r:
            print(f"  SKIP {p}: {r['err']}")
            continue
        rows.append(r)

    # Verify + table
    print()
    print(f"{'URL':<60} | {'HERO IMAGE':<40} | {'loading':<8} | {'fetchpri':<8} | type")
    print("-" * 60 + "-+-" + "-" * 40 + "-+-" + "-" * 8 + "-+-" + "-" * 8 + "-+-------")
    lazy_heroes = []
    for r in rows:
        p = r["page"]
        url = "/" + str(p.relative_to(SITE)).replace("\\", "/").replace("index.html", "")
        html = p.read_text(encoding="utf-8")
        body_m = re.search(r"<body[^>]*>", html)
        body = html[body_m.end():]
        hero_src = r["hero_src"]
        kind = r["hero_kind"]
        loading = fp = "n/a"
        if kind == "img":
            # Find the hero img tag again
            esc = re.escape(hero_src)
            tag_m = re.search(r'<img[^>]*src="' + esc + r'"[^>]*>', body)
            if tag_m:
                tag = tag_m.group(0)
                l = re.search(r'loading="([^"]*)"', tag)
                f = re.search(r'fetchpriority="([^"]*)"', tag)
                loading = l.group(1) if l else "(none)"
                fp = f.group(1) if f else "(none)"
            if loading == "lazy":
                lazy_heroes.append(url)
        else:
            # Background: check preload link in head
            head = html[:body_m.end()]
            if f'href="{hero_src}"' in head and 'rel="preload"' in head:
                loading = "preload"
                fp = "high" if 'fetchpriority="high"' in head else "(none)"
            else:
                loading = "(no preload!)"
                lazy_heroes.append(url)
        src_short = hero_src.split("/")[-1][:38]
        print(f"{url:<60} | {src_short:<40} | {loading:<8} | {fp:<8} | {kind}")
    print()
    print(f"Total pages: {len(rows)}")
    if lazy_heroes:
        print(f"LAZY HEROES ({len(lazy_heroes)}): {lazy_heroes}")
        return 1
    print("All heroes eager / preloaded. OK.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
