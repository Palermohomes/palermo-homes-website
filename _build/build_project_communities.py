"""Rebuild /projects/ hub as a community grid + generate one landing page per community.
Uses the About page's Divi shell for consistency with the rest of the site.
Idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SHELL_SRC = SITE / "about" / "index.html"

# --- Extract head shell + footer shell from about page ---
base = SHELL_SRC.read_text(encoding="utf-8")
open_marker = '<div id="et-main-area">'
close_marker = "<footer"
open_idx = base.find(open_marker)
inner_start = base.find(">", open_idx) + 1
footer_idx = base.find(close_marker, inner_start)
end = base.rfind("</div>", inner_start, footer_idx) + len("</div>")
SHELL_HEAD = base[:inner_start]
SHELL_FOOT = base[end:]

CSS_START = "/* ==== PROJECTS-V2 CSS START ==== */"
CSS_END = "/* ==== PROJECTS-V2 CSS END ==== */"

PROJECTS_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .pv{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .pv *{{box-sizing:border-box}}
html body #et-main-area .pv img{{display:block;max-width:100%;height:auto}}
html body #et-main-area .pv .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .pv .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}

/* Hero */
html body #et-main-area .pv-hero{{position:relative;min-height:clamp(240px,36vh,340px);padding:40px 0;display:flex;align-items:center;overflow:hidden;color:#fff}}
html body #et-main-area .pv-hero .bg{{position:absolute;inset:0;background-position:center;background-size:cover;background-repeat:no-repeat}}
html body #et-main-area .pv-hero::after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.50) 0%,rgba(0,0,0,.55) 50%,rgba(0,0,0,.70) 100%)}}
html body #et-main-area .pv-hero .inner{{position:relative;z-index:2;max-width:1360px;margin:0 auto;width:100%;padding:0 clamp(20px,3vw,48px);box-sizing:border-box}}
html body #et-main-area .pv-hero .eyebrow{{color:rgba(255,255,255,.9);margin:0 0 12px}}
html body #et-main-area .pv-hero h1{{font-size:clamp(28px,3.4vw,42px);font-weight:500;letter-spacing:-0.02em;line-height:1.05;margin:0;max-width:22ch;color:#fff}}
html body #et-main-area .pv-hero p.sub{{font-size:clamp(15px,1.2vw,17px);color:rgba(255,255,255,.9);margin:16px 0 0;max-width:56ch;line-height:1.55}}

/* Section head + grid (shared for hub + community pages) */
html body #et-main-area .pv-grid-section{{padding:32px 0 56px;background:#fff}}
html body #et-main-area .pv-grid-section .head{{max-width:820px;margin:0 0 22px}}
html body #et-main-area .pv-grid-section h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21}}
html body #et-main-area .pv-grid-section p.intro{{font-size:15px;font-weight:400;line-height:1.6;color:#4a5058;margin:12px 0 0;max-width:64ch}}
html body #et-main-area .pv-grid-section .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}

/* Card (community or home) */
html body #et-main-area .pv-card{{display:block;text-decoration:none;color:inherit;background:#fff;overflow:hidden;transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease;border:1px solid #c9c3b5;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
html body #et-main-area .pv-card:hover{{transform:translateY(-6px);box-shadow:0 18px 40px rgba(0,0,0,.14);border-color:#0085c9}}
html body #et-main-area .pv-card .photo{{aspect-ratio:4/3;overflow:hidden;background:#e8e5dd;position:relative}}
html body #et-main-area .pv-card .photo img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s ease,filter .3s ease;filter:brightness(.96)}}
html body #et-main-area .pv-card:hover .photo img{{transform:scale(1.04);filter:brightness(1)}}
html body #et-main-area .pv-card .meta{{padding:18px 22px 20px;border-top:2px solid #0085c9;display:flex;justify-content:space-between;align-items:center;gap:14px}}
html body #et-main-area .pv-card .meta .txt{{min-width:0}}
html body #et-main-area .pv-card .meta h3{{font-size:19px;font-weight:600;letter-spacing:-0.01em;line-height:1.2;margin:0;color:#1a1d21}}
html body #et-main-area .pv-card .meta .label{{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#7a828c;font-weight:500;margin:0 0 6px}}
html body #et-main-area .pv-card .meta .end{{flex-shrink:0;display:inline-flex;align-items:center;gap:8px}}
html body #et-main-area .pv-card .meta .count{{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#0085c9;font-weight:600}}
html body #et-main-area .pv-card .meta .arr{{color:#0085c9;font-size:20px;line-height:1;font-weight:400;transition:transform .25s ease}}
html body #et-main-area .pv-card:hover .meta .arr{{transform:translateX(4px)}}

/* CTA row */
html body #et-main-area .pv-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center}}
html body #et-main-area .pv-cta h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 14px;color:#fff !important}}
html body #et-main-area .pv-cta p{{color:rgba(255,255,255,.92) !important;font-size:16px;margin:0 0 26px}}
html body #et-main-area .pv-cta a.btn{{display:inline-block;background:#fff;color:#0085c9;padding:14px 30px;border-radius:999px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;text-decoration:none;transition:background .2s,color .2s}}
html body #et-main-area .pv-cta a.btn:hover{{background:#141821;color:#fff}}

/* Back link on community pages */
html body #et-main-area .pv-back{{padding:22px 0 0;background:#fff}}
html body #et-main-area .pv-back .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .pv-back a{{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#5a6069;text-decoration:none;font-weight:500}}
html body #et-main-area .pv-back a:hover{{color:#0085c9}}

@media (max-width:900px){{
  html body #et-main-area .pv-grid-section .grid{{grid-template-columns:1fr;gap:14px}}
  html body #et-main-area .pv-grid-section.homes .grid{{grid-template-columns:1fr 1fr;gap:10px}}
  html body #et-main-area .pv-grid-section.homes .pv-card .meta{{padding:12px 12px 14px;gap:8px}}
  html body #et-main-area .pv-grid-section.homes .pv-card .meta h3{{font-size:14px}}
  html body #et-main-area .pv-grid-section.homes .pv-card .meta .label{{font-size:10px;margin:0 0 4px}}
  html body #et-main-area .pv-grid-section.homes .pv-card .meta .arr{{font-size:16px}}
  /* Tight mobile hero so the first card peeks above the fold */
  html body #et-main-area .pv-hero{{min-height:150px;padding:20px 0}}
  html body #et-main-area .pv-hero .eyebrow{{margin-bottom:6px;font-size:10px}}
  html body #et-main-area .pv-hero h1{{font-size:28px;line-height:1.1}}
  html body #et-main-area .pv-hero p.sub{{font-size:13px;margin-top:8px;line-height:1.4}}
  /* Compress head spacing so intro block is minimal */
  html body #et-main-area .pv-grid-section{{padding:14px 0 22px}}
  html body #et-main-area .pv-grid-section .head{{margin:0 0 12px}}
  html body #et-main-area .pv-grid-section h2{{line-height:1.2}}
  html body #et-main-area .pv-grid-section p.intro{{font-size:13px;line-height:1.45;margin-top:6px}}
  /* Shorter card aspect so more of it fits above the fold */
  html body #et-main-area .pv-card .photo{{aspect-ratio:16/10}}
  html body #et-main-area .pv-grid-section.homes .pv-card .photo{{aspect-ratio:4/3}}
  html body #et-main-area .pv-card .meta{{padding:12px 16px 14px}}
  html body #et-main-area .pv-card .meta h3{{font-size:17px}}
  html body #et-main-area .pv-card .meta .label{{margin-bottom:4px}}
}}
{CSS_END}
"""

