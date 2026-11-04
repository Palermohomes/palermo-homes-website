"""Build /services/ hub + 3 sub-pages using About page's Divi shell.
Each page: unique title/meta, Service+FAQPage schema, editorial layout.
Idempotent. Safe to rerun."""
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
ABOUT = SITE / "about" / "index.html"
base = ABOUT.read_text(encoding="utf-8")

# --- Shell extraction: everything before <div id="et-main-area"> ... and everything after </div><footer...>
open_marker = '<div id="et-main-area">'
close_marker = '<footer'
open_idx = base.find(open_marker)
inner_start = base.find('>', open_idx) + 1
footer_idx = base.find(close_marker, inner_start)
end = base.rfind('</div>', inner_start, footer_idx) + len('</div>')

SHELL_HEAD = base[:inner_start]  # up to and including <div id="et-main-area">
SHELL_FOOT = base[end:]           # </div><footer>...</html>

# ---- Marker for CSS block ----
CSS_START = "/* ==== SERVICES-V2 CSS START ==== */"
CSS_END = "/* ==== SERVICES-V2 CSS END ==== */"

SERVICES_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .svc{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .svc *{{box-sizing:border-box}}
html body #et-main-area .svc img{{display:block;max-width:100%;height:auto}}
html body #et-main-area .svc .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .svc .eyebrow{{font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:#0085c9;font-weight:500;margin:0 0 20px}}

/* Hero. Full-bleed with left-aligned overlay (default: individual service pages) */
html body #et-main-area .svc-hero{{position:relative;min-height:clamp(240px,36vh,340px);padding:40px 0;display:flex;align-items:center;overflow:hidden;color:#fff}}
html body #et-main-area .svc-hero .bg{{position:absolute;inset:0;background-position:center center;background-size:cover;background-repeat:no-repeat;image-rendering:-webkit-optimize-contrast}}
html body #et-main-area .svc-hero::after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.50) 0%,rgba(0,0,0,.55) 50%,rgba(0,0,0,.70) 100%)}}
html body #et-main-area .svc-hero .inner{{position:relative;z-index:2;max-width:1360px;margin:0 auto;width:100%;padding:0 clamp(20px,3vw,48px);box-sizing:border-box}}
html body #et-main-area .svc-hero .eyebrow{{color:rgba(255,255,255,.9);margin:0 0 12px}}
html body #et-main-area .svc-hero h1{{font-size:clamp(28px,3.4vw,42px);font-weight:500;letter-spacing:-0.02em;line-height:1.05;margin:0;max-width:22ch;text-transform:none;color:#fff}}
html body #et-main-area .svc-hero p.sub{{font-size:clamp(15px,1.2vw,17px);color:rgba(255,255,255,.9);margin:16px 0 0;max-width:56ch;line-height:1.55}}

/* Hero. Centered/compact variant for the services hub */
html body #et-main-area .svc-hero.centered{{min-height:clamp(260px,38vh,360px)}}
html body #et-main-area .svc-hero.centered::after{{background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,.42) 50%,rgba(0,0,0,.52) 100%)}}
html body #et-main-area .svc-hero.centered .inner{{padding:0 clamp(20px,4vw,56px);text-align:center}}
html body #et-main-area .svc-hero.centered .eyebrow{{margin:0 auto 18px}}
html body #et-main-area .svc-hero.centered h1{{font-size:clamp(26px,3vw,38px);max-width:26ch;margin:0 auto;line-height:1.1}}
html body #et-main-area .svc-hero.centered p.sub{{margin:20px auto 0;max-width:56ch;text-align:center}}
/* Responsive hero image. Serve compressed version per viewport for Core Web Vitals */
html body #et-main-area .svc-hero.centered .bg{{background-image:url('/services/Cabernet-46-desktop.jpg')}}
@media (max-width:960px){{
  html body #et-main-area .svc-hero.centered .bg{{background-image:url('/services/Cabernet-46-mobile.jpg')}}
}}

/* Overview */
html body #et-main-area .svc-over{{padding:32px 0 24px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-over .head{{max-width:none;margin:0 0 20px;text-align:left}}
html body #et-main-area .svc-over .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-over h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21}}
html body #et-main-area .svc-over .body{{max-width:90ch}}
html body #et-main-area .svc-over p{{font-size:15px;line-height:1.65;color:#3a4048;margin:0 0 14px}}
html body #et-main-area .svc-over p:last-child{{margin:0}}

/* Split */
html body #et-main-area .svc-split{{padding:24px 0 32px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-split .grid{{display:grid;grid-template-columns:1fr 1.1fr;gap:56px;align-items:stretch}}
html body #et-main-area .svc-split .photo{{overflow:hidden;background:#f6f4ef;min-height:100%}}
html body #et-main-area .svc-split .photo img{{width:100%;height:100%;object-fit:cover;display:block}}
html body #et-main-area .svc-split .photo-col{{display:flex;flex-direction:column}}
html body #et-main-area .svc-split .photo-col .photo-loc{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 10px;text-align:left}}
html body #et-main-area .svc-split .photo-col .photo{{flex:1;min-height:0}}
html body #et-main-area .svc-split .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-split h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 18px;color:#1a1d21}}
html body #et-main-area .svc-split ul{{list-style:none;padding:0;margin:0}}
html body #et-main-area .svc-split li{{padding:16px 0;border-bottom:1px solid #ece8df;display:flex;gap:18px;align-items:flex-start}}
html body #et-main-area .svc-split li:last-child{{border-bottom:0}}
html body #et-main-area .svc-split li .num{{font-size:14px;color:#0085c9;font-weight:600;letter-spacing:.05em;flex:0 0 24px}}
html body #et-main-area .svc-split li .txt{{color:#2a2d33;font-size:15px;line-height:1.6}}
html body #et-main-area .svc-split li .txt strong{{color:#1a1d21;font-weight:600;display:block;margin-bottom:4px}}

/* FAQ */
html body #et-main-area .svc-faq{{padding:32px 0 36px;background:#fff;border-top:1px solid #e2ddd0}}
html body #et-main-area .svc-faq .head{{max-width:820px;margin:0 0 28px;text-align:left}}
html body #et-main-area .svc-faq .head .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-faq .head h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21;line-height:1.15}}
html body #et-main-area .svc-faq .items{{max-width:820px;margin:0}}
html body #et-main-area .svc-faq details{{background:#fff;border:1px solid #ece8df;margin-bottom:12px;padding:0}}
html body #et-main-area .svc-faq summary{{cursor:pointer;padding:20px 24px;font-weight:500;font-size:16px;color:#1a1d21;list-style:none;display:flex;justify-content:space-between;align-items:center}}
html body #et-main-area .svc-faq summary::-webkit-details-marker{{display:none}}
html body #et-main-area .svc-faq summary::after{{content:'+';font-size:22px;color:#0085c9;font-weight:400}}
html body #et-main-area .svc-faq details[open] summary::after{{content:'\\2013'}}
html body #et-main-area .svc-faq details[open] summary{{border-bottom:1px solid #ece8df}}
html body #et-main-area .svc-faq .ans{{padding:18px 24px 22px;color:#4a5058;font-size:15px;line-height:1.7}}

/* Related projects */
html body #et-main-area .svc-related{{padding:32px 0;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-related .head{{max-width:820px;margin:0 0 28px;text-align:left}}
html body #et-main-area .svc-related .head .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-related h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21;line-height:1.15}}
html body #et-main-area .svc-related .cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
html body #et-main-area .svc-related .card{{position:relative;overflow:hidden;aspect-ratio:4/3;text-decoration:none;color:#fff;background:#ddd}}
html body #et-main-area .svc-related .card img{{width:100%;height:100%;object-fit:cover;transition:transform .6s ease}}
html body #et-main-area .svc-related .card:hover img{{transform:scale(1.04)}}
html body #et-main-area .svc-related .card::after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(0,0,0,.7) 100%)}}
html body #et-main-area .svc-related .card .name{{position:absolute;left:20px;right:20px;bottom:18px;z-index:2;font-size:18px;font-weight:500;letter-spacing:-0.01em;display:flex;justify-content:space-between;align-items:flex-end}}

/* Hub. Services grid (full-width on desktop) */
html body #et-main-area .svc-hub{{padding:32px 0 60px;background:#fff}}
html body #et-main-area .svc-hub .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .svc-hub .head{{max-width:820px;margin:0 0 22px;text-align:left}}
html body #et-main-area .svc-hub .head .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-hub .head h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21;line-height:1.15}}
html body #et-main-area .svc-hub .cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:0}}
html body #et-main-area .svc-hub .card{{padding:44px 40px;border:1px solid #e2e0d9;text-decoration:none;color:inherit;transition:background .2s,border-color .2s;display:flex;flex-direction:column;gap:14px}}
html body #et-main-area .svc-hub .card+.card{{margin-left:-1px}}
html body #et-main-area .svc-hub .card:hover{{background:#faf9f5;border-color:#0085c9}}
html body #et-main-area .svc-hub .card h3{{font-size:22px;font-weight:600;letter-spacing:-0.01em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-hub .card p{{font-size:15px;color:#5a6069;line-height:1.6;margin:0}}
html body #et-main-area .svc-hub .card .go{{margin-top:auto;padding-top:24px;font-size:13px;letter-spacing:.15em;text-transform:uppercase;color:#0085c9;font-weight:500}}

/* CTA */
html body #et-main-area .svc-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center}}
html body #et-main-area .svc-cta h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 14px;color:#fff !important}}
html body #et-main-area .svc-cta p{{color:rgba(255,255,255,.92) !important;font-size:16px;margin:0 0 26px}}
html body #et-main-area .svc-cta a.btn{{display:inline-block;background:#fff;color:#0085c9;padding:14px 30px;border-radius:999px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;text-decoration:none;transition:background .2s,color .2s}}
html body #et-main-area .svc-cta a.btn:hover{{background:#141821;color:#fff}}

@media (max-width:900px){{
  /* Tight mobile hero so the CTA/services grid peeks above the fold */
  html body #et-main-area .svc-hero{{min-height:170px;padding:24px 0}}
  html body #et-main-area .svc-hero .eyebrow{{margin-bottom:6px;font-size:10px;letter-spacing:.24em}}
  html body #et-main-area .svc-hero h1{{font-size:28px;line-height:1.1;max-width:24ch}}
  html body #et-main-area .svc-hero p.sub{{font-size:13px;margin-top:8px;line-height:1.45}}
  html body #et-main-area .svc-split .grid{{grid-template-columns:1fr;gap:20px}}
  html body #et-main-area .svc-split .photo{{aspect-ratio:16/10;min-height:0}}
  html body #et-main-area .svc-related .cards{{grid-template-columns:1fr 1fr;gap:8px}}
  html body #et-main-area .svc-related .card{{aspect-ratio:1/1}}
  html body #et-main-area .svc-related .card .name{{left:12px;right:12px;bottom:12px;font-size:14px}}
  html body #et-main-area .svc-hub .cards{{grid-template-columns:1fr}}
  html body #et-main-area .svc-hub .card{{padding:14px 18px 14px;gap:5px}}
  html body #et-main-area .svc-hub .card+.card{{margin-left:0;margin-top:-1px}}
  html body #et-main-area .svc-hub .card h3{{font-size:16px}}
  html body #et-main-area .svc-hub .card p{{font-size:13px;line-height:1.45}}
  html body #et-main-area .svc-hub .card .go{{padding-top:4px;font-size:11px;letter-spacing:.14em}}
  html body #et-main-area .svc-over,html body #et-main-area .svc-faq,html body #et-main-area .svc-related,html body #et-main-area .svc-cta{{padding:24px 0}}
  html body #et-main-area .svc-split{{padding:16px 0 24px}}
  html body #et-main-area .svc-hub{{padding:16px 0 28px}}
}}
{CSS_END}
"""

# ---- Business info (used across all pages for schema) ----
BIZ_NAME = "Palermo Homes"
BIZ_URL = "https://palermohomes.com"
BIZ_PHONE = "+1-778-760-4113"
BIZ_CITY = "Kelowna"
BIZ_REGION = "BC"
BIZ_COUNTRY = "CA"
AREAS_SERVED = ["Kelowna", "West Kelowna", "Lake Country", "Peachland", "Vernon", "Penticton", "Okanagan Valley", "Fraser Valley", "Lower Mainland"]


def build_business_schema():
    areas = ",\n    ".join([f'{{"@type":"City","name":"{a}"}}' for a in AREAS_SERVED])
    return f'''{{
    "@type": "HomeAndConstructionBusiness",
    "@id": "{BIZ_URL}/#organization",
    "name": "{BIZ_NAME}",
    "url": "{BIZ_URL}",
    "telephone": "{BIZ_PHONE}",
    "address": {{"@type":"PostalAddress","addressLocality":"{BIZ_CITY}","addressRegion":"{BIZ_REGION}","addressCountry":"{BIZ_COUNTRY}"}},
    "areaServed": [{areas}]
  }}'''


def build_service_schema(name, description, service_type, page_url):
    return f'''{{
    "@type": "Service",
    "serviceType": "{service_type}",
    "name": "{name}",
    "description": "{description}",
    "url": "{page_url}",
    "provider": {build_business_schema()},
    "areaServed": [{", ".join([f'"{a}"' for a in AREAS_SERVED])}]
  }}'''


def build_faq_schema(faqs):
    items = []
    for q, a in faqs:
        items.append(f'''{{
      "@type": "Question",
      "name": {json.dumps(q)},
      "acceptedAnswer": {{"@type":"Answer","text":{json.dumps(a)}}}
    }}''')
    return f'''{{
    "@type": "FAQPage",
    "mainEntity": [{",".join(items)}]
  }}'''


def build_breadcrumb(page_name, page_url, is_hub=False):
    if is_hub:
        items = [
            f'{{"@type":"ListItem","position":1,"name":"Home","item":"{BIZ_URL}/"}}',
            f'{{"@type":"ListItem","position":2,"name":"Services","item":"{BIZ_URL}/services/"}}',
        ]
    else:
        items = [
            f'{{"@type":"ListItem","position":1,"name":"Home","item":"{BIZ_URL}/"}}',
            f'{{"@type":"ListItem","position":2,"name":"Services","item":"{BIZ_URL}/services/"}}',
            f'{{"@type":"ListItem","position":3,"name":"{page_name}","item":"{page_url}"}}',
        ]
    return '{"@type":"BreadcrumbList","itemListElement":[' + ",".join(items) + ']}'


def full_schema(page_schema, faq=None, breadcrumb=None):
    parts = [build_business_schema(), page_schema]
    if breadcrumb:
        parts.append(breadcrumb)
    if faq:
        parts.append(faq)
    return '<script type="application/ld+json">{"@context":"https://schema.org","@graph":[' + ",".join(parts) + ']}</script>'


# ---- Page renderer ----
def render_page(title, meta_desc, page_url, canonical, schema_block, main_html, out_path: Path):
    html = SHELL_HEAD + main_html + SHELL_FOOT
    # remove any prior SERVICES-V2 CSS block
    if CSS_START in html:
        html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.DOTALL)
    # remove any prior ABOUT-V2 CSS block on service pages (they don't need about styles)
    html = re.sub(r"/\* ==== ABOUT-V2 CSS START ==== \*/.*?/\* ==== ABOUT-V2 CSS END ==== \*/", "", html, flags=re.DOTALL)
    # inject services CSS (as its own style block before </head>, tolerating whatever's between </style> and </head>)
    html = html.replace("</head>", f"<style>{SERVICES_CSS}</style></head>", 1)
    # replace <title>
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', html, count=1)
    # Strip existing canonical (any attribute order), inject fresh
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{canonical}"/>\n</head>', 1)
    # Strip existing meta description, inject fresh
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{meta_desc}"/>\n</head>', 1)
    # Overwrite stale OG tags from the About shell
    _og_image = f"https://palermohomes.com/wp-content/uploads/2025/12/Cabernet-02.jpg"
    _og_title = title.replace(" | Palermo Homes", "")
    html = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{_og_title}" property="og:title"/>', html, count=1)
    html = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{canonical}" property="og:url"/>', html, count=1)
    html = re.sub(r'<meta[^>]*property="article:modified_time"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:data1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:label1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:description"/>\n?', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:image"/>\n?', '', html)
    html = re.sub(
        r'(<meta content="[^"]*" property="og:site_name"/>)',
        r'\1' + f'\n<meta content="{meta_desc}" property="og:description"/>\n<meta content="{_og_image}" property="og:image"/>',
        html, count=1,
    )
    html = re.sub(r'<script class="yoast-schema-graph"[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(
        r'<link rel="preload" as="image" href="[^"]*" fetchpriority="high">',
        f'<link rel="preload" as="image" href="{_og_image}" fetchpriority="high">',
        html, count=1,
    )
    # inject schema right before </head>
    html = html.replace("</head>", schema_block + "</head>", 1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"  wrote {out_path.relative_to(SITE)}")


# ---- Page content builders ----

def hub_page():
    hub_faqs = [
        ("Does Palermo Homes do both new custom homes and renovations?",
         "Yes. Palermo runs three service lines under one roof: custom home builds, whole-home renovations, and general contracting. The same in-house project managers, finish carpenters, and trade relationships handle every project, which keeps quality consistent across build types."),
        ("Which Okanagan cities do you serve?",
         "Palermo serves Kelowna, West Kelowna, Lake Country, Peachland, Vernon, and Penticton across the Okanagan Valley. We also take on select Lower Mainland projects in Abbotsford, Chilliwack, and Langley for returning clients and referrals."),
        ("How does Palermo pricing work?",
         "We offer both fixed-price contracts and cost-plus contracts depending on project scope and client preference. Fixed-price gives you a locked number up front after design. Cost-plus gives you full transparency on every trade invoice with a management fee on top. We walk through both options before contract signing."),
        ("How long does a custom home or whole-home renovation take?",
         "Custom home builds typically run 12 to 18 months from first design meeting to hand-over. Whole-home renovations run 4 to 9 months depending on scope. Kitchen or bathroom renovations run 6 to 12 weeks. Hillside lots, complex permits, or community design review can add time, which we flag at proposal stage."),
        ("Are all Palermo homes covered by the BC 2-5-10 warranty?",
         "Yes. Every Palermo new build is covered by the mandatory BC 2-5-10 New Home Warranty. Two years on labour and materials, five years on building envelope, ten years on structural. We're a BC Housing Licensed Residential Builder (License 42812)."),
        ("What's the difference between a custom home builder and a general contractor?",
         "A custom home builder designs and builds a home from scratch on your lot. A general contractor manages the trades and schedule for any construction project, custom or otherwise. Palermo offers both because many projects (additions, major renovations, outbuildings) need GC services without being full custom builds."),
        ("Can I meet the team before signing a contract?",
         "Yes. We always meet in person before any contract. Walk the lot, review your scope, and talk through contract options with Jas or a senior project manager. No cost, no pressure."),
    ]

    faq_items_html = "\n        ".join([
        f'<details><summary>{q}</summary><div class="ans">{a}</div></details>'
        for q, a in hub_faqs
    ])

    schema = full_schema(f'''{{
    "@type": "CollectionPage",
    "name": "Services. Palermo Homes",
    "url": "{BIZ_URL}/services/",
    "description": "Custom homes, home renovations, and general contracting services from Palermo Homes in Kelowna, BC."
  }}''', faq=build_faq_schema(hub_faqs), breadcrumb=build_breadcrumb("Services", f"{BIZ_URL}/services/", is_hub=True))
    main = f"""
<div class="svc">
  <section class="svc-hero">
    <div class="bg" style="background-image:url('/services/Cabernet-46-desktop.jpg')"></div>
    <link rel="preload" as="image" href="/services/Cabernet-46-desktop.jpg" media="(min-width: 961px)">
    <div class="inner">
      <p class="eyebrow">Services · Kelowna, BC</p>
      <h1>Custom homes, home renovations, and general contracting across the Okanagan.</h1>
      <p class="sub">One team. One contract. One point of accountability. From first concept to final walk-through.</p>
    </div>
  </section>

  <section class="svc-over">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Overview</p>
        <h2>A full-service custom home builder serving Kelowna and the Okanagan since 2014.</h2>
      </div>
      <div class="body">
        <p>Palermo Homes Ltd. is a BC Housing Licensed Residential Builder (License 42812) running three service lines under one roof: custom home design and construction, whole-home renovations, and project management on general contracting work. Every project is handled by in-house staff from first design meeting through final walk-through, which keeps the finish standard consistent whether we are building a lakefront custom home on Cabernet Way or renovating a 1980s split-level in Glenmore.</p>
        <p>Our primary service area is the Central Okanagan (Kelowna, West Kelowna, Lake Country, Peachland), with active work in Vernon and Penticton and select Fraser Valley and Lower Mainland projects in Abbotsford. Pricing is transparent: we offer both fixed-price and cost-plus contract structures and walk through both before signing. Every new build carries the BC 2-5-10 New Home Warranty. Call <a href="tel:+17787604113" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1;font-weight:600">(778) 760-4113</a> for a no-pressure consultation.</p>
      </div>
    </div>
  </section>

  <section class="svc-hub">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Services</p>
        <h2>Three service lines, one team, one contract.</h2>
      </div>
      <div class="cards">
        <a class="card" href="custom-homes/">
          <h3>Custom Homes</h3>
          <p>New custom home builds across Kelowna, West Kelowna, Lake Country, Peachland, Vernon, and Penticton. Lakeview, hillside, and view-lot specialists. Full-service from land evaluation and design through finish carpentry and the BC 2-5-10 warranty handover.</p>
          <span class="go">Custom Homes →</span>
        </a>
        <a class="card" href="renovations/">
          <h3>Home Renovations</h3>
          <p>Whole-home renovations, major kitchens and bathrooms, additions, and exterior transformations across the Okanagan. Built to the same finish standard as our custom homes, with scope planning that keeps you in the home where possible.</p>
          <span class="go">Renovations →</span>
        </a>
        <a class="card" href="general-contracting/">
          <h3>General Contracting</h3>
          <p>Project management on complex builds that don't fit the custom-home box. Transparent budget reporting, weekly progress updates, in-house quality control, and the trade relationships we've built over 15+ years in the Okanagan.</p>
          <span class="go">General Contracting →</span>
        </a>
      </div>
    </div>
  </section>

  <section class="svc-faq">
    <div class="wrap">
      <div class="head"><p class="eyebrow">FAQ</p><h2>Palermo services, answered.</h2></div>
      <div class="items">
        {faq_items_html}
      </div>
    </div>
  </section>

  <section class="svc-cta">
    <div class="wrap">
      <h2>Ready to start?</h2>
      <p>Tell us about your project. We will book a no-pressure consultation.</p>
      <a class="btn" href="../contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""
    render_page(
        title="Services | Palermo Homes. Custom Home Builder in Kelowna, BC",
        meta_desc="Palermo Homes offers custom home builds, whole-home renovations, and general contracting across Kelowna, West Kelowna, and the Okanagan since 2014.",
        page_url=f"{BIZ_URL}/services/",
        canonical=f"{BIZ_URL}/services/",
        schema_block=schema,
        main_html=main,
        out_path=SITE / "services" / "index.html",
    )


def custom_homes_page():
    faqs = [
        ("How long does a custom home take to build in Kelowna?",
         "Most Palermo custom homes take 10 to 16 months from foundation to hand-over, depending on size, site conditions, and finish level. Design and permitting typically add another 3 to 6 months before ground-break."),
        ("What is the typical budget range for a Palermo custom home?",
         "Our custom builds generally start at $1.5M and scale up based on square footage, site work, and specification. We provide transparent line-item budgeting so you see exactly where your investment goes."),
        ("Do you work with my architect and existing plans, or do you design from scratch?",
         "Both. We work with your architect, refer you to trusted local designers, or manage design in-house through our network. We prefer to be involved early. The sooner we’re at the table, the better we can optimize cost and constructability."),
        ("Do you handle permits and inspections?",
         "Yes. Full-service general contracting means we handle municipal permits, engineering coordination, and every inspection through occupancy. You get one point of contact for the entire process."),
        ("Where do you build custom homes?",
         "Primarily Kelowna, West Kelowna, Lake Country, and Peachland. We also take on select projects across the Okanagan Valley and continue serving past clients in the Fraser Valley and Lower Mainland."),
    ]
    schema = full_schema(
        build_service_schema(
            name="Custom Home Construction",
            description="Custom home design and construction in Kelowna, BC and the Okanagan Valley by Palermo Homes.",
            service_type="Custom Home Construction",
            page_url=f"{BIZ_URL}/services/custom-homes/",
        ),
        faq=build_faq_schema(faqs),
        breadcrumb=build_breadcrumb("Custom Homes", f"{BIZ_URL}/services/custom-homes/"),
    )
    faq_html = "\n".join([
        f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in faqs
    ])
    main = f"""
<div class="svc">
  <section class="svc-hero">
    <div class="bg" style="background-image:url('../../wp-content/uploads/2026/01/1556-Cabernet-nate-42.jpg')"></div>
    <div class="inner">
      <p class="eyebrow">Custom Homes · Kelowna, BC</p>
      <h1>Custom homes built around how you actually live.</h1>
      <p class="sub">Custom home design and construction across Kelowna, West Kelowna, and the Okanagan Valley.</p>
    </div>
  </section>

  <section class="svc-over">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Overview</p>
        <h2>Custom home construction across Kelowna, West Kelowna, and the Okanagan.</h2>
      </div>
      <div class="body">
        <p>Palermo is a custom home builder based in Kelowna, BC, building custom homes across Kelowna, West Kelowna, Lake Country, Peachland, and the Okanagan Valley. Commercial-grade construction, honest project management, and homes that hold their value for decades.</p>
      </div>
    </div>
  </section>

  <section class="svc-split">
    <div class="wrap"><div class="grid">
      <div class="photo">
        <img src="../../wp-content/uploads/2025/12/Cabernet-02.jpg" alt="Custom home built by Palermo Homes in Kelowna, BC">
      </div>
      <div>
        <p class="eyebrow">Our process</p>
        <h2>Four phases, one team, zero handoffs.</h2>
        <ul>
          <li><span class="num">01</span><span class="txt"><strong>Concept &amp; feasibility</strong>Site walk, budget alignment, and early architectural direction so nothing is a surprise at permit time.</span></li>
          <li><span class="num">02</span><span class="txt"><strong>Design &amp; engineering</strong>We coordinate architect, interior designer, and structural engineer as one team. All under our project management.</span></li>
          <li><span class="num">03</span><span class="txt"><strong>Construction</strong>In-house trades on the work that defines quality; hand-picked specialists everywhere else. Weekly progress reporting from day one.</span></li>
          <li><span class="num">04</span><span class="txt"><strong>Hand-over &amp; warranty</strong>Detailed walk-through, homeowner orientation, and a full warranty period. We stay reachable long after the keys change hands.</span></li>
        </ul>
      </div>
    </div></div>
  </section>

  <section class="svc-related">
    <div class="wrap">
      <div class="head"><p class="eyebrow">Selected work</p><h2>Recent custom builds.</h2></div>
      <div class="cards">
        <a class="card" href="../../project/cabernet-2/"><img src="../../wp-content/uploads/2026/01/1556-Cabernet-nate-42.jpg" alt="Luxury Modern Custom Home on Cabernet Way, West Kelowna" loading="lazy"><div class="name"><span>Luxury Modern Home on Cabernet Way</span><span>→</span></div></a>
        <a class="card" href="../../project/touriga-place-1/"><img src="../../wp-content/uploads/2025/12/Touriga-109.jpg" alt="Modern Lakeview Custom Home on Touriga Place, West Kelowna" loading="lazy"><div class="name"><span>Modern Lakeview Home on Touriga Place</span><span>→</span></div></a>
        <a class="card" href="../../project/vineyard-estates-4/"><img src="../../wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg" alt="Modern Hillside Custom Home in Vineyard Estates, West Kelowna" loading="lazy"><div class="name"><span>Modern Hillside Home in Vineyard Estates</span><span>→</span></div></a>
      </div>
    </div>
  </section>

  <section class="svc-faq">
    <div class="wrap">
      <div class="head"><p class="eyebrow">FAQ</p><h2>Custom home questions, answered.</h2></div>
      <div class="items">{faq_html}</div>
    </div>
  </section>

  <section class="svc-cta">
    <div class="wrap">
      <h2>Have a custom build in mind?</h2>
      <p>Book a no-pressure consultation. We’ll walk your site and talk feasibility.</p>
      <a class="btn" href="../../contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""
    render_page(
        title="Custom Home Construction in Kelowna, BC | Palermo Homes",
        meta_desc="Custom home design and construction in Kelowna, West Kelowna, and the Okanagan Valley. 15+ years of hands-on building. Get a consultation.",
        page_url=f"{BIZ_URL}/services/custom-homes/",
        canonical=f"{BIZ_URL}/services/custom-homes/",
        schema_block=schema,
        main_html=main,
        out_path=SITE / "services" / "custom-homes" / "index.html",
    )


def renovations_page():
    faqs = [
        ("What kinds of home renovations do you take on?",
         "Everything from whole-home renovations and additions to kitchens, bathrooms, exteriors, and basement suites. If it needs custom-home finish quality, we take it on. Our team is best suited to substantial renovations rather than small repair work."),
        ("Do you renovate in Kelowna and West Kelowna?",
         "Yes. Renovations across Kelowna, West Kelowna, Lake Country, and Peachland are our primary market. We also take on select projects in the Fraser Valley and Lower Mainland for returning and referred clients."),
        ("How long does a typical home renovation take?",
         "A kitchen or single-room renovation typically runs 6 to 12 weeks. A whole-home renovation is usually 4 to 9 months depending on scope. We build a critical-path schedule for every project so you know the timeline before we start."),
        ("Can we live in the home during the renovation?",
         "Sometimes, yes. If we're renovating a defined zone (kitchen, primary suite, basement) we can typically dust-wall the work area and keep the rest of the home livable. Whole-home renovations usually mean moving out for at least part of the project."),
        ("Do you handle permits, inspections, and drawings?",
         "Yes. Permit coordination, structural drawings, engineering, and municipal inspections are all handled in-house or by our regular consulting team. You get one point of contact for the entire project."),
        ("How is a Palermo renovation different from a general contractor?",
         "Our renovations are built to the same standard as our custom homes. Commercial-grade materials, in-house finish carpentry, designer-selected finishes, and 2-5-10 warranty coverage on the new work where applicable. We treat every renovation like a custom build inside an existing home."),
    ]
    schema = full_schema(
        build_service_schema(
            name="Home Renovations",
            description="Whole-home renovations, kitchens, bathrooms, and additions across Kelowna, the Okanagan, the Fraser Valley, and the Lower Mainland by Palermo Homes.",
            service_type="Home Renovation",
            page_url=f"{BIZ_URL}/services/renovations/",
        ),
        faq=build_faq_schema(faqs),
        breadcrumb=build_breadcrumb("Renovations", f"{BIZ_URL}/services/renovations/"),
    )
    faq_html = "\n".join([
        f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in faqs
    ])
    main = f"""
<div class="svc">
  <section class="svc-hero">
    <div class="bg" style="background-image:url('../../wp-content/uploads/2023/08/Vineyard-Estates-3-Re-Sized-Photo_2.jpg')"></div>
    <div class="inner">
      <p class="eyebrow">Home Renovations · Kelowna, BC</p>
      <h1>Custom-quality home renovations across Kelowna, the Okanagan, the Fraser Valley, and the Lower Mainland.</h1>
      <p class="sub">Whole-home renovations, kitchens, bathrooms, and additions. Built to the same standard as our custom homes.</p>
    </div>
  </section>

  <section class="svc-over">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Overview</p>
        <h2>Home renovations across Kelowna, the Okanagan, the Fraser Valley, and the Lower Mainland.</h2>
      </div>
      <div class="body">
        <p>Palermo is a home renovation contractor based in Kelowna, BC, handling whole-home renovations, kitchen renovations, bathroom renovations, and additions across Kelowna, West Kelowna, Lake Country, and the Okanagan Valley.</p>
      </div>
    </div>
  </section>

  <section class="svc-split">
    <div class="wrap"><div class="grid">
      <div class="photo-col">
        <p class="photo-loc">West Kelowna</p>
        <div class="photo">
          <img src="../../wp-content/uploads/2025/12/Cabernet-25.jpg" alt="Custom home renovation interior finish in West Kelowna by Palermo Homes">
        </div>
      </div>
      <div>
        <p class="eyebrow">What we renovate</p>
        <h2>All scopes. Custom-home quality.</h2>
        <ul>
          <li><span class="num">01</span><span class="txt"><strong>Whole-home renovations</strong>Full interior overhauls, structural reconfiguration, envelope upgrades. Older Kelowna homes brought up to modern performance and finish standards.</span></li>
          <li><span class="num">02</span><span class="txt"><strong>Kitchen renovations</strong>Custom cabinetry, stone countertops, high-end appliances, and layouts designed around how you actually cook and entertain.</span></li>
          <li><span class="num">03</span><span class="txt"><strong>Bathroom renovations</strong>Primary suites, ensuites, powder rooms. Custom tile work, curbless showers, heated floors, and considered fixtures.</span></li>
          <li><span class="num">04</span><span class="txt"><strong>Additions and expansions</strong>Second-storey additions, primary-suite extensions, and garage-to-living conversions. Structural, envelope, and finish all handled in-house.</span></li>
          <li><span class="num">05</span><span class="txt"><strong>Exterior renovations</strong>Siding, roofing, windows, decks, and outdoor living spaces. Practical performance upgrades that also refresh curb appeal.</span></li>
        </ul>
      </div>
    </div></div>
  </section>

  <section class="svc-faq">
    <div class="wrap">
      <div class="head"><p class="eyebrow">FAQ</p><h2>Home renovation questions, answered.</h2></div>
      <div class="items">{faq_html}</div>
    </div>
  </section>

  <section class="svc-cta">
    <div class="wrap">
      <h2>Renovating a home in Kelowna or the Okanagan?</h2>
      <p>Tell us about the project. We'll walk the space and talk feasibility.</p>
      <a class="btn" href="../../contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""
    render_page(
        title="Home Renovations in Kelowna & the Okanagan | Palermo Homes",
        meta_desc="Custom-quality home renovations by Palermo Homes in Kelowna, West Kelowna, Lake Country, the Fraser Valley, and the Lower Mainland. Whole-home, kitchen, bath.",
        page_url=f"{BIZ_URL}/services/renovations/",
        canonical=f"{BIZ_URL}/services/renovations/",
        schema_block=schema,
        main_html=main,
        out_path=SITE / "services" / "renovations" / "index.html",
    )


def general_contracting_page():
    faqs = [
        ("What does full-service general contracting include?",
         "Everything from initial budgeting and permit coordination through trade management, scheduling, on-site supervision, quality control, and final hand-over. You get one point of contact for the entire project."),
        ("Do you self-perform any trades?",
         "Yes. We keep the trades that define quality in-house (framing, finish carpentry, and site management), and coordinate hand-picked subcontractors for the specialised work. That way accountability doesn’t get lost between crews."),
        ("How do you manage project timelines?",
         "Every project runs on a critical-path schedule that’s reviewed weekly. Clients get regular progress updates with photos and any variance from the plan flagged early. No surprises at hand-over."),
        ("Do you take on renovations or only new builds?",
         "Our focus is new residential construction, but we take on select high-end renovations and additions for existing clients or projects where the scope aligns with our team."),
        ("Where do you take on GC work?",
         "Primarily the Central Okanagan. Kelowna, West Kelowna, Lake Country, and Peachland. Select projects further afield in the North and South Okanagan, the Fraser Valley, and the Lower Mainland based on scope and client fit. Palermo has 15+ years of general contracting experience across both regions."),
    ]
    schema = full_schema(
        build_service_schema(
            name="General Contracting",
            description="Full-service residential general contracting in Kelowna, BC and the Okanagan by Palermo Homes.",
            service_type="General Contracting",
            page_url=f"{BIZ_URL}/services/general-contracting/",
        ),
        faq=build_faq_schema(faqs),
        breadcrumb=build_breadcrumb("General Contracting", f"{BIZ_URL}/services/general-contracting/"),
    )
    faq_html = "\n".join([
        f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in faqs
    ])
    main = f"""
<div class="svc">
  <section class="svc-hero">
    <div class="bg" style="background-image:url('../../wp-content/uploads/2025/12/gc-hero-exterior.jpg')"></div>
    <div class="inner">
      <p class="eyebrow">General Contracting · Kelowna, BC</p>
      <h1>Full-service general contracting for residential builds.</h1>
      <p class="sub">One team, one contract, one point of accountability from permits to hand-over.</p>
    </div>
  </section>

  <section class="svc-over">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Overview</p>
        <h2>The coordination is the craft.</h2>
      </div>
      <div class="body">
        <p>Palermo is a residential general contractor in Kelowna, BC, coordinating custom home construction across Kelowna, West Kelowna, Lake Country, and the Okanagan Valley with in-house crews and detailed project management.</p>
      </div>
    </div>
  </section>

  <section class="svc-split">
    <div class="wrap"><div class="grid">
      <div class="photo">
        <img src="../../wp-content/uploads/2025/12/gc-split-interior.jpg" alt="Palermo Homes general contracting project interior in Kelowna">
      </div>
      <div>
        <p class="eyebrow">How we work</p>
        <h2>A GC that’s actually on-site.</h2>
        <ul>
          <li><span class="num">01</span><span class="txt"><strong>Transparent budgeting</strong>Line-item pricing from the start, with change orders tracked in real time. You always know where the project stands financially.</span></li>
          <li><span class="num">02</span><span class="txt"><strong>Weekly progress reporting</strong>Photos, milestones, and any variance from the schedule. Delivered to your inbox every week, no chasing required.</span></li>
          <li><span class="num">03</span><span class="txt"><strong>In-house quality control</strong>Site supervisors on every project. We catch issues at framing so they don’t become drywall problems.</span></li>
          <li><span class="num">04</span><span class="txt"><strong>Trade relationships that matter</strong>The same electricians, plumbers, and finishers on every job. Consistent quality, predictable pricing.</span></li>
        </ul>
      </div>
    </div></div>
  </section>

  <section class="svc-related">
    <div class="wrap">
      <div class="head"><p class="eyebrow">Recent projects</p><h2>See our GC work.</h2></div>
      <div class="cards">
        <a class="card" href="../../project/1252/"><img src="../../wp-content/uploads/2025/12/Cabernet-02.jpg" alt="Modern Lakeview Custom Home on Cabernet Way, West Kelowna" loading="lazy"><div class="name"><span>Modern Lakeview Home on Cabernet Way</span><span>→</span></div></a>
        <a class="card" href="../../project/malbec-place-1/"><img src="../../wp-content/uploads/2025/12/1587-Malbec-14.jpg" alt="Modern Lakeview Custom Home on Malbec Place, West Kelowna" loading="lazy"><div class="name"><span>Modern Lakeview Home on Malbec Place</span><span>→</span></div></a>
        <a class="card" href="../../project/vineyard-estates-4/"><img src="../../wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg" alt="Modern Hillside Custom Home in Vineyard Estates, West Kelowna" loading="lazy"><div class="name"><span>Modern Hillside Home in Vineyard Estates</span><span>→</span></div></a>
      </div>
    </div>
  </section>

  <section class="svc-faq">
    <div class="wrap">
      <div class="head"><p class="eyebrow">FAQ</p><h2>General contracting questions, answered.</h2></div>
      <div class="items">{faq_html}</div>
    </div>
  </section>

  <section class="svc-cta">
    <div class="wrap">
      <h2>Need a GC who’s actually on-site?</h2>
      <p>Tell us about your project. We’ll walk you through how we’d run it.</p>
      <a class="btn" href="../../contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""
    render_page(
        title="General Contractor in Kelowna, BC | Palermo Homes",
        meta_desc="Full-service residential general contracting in Kelowna and the Okanagan. Transparent budgeting, weekly reporting, in-house crews. Get a consultation.",
        page_url=f"{BIZ_URL}/services/general-contracting/",
        canonical=f"{BIZ_URL}/services/general-contracting/",
        schema_block=schema,
        main_html=main,
        out_path=SITE / "services" / "general-contracting" / "index.html",
    )


if __name__ == "__main__":
    print("Building services pages...")
    hub_page()
    custom_homes_page()
    renovations_page()
    general_contracting_page()
    print("Done.")


_POSTBUILD_DIR = Path(__file__).parent

def run_post_build():
    import subprocess, sys
    for script in ("replace_nav.py", "replace_footer.py", "kill_dashes.py", "validate_links.py"):
        print("\n>>> " + script)
        r = subprocess.run([sys.executable, str(_POSTBUILD_DIR / script)])
        if r.returncode != 0 and script == "validate_links.py":
            raise SystemExit("validate_links.py failed exit " + str(r.returncode))

import atexit
atexit.register(run_post_build)
