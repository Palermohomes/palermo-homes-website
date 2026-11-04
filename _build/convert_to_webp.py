"""Generate .webp companions for every JPEG, then rewrite <img> tags into <picture>.

Safety:
- Preserves original .jpg files (fallback for old browsers)
- Idempotent: skips <img> already inside a <picture>
- Skips external URLs (http/https/protocol-relative)
- Preserves all attributes on the original <img> tag
- Only touches .jpg/.jpeg; PNGs (logos, UI) untouched
"""
import re
import pathlib
from PIL import Image, ImageOps

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
WEBP_QUALITY = 82


def generate_webp():
    """Create .webp beside every .jpg/.jpeg. Skip if exists or fails."""
    n_new = 0
    n_skipped = 0
    jpg_bytes = 0
    webp_bytes = 0
    for jpg in list(SITE.rglob("*.jpg")) + list(SITE.rglob("*.jpeg")):
        webp = jpg.with_suffix(".webp")
        jpg_size = jpg.stat().st_size
        jpg_bytes += jpg_size
        if webp.exists():
            webp_bytes += webp.stat().st_size
            n_skipped += 1
            continue
        try:
            img = Image.open(jpg)
            img = ImageOps.exif_transpose(img)
            img.save(webp, "WebP", quality=WEBP_QUALITY, method=6)
            webp_bytes += webp.stat().st_size
            n_new += 1
        except Exception as e:
            print(f"  SKIP {jpg.relative_to(SITE)}: {e}")
    print(f"WebP generated: {n_new} new, {n_skipped} already existed")
    print(f"  JPG total:  {jpg_bytes/1024/1024:.1f} MB")
    print(f"  WebP total: {webp_bytes/1024/1024:.1f} MB")
    print(f"  Savings vs JPG: {(1-webp_bytes/max(1,jpg_bytes))*100:.0f}%")


IMG_RE = re.compile(r"<img\b([^>]*?)(/?)>", re.I | re.S)
SRC_RE = re.compile(r'\bsrc\s*=\s*["\']([^"\']+)["\']', re.I)
JPG_RE = re.compile(r"\.(jpe?g)(\?|$)", re.I)


def rewrite_html(html: str) -> tuple[str, int]:
    """Wrap each <img src="X.jpg"> in a <picture>.  Skip if already wrapped."""
    count = [0]

    def repl(m):
        tag = m.group(0)
        attrs = m.group(1)
        src_match = SRC_RE.search(attrs)
        if not src_match:
            return tag
        src = src_match.group(1)
        # Only convert local jpg/jpeg
        if not JPG_RE.search(src):
            return tag
        if src.startswith(("http://", "https://", "//")):
            return tag
        # Idempotency: check what's immediately before this match. If <picture> is open, skip.
        start = m.start()
        window = html[max(0, start - 200):start]
        if "<picture>" in window and "</picture>" not in window:
            return tag
        # Build WebP src (replace extension only in the last path segment)
        webp_src = JPG_RE.sub(r".webp\2", src)
        count[0] += 1
        return f'<picture><source srcset="{webp_src}" type="image/webp">{tag}</picture>'

    new_html = IMG_RE.sub(repl, html)
    return new_html, count[0]


def rewrite_all_html():
    files_touched = 0
    imgs_wrapped = 0
    for f in SITE.rglob("*.html"):
        t = f.read_text(encoding="utf-8")
        new, n = rewrite_html(t)
        if n > 0 and new != t:
            f.write_text(new, encoding="utf-8")
            files_touched += 1
            imgs_wrapped += n
    print(f"HTML rewritten: {files_touched} files, {imgs_wrapped} <img> tags wrapped")


if __name__ == "__main__":
    print("=== Step 1: Generating WebP files ===")
    generate_webp()
    print()
    print("=== Step 2: Rewriting <img> tags to <picture> ===")
    rewrite_all_html()