# ---- Data model ----
# Each community: slug, display name, tagline, cover img, and list of homes
COMMUNITIES = [
    {
        "slug": 'cabernet',
        "name": 'Cabernet Way',
        "location": 'West Kelowna, BC',
        "hub_eyebrow": 'West Kelowna · Wine District',
        "tagline": "Custom homes on West Kelowna's Cabernet Way.",
        "intro": "Three custom builds on Cabernet Way in West Kelowna's wine district. Contemporary architecture, refined finishes, and considered layouts designed around lake views and Okanagan light.",
        "cover": '/wp-content/uploads/2025/12/Cabernet-02.jpg',
        "homes": [
            ('1252', 'Modern Lakeview Home on Cabernet Way', '/wp-content/uploads/2025/12/Cabernet-02.jpg'),
            ('cabernet-2', 'Luxury Modern Home on Cabernet Way', '/wp-content/uploads/2026/01/1556-Cabernet-nate-42.jpg'),
            ('cabernet-3', 'Modern Hillside Home on Cabernet Way', '/wp-content/uploads/2026/01/fplNrDJA.jpeg'),
        ],
    },
    {
        "slug": 'malbec',
        "name": 'Malbec Place',
        "location": 'West Kelowna, BC',
        "hub_eyebrow": 'West Kelowna · Wine District',
        "tagline": 'Modern custom homes on Malbec Place.',
        "intro": "Custom builds on Malbec Place. One of West Kelowna's most sought-after cul-de-sacs in the wine district. Modern architecture built around natural light, indoor-outdoor flow, and honest finish work.",
        "cover": '/wp-content/uploads/2025/12/1587-Malbec-14.jpg',
        "homes": [
            ('malbec-place-1', 'Modern Lakeview Home on Malbec Place', '/wp-content/uploads/2025/12/1587-Malbec-14.jpg'),
            ('malbec-2', 'Luxury Modern Home on Malbec Place', '/wp-content/uploads/2026/01/1583-Malbec-13.jpg'),
        ],
    },
    {
        "slug": 'eagle-mountain',
        "name": 'Eagle Mountain',
        "location": 'Abbotsford, BC',
        "tagline": "One of Abbotsford's most sought-after hillside communities.",
        "intro": "Nine custom builds on Eagle Mountain's dramatic hillside lots in Abbotsford. Every home takes full advantage of the elevation with panoramic Fraser Valley views, engineered for the mountain terrain and finished for four-season living.",
        "cover": '/wp-content/uploads/2019/06/PAL_Projects_Mahogany2_FEATURE.jpg',
        "homes": [
            ('713', 'New Build Custom Home on Eagle Summit Drive', '/wp-content/uploads/2020/05/PAL_Projects_NewHouse_FEATURE.jpg'),
            ('eagle-mountain-2', 'Luxury Mountain View Home on Mahogany Drive, Eagle Mountain', '/wp-content/uploads/2019/06/PAL_Projects_Mahogany2_FEATURE.jpg'),
            ('eagle-mountain-9', 'Modern Valley View Home on Verado Court, Eagle Mountain', '/wp-content/uploads/2023/08/WhatsApp-Image-2026-01-22-at-22.41.31-6.jpeg'),
            ('eagle-mountain-6', 'Modern Family Home on Eagle Summit Drive', '/wp-content/uploads/2019/07/PAL_Projects_GreenChairs_Row1a.jpg'),
            ('verado-court', 'Custom Home on Verado Court, Eagle Mountain', '/wp-content/uploads/2021/10/PAL_Projects_Verado_FEATURE211005.jpg'),
            ('eagle-mountain-4', 'Executive Modern Home on Montana Place, Eagle Mountain', '/wp-content/uploads/2019/06/PAL_Projects_EagleSummit_FEATURE.jpg'),
            ('eagle-mountain-3', 'Custom Home on Aquila Drive, Eagle Mountain', '/wp-content/uploads/2019/06/2773-Aquila-Drive-Abbotsford-1.jpg'),
            ('eagle-mountain-1', 'Modern Custom Home on Mahogany Drive, Eagle Mountain', '/wp-content/uploads/2019/06/PAL_Projects_Mahogany_FEATURE.jpg'),
            ('eagle-mountain-5', 'Hillside Walkout Home on Eagle Peak Drive, Eagle Mountain', '/wp-content/uploads/2019/06/35624-Eagle-Peak-Drive-5.jpg'),
        ],
    },
    {
        "slug": 'touriga',
        "name": 'Touriga Place',
        "location": 'West Kelowna, BC',
        "hub_eyebrow": 'West Kelowna · Wine District',
        "tagline": 'A signature build on Touriga Place.',
        "intro": 'A recent custom build on Touriga Place in West Kelowna with wide-open lakeview living, generous outdoor entertaining space, and material choices meant to weather decades of Okanagan seasons.',
        "cover": '/wp-content/uploads/2025/12/Touriga-109.jpg',
        "homes": [
            ('touriga-place-1', 'Modern Lakeview Home on Touriga Place', '/wp-content/uploads/2025/12/Touriga-109.jpg'),
        ],
    },
    {
        "slug": 'vineyard-estates',
        "name": 'Vineyard Estates',
        "location": 'West Kelowna, BC',
        "tagline": 'Refined homes in Vineyard Estates, West Kelowna.',
        "intro": "Two completed builds in Vineyard Estates, one of West Kelowna's most established custom-home neighbourhoods. Each home is designed to hold its value and its beauty for decades.",
        "cover": '/wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg',
        "homes": [
            ('vineyard-estates-4', 'Modern Hillside Home in Vineyard Estates', '/wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg'),
            ('vineyard-estates-3', 'Luxury Custom Home in Vineyard Estates', '/wp-content/uploads/2023/08/Vineyard-Estates-3-Re-Sized-Photo_2.jpg'),
        ],
    },
    {
        "slug": 'ledgestone',
        "name": 'Ledgestone Road',
        "location": 'Lake Country, BC',
        "tagline": "Hometown Heroes Lottery grand-prize home on Ledgestone Road.",
        "intro": "The Ledgestone Road build was Palermo Homes' Hometown Heroes Lottery grand-prize home in Lake Country. A benchmark project that raised funds for the BC Professional Fire Fighters' Burn Fund and VGH & UBC Hospital Foundation.",
        "cover": '/wp-content/uploads/2022/04/PAL_220411_Main2.jpg',
        "homes": [
            ('lakestone', "Custom Home on Ledgestone Road", '/wp-content/uploads/2022/04/PAL_220411_Main2.jpg'),
        ],
    },
    {
        "slug": 'west-abbotsford',
        "name": 'West Abbotsford',
        "location": 'Abbotsford, BC',
        "tagline": 'Legacy custom build in the Fraser Valley.',
        "intro": "A completed custom home in West Abbotsford. Part of Palermo's earlier body of work across the Fraser Valley and Lower Mainland.",
        "cover": '/wp-content/uploads/2019/06/PAL_Projects_Cambie_FEATURE-e1571985525124.jpg',
        "homes": [
            ('west-abbotsford', 'Modern Custom Home in West Abbotsford', '/wp-content/uploads/2019/06/PAL_Projects_Cambie_FEATURE-e1571985525124.jpg'),
        ],
    },
]


