"""
Static mirror of palermohomes.com for Netlify.
Downloads all pages listed in the sitemaps + every asset they reference,
strips WordPress bloat, rewrites URLs to local relative paths.
"""
from __future__ import annotations

import os
import re
import sys
import time
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
BUILD = ROOT / "_build"
CACHE = BUILD / "cache"
CACHE.mkdir(parents=True, exist_ok=True)

BASE = "https://palermohomes.com"
HOST = "palermohomes.com"

PAGES = [
    "https://palermohomes.com/",
    "https://palermohomes.com/about/",
    "https://palermohomes.com/awards/",
    "https://palermohomes.com/contact/",
    "https://palermohomes.com/media/",
    "https://palermohomes.com/projects/",
    "https://palermohomes.com/project/1252/",
    "https://palermohomes.com/project/713/",
    "https://palermohomes.com/project/cabernet-2/",
    "https://palermohomes.com/project/cabernet-3/",
    "https://palermohomes.com/project/eagle-mountain-1/",
    "https://palermohomes.com/project/eagle-mountain-2/",
    "https://palermohomes.com/project/eagle-mountain-3/",
    "https://palermohomes.com/project/eagle-mountain-4/",
    "https://palermohomes.com/project/eagle-mountain-5/",
    "https://palermohomes.com/project/eagle-mountain-6/",
    "https://palermohomes.com/project/eagle-mountain-9/",
    "https://palermohomes.com/project/lakestone/",
    "https://palermohomes.com/project/malbec-2/",
    "https://palermohomes.com/project/malbec-place-1/",
    "https://palermohomes.com/project/touriga-place-1/",
    "https://palermohomes.com/project/verado-court-2/",
    "https://palermohomes.com/project/verado-court/",
    "https://palermohomes.com/project/vineyard-estates-1/",
    "https://palermohomes.com/project/vineyard-estates-3/",
    "https://palermohomes.com/project/vineyard-estates-4/",
    "https://palermohomes.com/project/west-abbotsford/",
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept": "*/*"})

# Track what we've downloaded so we don't re-do work
downloaded_assets: dict[str, str] = {}   # abs_url -> local relative path (from site root)
asset_queue: list[str] = []
seen_asset_urls: set[str] = set()


def cache_path_for(url: str) -> Path:
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()
    return CACHE / h


def http_get(url: str, binary: bool = False):
    cp = cache_path_for(url)
    if cp.exists():
        data = cp.read_bytes()
        return data if binary else data.decode("utf-8", errors="replace")
    for attempt in range(3):
        try:
            r = session.get(url, timeout=45)
            if r.status_code == 200:
                cp.write_bytes(r.content)
                return r.content if binary else r.text
            print(f"  [{r.status_code}] {url}")
            return None
        except Exception as e:
            print(f"  retry {attempt+1}: {url} ({e})")
            time.sleep(1.5 * (attempt + 1))
    return None


def url_to_local_asset_path(abs_url: str) -> str:
    """Map an absolute palermohomes.com asset URL to a local path under site/.
    Strips query strings entirely for clean filenames."""
    p = urlparse(abs_url)
    path = unquote(p.path).lstrip("/")
    if not path:
        path = "index"
    # WordPress uploads / plugins / themes / includes -> preserve structure
    # But some URLs have no extension (rare); leave as-is
    return path.replace("\\", "/")


def url_to_local_page_path(page_url: str) -> str:
    """Homepage -> index.html; /about/ -> about/index.html; /project/xxx/ -> project/xxx/index.html"""
    p = urlparse(page_url)
    path = p.path.strip("/")
    if not path:
        return "index.html"
    return f"{path}/index.html"


ASSET_EXTS = {
    ".css", ".js", ".mjs", ".json", ".map",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".avif",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp4", ".webm", ".mov", ".m4v", ".ogg", ".mp3", ".wav",
    ".pdf", ".zip",
    ".webmanifest",
}


def queue_asset(abs_url: str, force: bool = False) -> str | None:
    """Register an asset for download and return its site-relative path.
    Rejects URLs that don't look like assets (no extension, wp-json, xmlrpc, etc.)
    unless force=True."""
    if not abs_url:
        return None
    p = urlparse(abs_url)
    if not p.scheme.startswith("http"):
        return None
    path_lower = p.path.lower()
    # Hard rejects
    if any(bad in path_lower for bad in ("/wp-json", "xmlrpc.php", "/feed", "wp-login")):
        return None
    ext = os.path.splitext(p.path)[1].lower()
    # Special-case: Google Fonts CSS endpoint has no extension AND needs query preserved
    is_gfont_css = (p.netloc == "fonts.googleapis.com" and path_lower.startswith("/css"))
    if not force and not is_gfont_css and ext not in ASSET_EXTS:
        return None

    if is_gfont_css:
        # keep query in the storage key so different font families become different files
        clean = f"{p.scheme}://{p.netloc}{p.path}?{p.query}"
        h = hashlib.sha1(clean.encode()).hexdigest()[:10]
        local = f"fonts/googleapis-{h}.css"
    else:
        clean = f"{p.scheme}://{p.netloc}{p.path}"
        if p.netloc.endswith(HOST):
            local = url_to_local_asset_path(clean)
        elif p.netloc in ("fonts.gstatic.com",):
            local = "fonts/gstatic" + p.path
        else:
            local = "vendor/" + p.netloc + p.path
    local = local.replace("//", "/").lstrip("/")

    if clean not in seen_asset_urls:
        seen_asset_urls.add(clean)
        asset_queue.append(clean)
        downloaded_assets[clean] = local
    return downloaded_assets[clean]


def make_relative(from_page_path: str, to_local_path: str) -> str:
    """from_page_path is e.g. 'about/index.html', to_local_path is 'wp-content/uploads/x.jpg'.
    Returns a relative URL from the page to the asset."""
    from_dir = Path(from_page_path).parent
    to_path = Path(to_local_path)
    try:
        rel = os.path.relpath(to_path, from_dir).replace("\\", "/")
    except ValueError:
        rel = to_local_path
    return rel


def rewrite_internal_link(href: str, from_page_path: str) -> str:
    """Rewrite palermohomes.com page/asset links to relative local paths.
    Preserves fragments and mailto/tel/etc."""
    if not href:
        return href
    if href.startswith(("mailto:", "tel:", "javascript:", "#", "data:")):
        return href
    abs_url = urljoin(BASE + "/", href)
    p = urlparse(abs_url)
    if not p.netloc.endswith(HOST):
        return href  # external link. Leave as-is
    fragment = f"#{p.fragment}" if p.fragment else ""
    path = p.path
    # is this a known page?
    canonical = f"https://{HOST}{path}"
    if not canonical.endswith("/") and not Path(path).suffix:
        canonical += "/"
    if canonical in PAGES:
        target = url_to_local_page_path(canonical)
        return make_relative(from_page_path, target) + fragment
    # is it an asset we've queued?
    clean = f"https://{HOST}{path}"
    if clean in downloaded_assets:
        return make_relative(from_page_path, downloaded_assets[clean]) + fragment
    # Looks like an asset link (has recognized extension) but not yet queued -> queue it
    ext = Path(path).suffix.lower()
    if ext in ASSET_EXTS:
        local = queue_asset(clean)
        if local:
            return make_relative(from_page_path, local) + fragment
    # Unknown internal link. Best effort: point to the path with trailing slash
    if path.startswith("/") and not ext:
        # unknown WP page; leave as absolute-root so Netlify _redirects can catch
        return path + fragment
    return href


CSS_URL_RE = re.compile(rb'url\((["\']?)([^"\')]+)\1\)')
CSS_IMPORT_RE = re.compile(rb'@import\s+(?:url\()?["\']([^"\']+)["\']\)?', re.I)


def process_css(css_bytes: bytes, css_url: str, css_local_path: str) -> bytes:
    """Rewrite url(...) and @import in CSS to local paths and queue those assets."""
    def repl_url(m: re.Match) -> bytes:
        quote = m.group(1)
        raw = m.group(2).decode("utf-8", errors="replace").strip()
        if raw.startswith(("data:", "#")):
            return m.group(0)
        # strip query string / fragment
        raw_clean = raw.split("?", 1)[0].split("#", 1)[0]
        if not raw_clean:
            return m.group(0)
        abs_url = urljoin(css_url, raw_clean)
        local = queue_asset(abs_url)
        if not local:
            return m.group(0)
        rel = make_relative(css_local_path, local)
        q = quote.decode() if quote else ""
        return f"url({q}{rel}{q})".encode("utf-8")

    def repl_import(m: re.Match) -> bytes:
        raw = m.group(1).decode("utf-8", errors="replace").strip()
        raw_clean = raw.split("?", 1)[0].split("#", 1)[0]
        abs_url = urljoin(css_url, raw_clean)
        local = queue_asset(abs_url)
        if not local:
            return m.group(0)
        rel = make_relative(css_local_path, local)
        return f'@import "{rel}"'.encode("utf-8")

    css_bytes = CSS_IMPORT_RE.sub(repl_import, css_bytes)
    css_bytes = CSS_URL_RE.sub(repl_url, css_bytes)
    return css_bytes


def is_wp_bloat_link(tag) -> bool:
    """Detect head <link> tags that are pure WordPress noise (safe to remove)."""
    rel = " ".join(tag.get("rel") or []).lower()
    href = (tag.get("href") or "").lower()
    if rel in {"pingback", "wlwmanifest", "edituri", "https://api.w.org/", "alternate", "shortlink", "profile"}:
        if rel == "alternate":
            if tag.get("hreflang"):
                return False
            typ = (tag.get("type") or "").lower()
            if typ in {"application/rss+xml", "application/atom+xml", "application/json+oembed", "text/xml+oembed", "application/json"}:
                return True
            return False
        return True
    if "xmlrpc.php" in href or "wp-json" in href or "oembed" in href or "wlwmanifest" in href:
        return True
    return False


def strip_wp_bloat(soup: BeautifulSoup):
    # Remove emoji scripts + styles
    for s in soup.find_all("script"):
        text = (s.string or "").lower()
        src = (s.get("src") or "").lower()
        if "wp-emoji" in src or "concatemoji" in text or "wpemojisettings" in text:
            s.decompose()
            continue
    for s in soup.find_all("style"):
        css = (s.string or "").lower()
        if "img.wp-smiley" in css or "img.emoji" in css:
            s.decompose()
            continue
    # Remove RSD, wlwmanifest, pingback, oembed, wp-json links
    for l in list(soup.find_all("link")):
        if is_wp_bloat_link(l):
            l.decompose()
    # Remove generator meta
    for m in soup.find_all("meta", attrs={"name": "generator"}):
        m.decompose()
    # Remove HTML comments (WP leaves lots)
    for c in list(soup.find_all(string=lambda t: isinstance(t, Comment))):
        # keep conditional comments just in case
        if "if IE" in c or "endif" in c:
            continue
        c.extract()
    # Remove wp-block-library duplicate / classic-theme styles that only load block editor styles no theme needs
    # (safer to keep. We only remove verifiable bloat)


def strip_query(u: str) -> str:
    return u.split("?", 1)[0].split("#", 1)[0]


def process_page(page_url: str) -> tuple[str, str] | None:
    print(f"[page] {page_url}")
    html = http_get(page_url)
    if html is None:
        print(f"  FAILED: {page_url}")
        return None
    soup = BeautifulSoup(html, "lxml")
    local_page_path = url_to_local_page_path(page_url)

    strip_wp_bloat(soup)

    # First pass: queue all assets and rewrite tag attrs
    # <link href>: only real asset rels. Canonical/alternate/next/prev are page metadata
    ASSET_LINK_RELS = {
        "stylesheet", "icon", "shortcut", "shortcut icon",
        "apple-touch-icon", "apple-touch-icon-precomposed",
        "mask-icon", "manifest", "preload", "modulepreload",
        "prefetch", "subresource",
    }
    for l in soup.find_all("link"):
        rel = " ".join(l.get("rel") or []).lower().strip()
        if rel not in ASSET_LINK_RELS:
            # canonical / alternate / dns-prefetch / preconnect / next / prev / etc.
            # rewrite href only if it's a same-host PAGE link
            href = l.get("href")
            if href and rel in ("next", "prev", "canonical", "alternate"):
                # canonical/alternate we leave absolute for SEO; next/prev we can localize
                if rel in ("next", "prev"):
                    l["href"] = rewrite_internal_link(href, local_page_path)
            continue
        href = l.get("href")
        if not href:
            continue
        abs_url = urljoin(page_url, href)
        p = urlparse(abs_url)
        if p.netloc.endswith(HOST) or p.netloc in ("fonts.googleapis.com", "fonts.gstatic.com"):
            # keep query for gfont css; drop for everything else
            if p.netloc == "fonts.googleapis.com":
                local = queue_asset(abs_url)
            else:
                local = queue_asset(strip_query(abs_url))
            if local:
                l["href"] = make_relative(local_page_path, local)

    # <script src>
    for s in soup.find_all("script"):
        src = s.get("src")
        if not src:
            continue
        abs_url = urljoin(page_url, src)
        p = urlparse(abs_url)
        if p.netloc.endswith(HOST):
            clean = strip_query(abs_url)
            local = queue_asset(clean)
            if local:
                s["src"] = make_relative(local_page_path, local)

    # <img src / srcset / data-src / data-lazy-src>
    for img in soup.find_all(["img", "source"]):
        for attr in ("src", "data-src", "data-lazy-src", "data-original"):
            v = img.get(attr)
            if v:
                abs_url = urljoin(page_url, v)
                if urlparse(abs_url).netloc.endswith(HOST):
                    clean = strip_query(abs_url)
                    local = queue_asset(clean)
                    if local:
                        img[attr] = make_relative(local_page_path, local)
        for attr in ("srcset", "data-srcset", "data-lazy-srcset"):
            v = img.get(attr)
            if not v:
                continue
            new_parts = []
            for part in v.split(","):
                part = part.strip()
                if not part:
                    continue
                bits = part.split()
                u = bits[0]
                abs_url = urljoin(page_url, u)
                if urlparse(abs_url).netloc.endswith(HOST):
                    clean = strip_query(abs_url)
                    local = queue_asset(clean)
                    if local:
                        bits[0] = make_relative(local_page_path, local)
                new_parts.append(" ".join(bits))
            img[attr] = ", ".join(new_parts)

    # og:image, twitter:image, msapplication-TileImage
    IMAGE_META_KEYS = {
        "og:image", "og:image:url", "og:image:secure_url",
        "twitter:image", "twitter:image:src",
        "msapplication-tileimage",
    }
    for m in soup.find_all("meta"):
        prop = (m.get("property") or m.get("name") or "").lower()
        if prop in IMAGE_META_KEYS:
            v = m.get("content")
            if v:
                abs_url = urljoin(page_url, v)
                if urlparse(abs_url).netloc.endswith(HOST):
                    clean = strip_query(abs_url)
                    local = queue_asset(clean)
                    if local:
                        m["content"] = make_relative(local_page_path, local)

    # background style attributes
    for el in soup.find_all(style=True):
        style = el["style"]
        def repl(m):
            u = m.group(2)
            if u.startswith("data:"):
                return m.group(0)
            u_clean = u.split("?", 1)[0].split("#", 1)[0]
            abs_url = urljoin(page_url, u_clean)
            if urlparse(abs_url).netloc.endswith(HOST):
                local = queue_asset(abs_url)
                if local:
                    rel = make_relative(local_page_path, local)
                    return f"url({m.group(1)}{rel}{m.group(1)})"
            return m.group(0)
        el["style"] = re.sub(r'url\((["\']?)([^"\')]+)\1\)', repl, style)

    # Inline <style> tags. Rewrite url()
    for st in soup.find_all("style"):
        if not st.string:
            continue
        css = st.string.encode("utf-8")
        css = process_css(css, page_url, local_page_path)
        st.string.replace_with(css.decode("utf-8", errors="replace"))

    # Second pass: rewrite <a href> internal links
    for a in soup.find_all("a"):
        href = a.get("href")
        if not href:
            continue
        a["href"] = rewrite_internal_link(href, local_page_path)

    # Form actions: search form points at homepage (harmless), contact form posts to WP.
    # Neutralize both so nothing 404s. User will wire Netlify Forms later.
    for f in soup.find_all("form"):
        action = f.get("action") or ""
        if HOST in action:
            # search form -> keep as # to disable; contact form -> mark for Netlify wiring
            classes = " ".join(f.get("class") or [])
            if "et-search-form" in classes:
                f["action"] = "#"
            elif "et_pb_contact_form" in classes:
                f["action"] = "#"
                f["data-needs-netlify-forms"] = "true"
            else:
                f["action"] = "#"

    # Preserve Yoast/schema.org JSON-LD absolute URLs (SEO requires absolute URLs
    # in structured data). Swap those blocks out with placeholders before the
    # text-substitution pass, then restore them.
    ld_json_blocks: list[str] = []
    for s in soup.find_all("script", type="application/ld+json"):
        ld_json_blocks.append(str(s))

    html_str = str(soup)

    placeholders: dict[str, str] = {}
    for i, block in enumerate(ld_json_blocks):
        ph = f"__LDJSON_PLACEHOLDER_{i}__"
        placeholders[ph] = block
        html_str = html_str.replace(block, ph, 1)

    # Final text pass: catch URL strings baked into inline JSON/scripts.
    # Handles plain and JSON-escaped forms separately so any mix of slashes matches.
    # Output: ROOT-RELATIVE paths so JS-loaded URLs resolve identically at any depth.
    def make_rewriter(escaped: bool):
        def rewrite(match: re.Match) -> str:
            raw = match.group(0).replace("\\/", "/") if escaped else match.group(0)
            abs_url = raw
            clean = strip_query(abs_url)
            ext = os.path.splitext(urlparse(clean).path)[1].lower()
            if ext in ASSET_EXTS and clean not in downloaded_assets:
                queue_asset(clean)
            if clean in downloaded_assets:
                root_rel = "/" + downloaded_assets[clean]
            else:
                root_rel = urlparse(abs_url).path
            return root_rel.replace("/", "\\/") if escaped else root_rel
        return rewrite

    # Unescaped: https://palermohomes.com/wp-content/...
    html_str = re.sub(
        r'https://palermohomes\.com/(?:wp-content|wp-includes)/[^\s"\'<>)]+',
        make_rewriter(escaped=False),
        html_str,
    )
    # JSON-escaped: https:\/\/palermohomes.com\/wp-content\/...
    html_str = re.sub(
        r'https:\\/\\/palermohomes\.com\\/(?:wp-content|wp-includes)(?:\\/[^\s"\'<>)\\]+)+',
        make_rewriter(escaped=True),
        html_str,
    )

    for ph, block in placeholders.items():
        html_str = html_str.replace(ph, block, 1)

    return local_page_path, html_str


def write_page(local_path: str, html: str):
    out_file = OUT / local_path
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")


def download_assets():
    """Drain the asset queue; recursively process CSS assets to pick up their url() references."""
    idx = 0
    while idx < len(asset_queue):
        url = asset_queue[idx]
        idx += 1
        local = downloaded_assets[url]
        out_file = OUT / local
        if out_file.exists():
            continue
        data = http_get(url, binary=True)
        if data is None:
            print(f"  asset FAILED: {url}")
            continue
        out_file.parent.mkdir(parents=True, exist_ok=True)
        # CSS: rewrite inner urls
        if local.lower().endswith(".css") or (url.lower().endswith(".css")):
            data = process_css(data, url, local)
        out_file.write_bytes(data)
        if idx % 25 == 0:
            print(f"  ...downloaded {idx} assets so far ({len(asset_queue)} queued)")


def write_netlify_config():
    # _redirects: map trailing-slash URLs to the /index.html files (Netlify serves them
    # automatically, but this makes "pretty URLs" bulletproof).
    redirects = OUT / "_redirects"
    redirects.write_text(
        "# clean-URL redirects (Netlify auto-handles /path/ -> /path/index.html but keep explicit)\n"
        "/home              /                    301\n",
        encoding="utf-8",
    )
    # netlify.toml with basic headers for static asset caching
    (OUT / "netlify.toml").write_text(
        """[build]
publish = "."

[[headers]]
  for = "/wp-content/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.css"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.js"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
""",
        encoding="utf-8",
    )


def main():
    # Pass 1: fetch every page HTML, queue assets, get rewritten HTML back
    processed: list[tuple[str, str]] = []
    for url in PAGES:
        result = process_page(url)
        if result:
            processed.append(result)

    # Pass 2: download the entire asset queue (which grows as we process CSS)
    print(f"\n[assets] {len(asset_queue)} queued initially")
    download_assets()
    print(f"[assets] final total: {len(asset_queue)}")

    # Pass 3: re-run the anchor rewriter now that ALL assets are known
    # (some anchor links may point to assets. E.g. PDF downloads)
    print("\n[pages] second pass. Anchor rewrites with full asset map")
    final_pages: list[tuple[str, str]] = []
    for url in PAGES:
        result = process_page(url)
        if result:
            final_pages.append(result)

    for local_path, html in final_pages:
        write_page(local_path, html)
        print(f"  wrote {local_path}")

    # Any late CSS-referenced assets
    print(f"\n[assets] final drain. Queue is now {len(asset_queue)}")
    download_assets()

    write_netlify_config()

    print(f"\nDone. Wrote {len(final_pages)} pages + {len(asset_queue)} assets to {OUT}")


if __name__ == "__main__":
    main()
