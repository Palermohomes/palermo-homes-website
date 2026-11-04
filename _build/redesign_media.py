"""Media page: mirrors services/about/awards format.
White hero text. Keyword-rich SEO copy. VideoObject schema for each video.
Idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "site" / "media" / "index.html"
html = MEDIA.read_text(encoding="utf-8")

# --- 1) Title + meta description
html = re.sub(
    r'<title>[^<]*</title>',
    '<title>Media Coverage &amp; Press | Palermo Homes, Kelowna</title>',
    html, count=1,
)
# Strip any existing meta description (any attribute order), inject fresh
_desc = 'Palermo Homes featured on Hometown Heroes Lottery, West Coast Homes, and Live Like a Millionaire. Custom home builder in Kelowna, BC.'
html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
html = html.replace("</head>", f'<meta name="description" content="{_desc}"/>\n</head>', 1)

# --- 2) Custom CSS (wrapped in markers so we can rerun cleanly). Mirrors services/about/awards tokens.
CSS_START = "/* ==== MEDIA-V2 CSS START ==== */"
CSS_END = "/* ==== MEDIA-V2 CSS END ==== */"

CUSTOM_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .md-v2{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .md-v2 *{{box-sizing:border-box}}
html body #et-main-area .md-v2 img{{display:block;max-width:100%;height:auto}}
html body #et-main-area .md-v2 .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .md-v2 .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}

/* HERO. Mirrors svc-hero */
html body #et-main-area .md-hero{{position:relative;min-height:clamp(240px,36vh,340px);padding:40px 0;display:flex;align-items:center;overflow:hidden;color:#fff}}
html body #et-main-area .md-hero .bg{{position:absolute;inset:0;background-position:center center;background-size:cover;background-repeat:no-repeat}}
html body #et-main-area .md-hero::after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.50) 0%,rgba(0,0,0,.55) 50%,rgba(0,0,0,.70) 100%)}}
html body #et-main-area .md-hero .inner{{position:relative;z-index:2;max-width:1360px;margin:0 auto;width:100%;padding:0 clamp(20px,3vw,48px);box-sizing:border-box}}
html body #et-main-area .md-hero .eyebrow{{color:rgba(255,255,255,.9) !important;margin:0 0 12px;text-align:left !important}}
html body #et-main-area .md-hero h1{{font-size:clamp(28px,3.4vw,42px) !important;font-weight:500 !important;letter-spacing:-0.02em !important;line-height:1.05 !important;margin:0 !important;max-width:22ch !important;text-transform:none !important;color:#fff !important;text-align:left !important}}
html body #et-main-area .md-hero p.sub{{font-size:clamp(15px,1.2vw,17px);color:rgba(255,255,255,.9);margin:16px 0 0;max-width:60ch;line-height:1.55;text-align:left !important}}

/* Overview. Mirrors aw-over */
html body #et-main-area .md-over{{padding:32px 0 24px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .md-over .head{{max-width:none;margin:0 0 20px;text-align:left}}
html body #et-main-area .md-over h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21}}
html body #et-main-area .md-over .body{{max-width:90ch}}
html body #et-main-area .md-over p{{font-size:15px;line-height:1.65;color:#3a4048;margin:0 0 14px}}
html body #et-main-area .md-over p:last-child{{margin:0}}

/* Video grid */
html body #et-main-area .md-videos{{padding:24px 0 40px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .md-videos .head{{max-width:820px;margin:0 0 24px;text-align:left}}
html body #et-main-area .md-videos h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21}}
html body #et-main-area .md-videos .grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:32px}}
html body #et-main-area .md-videos .video-card{{background:#fff;border:1px solid #ece8df;overflow:hidden;transition:box-shadow .25s ease,border-color .25s ease;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
html body #et-main-area .md-videos .video-card:hover{{border-color:#0085c9;box-shadow:0 18px 40px rgba(0,0,0,.14)}}
html body #et-main-area .md-videos .video-frame{{position:relative;aspect-ratio:16/9;overflow:hidden;background:#141821}}
html body #et-main-area .md-videos .video-frame iframe{{position:absolute;inset:0;width:100%;height:100%;border:0;display:block}}
html body #et-main-area .md-videos .video-meta{{padding:18px 22px 20px;border-top:2px solid #0085c9}}
html body #et-main-area .md-videos .source{{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 6px}}
html body #et-main-area .md-videos h3{{font-size:17px;font-weight:600;letter-spacing:-0.01em;line-height:1.25;margin:0 0 8px;color:#1a1d21}}
html body #et-main-area .md-videos .desc{{font-size:14px;line-height:1.55;color:#5a6069;margin:0}}

/* CTA. Palermo blue band */
html body #et-main-area .md-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center}}
html body #et-main-area .md-cta h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 14px;color:#fff !important}}
html body #et-main-area .md-cta p{{color:rgba(255,255,255,.92) !important;font-size:16px;margin:0 0 26px}}
html body #et-main-area .md-cta a.btn{{display:inline-block;background:#fff;color:#0085c9;padding:14px 30px;border-radius:999px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;text-decoration:none;transition:background .2s,color .2s}}
html body #et-main-area .md-cta a.btn:hover{{background:#141821;color:#fff}}

@media (max-width:900px){{
  html body #et-main-area .md-hero{{min-height:170px;padding:24px 0}}
  html body #et-main-area .md-hero .eyebrow{{margin-bottom:6px;font-size:10px;letter-spacing:.24em}}
  html body #et-main-area .md-hero h1{{font-size:28px !important;line-height:1.1 !important;max-width:24ch !important}}
  html body #et-main-area .md-hero p.sub{{font-size:13px;margin-top:8px;line-height:1.45}}
  html body #et-main-area .md-videos .grid{{grid-template-columns:1fr;gap:20px}}
  html body #et-main-area .md-over,html body #et-main-area .md-videos,html body #et-main-area .md-cta{{padding:24px 0}}
}}
{CSS_END}
"""

