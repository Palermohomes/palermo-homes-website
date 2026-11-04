"""Replace the 'Share your vision!' form section with a 'Where We Build' region
section on any page that has it. Target: home page (primary SEO). Idempotent."""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
TARGETS = [SITE / "index.html"]  # home page only. contact keeps its own WWB from prior run

CSS_START = "/* ==== WHERE-WE-BUILD CSS START ==== */"
CSS_END = "/* ==== WHERE-WE-BUILD CSS END ==== */"
HTML_START = "<!-- WHERE-WE-BUILD START -->"
HTML_END = "<!-- WHERE-WE-BUILD END -->"

WWB_CSS = f"""
{CSS_START}
html body #et-main-area .wwb{{background:#fff;padding:44px 0 44px;font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;border-top:1px solid #e2ddd0;border-bottom:1px solid #e2ddd0}}
/* Awards section: restore Divi's equal-column layout (image + blue panel same height).
   Just add breathing room above so it doesn't butt against the WWB cream section. */
html body #et-main-area .et_pb_row.et_pb_row_5{{margin-top:44px !important;margin-bottom:24px !important}}

/* Awards blue panel: prominent CTA + clickable feel */
html body #et-main-area .et_pb_row_5 .et_pb_column_7{{cursor:pointer;transition:box-shadow .25s ease,transform .25s ease}}
html body #et-main-area .et_pb_row_5 .et_pb_column_7:hover{{transform:translateY(-2px);box-shadow:0 14px 34px rgba(0,133,201,.28)}}
html body #et-main-area .awards-cta{{display:inline-flex !important;align-items:center;gap:10px;padding:6px 0;background:transparent;color:#fff !important;font-size:13px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;text-decoration:none !important;position:relative;margin-top:6px;border:0}}
html body #et-main-area .awards-cta strong{{color:inherit;font-weight:600;letter-spacing:inherit}}
html body #et-main-area .awards-cta .arr{{font-size:16px;line-height:1;transition:transform .25s ease}}
html body #et-main-area .awards-cta::after{{content:'';position:absolute;left:0;right:26px;bottom:0;height:1px;background:#fff;transform:scaleX(1);transform-origin:left;transition:transform .3s ease}}
html body #et-main-area .awards-cta:hover .arr{{transform:translateX(6px)}}
html body #et-main-area .awards-cta:hover::after{{transform:scaleX(1.05)}}

html body #et-main-area .wwb .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .wwb .head{{max-width:820px;margin:0 0 28px;text-align:left}}
html body #et-main-area .wwb .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 16px}}
html body #et-main-area .wwb h2{{font-size:clamp(22px,2.5vw,34px);font-weight:500;letter-spacing:-0.02em;line-height:1.1;margin:0;color:#1a1d21}}
html body #et-main-area .wwb .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:8px}}
html body #et-main-area .wwb .col{{padding:30px 30px 32px;border:1px solid rgba(255,255,255,.35);background:#0085c9}}
html body #et-main-area .wwb .col+.col{{margin-left:-1px}}
html body #et-main-area .wwb .col h3{{font-size:14px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#fff;margin:0 0 14px}}
html body #et-main-area .wwb .col p{{font-size:15px;line-height:1.65;color:rgba(255,255,255,.9);margin:0}}
html body #et-main-area .wwb .col p .primary{{color:#fff;font-weight:400}}
html body #et-main-area .wwb .col p .cities{{color:rgba(255,255,255,.75)}}
@media (max-width:900px){{
  html body #et-main-area .wwb .grid{{grid-template-columns:1fr}}
  html body #et-main-area .wwb .col+.col{{margin-left:0;margin-top:-1px}}
}}
{CSS_END}
"""

WWB_HTML = f"""{HTML_START}
<section class="wwb">
  <div class="wrap">
    <div class="head">
      <p class="eyebrow">Where we build</p>
      <h2>Kelowna based. Building across BC's most desirable regions.</h2>
    </div>
    <div class="grid">
      <div class="col">
        <h3>Central Okanagan · Primary</h3>
        <p><span class="primary">Kelowna, West Kelowna, Lake Country, and Peachland.</span> Where we're based and where we build most of our custom homes.</p>
      </div>
      <div class="col">
        <h3>Okanagan Valley</h3>
        <p><span class="primary">Vernon and Penticton.</span> Custom homes and renovations for referred clients across the wider Okanagan.</p>
      </div>
      <div class="col">
        <h3>Select Referrals</h3>
        <p><span class="primary">Chilliwack, Abbotsford, Langley, Vancouver, and West Vancouver.</span> Custom home projects in the Fraser Valley and Greater Vancouver for existing clients.</p>
      </div>
    </div>
  </div>
</section>
{HTML_END}"""


SEC_OPEN_RE = re.compile(r'<div\s+class="[^"]*et_pb_section(_\d+)?[^"]*"[^>]*>')


def find_section_containing(html: str, needle: str) -> tuple[int, int] | None:
    """Byte range of the et_pb_section that contains a given text."""
    marker = html.find(needle)
    if marker < 0:
        return None
    starts = [m for m in SEC_OPEN_RE.finditer(html) if m.start() < marker]
    if not starts:
        return None
    open_m = starts[-1]
    rest = html[open_m.end():]
    next_m = SEC_OPEN_RE.search(rest)
    if not next_m:
        j = html.find("<footer", open_m.end())
        return (open_m.start(), j) if j > 0 else None
    return open_m.start(), open_m.end() + next_m.start()


def find_section_start(html: str, needle: str) -> int | None:
    """Byte offset where the et_pb_section containing `needle` opens."""
    span = find_section_containing(html, needle)
    return span[0] if span else None


def process(page: Path) -> None:
    html = page.read_text(encoding="utf-8")

    # 1) Refresh CSS block in head
    if CSS_START in html:
        html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.DOTALL)
    if "</head>" not in html:
        print(f"  {page.name}: no </head>, skipping")
        return
    html = html.replace("</head>", f"<style>{WWB_CSS}</style></head>", 1)

    # 2) If WWB markers already exist, swap between them and stop (idempotent rerun path)
    if HTML_START in html:
        html = re.sub(
            re.escape(HTML_START) + r".*?" + re.escape(HTML_END),
            lambda m: WWB_HTML,
            html, count=1, flags=re.DOTALL,
        )
        page.write_text(html, encoding="utf-8")
        print(f"  {page.name}: WWB refreshed ({len(html):,} bytes)")
        return

    # Also remove the "Share your vision" section entirely if it still exists on this page
    sv = find_section_containing(html, "Share your vision")
    if sv:
        html = html[:sv[0]] + html[sv[1]:]

    # 2) Preferred: insert WWB immediately before the Award of Excellence row
    #    (row_5 inside section_2. Sits between OUR HOMES projects and the Awards block).
    row_m = re.search(r'<div\s+class="[^"]*et_pb_row_5[^"]*"', html)
    if row_m and "Award of Excellence" in html[row_m.start():row_m.start() + 2000]:
        html = html[:row_m.start()] + WWB_HTML + "\n" + html[row_m.start():]
    else:
        # Fallback: before the whole "Award of Excellence" section
        insert_at = find_section_start(html, "Award of Excellence")
        if insert_at is None:
            print(f"  {page.name}: no Award anchor found, skipping")
            return
        html = html[:insert_at] + WWB_HTML + "\n" + html[insert_at:]

    page.write_text(html, encoding="utf-8")
    print(f"  {page.name}: WWB placed ({len(html):,} bytes)")


def main():
    for p in TARGETS:
        if p.exists():
            process(p)


if __name__ == "__main__":
    main()
