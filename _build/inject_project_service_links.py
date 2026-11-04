"""Inject a 'Built in [city]' link block into each project page, pointing to
the service area page where that project is located. Compounds internal linking
authority to service area pages.

Injects INSIDE #et-main-area (right before its closing </div>) so the block
inherits the main content container styling and renders aligned with the rest
of the page.

Idempotent. Safe to rerun. Uses markers so re-running replaces cleanly."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

MARKER_START = "<!-- PROJ-SVC-LINK START -->"
MARKER_END = "<!-- PROJ-SVC-LINK END -->"

# Map each project slug to (service_area_slug, service_area_name, neighborhood_slug?)
PROJECT_MAP = {
    "1252": ("west-kelowna", "West Kelowna", None),
    "713":  ("lower-mainland", "the Lower Mainland", None),
    "cabernet-2": ("west-kelowna", "West Kelowna", None),
    "cabernet-3": ("west-kelowna", "West Kelowna", None),
    "eagle-mountain-1": ("lower-mainland", "the Lower Mainland", "eagle-mountain"),
    "eagle-mountain-2": ("lower-mainland", "the Lower Mainland", "eagle-mountain"),
    "eagle-mountain-3": ("lower-mainland", "the Lower Mainland", "eagle-mountain"),
    "eagle-mountain-4": ("lower-mainland", "the Lower Mainland", "eagle-mountain"),
    "eagle-mountain-5": ("lower-mainland", "the Lower Mainland", "eagle-mountain"),
    "eagle-mountain-6": ("lower-mainland", "the Lower Mainland", "eagle-mountain"),
    "eagle-mountain-9": ("lower-mainland", "the Lower Mainland", "eagle-mountain"),
    "lakestone": ("lake-country", "Lake Country", None),
    "malbec-2": ("west-kelowna", "West Kelowna", None),
    "malbec-place-1": ("west-kelowna", "West Kelowna", None),
    "touriga-place-1": ("west-kelowna", "West Kelowna", None),
    "verado-court": ("lower-mainland", "the Lower Mainland", "eagle-mountain"),
    "vineyard-estates-3": ("west-kelowna", "West Kelowna", None),
    "vineyard-estates-4": ("west-kelowna", "West Kelowna", None),
    "west-abbotsford": ("lower-mainland", "the Lower Mainland", None),
}

CSS_START = "/* ==== PROJ-SVC-LINK CSS START ==== */"
CSS_END = "/* ==== PROJ-SVC-LINK CSS END ==== */"

CSS = f"""
{CSS_START}
html body #et-main-area .proj-svc-link{{background:#0085c9;padding:72px 0;margin:-30px 0 0;font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;width:100vw;position:relative;left:50%;right:50%;margin-left:-50vw;margin-right:-50vw;overflow:hidden}}
html body #et-main-area .proj-svc-link::before{{content:"";position:absolute;top:0;right:0;width:40%;height:100%;background:linear-gradient(135deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.06) 100%);pointer-events:none}}
html body #et-main-area .proj-svc-link .wrap{{max-width:1200px;margin:0 auto;padding:0 clamp(24px,5vw,48px);display:flex;align-items:center;justify-content:space-between;gap:48px;flex-wrap:wrap;box-sizing:border-box;position:relative;z-index:1}}
html body #et-main-area .proj-svc-link .txt{{flex:1;min-width:300px;text-align:left;max-width:720px}}
html body #et-main-area .proj-svc-link .lab{{font-size:13px;letter-spacing:.3em;text-transform:uppercase;color:#fff;font-weight:600;margin:0 0 20px;padding:0;font-family:'Inter',system-ui,sans-serif}}
html body #et-main-area .proj-svc-link .head{{font-size:34px;line-height:1.15;font-weight:600;color:#fff;margin:0 0 16px;padding:0;font-family:'Inter',system-ui,sans-serif;letter-spacing:-.015em}}
html body #et-main-area .proj-svc-link .msg{{font-size:17px;color:rgba(255,255,255,.92);margin:0;padding:0;line-height:1.6;font-weight:400;font-family:'Inter',system-ui,sans-serif}}
html body #et-main-area .proj-svc-link .msg a{{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.5);font-weight:500;transition:border-color .2s}}
html body #et-main-area .proj-svc-link .msg a:hover{{border-bottom-color:#fff}}
html body #et-main-area .proj-svc-link .cta{{flex-shrink:0}}
html body #et-main-area .proj-svc-link .cta a{{display:inline-flex;align-items:center;gap:12px;background:#fff;color:#0085c9;font-size:14px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:18px 34px;text-decoration:none;border-radius:999px;transition:background .2s,color .2s,transform .2s,box-shadow .2s;font-family:'Inter',system-ui,sans-serif;line-height:1.2;box-shadow:0 4px 14px rgba(0,0,0,.1)}}
html body #et-main-area .proj-svc-link .cta a::after{{content:"\\2192";font-size:18px;font-weight:400;letter-spacing:0;transition:transform .2s;line-height:1}}
html body #et-main-area .proj-svc-link .cta a:hover{{background:#1a1d21;color:#fff;transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,.18)}}
html body #et-main-area .proj-svc-link .cta a:hover::after{{transform:translateX(4px)}}
@media (max-width:900px){{
  html body #et-main-area .proj-svc-link{{padding:56px 0}}
  html body #et-main-area .proj-svc-link .head{{font-size:28px}}
  html body #et-main-area .proj-svc-link .wrap{{gap:32px}}
}}
@media (max-width:640px){{
  html body #et-main-area .proj-svc-link{{padding:44px 24px;margin:-15px 0 0;width:auto;left:auto;right:auto;margin-left:0;margin-right:0;box-sizing:border-box;max-width:100%}}
  html body #et-main-area .proj-svc-link .wrap{{flex-direction:column;align-items:flex-start;gap:28px;padding:0;max-width:100%}}
  html body #et-main-area .proj-svc-link .txt{{min-width:0;width:100%;max-width:100%}}
  html body #et-main-area .proj-svc-link .lab{{font-size:12px;letter-spacing:.26em;margin:0 0 16px}}
  html body #et-main-area .proj-svc-link .head{{font-size:24px;line-height:1.2;margin:0 0 12px;letter-spacing:-.01em}}
  html body #et-main-area .proj-svc-link .msg{{font-size:16px;line-height:1.55;word-wrap:break-word;overflow-wrap:break-word}}
  html body #et-main-area .proj-svc-link .cta{{width:100%}}
  html body #et-main-area .proj-svc-link .cta a{{display:flex;justify-content:center;padding:16px 28px;font-size:13px;letter-spacing:.08em;max-width:100%;white-space:normal;box-sizing:border-box;width:100%}}
}}
{CSS_END}
"""


def build_block(svc_slug, svc_name, hood_slug):
    """Return the HTML block for a project page's service area link."""
    svc_href = f"/service-areas/{svc_slug}/"
    headline = f"Custom homes in {svc_name}"
    if hood_slug:
        hood_href = f"/neighborhoods/{hood_slug}/"
        hood_name = hood_slug.replace("-", " ").title()
        msg = (
            f'A custom home in '
            f'<a href="{hood_href}">{hood_name}</a>, part of our '
            f'<a href="{svc_href}">{svc_name}</a> service area. '
            f'See more of our work in the region.'
        )
    else:
        msg = (
            f'A custom home in our '
            f'<a href="{svc_href}">{svc_name}</a> service area. '
            f'See more of our work nearby.'
        )
    return (
        f'{MARKER_START}\n'
        f'<section class="proj-svc-link">\n'
        f'  <div class="wrap">\n'
        f'    <div class="txt">\n'
        f'      <p class="lab">Service Area</p>\n'
        f'      <h2 class="head">{headline}</h2>\n'
        f'      <p class="msg">{msg}</p>\n'
        f'    </div>\n'
        f'    <div class="cta"><a href="{svc_href}">View all {svc_name} builds</a></div>\n'
        f'  </div>\n'
        f'</section>\n'
        f'{MARKER_END}\n'
    )


