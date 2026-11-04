"""Replace Divi's broken header (mobile-only) with a clean sticky desktop nav.
Idempotent. Safe to rerun after content changes."""
import os
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

NAV_CSS_START = "/* ==== SITE-NAV-V2 CSS START ==== */"
NAV_CSS_END = "/* ==== SITE-NAV-V2 CSS END ==== */"

NAV_HTML_START = "<!-- SITE-NAV-V2 START -->"
NAV_HTML_END = "<!-- SITE-NAV-V2 END -->"

NAV_CSS = f"""
{NAV_CSS_START}
html body #site-nav{{position:sticky;top:0;z-index:1000;background:#fff;border-bottom:1px solid #ece8df;font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
html body #site-nav .bar{{max-width:1360px;margin:0 auto;padding:16px clamp(20px,3vw,40px);display:flex;align-items:center;justify-content:space-between;gap:32px}}
html body #site-nav .brand{{display:flex;align-items:center;text-decoration:none;flex:0 0 auto}}
html body #site-nav .brand img{{height:34px;width:auto;display:block}}
html body #site-nav .menu{{display:flex;align-items:center;gap:clamp(20px,3vw,44px);list-style:none;margin:0;padding:0}}
html body #site-nav .menu li{{margin:0;padding:0;list-style:none}}
html body #site-nav .menu a{{display:inline-block;padding:8px 0;text-decoration:none;color:#0085c9;font-size:12px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;position:relative;transition:color .2s}}
html body #site-nav .menu a::after{{content:'';position:absolute;left:0;right:0;bottom:0;height:1px;background:#0085c9;transform:scaleX(0);transform-origin:left;transition:transform .25s ease}}
html body #site-nav .menu a:hover{{color:#006ba1}}
html body #site-nav .menu a:hover::after,html body #site-nav .menu a.active::after{{transform:scaleX(1)}}
html body #site-nav .nav-toggle{{display:none;background:none;border:0;padding:8px;cursor:pointer}}
html body #site-nav .nav-toggle span,html body #site-nav .nav-toggle span::before,html body #site-nav .nav-toggle span::after{{content:'';display:block;width:24px;height:2px;background:#0085c9;position:relative}}
html body #site-nav .nav-toggle span::before{{position:absolute;top:-7px}}
html body #site-nav .nav-toggle span::after{{position:absolute;top:7px}}

/* Hide Divi's original header entirely */
html body #main-header{{display:none !important}}
html body #page-container{{padding-top:0 !important}}
/* Remove any prior NAV-FIX we injected */
html body #et_mobile_nav_menu,html body .mobile_menu_bar,html body #top-menu{{display:none !important}}
/* Hide Divi slider left/right arrows site-wide (dots pagination stays) */
html body .et-pb-arrow-prev,html body .et-pb-arrow-next,html body .et_pb_slider .et-pb-arrow-prev,html body .et_pb_slider .et-pb-arrow-next{{display:none !important}}
/* Also hide Flickity carousel arrows (used by the mobile homes-carousel) */
html body .flickity-prev-next-button,html body .flickity-button.previous,html body .flickity-button.next,html body .homes-carousel .flickity-prev-next-button{{display:none !important}}
/* Hide Divi prev/next post navigation on project detail pages */
html body .et_pb_posts_nav,html body .nav-single,html body [class*="et_pb_post_nav"]{{display:none !important}}
/* Hide Divi's built-in divider modules (they render as dotted blue lines that clash with our layout) */
html body [class*="et_pb_divider"]{{display:none !important}}
/* Hide Divi gallery/portfolio pagination and force every item to render (no more "1 2 Next"). */
html body .et_pb_gallery_pagination,html body .et_pb_portofolio_pagination,html body .wp-pagenavi{{display:none !important}}
html body .et_pb_gallery .et_pb_gallery_item,html body .et_pb_gallery_items .et_pb_gallery_item{{display:block !important;opacity:1 !important;visibility:visible !important}}
/* Cap the featured hero image on individual project pages (desktop only) so it doesn't dominate the viewport */
@media (min-width:981px){{
  html body .et_pb_post_title .et_pb_title_featured_container{{height:600px !important;overflow:hidden !important}}
  html body .et_pb_post_title .et_pb_title_featured_container .et_pb_image_wrap{{width:100%;height:100%;display:block}}
  html body .et_pb_post_title .et_pb_title_featured_container img{{width:100% !important;height:100% !important;object-fit:cover !important;display:block !important}}
}}

@media (max-width:900px){{
  html body #site-nav .menu{{display:none;position:absolute;top:100%;left:0;right:0;background:#fff;flex-direction:column;align-items:stretch;padding:12px clamp(20px,3vw,40px) 20px;border-bottom:1px solid #ece8df;gap:4px}}
  html body #site-nav .menu.open{{display:flex}}
  html body #site-nav .menu a{{padding:14px 0;font-size:14px;letter-spacing:.12em}}
  html body #site-nav .nav-toggle{{display:block}}
  /* Shrink the huge Divi post title on individual project detail pages. Keep Divi's font/weight/color for style consistency with desktop. Centered with capped width so it wraps into a pyramid (longer top line, shorter bottom line). */
  html body .et_pb_post_title h1.entry-title,
  html body .et_pb_post_title_0 h1.entry-title,
  html body h1.entry-title{{font-size:30px !important;line-height:1.15 !important;text-align:center !important;max-width:20ch !important;margin-left:auto !important;margin-right:auto !important}}
  html body .et_pb_post_title,
  html body .et_pb_post_title .et_pb_title_container{{padding:18px 0 !important;text-align:center !important}}
}}
/* Mobile: project detail image grid = every image in 2-col grid with truly equal spacing (outer padding = inner column gap). Escape any parent Divi padding by pulling the grid to full viewport width, then apply matched 20px padding on all sides and 20px column-gap so the visual spacing is uniform. */
@media (max-width:680px){{
  html body .project-image-grid{{width:100vw !important;margin-left:calc(50% - 50vw) !important;margin-right:calc(50% - 50vw) !important;grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;column-gap:20px !important;row-gap:20px !important;padding:0 20px !important;box-sizing:border-box !important}}
  html body .project-image-grid figure.wp-block-image{{grid-column:span 1 !important;margin:0 !important;width:100% !important;max-width:100% !important}}
  html body .project-image-grid figure.wp-block-image>a{{display:block !important;width:100% !important}}
  html body .project-image-grid figure.wp-block-image img{{width:100% !important;height:220px !important;object-fit:cover !important;display:block !important}}
}}
{NAV_CSS_END}
"""

