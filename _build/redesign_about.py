"""About page: mirrors the services page format (hero, overview, split, coverage, FAQ, blue CTA).
White hero text. Keyword-rich SEO copy. Idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ABOUT = ROOT / "site" / "about" / "index.html"
html = ABOUT.read_text(encoding="utf-8")

# --- 1) Title + meta description (Kelowna primary)
html = re.sub(
    r'<title>[^<]*</title>',
    '<title>About Palermo Homes | Custom Home Builder in Kelowna, BC</title>',
    html, count=1,
)
# Strip any existing meta description (any attribute order), inject fresh
_desc = 'Palermo Homes is a custom home builder based in Kelowna, BC. 15+ years building custom homes and renovations across the Okanagan.'
html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
html = html.replace("</head>", f'<meta name="description" content="{_desc}"/>\n</head>', 1)

# --- 2) Custom CSS (wrapped in markers so we can rerun cleanly). Mirrors services page tokens.
CSS_START = "/* ==== ABOUT-V2 CSS START ==== */"
CSS_END = "/* ==== ABOUT-V2 CSS END ==== */"

CUSTOM_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .about-v2{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .about-v2 *{{box-sizing:border-box}}
html body #et-main-area .about-v2 img{{display:block;max-width:100%;height:auto}}
html body #et-main-area .about-v2 .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .about-v2 .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}

/* HERO. Mirrors svc-hero */
html body #et-main-area .about-hero{{position:relative;min-height:clamp(240px,36vh,340px);padding:40px 0;display:flex;align-items:center;overflow:hidden;color:#fff}}
html body #et-main-area .about-hero .bg{{position:absolute;inset:0;background-position:center center;background-size:cover;background-repeat:no-repeat}}
html body #et-main-area .about-hero::after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.50) 0%,rgba(0,0,0,.55) 50%,rgba(0,0,0,.70) 100%)}}
html body #et-main-area .about-hero .inner{{position:relative;z-index:2;max-width:1360px;margin:0 auto;width:100%;padding:0 clamp(20px,3vw,48px);box-sizing:border-box}}
html body #et-main-area .about-hero .eyebrow{{color:rgba(255,255,255,.9) !important;margin:0 0 12px;text-align:left !important}}
html body #et-main-area .about-hero h1{{font-size:clamp(28px,3.4vw,42px) !important;font-weight:500 !important;letter-spacing:-0.02em !important;line-height:1.05 !important;margin:0 !important;max-width:22ch !important;text-transform:none !important;color:#fff !important;text-align:left !important}}
html body #et-main-area .about-hero p.sub{{font-size:clamp(15px,1.2vw,17px);color:rgba(255,255,255,.9);margin:16px 0 0;max-width:56ch;line-height:1.55;text-align:left !important}}

/* Overview. Mirrors svc-over */
html body #et-main-area .about-over{{padding:32px 0 24px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .about-over .head{{max-width:none;margin:0 0 20px;text-align:left}}
html body #et-main-area .about-over .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .about-over h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21}}
html body #et-main-area .about-over .body{{max-width:90ch}}
html body #et-main-area .about-over p{{font-size:15px;line-height:1.65;color:#3a4048;margin:0 0 14px}}
html body #et-main-area .about-over p:last-child{{margin:0}}

/* Split (photo + numbered list). Mirrors svc-split */
html body #et-main-area .about-split{{padding:24px 0 32px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .about-split .grid{{display:grid;grid-template-columns:1fr 1.1fr;gap:56px;align-items:stretch}}
html body #et-main-area .about-split .grid>div:not(.photo){{display:flex;flex-direction:column}}
html body #et-main-area .about-split .photo{{overflow:hidden;background:#f6f4ef;min-height:100%}}
html body #et-main-area .about-split .photo img{{width:100%;height:100%;object-fit:cover;display:block}}
html body #et-main-area .about-split .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .about-split h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 18px;color:#1a1d21}}
html body #et-main-area .about-split ul{{list-style:none;padding:0;margin:0}}
html body #et-main-area .about-split li{{padding:16px 0;border-bottom:1px solid #ece8df;display:flex;gap:18px;align-items:flex-start}}
html body #et-main-area .about-split li:last-child{{border-bottom:0}}
html body #et-main-area .about-split li .num{{font-size:14px;color:#0085c9;font-weight:600;letter-spacing:.05em;flex:0 0 24px}}
html body #et-main-area .about-split li .txt{{color:#2a2d33;font-size:15px;line-height:1.6}}
html body #et-main-area .about-split li .txt strong{{color:#1a1d21;font-weight:600;display:block;margin-bottom:4px}}
/* Inline stats strip inside the split section's right column */
html body #et-main-area .about-split .stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:auto;padding-top:22px;border-top:1px solid #ece8df}}
html body #et-main-area .about-split .stat{{text-align:center}}
html body #et-main-area .about-split .stat .num{{font-size:28px;font-weight:500;color:#0085c9;letter-spacing:-0.02em;line-height:1}}
html body #et-main-area .about-split .stat .lab{{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#7a828c;margin-top:6px;font-weight:500}}

/* Coverage. 3-col connected region boxes (region name + cities). */
html body #et-main-area .about-coverage{{padding:32px 0 44px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .about-coverage .head{{max-width:820px;margin:0 0 28px;text-align:left}}
html body #et-main-area .about-coverage .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .about-coverage h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21}}
html body #et-main-area .about-coverage .regions-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:8px}}
html body #et-main-area .about-coverage .col{{padding:30px 30px 32px;border:1px solid rgba(255,255,255,.35);background:#0085c9}}
html body #et-main-area .about-coverage .col+.col{{margin-left:-1px}}
html body #et-main-area .about-coverage .col h3{{font-size:14px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#fff;margin:0 0 14px}}
html body #et-main-area .about-coverage .col p{{font-size:15px;line-height:1.65;color:rgba(255,255,255,.9);margin:0}}
html body #et-main-area .about-coverage .col p .primary{{color:#fff;font-weight:400}}
html body #et-main-area .about-coverage .col p .cities{{color:rgba(255,255,255,.75)}}

/* Owner spotlight. Mirrors about-split but tighter (intro + link, no numbered list). */
html body #et-main-area .about-owner{{padding:32px 0 40px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .about-owner .grid{{display:grid;grid-template-columns:0.9fr 1.3fr;gap:48px;align-items:center;max-width:1200px;margin:0 auto}}
html body #et-main-area .about-owner .photo{{overflow:hidden;background:#fff;border-radius:4px;aspect-ratio:4/3}}
html body #et-main-area .about-owner .photo img{{width:100%;height:100%;object-fit:cover;display:block}}
html body #et-main-area .about-owner .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .about-owner h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 16px;color:#1a1d21}}
html body #et-main-area .about-owner p{{font-size:16px;line-height:1.7;color:#3a4048;margin:0 0 14px}}
html body #et-main-area .about-owner .creds{{font-size:14px;line-height:1.6;color:#5a6069;margin:16px 0 22px;padding:14px 18px;background:#f4f9fc;border-left:3px solid #0085c9;border-radius:0 4px 4px 0}}
html body #et-main-area .about-owner .creds strong{{color:#1a1d21;font-weight:600}}
html body #et-main-area .about-owner a.more{{display:inline-flex;align-items:center;gap:10px;background:#0085c9;color:#fff;padding:13px 26px;border-radius:999px;font-size:13px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;text-decoration:none;transition:background .2s}}
html body #et-main-area .about-owner a.more:hover{{background:#141821;color:#fff}}
html body #et-main-area .about-owner a.more .arr{{transition:transform .2s}}
html body #et-main-area .about-owner a.more:hover .arr{{transform:translateX(4px)}}

/* FAQ. Mirrors svc-faq */
html body #et-main-area .about-faq{{padding:32px 0 36px;background:#fff}}
html body #et-main-area .about-faq .head{{max-width:820px;margin:0 0 28px;text-align:left}}
html body #et-main-area .about-faq .head .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .about-faq .head h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21;line-height:1.15}}
html body #et-main-area .about-faq .items{{max-width:820px;margin:0}}
html body #et-main-area .about-faq details{{background:#fff;border:1px solid #ece8df;margin-bottom:12px;padding:0}}
html body #et-main-area .about-faq summary{{cursor:pointer;padding:20px 24px;font-weight:500;font-size:16px;color:#1a1d21;list-style:none;display:flex;justify-content:space-between;align-items:center}}
html body #et-main-area .about-faq summary::-webkit-details-marker{{display:none}}
html body #et-main-area .about-faq summary::after{{content:'+';font-size:22px;color:#0085c9;font-weight:400}}
html body #et-main-area .about-faq details[open] summary::after{{content:'\\2013'}}
html body #et-main-area .about-faq details[open] summary{{border-bottom:1px solid #ece8df}}
html body #et-main-area .about-faq .ans{{padding:18px 24px 22px;color:#4a5058;font-size:15px;line-height:1.7}}

/* CTA. Palermo blue band, white pill button */
html body #et-main-area .about-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center}}
html body #et-main-area .about-cta h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 14px;color:#fff !important}}
html body #et-main-area .about-cta p{{color:rgba(255,255,255,.92) !important;font-size:16px;margin:0 0 26px}}
html body #et-main-area .about-cta a.btn{{display:inline-block;background:#fff;color:#0085c9;padding:14px 30px;border-radius:999px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;text-decoration:none;transition:background .2s,color .2s}}
html body #et-main-area .about-cta a.btn:hover{{background:#141821;color:#fff}}

@media (max-width:900px){{
  html body #et-main-area .about-hero{{min-height:170px;padding:24px 0}}
  html body #et-main-area .about-hero .eyebrow{{margin-bottom:6px;font-size:10px;letter-spacing:.24em}}
  html body #et-main-area .about-hero h1{{font-size:28px !important;line-height:1.1 !important;max-width:24ch !important}}
  html body #et-main-area .about-hero p.sub{{font-size:13px;margin-top:8px;line-height:1.45}}
  html body #et-main-area .about-split .grid{{grid-template-columns:1fr;gap:20px}}
  html body #et-main-area .about-split .photo{{aspect-ratio:16/10;min-height:0}}
  html body #et-main-area .about-split .stats{{grid-template-columns:1fr 1fr;gap:22px;margin-top:20px;padding-top:26px;padding-bottom:8px}}
  html body #et-main-area .about-coverage .regions-grid{{grid-template-columns:1fr}}
  html body #et-main-area .about-coverage .col+.col{{margin-left:0;margin-top:-1px}}
  html body #et-main-area .about-split .stat .num{{font-size:24px}}
  html body #et-main-area .about-over,html body #et-main-area .about-faq,html body #et-main-area .about-coverage,html body #et-main-area .about-cta{{padding:24px 0}}
  html body #et-main-area .about-split{{padding:16px 0 24px}}
  html body #et-main-area .about-owner .grid{{grid-template-columns:1fr;gap:24px}}
  html body #et-main-area .about-owner{{padding:24px 0 28px}}
}}
{CSS_END}
"""