def inject_css(html: str) -> str:
    if CSS_START in html:
        html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.DOTALL)
    if "</head>" not in html:
        return html
    return html.replace("</head>", f"<style>{PROJECTS_CSS}</style></head>", 1)


def build_hub_html() -> str:
    cards = ""
    for c in COMMUNITIES:
        n = len(c["homes"])
        suffix = "home" if n == 1 else "homes"
        eyebrow = c.get("hub_eyebrow", c["location"])
        cards += f'''      <a class="pv-card" href="/projects/{c["slug"]}/" aria-label="View {c["name"]} custom homes">
        <div class="photo"><img src="{c["cover"]}" alt="{c["name"]} custom homes by Palermo Homes in {c["location"]}" loading="lazy"></div>
        <div class="meta">
          <div class="txt"><p class="label">{eyebrow}</p><h3>{c["name"]} Custom Homes</h3></div>
          <span class="end"><span class="count">{n} {suffix}</span><span class="arr" aria-hidden="true">&rarr;</span></span>
        </div>
      </a>
'''
    return f"""
<div class="pv">
  <section class="pv-hero">
    <div class="bg" style="background-image:url('/wp-content/uploads/2025/12/Cabernet-71.jpg')"></div>
    <div class="inner">
      <p class="eyebrow">Our communities</p>
      <h1>Custom homes across Kelowna's most sought-after neighbourhoods.</h1>
      <p class="sub">{sum(len(c['homes']) for c in COMMUNITIES)} completed custom builds grouped by community. Rooted in Kelowna and the Okanagan, with select projects across the Fraser Valley.</p>
    </div>
  </section>

  <section class="pv-grid-section">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Communities</p>
        <h2>Choose a community to see the homes.</h2>
      </div>
      <div class="grid">
{cards}      </div>
    </div>
  </section>

  <section class="pv-cta">
    <div class="wrap">
      <h2>Have a lot in mind?</h2>
      <p>Tell us where you want to build. We'll walk your site and talk feasibility.</p>
      <a class="btn" href="/contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""


def build_community_html(c: dict) -> str:
    cards = ""
    for slug, name, img in c["homes"]:
        cards += f'''      <a class="pv-card" href="/project/{slug}/" aria-label="View {name}">
        <div class="photo"><img src="{img}" alt="{name} custom home by Palermo Homes in {c["location"]}" loading="lazy"></div>
        <div class="meta">
          <div class="txt"><p class="label">{c["location"]}</p><h3>{name}</h3></div>
          <span class="arr" aria-hidden="true">&rarr;</span>
        </div>
      </a>
'''
    n = len(c["homes"])
    home_word = "home" if n == 1 else "homes"
    return f"""
