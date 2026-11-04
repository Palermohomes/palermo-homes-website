"""Awards page: mirrors the services/about page format.
White hero text. Keyword-rich SEO copy. Keeps CHBA winner logo intact.
Idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AWARDS = ROOT / "site" / "awards" / "index.html"
html = AWARDS.read_text(encoding="utf-8")

# --- 1) Title + meta description
html = re.sub(
    r'<title>[^<]*</title>',
    '<title>Awards | Palermo Homes | Kelowna Custom Home Builder</title>',
    html, count=1,
)
# Strip any existing meta description (any attribute order), inject fresh
_desc = 'Palermo Homes is an award-winning custom home builder in Kelowna, BC, recognized by CHBA Fraser Valley for our custom home builds.'
html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
html = html.replace("</head>", f'<meta name="description" content="{_desc}"/>\n</head>', 1)

# --- 2) Custom CSS (wrapped in markers so we can rerun cleanly). Mirrors services/about tokens.
CSS_START = "/* ==== AWARDS-V2 CSS START ==== */"
CSS_END = "/* ==== AWARDS-V2 CSS END ==== */"

CUSTOM_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .aw-v2{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff;display:flex;flex-direction:column}}
/* Section order: hero > overview > gallery > featured recognition > CTA (both desktop + mobile) */
html body #et-main-area .aw-hero{{order:1}}
html body #et-main-area .aw-over{{order:2}}
html body #et-main-area .aw-gallery{{order:3}}
html body #et-main-area .aw-feature{{order:4}}
html body #et-main-area .aw-cta{{order:5}}
html body #et-main-area .aw-v2 *{{box-sizing:border-box}}
html body #et-main-area .aw-v2 img{{display:block;max-width:100%;height:auto}}
html body #et-main-area .aw-v2 .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .aw-v2 .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}

/* HERO. Split background showing 2 award-night photos (mirrors svc-hero sizing). */
html body #et-main-area .aw-hero{{position:relative;min-height:clamp(240px,36vh,340px);padding:40px 0;display:flex;align-items:center;overflow:hidden;color:#fff}}
html body #et-main-area .aw-hero .bg-split{{position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr}}
html body #et-main-area .aw-hero .bg-split .bg{{background-position:center center;background-size:cover;background-repeat:no-repeat}}
html body #et-main-area .aw-hero::after{{content:'';position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.75) 0%,rgba(0,0,0,.55) 40%,rgba(0,0,0,.45) 60%,rgba(0,0,0,.65) 100%)}}
html body #et-main-area .aw-hero .inner{{position:relative;z-index:2;max-width:1360px;margin:0 auto;width:100%;padding:0 clamp(20px,3vw,48px);box-sizing:border-box}}
html body #et-main-area .aw-hero .eyebrow{{color:rgba(255,255,255,.9) !important;margin:0 0 12px;text-align:left !important}}
html body #et-main-area .aw-hero h1{{font-size:clamp(28px,3.4vw,42px) !important;font-weight:500 !important;letter-spacing:-0.02em !important;line-height:1.05 !important;margin:0 !important;max-width:22ch !important;text-transform:none !important;color:#fff !important;text-align:left !important}}
html body #et-main-area .aw-hero p.sub{{font-size:clamp(15px,1.2vw,17px);color:rgba(255,255,255,.9);margin:16px 0 0;max-width:60ch;line-height:1.55;text-align:left !important}}

/* Overview. Mirrors about-over */
html body #et-main-area .aw-over{{padding:32px 0 24px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .aw-over .head{{max-width:none;margin:0 0 20px;text-align:left}}
html body #et-main-area .aw-over h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21}}
html body #et-main-area .aw-over .body{{max-width:90ch}}
html body #et-main-area .aw-over p{{font-size:15px;line-height:1.65;color:#3a4048;margin:0 0 14px}}
html body #et-main-area .aw-over p:last-child{{margin:0}}

/* Featured award. Desktop: left = details + wins, right = CHBA logo (top) + featured photo (bottom). Mobile: stacked. */
html body #et-main-area .aw-feature{{padding:24px 0 32px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .aw-feature .grid{{display:grid;grid-template-columns:1.3fr 1fr;grid-template-rows:min-content;gap:56px;align-items:stretch}}
html body #et-main-area .aw-feature .body{{max-width:640px;min-width:0}}
html body #et-main-area .aw-feature .aside{{display:grid;grid-template-rows:auto 1fr;gap:20px;min-height:0;min-width:0;height:100%}}
html body #et-main-area .aw-feature .logo{{padding:22px;background:#fbfaf6;border:1px solid #e2ddd0}}
html body #et-main-area .aw-feature .logo img{{width:100%;height:auto;display:block}}
html body #et-main-area .aw-feature .featured-photo{{overflow:hidden;background:#f6f4ef;min-height:0;position:relative}}
html body #et-main-area .aw-feature .featured-photo img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}}
html body #et-main-area .aw-feature h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 12px;color:#1a1d21}}
html body #et-main-area .aw-feature .meta{{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:#7a828c;font-weight:500;margin:0 0 20px}}
html body #et-main-area .aw-feature .wins{{list-style:none;padding:0;margin:0}}
html body #et-main-area .aw-feature .wins li{{padding:14px 0;border-bottom:1px solid #ece8df;display:flex;gap:18px;align-items:baseline;font-size:15px;color:#1a1d21;line-height:1.5}}
html body #et-main-area .aw-feature .wins li:last-child{{border-bottom:0}}
html body #et-main-area .aw-feature .wins .badge{{flex:0 0 110px;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#0085c9;background:transparent;padding:0;border-radius:0;font-weight:600;line-height:1.4}}
html body #et-main-area .aw-feature .wins .badge.finalist{{color:#7a828c;font-weight:500}}

/* Gallery. 3-col grid of award night photos */
html body #et-main-area .aw-gallery{{padding:24px 0 40px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .aw-gallery .head{{max-width:820px;margin:0 0 22px;text-align:left}}
html body #et-main-area .aw-gallery h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21}}
html body #et-main-area .aw-gallery .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
html body #et-main-area .aw-gallery .cell{{aspect-ratio:4/3;overflow:hidden;background:#f6f4ef;position:relative}}
html body #et-main-area .aw-gallery .cell img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s ease,filter .3s ease;filter:brightness(.96)}}
html body #et-main-area .aw-gallery .cell:hover img{{transform:scale(1.04);filter:brightness(1)}}

/* Mobile-only CHBA logo appended below the gallery. Hidden on desktop. */
html body #et-main-area .aw-gallery .chba-mobile{{display:none}}

/* CTA. Palermo blue band */
html body #et-main-area .aw-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center}}
html body #et-main-area .aw-cta h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 14px;color:#fff !important}}
html body #et-main-area .aw-cta p{{color:rgba(255,255,255,.92) !important;font-size:16px;margin:0 0 26px}}
html body #et-main-area .aw-cta a.btn{{display:inline-block;background:#fff;color:#0085c9;padding:14px 30px;border-radius:999px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;text-decoration:none;transition:background .2s,color .2s}}
html body #et-main-area .aw-cta a.btn:hover{{background:#141821;color:#fff}}

@media (max-width:900px){{
  html body #et-main-area .aw-hero{{min-height:170px;padding:24px 0}}
  html body #et-main-area .aw-hero .eyebrow{{margin-bottom:6px;font-size:10px;letter-spacing:.24em}}
  html body #et-main-area .aw-hero h1{{font-size:28px !important;line-height:1.1 !important;max-width:24ch !important}}
  html body #et-main-area .aw-hero p.sub{{font-size:13px;margin-top:8px;line-height:1.45}}
  /* Mobile: single hero photo (dominant) instead of split so it doesn't look cramped */
  html body #et-main-area .aw-hero .bg-split{{grid-template-columns:1fr}}
  html body #et-main-area .aw-hero .bg-split .bg:nth-child(1){{display:none}}
  html body #et-main-area .aw-feature .grid{{grid-template-columns:1fr;gap:24px;align-items:stretch}}
  html body #et-main-area .aw-feature .aside{{grid-template-rows:auto;gap:14px;min-height:0}}
  html body #et-main-area .aw-feature .aside .logo{{display:none}}
  html body #et-main-area .aw-feature .featured-photo{{aspect-ratio:16/10;position:relative}}
  /* Show mobile CHBA logo at the bottom of the gallery section */
  html body #et-main-area .aw-gallery .chba-mobile{{display:block;margin-top:24px;padding:18px;background:#fbfaf6;border:1px solid #e2ddd0;max-width:520px;margin-left:auto;margin-right:auto}}
  html body #et-main-area .aw-gallery .chba-mobile img{{width:100%;height:auto;display:block}}
  html body #et-main-area .aw-gallery .grid{{grid-template-columns:1fr 1fr;gap:8px}}
  html body #et-main-area .aw-over,html body #et-main-area .aw-gallery,html body #et-main-area .aw-cta{{padding:24px 0}}
  html body #et-main-area .aw-feature{{padding:16px 0 24px}}
}}
{CSS_END}
"""