# Compute nav items (label -> path relative to site root)
NAV_ITEMS = [
    ("Projects", "projects/"),
    ("Services", "services/"),
    ("Service Areas", "service-areas/"),
    ("Guides", "guides/"),
    ("About", "about/"),
    ("Awards", "awards/"),
    ("Media", "media/"),
    ("Contact", "contact/"),
]


def depth_of(page_path: Path) -> int:
    """Path depth from site root (excluding index.html itself)."""
    rel = page_path.relative_to(SITE).parts
    return len(rel) - 1  # subtract index.html filename


def build_nav_html(page_path: Path, active_slug: str | None) -> str:
    # Use root-relative paths so nav works at any depth without recomputing.
    logo_href = "/"
    logo_src = "/wp-content/uploads/brand/palermo-logo-blue.png"
    items_html = ""
    for label, slug in NAV_ITEMS:
        href = "/" + slug
        cls = " class=\"active\"" if slug == active_slug else ""
        items_html += f'<li><a href="{href}"{cls}>{label}</a></li>'
    return (
        f'{NAV_HTML_START}\n'
        f'<header id="site-nav">'
        f'<div class="bar">'
        f'<a class="brand" href="{logo_href}"><img src="{logo_src}" alt="Palermo Homes"></a>'
        f'<button class="nav-toggle" aria-label="Menu" onclick="var m=document.querySelector(\'#site-nav .menu\');m.classList.toggle(\'open\')"><span></span></button>'
        f'<ul class="menu">{items_html}</ul>'
        f'</div>'
        f'</header>\n'
        f'{NAV_HTML_END}'
    )


def active_slug_for(page_path: Path) -> str | None:
    rel = page_path.relative_to(SITE)
    parts = rel.parts
    if len(parts) == 1:
        return None  # home
    first = parts[0]
    if first == "project":
        return "projects/"
    return f"{first}/"


def process_page(page_path: Path) -> bool:
    html = page_path.read_text(encoding="utf-8")

    # 1) Remove any prior NAV-FIX injection (from fix_desktop_nav.py)
    html = re.sub(r"/\* ==== NAV-FIX START ==== \*/.*?/\* ==== NAV-FIX END ==== \*/", "", html, flags=re.DOTALL)
    # 2) Remove any prior SITE-NAV-V2 CSS block
    if NAV_CSS_START in html:
        html = re.sub(re.escape(NAV_CSS_START) + r".*?" + re.escape(NAV_CSS_END), "", html, flags=re.DOTALL)
    # 3) Remove any prior SITE-NAV-V2 HTML block
    if NAV_HTML_START in html:
        html = re.sub(re.escape(NAV_HTML_START) + r".*?" + re.escape(NAV_HTML_END), "", html, flags=re.DOTALL)
    # 3a) Strip the Divi legacy mobile/slide/fullscreen menus. These were duplicated
    # from the About shell with relative hrefs like 'index.html' that resolve to the
    # current page instead of /about/. CSS hides them but Google still crawls the links.
    html = re.sub(r'<div class="et_slide_in_menu_container">.*?</div>\s*</div>', '', html, flags=re.DOTALL, count=1)
    html = re.sub(r'<div class="et_pb_fullscreen_nav_container">.*?</div>\s*</div>', '', html, flags=re.DOTALL, count=1)
    html = re.sub(r'<header[^>]*id="main-header"[^>]*>.*?</header>', '', html, flags=re.DOTALL, count=1)

    # 4) Inject CSS as its own <style> block right before </head>
    if "</head>" not in html:
        return False
    html = html.replace("</head>", f"<style>{NAV_CSS}</style></head>", 1)

    # 5) Inject nav HTML right after opening <body ...> tag
    body_m = re.search(r"(<body[^>]*>)", html)
    if not body_m:
        return False
    nav_html = build_nav_html(page_path, active_slug_for(page_path))
    html = html[: body_m.end()] + nav_html + html[body_m.end():]

    page_path.write_text(html, encoding="utf-8")
    return True


def main():
    count = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = Path(root) / f
            if process_page(p):
                count += 1
    print(f"Replaced nav on {count} pages")


if __name__ == "__main__":
    main()