<div class="pv">
  <section class="pv-hero">
    <div class="bg" style="background-image:url('{c["cover"]}')"></div>
    <div class="inner">
      <p class="eyebrow">Community · {c["location"]}</p>
      <h1>{c["name"]}</h1>
      <p class="sub">{c["tagline"]}</p>
    </div>
  </section>

  <section class="pv-grid-section homes">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">{n} {home_word}</p>
        <h2>Custom {home_word} in {c["name"]}, {c["location"]}</h2>
        <p class="intro">{c["intro"]}</p>
      </div>
      <div class="grid">
{cards}      </div>
    </div>
  </section>

  <section class="pv-cta">
    <div class="wrap">
      <h2>Interested in {c["name"]}?</h2>
      <p>Ask about lot availability, current builds, and next opportunities.</p>
      <a class="btn" href="/contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""


def build_page(main_html: str, title: str, meta_description: str, canonical: str, schema_json: str = "") -> str:
    html = SHELL_HEAD + main_html + SHELL_FOOT

    # update title
    html = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", html, count=1)
    # Strip existing canonical (any attribute order), inject fresh
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{canonical}"/>\n</head>', 1)
    # Strip existing meta description, inject fresh
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{meta_description}"/>\n</head>', 1)
    # Overwrite stale OG tags from the About shell
    _og_image = f"https://palermohomes.com/wp-content/uploads/2025/12/Cabernet-02.jpg"
    _og_title = title.replace(" | Palermo Homes | Custom Home Builder in Kelowna, BC", "").replace(" | Palermo Homes", "")
    html = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{_og_title}" property="og:title"/>', html, count=1)
    html = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{canonical}" property="og:url"/>', html, count=1)
    html = re.sub(r'<meta[^>]*property="article:modified_time"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:data1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:label1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:description"/>\n?', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:image"/>\n?', '', html)
    html = re.sub(
        r'(<meta content="[^"]*" property="og:site_name"/>)',
        r'\1' + f'\n<meta content="{meta_description}" property="og:description"/>\n<meta content="{_og_image}" property="og:image"/>',
        html, count=1,
    )
    html = re.sub(r'<script class="yoast-schema-graph"[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(
        r'<link rel="preload" as="image" href="[^"]*" fetchpriority="high">',
        f'<link rel="preload" as="image" href="{_og_image}" fetchpriority="high">',
        html, count=1,
    )
    # inject Projects CSS
    html = inject_css(html)
    # optional JSON-LD schema before </head>
    if schema_json:
        html = html.replace("</head>", f'<script type="application/ld+json">{schema_json}</script></head>', 1)
    return html


def write_pages():
    # --- Hub ---
    hub = SITE / "projects" / "index.html"
    hub_title = "Our Project Communities | Palermo Homes, Kelowna"
    hub_desc = "Browse custom homes by Palermo Homes across Kelowna, West Kelowna, Lake Country, Abbotsford, and the Lower Mainland."
    hub_canonical = "https://palermohomes.com/projects/"
    hub_schema = (
        '{"@context":"https://schema.org","@graph":['
        '{"@type":"CollectionPage","@id":"' + hub_canonical + '","url":"' + hub_canonical + '","name":"Palermo Homes Communities","description":"Custom homes by Palermo Homes across Kelowna and the Okanagan.","publisher":{"@type":"HomeAndConstructionBusiness","name":"Palermo Homes","address":{"@type":"PostalAddress","addressLocality":"Kelowna","addressRegion":"BC","addressCountry":"CA"},"telephone":"+1-778-760-4113"}},'
        '{"@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://palermohomes.com/"},'
        '{"@type":"ListItem","position":2,"name":"Projects","item":"https://palermohomes.com/projects/"}'
        ']}'
        ']}'
    )
    hub.write_text(build_page(build_hub_html(), hub_title, hub_desc, hub_canonical, hub_schema), encoding="utf-8")
    print(f"  wrote projects/index.html")

    # --- Community pages ---
    for c in COMMUNITIES:
        out = SITE / "projects" / c["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        canonical = f'https://palermohomes.com/projects/{c["slug"]}/'
        title = f'{c["name"]} Homes | Palermo Homes | {c["location"]}'
        # Per-community meta descriptions, factual, <=155 chars, no banned facts
        COMMUNITY_DESCS = {
            'cabernet':         "Palermo Homes custom builds on Cabernet Way in West Kelowna's wine district. Contemporary architecture and refined finishes.",
            'malbec':           "Palermo Homes custom builds on Malbec Place, a sought-after cul-de-sac in West Kelowna's wine district.",
            'eagle-mountain':   "Custom homes by Palermo Homes on Eagle Mountain's hillside lots in Abbotsford, BC. Every home designed around the elevation.",
            'touriga':          "A Palermo Homes custom build on Touriga Place in West Kelowna with lakeview living and generous outdoor entertaining space.",
            'vineyard-estates': "Palermo Homes custom builds in Vineyard Estates, one of West Kelowna's established custom-home neighbourhoods on the lakeview hillside.",
            'ledgestone':       "Palermo Homes' Hometown Heroes Lottery grand-prize custom home on Ledgestone Road in Lake Country, BC. A 2022 benchmark project.",
            'west-abbotsford':  "A completed Palermo Homes custom home in West Abbotsford, part of our Fraser Valley and Lower Mainland portfolio.",
        }
        desc = COMMUNITY_DESCS.get(c["slug"], f'{c["tagline"]} {c["intro"][:140]}')[:155]
        schema = (
            '{"@context":"https://schema.org","@graph":['
            '{"@type":"CollectionPage","@id":"' + canonical + '","url":"' + canonical + '","name":"' + c["name"] + ' Homes",'
            '"about":"' + c["intro"].replace('"', "'") + '",'
            '"publisher":{"@type":"HomeAndConstructionBusiness","name":"Palermo Homes",'
            '"address":{"@type":"PostalAddress","addressLocality":"Kelowna","addressRegion":"BC","addressCountry":"CA"},'
            '"telephone":"+1-778-760-4113"}},'
            '{"@type":"BreadcrumbList","itemListElement":['
            '{"@type":"ListItem","position":1,"name":"Home","item":"https://palermohomes.com/"},'
            '{"@type":"ListItem","position":2,"name":"Projects","item":"https://palermohomes.com/projects/"},'
            '{"@type":"ListItem","position":3,"name":"' + c["name"] + '","item":"' + canonical + '"}'
            ']}'
            ']}'
        )
        out.write_text(build_page(build_community_html(c), title, desc, canonical, schema), encoding="utf-8")
        print(f"  wrote projects/{c['slug']}/index.html")


if __name__ == "__main__":
    print("Building projects hub + community pages...")
    write_pages()
    print("Done.")


_POSTBUILD_DIR = Path(__file__).parent

def run_post_build():
    import subprocess, sys
    for script in ("update_project_seo_titles.py", "replace_nav.py", "replace_footer.py", "kill_dashes.py", "validate_links.py"):
        print("\n>>> " + script)
        r = subprocess.run([sys.executable, str(_POSTBUILD_DIR / script)])
        if r.returncode != 0 and script == "validate_links.py":
            raise SystemExit("validate_links.py failed exit " + str(r.returncode))

import atexit
atexit.register(run_post_build)