# Remove any previous injection between markers (both the wrapped and raw forms)
html = re.sub(r'<style[^>]*>\s*' + re.escape(CSS_START) + r".*?" + re.escape(CSS_END) + r'\s*</style>', "", html, flags=re.DOTALL)
if CSS_START in html:
    html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.DOTALL)

# Inject fresh CSS as its own <style> block right before </head>
html = html.replace("</head>", f"<style>{CUSTOM_CSS}</style></head>", 1)

# --- 3) VideoObject schema (embedded in <head>) for SEO rich results
video_schema = """<script type="application/ld+json">{"@context":"https://schema.org","@graph":[
{"@type":"VideoObject","name":"Hometown Heroes Lottery 2022 - Living Large in Lake Country","description":"Palermo Homes' Hometown Heroes Lottery 2022 grand-prize custom home on Ledgestone Road, Lake Country, BC.","thumbnailUrl":"https://i.ytimg.com/vi/t_5iLCdyMjc/maxresdefault.jpg","uploadDate":"2022-04-01","embedUrl":"https://www.youtube.com/embed/t_5iLCdyMjc","publisher":{"@type":"HomeAndConstructionBusiness","name":"Palermo Homes"}},
{"@type":"VideoObject","name":"Live Like a Millionaire: Abbotsford, B.C.","description":"Featured Palermo Homes custom home in Abbotsford, BC from the Millionaire Lottery Live Like a Millionaire campaign.","thumbnailUrl":"https://i.ytimg.com/vi/7VNiyvo2v2s/maxresdefault.jpg","embedUrl":"https://www.youtube.com/embed/7VNiyvo2v2s","publisher":{"@type":"HomeAndConstructionBusiness","name":"Palermo Homes"}},
{"@type":"VideoObject","name":"West Coast Homes: Valley Views from Abbotsford's Eagle Mountain","description":"Palermo Homes custom hillside build featured on West Coast Homes, Eagle Mountain in Abbotsford, BC.","thumbnailUrl":"https://i.ytimg.com/vi/V_PL58NSme4/maxresdefault.jpg","embedUrl":"https://www.youtube.com/embed/V_PL58NSme4","publisher":{"@type":"HomeAndConstructionBusiness","name":"Palermo Homes"}},
{"@type":"VideoObject","name":"West Coast Homes: Views and Big Skies at Abbotsford's Eagle Mountain","description":"Second Palermo Homes custom home featured on West Coast Homes, Eagle Mountain in Abbotsford, BC.","thumbnailUrl":"https://i.ytimg.com/vi/pb5rkZwl8hE/maxresdefault.jpg","embedUrl":"https://www.youtube.com/embed/pb5rkZwl8hE","publisher":{"@type":"HomeAndConstructionBusiness","name":"Palermo Homes"}}
]}</script>"""