# Remove any previous injection between markers (including the wrapper <style>...</style>)
html = re.sub(r'<style[^>]*>\s*' + re.escape(CSS_START) + r".*?" + re.escape(CSS_END) + r'\s*</style>', "", html, flags=re.DOTALL)
# Also strip the raw-CSS form (older builds injected inside an existing <style> block)
if CSS_START in html:
    html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.DOTALL)

# Inject fresh CSS as its own <style> block right before </head> (robust against prior meta/link insertions)
html = html.replace("</head>", f"<style>{CUSTOM_CSS}</style></head>", 1)

# --- 3) Replace main-area inner content
NEW_MAIN = """
<div class="about-v2">

  <section class="about-hero">
    <div class="bg" style="background-image:url('../wp-content/uploads/2025/12/Touriga-109.jpg')"></div>
    <div class="inner">
      <p class="eyebrow">About Palermo Homes · Kelowna, BC</p>
      <h1>Custom home builder based in Kelowna, BC.</h1>
      <p class="sub">Fifteen-plus years designing and building custom homes and renovations across Kelowna, West Kelowna, Lake Country, and the Okanagan Valley.</p>
    </div>
  </section>

  <section class="about-over">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Overview</p>
        <h2>Custom homes and renovations across Kelowna, the Okanagan, and Lower Mainland.</h2>
      </div>
      <div class="body">
        <p>Palermo Homes is a custom home builder in Kelowna, BC. We build custom homes, renovations, and take on general contracting across Kelowna, West Kelowna, Lake Country, Peachland, and the Okanagan Valley.</p>
      </div>
    </div>
  </section>

  <section class="about-split">
    <div class="wrap"><div class="grid">
      <div class="photo">
        <img src="../wp-content/uploads/2026/01/Cabernet-47-about.jpg" alt="Palermo Homes custom home in Kelowna, BC">
      </div>
      <div>
        <p class="eyebrow">Our approach</p>
        <h2>Three ideas that shape every home we build.</h2>
        <ul>
          <li><span class="num">01</span><span class="txt"><strong>Accountability</strong>One team, one contract, one point of contact. We self-perform the trades that matter most and coordinate the rest as your general contractor, so quality stays in-house.</span></li>
          <li><span class="num">02</span><span class="txt"><strong>Transparency</strong>Line-item pricing from the start. Weekly progress reporting with photos and milestones. No surprises at draw stages or hand-over.</span></li>
          <li><span class="num">03</span><span class="txt"><strong>Long-term value</strong>Commercial-grade construction paired with design that respects the Kelowna resale market. Homes that hold their look and their value for decades.</span></li>
        </ul>
        <div class="stats">
          <div class="stat"><div class="num">15+</div><div class="lab">Years Building</div></div>
          <div class="stat"><div class="num">50+</div><div class="lab">Homes Delivered</div></div>
          <div class="stat"><div class="num">100%</div><div class="lab">Hands-On</div></div>
          <div class="stat"><div class="num">Award</div><div class="lab">Winning</div></div>
        </div>
      </div>
    </div></div>
  </section>

  <section class="about-coverage">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Where we build</p>
        <h2>Kelowna rooted. Building across BC's most desirable regions.</h2>
      </div>
      <div class="regions-grid">
        <div class="col">
          <h3>Central Okanagan · Primary</h3>
          <p><span class="primary">Custom home builder in Kelowna</span>, West Kelowna, Lake Country, and Peachland. Our headquarters and primary service area for custom home construction and renovations. Most of our current builds are underway here.</p>
        </div>
        <div class="col">
          <h3>Okanagan Valley</h3>
          <p><span class="primary">Custom homes and renovations</span> in Vernon and Penticton across the wider Okanagan Valley for returning and referred clients.</p>
        </div>
        <div class="col">
          <h3>Select Referrals</h3>
          <p><span class="primary">Select custom home projects</span> in the Fraser Valley and Greater Vancouver ,  Chilliwack, Abbotsford, Langley, Vancouver, and West Vancouver ,  for existing clients and referrals.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="about-owner">
    <div class="wrap">
      <div class="grid">
        <div class="photo">
          <img src="../wp-content/uploads/2020/03/TCP_1620.jpg" alt="Jas Sidhu, owner of Palermo Homes, custom home builder in West Kelowna, BC">
        </div>
        <div class="copy">
          <p class="eyebrow">Meet the owner</p>
          <h2>Jas Sidhu, owner of Palermo Homes.</h2>
          <p>Jas has led Palermo Homes for over 15 years, personally overseeing every custom home build from first design meeting to final walkthrough. He takes the first call on every new project.</p>
          <p>His approach is grounded in fixed-price contracts, documented change orders, and senior on-site project management on every build. No cost-plus surprises, no handoffs to junior PMs stretched across six jobs.</p>
          <p class="creds"><strong>Verifiable credentials:</strong> BC Housing Licensed Residential Builder number 42812, BC Corporate Registration BC1017682, member of the Canadian Home Builders' Association of British Columbia.</p>
          <a class="more" href="/about/jas-sidhu/">Read the full bio <span class="arr">&rarr;</span></a>
        </div>
      </div>
    </div>
  </section>

  <section class="about-faq">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">FAQ</p>
        <h2>About Palermo Homes, answered.</h2>
      </div>
      <div class="items">
        <details><summary>Where is Palermo Homes based?</summary><div class="ans">Palermo Homes is headquartered in Kelowna, BC. Our primary service area is Kelowna, West Kelowna, Lake Country, and Peachland, with select custom home and renovation projects across the Fraser Valley and Lower Mainland.</div></details>
        <details><summary>What kinds of projects do you take on?</summary><div class="ans">Fully custom new-build homes, whole-home renovations, kitchen and bathroom renovations, additions, and full-service general contracting. Every project is built to the same custom-home finish standard, regardless of scope.</div></details>
        <details><summary>How long has Palermo Homes been building?</summary><div class="ans">Fifteen-plus years designing and building custom homes across British Columbia, from the Okanagan to the Lower Mainland, with a hands-on team that self-performs the trades that define quality.</div></details>
        <details><summary>Do you take on custom home projects outside the Okanagan?</summary><div class="ans">Yes. While our headquarters and the majority of our current custom builds are in Kelowna and the Central Okanagan, we take on select custom home and renovation projects in the Fraser Valley and Lower Mainland for returning and referred clients.</div></details>
        <details><summary>What makes Palermo Homes different from other custom home builders in Kelowna?</summary><div class="ans">Three things: in-house crews on the trades that matter most, transparent line-item pricing with weekly progress reporting, and commercial-grade construction standards paired with market-aware design so every home holds its long-term value.</div></details>
      </div>
    </div>
  </section>

  <section class="about-cta">
    <div class="wrap">
      <h2>Ready to start your custom home in Kelowna?</h2>
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

ABOUT.write_text(new_html, encoding="utf-8")
print(f"About rebuilt. size {len(html)} -> {len(new_html)}")

# Always refresh nav/footer/dashes/validate after any page rewrite
import subprocess, sys
here = Path(__file__).parent
for script in ("replace_nav.py", "replace_footer.py", "kill_dashes.py", "validate_links.py"):
    print(f"\n>>> {script}")
    r = subprocess.run([sys.executable, str(here / script)])
    if r.returncode != 0 and script == "validate_links.py":
        raise SystemExit(f"validate_links.py failed with exit {r.returncode}")
