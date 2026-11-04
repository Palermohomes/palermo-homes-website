"""Replace the OUR HOMES / 'If you can envision it' carousel row on the home page
with a modern 3-card 'A few homes we've built' section. Palermo colours, light theme.
Idempotent."""
import re
from pathlib import Path

HOME = Path(__file__).resolve().parent.parent / "site" / "index.html"

CSS_START = "/* ==== FEATURED-HOMES CSS START ==== */"
CSS_END = "/* ==== FEATURED-HOMES CSS END ==== */"
HTML_START = "<!-- FEATURED-HOMES START -->"
HTML_END = "<!-- FEATURED-HOMES END -->"

FH_CSS = f"""
{CSS_START}
html body #et-main-area .fh{{background:#fff;padding:0 0 44px;margin-top:-24px;font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;border:0}}
/* Kill parent Divi section's top padding so featured-homes sits close to the cream */
html body #et-main-area .et_pb_section.et_pb_section_2{{padding-top:0 !important}}
html body #et-main-area .fh .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .fh .head{{max-width:820px;margin:0 0 14px;text-align:left}}
html body #et-main-area .fh .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 8px}}
html body #et-main-area .fh h2{{font-size:clamp(22px,2.5vw,34px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21}}
html body #et-main-area .fh .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
html body #et-main-area .fh .card{{display:block;text-decoration:none;color:inherit;background:#fff;overflow:hidden;transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease;border:1px solid #c9c3b5;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
html body #et-main-area .fh .card:hover{{transform:translateY(-6px);box-shadow:0 18px 40px rgba(0,0,0,.14);border-color:#0085c9}}
html body #et-main-area .fh .photo{{aspect-ratio:16/10;overflow:hidden;background:#e8e5dd;position:relative}}
html body #et-main-area .fh .photo img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s ease,filter .3s ease;filter:brightness(.96)}}
html body #et-main-area .fh .card:hover .photo img{{transform:scale(1.04);filter:brightness(1)}}
html body #et-main-area .fh .meta{{padding:18px 22px 20px;border-top:2px solid #0085c9;display:flex;justify-content:space-between;align-items:center;gap:14px}}
html body #et-main-area .fh .meta .txt{{min-width:0}}
html body #et-main-area .fh .meta .arr{{flex-shrink:0;color:#0085c9;font-size:20px;line-height:1;font-weight:400;transition:transform .25s ease}}
html body #et-main-area .fh .card:hover .meta .arr{{transform:translateX(4px)}}
html body #et-main-area .fh .location{{font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:#7a828c;font-weight:500;margin:0 0 6px}}
html body #et-main-area .fh h3{{font-size:19px;font-weight:600;letter-spacing:-0.01em;line-height:1.2;margin:0;color:#1a1d21}}
html body #et-main-area .fh .cta-row{{display:flex;justify-content:center;margin-top:18px}}
html body #et-main-area .fh .cta-row a{{display:inline-block;padding:14px 30px;border:1px solid #1a1d21;border-radius:999px;font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:#1a1d21;text-decoration:none;font-weight:600;transition:background .2s,color .2s,border-color .2s}}
html body #et-main-area .fh .cta-row a:hover{{background:#0085c9;color:#fff;border-color:#0085c9}}
@media (max-width:900px){{
  html body #et-main-area .fh{{padding:12px 0 20px}}
  html body #et-main-area .fh .grid{{grid-template-columns:1fr;gap:14px}}
}}
{CSS_END}
"""

CARDS = [
    ("touriga-place-1", "Modern Lakeview Home on Touriga Place", "/wp-content/uploads/2025/12/Touriga-109.jpg",   "West Kelowna, BC"),
    ("malbec-place-1",  "Modern Lakeview Home on Malbec Place",  "/wp-content/uploads/2025/12/1587-Malbec-14.jpg", "West Kelowna, BC"),
    ("1252",            "Modern Lakeview Home on Cabernet Way",  "/wp-content/uploads/2025/12/Cabernet-02.jpg",   "West Kelowna, BC"),
]