def find_et_main_area_close(html):
    """Walk the HTML and find the position of the </div> that closes #et-main-area."""
    start = html.find('<div id="et-main-area">')
    if start == -1:
        return -1
    # Start depth at 1 since we're already inside et-main-area after this div
    depth = 1
    i = start + len('<div id="et-main-area">')
    while i < len(html):
        next_open = html.find('<div', i)
        next_close = html.find('</div>', i)
        if next_close == -1:
            return -1
        if next_open != -1 and next_open < next_close:
            depth += 1
            i = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                return next_close
            i = next_close + 6
    return -1


def inject(slug, svc_slug, svc_name, hood_slug):
    path = SITE / "project" / slug / "index.html"
    if not path.exists():
        return False
    html = path.read_text(encoding="utf-8")

    # Remove any prior block (idempotent)
    html = re.sub(
        re.escape(MARKER_START) + ".*?" + re.escape(MARKER_END) + r"\n?",
        "",
        html,
        flags=re.DOTALL,
    )
    # Remove any prior CSS block
    html = re.sub(
        re.escape(CSS_START) + ".*?" + re.escape(CSS_END),
        "",
        html,
        flags=re.DOTALL,
    )
    # Remove empty style tags left behind
    html = re.sub(r"<style>\s*</style>", "", html)

    # Inject CSS before </head>
    html = html.replace("</head>", f"<style>{CSS}</style></head>", 1)

    # Find where #et-main-area closes and inject the block right before it
    close_pos = find_et_main_area_close(html)
    if close_pos == -1:
        print(f"  WARN: {slug} has no #et-main-area close, skipping block injection")
        path.write_text(html, encoding="utf-8")
        return True

    block = build_block(svc_slug, svc_name, hood_slug)
    html = html[:close_pos] + block + html[close_pos:]

    path.write_text(html, encoding="utf-8")
    return True


def main():
    print("Injecting project -> service area links (inside #et-main-area)...")
    done = 0
    for slug, (svc_slug, svc_name, hood_slug) in PROJECT_MAP.items():
        if inject(slug, svc_slug, svc_name, hood_slug):
            print(f"  wrote project/{slug}/ -> /service-areas/{svc_slug}/")
            done += 1
    print(f"Done. Injected links on {done} project pages.")


if __name__ == "__main__":
    main()