# Remove any previous injection between markers (both the wrapped and raw forms)
html = re.sub(r'<style[^>]*>\s*' + re.escape(CSS_START) + r".*?" + re.escape(CSS_END) + r'\s*</style>', "", html, flags=re.DOTALL)
if CSS_START in html:
    html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.DOTALL)

# Inject fresh CSS as its own <style> block right before </head>
html = html.replace("</head>", f"<style>{CUSTOM_CSS}</style></head>", 1)

# --- 3) Replace main-area inner content
NEW_MAIN = """
<div class="aw-v2">

  <section class="aw-hero">
    <div class="bg-split">
      <div class="bg" style="background-image:url('/wp-content/uploads/2020/03/TCP_1084.jpg')"></div>
      <div class="bg" style="background-image:url('/wp-content/uploads/2020/03/TCP_6696.jpg')"></div>
    </div>
    <div class="inner">
      <p class="eyebrow">Awards · Palermo Homes</p>
      <h1>Award-winning custom home builder in Kelowna, BC.</h1>
      <p class="sub">Recognized by CHBA Fraser Valley and BC's home building industry for our custom home builds, design, and construction.</p>
    </div>
  </section>

  <section class="aw-over">
    <div class="wrap">
      <div class="head">
        <h2>Recognized across BC's custom home industry.</h2>
      </div>
      <div class="body">
        <p>Palermo Homes is an award-winning custom home builder based in Kelowna, BC. Recognized by the Canadian Home Builders' Association (CHBA) Fraser Valley Housing Awards of Excellence for custom home construction and design across Kelowna, West Kelowna, the Okanagan Valley, and the Lower Mainland.</p>
      </div>
    </div>
  </section>

  <section class="aw-feature">
    <div class="wrap"><div class="grid">
      <div class="body">
        <p class="eyebrow">Featured recognition</p>
        <h2>4th Annual Fraser Valley Housing Awards of Excellence.</h2>
        <p class="meta">Feb 22, 2020 · Airside Event Spaces, Abbotsford BC</p>
        <ul class="wins">
          <li><span class="badge">Winner</span><span>Best Master Suite</span></li>
          <li><span class="badge finalist">Top 3 Finalist</span><span>Custom Home Builder of the Year</span></li>
          <li><span class="badge finalist">Top 3 Finalist</span><span>Best Custom Home ($1M-$1.5M)</span></li>
          <li><span class="badge finalist">Top 3 Finalist</span><span>Best Kitchen</span></li>
          <li><span class="badge finalist">Top 3 Finalist</span><span>Best Outdoor Living Space</span></li>
        </ul>
      </div>
      <div class="aside">
        <div class="logo">
          <img src="/wp-content/uploads/2020/03/Winner_Goldblack-1.jpg" alt="CHBA Fraser Valley Housing Awards of Excellence Winner">
        </div>
        <div class="featured-photo">
          <img src="/wp-content/uploads/2020/03/awards-featured-home.jpg" alt="Palermo Homes Best Master Suite award-winning custom home in Kelowna" loading="lazy">
        </div>
      </div>
    </div></div>
  </section>

  <section class="aw-gallery">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Award night</p>
        <h2>From the CHBA Awards Gala.</h2>
      </div>
      <div class="grid">
        <div class="cell"><img src="/wp-content/uploads/2020/03/TCP_1084.jpg" alt="Palermo Homes team at CHBA Fraser Valley Housing Awards Gala" loading="lazy"></div>
        <div class="cell"><img src="/wp-content/uploads/2020/03/TCP_6696.jpg" alt="Palermo Homes accepting CHBA Best Master Suite award" loading="lazy"></div>
        <div class="cell"><img src="/wp-content/uploads/2020/03/TCP_6609.jpg" alt="Palermo Homes at CHBA Fraser Valley Housing Awards of Excellence" loading="lazy"></div>
        <div class="cell"><img src="/wp-content/uploads/2020/03/TCP_6576.jpg" alt="CHBA Fraser Valley Housing Awards of Excellence event" loading="lazy"></div>
        <div class="cell"><img src="/wp-content/uploads/2020/03/TCP_1620.jpg" alt="CHBA award trophy for Best Master Suite" loading="lazy"></div>
        <div class="cell"><img src="/wp-content/uploads/2020/03/TCP_6586.jpg" alt="Custom home builder award ceremony in Abbotsford BC" loading="lazy"></div>
      </div>
      <div class="chba-mobile">
        <img src="/wp-content/uploads/2020/03/Winner_Goldblack-1.jpg" alt="CHBA Fraser Valley Housing Awards of Excellence Winner">
      </div>
    </div>
  </section>

  <section class="aw-cta">
    <div class="wrap">
      <h2>Build with an award-winning Kelowna custom home builder.</h2>
      <p>Tell us about your project. We'll book a no-pressure consultation.</p>
      <a class="btn" href="../contact/">Start a conversation</a>
    </div>
  </section>

</div>
"""

open_marker = '<div id="et-main-area">'
close_marker = '<footer'
start = html.find(open_marker)
inner_start = html.find('>', start) + 1
footer_start = html.find(close_marker, inner_start)
end = html.rfind('</div>', inner_start, footer_start) + len('</div>')
new_html = html[:inner_start] + NEW_MAIN + html[end:]

AWARDS.write_text(new_html, encoding="utf-8")
print(f"Awards rebuilt. size {len(html)} -> {len(new_html)}")

# Always refresh nav/footer/dashes/validate after any page rewrite
import subprocess, sys
here = Path(__file__).parent
for script in ("replace_nav.py", "replace_footer.py", "kill_dashes.py", "validate_links.py"):
    print(f"\n>>> {script}")
    r = subprocess.run([sys.executable, str(here / script)])
    if r.returncode != 0 and script == "validate_links.py":
        raise SystemExit(f"validate_links.py failed with exit {r.returncode}")