cards_html = "\n".join(
    f'''      <a class="card" href="/project/{slug}/" aria-label="View {name} project">
        <div class="photo"><img src="{img}" alt="{name} custom home by Palermo Homes in {loc}" loading="lazy"></div>
        <div class="meta">
          <div class="txt">
            <p class="location">{loc}</p>
            <h3>{name}</h3>
          </div>
          <span class="arr" aria-hidden="true">&rarr;</span>
        </div>
      </a>'''
    for slug, name, img, loc in CARDS
)

FH_HTML = f"""{HTML_START}
<section class="fh">
  <div class="wrap">
    <div class="head">
      <p class="eyebrow">Selected work</p>
      <h2>A few homes we've built.</h2>
    </div>
    <div class="grid">
{cards_html}
    </div>
    <div class="cta-row">
      <a href="/projects/">View all projects</a>
    </div>
  </div>
</section>
{HTML_END}"""


def find_our_homes_row_span(html: str) -> tuple[int, int] | None:
    """Locate byte range of the et_pb_row that contains the OUR HOMES carousel."""
    marker = html.find("If you can envision")
    if marker < 0:
        return None
    row_re = re.compile(r'<div\s+class="[^"]*(et_pb_row_\d+)[^"]*"[^>]*>')
    starts = [m for m in row_re.finditer(html) if m.start() < marker]
    if not starts:
        return None
    open_m = starts[-1]
    rest = html[open_m.end():]
    next_row = row_re.search(rest)
    sec_re = re.compile(r'<div\s+class="[^"]*et_pb_section_\d+[^"]*"[^>]*>')
    next_sec = sec_re.search(rest)
    candidates = [x.start() for x in (next_row, next_sec) if x]
    if not candidates:
        return None
    return open_m.start(), open_m.end() + min(candidates)


def main():
    html = HOME.read_text(encoding="utf-8")

    # 1) Refresh CSS block in head
    if CSS_START in html:
        html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.DOTALL)
    if "</head>" not in html:
        raise SystemExit("no </head> in home page")
    html = html.replace("</head>", f"<style>{FH_CSS}</style></head>", 1)

    # 2) Replace the section body:
    #    - If markers already exist, swap between them (rerun case)
    #    - Otherwise, find the original OUR HOMES row and replace it (first install)
    if HTML_START in html:
        html = re.sub(
            re.escape(HTML_START) + r".*?" + re.escape(HTML_END),
            lambda m: FH_HTML,
            html, count=1, flags=re.DOTALL,
        )
        print(f"  index.html: featured-homes refreshed ({len(html):,} bytes)")
    else:
        span = find_our_homes_row_span(html)
        if span is not None:
            start, end = span
            html = html[:start] + FH_HTML + html[end:]
            print(f"  index.html: featured-homes installed at OUR HOMES row ({len(html):,} bytes)")
        else:
            # Fallback: original row already gone AND no marker. Insert before WWB.
            wwb_pos = html.find("<!-- WHERE-WE-BUILD START -->")
            if wwb_pos < 0:
                # Second fallback: before the Award of Excellence section
                award_pos = html.find("Award of Excellence")
                if award_pos < 0:
                    print("  index.html: no anchor found anywhere, skipping")
                    HOME.write_text(html, encoding="utf-8")
                    return
                sec_re = re.compile(r'<div\s+class="[^"]*et_pb_section_\d+[^"]*"[^>]*>')
                starts = [m for m in sec_re.finditer(html) if m.start() < award_pos]
                wwb_pos = starts[-1].start() if starts else award_pos
            html = html[:wwb_pos] + FH_HTML + "\n" + html[wwb_pos:]
            print(f"  index.html: featured-homes re-inserted at fallback ({len(html):,} bytes)")

    HOME.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