# Inject video schema before </head> (idempotent. Check if already present)
if 'VideoObject' not in html:
    html = html.replace("</head>", video_schema + "</head>", 1)

# --- 4) Replace main-area inner content
NEW_MAIN = """
<div class="md-v2">

  <section class="md-hero">
    <div class="bg" style="background-image:url('../wp-content/uploads/2025/12/media-hero.jpg')"></div>
    <div class="inner">
      <p class="eyebrow">Media &amp; Press · Palermo Homes</p>
      <h1>Palermo Homes in the media.</h1>
      <p class="sub">Featured on Hometown Heroes Lottery, West Coast Homes, and Live Like a Millionaire. Custom home builder based in Kelowna, BC.</p>
    </div>
  </section>

  <section class="md-over">
    <div class="wrap">
      <div class="head">
        <h2>Featured coverage of Palermo Homes across BC's home building media.</h2>
      </div>
      <div class="body">
        <p>Palermo Homes is an award-winning custom home builder in Kelowna, BC, featured on Hometown Heroes Lottery, West Coast Homes, and Live Like a Millionaire for custom homes across Kelowna, Lake Country, Abbotsford, and the Fraser Valley.</p>
      </div>
    </div>
  </section>

  <section class="md-videos">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Featured videos</p>
        <h2>Watch Palermo Homes on TV and lottery grand-prize features.</h2>
      </div>
      <div class="grid">

        <div class="video-card">
          <div class="video-frame">
            <iframe src="https://www.youtube.com/embed/t_5iLCdyMjc?rel=0" title="Hometown Heroes Lottery 2022 - Living Large in Lake Country" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
          </div>
          <div class="video-meta">
            <p class="source">Hometown Heroes Lottery · 2022</p>
            <h3>Living Large in Lake Country</h3>
            <p class="desc">Palermo Homes' Hometown Heroes Lottery grand-prize custom home on Ledgestone Road, Lake Country, BC.</p>
          </div>
        </div>

        <div class="video-card">
          <div class="video-frame">
            <iframe src="https://www.youtube.com/embed/7VNiyvo2v2s?rel=0" title="Live Like a Millionaire: Abbotsford, B.C." loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
          </div>
          <div class="video-meta">
            <p class="source">Millionaire Lottery · Abbotsford</p>
            <h3>Live Like a Millionaire: Abbotsford, B.C.</h3>
            <p class="desc">Palermo Homes custom home featured in the Millionaire Lottery Live Like a Millionaire campaign in Abbotsford, BC.</p>
          </div>
        </div>

        <div class="video-card">
          <div class="video-frame">
            <iframe src="https://www.youtube.com/embed/V_PL58NSme4?rel=0" title="West Coast Homes: Valley Views from Abbotsford's Eagle Mountain" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
          </div>
          <div class="video-meta">
            <p class="source">West Coast Homes · Eagle Mountain</p>
            <h3>Valley Views from Abbotsford's Eagle Mountain</h3>
            <p class="desc">Palermo Homes custom hillside build featured on West Coast Homes, Eagle Mountain in Abbotsford, BC.</p>
          </div>
        </div>

        <div class="video-card">
          <div class="video-frame">
            <iframe src="https://www.youtube.com/embed/pb5rkZwl8hE?rel=0" title="West Coast Homes: Views and Big Skies at Abbotsford's Eagle Mountain" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
          </div>
          <div class="video-meta">
            <p class="source">West Coast Homes · Eagle Mountain</p>
            <h3>Views and Big Skies at Abbotsford's Eagle Mountain</h3>
            <p class="desc">Second Palermo Homes custom home featured on West Coast Homes, Eagle Mountain in Abbotsford, BC.</p>
          </div>
        </div>

      </div>
    </div>
  </section>

  <section class="md-cta">
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

MEDIA.write_text(new_html, encoding="utf-8")
print(f"Media rebuilt. size {len(html)} -> {len(new_html)}")

# Always refresh nav/footer/dashes/validate after any page rewrite
import subprocess, sys
here = Path(__file__).parent
for script in ("replace_nav.py", "replace_footer.py", "kill_dashes.py", "validate_links.py"):
    print(f"\n>>> {script}")
    r = subprocess.run([sys.executable, str(here / script)])
    if r.returncode != 0 and script == "validate_links.py":
        raise SystemExit(f"validate_links.py failed with exit {r.returncode}")
