"""Build /guides/ hub page. Landing page listing all guide articles.
As we add more guides, add entries to the GUIDES list below.
Idempotent. Safe to rerun."""
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
ABOUT = SITE / "about" / "index.html"
base = ABOUT.read_text(encoding="utf-8")

open_marker = '<div id="et-main-area">'
close_marker = '<footer'
open_idx = base.find(open_marker)
inner_start = base.find('>', open_idx) + 1
footer_idx = base.find(close_marker, inner_start)
end = base.rfind('</div>', inner_start, footer_idx) + len('</div>')
SHELL_HEAD = base[:inner_start]
SHELL_FOOT = base[end:]

BIZ_URL = "https://palermohomes.com"
PAGE_URL = f"{BIZ_URL}/guides/"

# Add new guides to this list as they're published
GUIDES = [
    {
        "slug": "bc-2-5-10-new-home-warranty-explained",
        "title": "BC's 2-5-10 New Home Warranty Explained: What's Covered, What Isn't, and How to Claim",
        "desc": "A plain-English guide to BC's mandatory new home warranty. Three coverage periods explained, exclusions nobody mentions, claims process, builder failure protection, and resale transfer.",
        "category": "Warranty & Protection",
    },
    {
        "slug": "financing-custom-home-bc",
        "title": "Financing a Custom Home in BC: Construction Mortgages, Progress Draws, and Builders Lien Act Holdback",
        "desc": "How construction financing actually works in BC. Progress draw schedules, the 10% Builders Lien Act holdback, down payment, interest costs, and what lenders need before approving your custom home mortgage.",
        "category": "Financing",
    },
    {
        "slug": "custom-home-building-process-kelowna",
        "title": "The Custom Home Building Process in Kelowna: A Phase-by-Phase 2026 Guide",
        "desc": "Everything that happens when you build a custom home in Kelowna, from first consultation to move-in. 8 phases explained with durations, who is involved, and what the client is responsible for.",
        "category": "Process & Timeline",
    },
    {
        "slug": "whole-home-renovation-cost-okanagan",
        "title": "Whole-Home Renovation Cost in Kelowna and the Okanagan: 2026 Pricing Guide",
        "desc": "What a whole-home renovation really costs in Kelowna and the Central Okanagan in 2026. Pricing by scope level, by room, by renovation type, plus hidden costs that catch most homeowners off guard.",
        "category": "Cost & Budgeting",
    },
    {
        "slug": "custom-home-permits-okanagan",
        "title": "Custom Home Permits in Kelowna and the Okanagan: A 2026 Guide to Fees, Timelines, and Requirements",
        "desc": "Fees by municipality, required documents, Energy Step Code, Home Warranty, Development Cost Charges, and realistic permit review timelines for a custom home in the Central Okanagan.",
        "category": "Permits & Approvals",
    },
    {
        "slug": "hillside-custom-home-kelowna",
        "title": "Hillside Custom Home Builds in Kelowna and the Okanagan: Costs, Permits, and Timeline",
        "desc": "What a sloped lot really adds to the cost and schedule of a Kelowna custom home. Geotechnical requirements, Development Permit rules, retaining walls, and setback rules by municipality.",
        "category": "Site & Design",
    },
    {
        "slug": "fixed-price-vs-cost-plus-custom-home-kelowna",
        "title": "Fixed-Price vs Cost-Plus Contracts for Custom Homes in BC: A 2026 Guide",
        "desc": "A plain-English comparison of the two main construction contract types for custom homes in Kelowna. Which protects you from cost overruns, and when each one makes sense.",
        "category": "Contracts & Budgeting",
    },
    {
        "slug": "how-long-to-build-custom-home-kelowna",
        "title": "How Long Does It Take to Build a Custom Home in Kelowna? A 2026 Timeline Guide",
        "desc": "A realistic month-by-month timeline for designing, permitting, and building a custom home in Kelowna, plus the factors that extend or compress each phase.",
        "category": "Process & Timeline",
    },
    {
        "slug": "how-to-choose-custom-home-builder-kelowna",
        "title": "How to Choose a Custom Home Builder in Kelowna: A 2026 Guide",
        "desc": "Seven verification criteria, red flags to avoid, and how to compare bids from Kelowna custom home builders before signing any contract.",
        "category": "Choosing a Builder",
    },
    {
        "slug": "custom-home-cost-kelowna",
        "title": "What Is the Typical Cost to Build a Custom Home in Kelowna in 2026?",
        "desc": "Complete cost breakdown by home size, tier, hillside premiums, and hidden costs most builders don't tell you about.",
        "category": "Cost & Budgeting",
    },
]

CSS_START = "/* ==== GUIDES-HUB CSS START ==== */"
CSS_END = "/* ==== GUIDES-HUB CSS END ==== */"

HUB_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .guides-hub{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .guides-hub *{{box-sizing:border-box}}
html body #et-main-area .guides-hub .wrap{{max-width:1080px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}

/* Hero */
html body #et-main-area .guides-hero{{background:#fff;color:#1a1d21;border-bottom:1px solid #e2ddd0;padding:56px 0 44px}}
html body #et-main-area .guides-hero .crumb{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 22px;padding:0}}
html body #et-main-area .guides-hero .crumb a{{color:#0085c9;text-decoration:none;opacity:.75;transition:opacity .2s}}
html body #et-main-area .guides-hero .crumb a:hover{{opacity:1}}
html body #et-main-area .guides-hero .crumb .sep{{margin:0 10px;opacity:.5}}
html body #et-main-area .guides-hero h1{{font-size:clamp(28px,3.4vw,44px);font-weight:700;letter-spacing:-0.02em;line-height:1.1;margin:0 0 18px;padding:0;color:#1a1d21}}
html body #et-main-area .guides-hero .sub{{font-size:clamp(15px,1.15vw,17px);line-height:1.55;color:#3a4048;margin:0;padding:0;max-width:60ch}}

/* Grid */
html body #et-main-area .guides-list{{background:#fff;padding:44px 0 64px}}
html body #et-main-area .guides-list .grid{{display:grid;grid-template-columns:1fr;gap:20px}}
html body #et-main-area .guides-list .card{{display:block;padding:28px 30px;background:#fff;border:1px solid #e2ddd0;border-radius:4px;text-decoration:none;transition:border-color .2s,box-shadow .2s,transform .2s;cursor:pointer;position:relative}}
html body #et-main-area .guides-list .card:hover{{border-color:#0085c9;box-shadow:0 6px 24px rgba(0,133,201,.12);transform:translateY(-2px)}}
html body #et-main-area .guides-list .card .cat{{font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .guides-list .card h2{{font-size:clamp(18px,1.7vw,22px);font-weight:600;letter-spacing:-0.015em;line-height:1.3;color:#1a1d21;margin:0 0 10px;padding:0;transition:color .2s}}
html body #et-main-area .guides-list .card:hover h2{{color:#0085c9}}
html body #et-main-area .guides-list .card p{{font-size:15px;line-height:1.55;color:#3a4048;margin:0 0 18px}}
html body #et-main-area .guides-list .card .read-more{{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#0085c9;margin:0;transition:gap .2s}}
html body #et-main-area .guides-list .card .read-more .arrow{{display:inline-block;transition:transform .2s}}
html body #et-main-area .guides-list .card:hover .read-more{{gap:12px}}
html body #et-main-area .guides-list .card:hover .read-more .arrow{{transform:translateX(4px)}}
html body #et-main-area .guides-list .empty{{padding:40px 0;text-align:center;color:#8a8f97;font-size:15px}}

/* CTA */
html body #et-main-area .guides-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center}}
html body #et-main-area .guides-cta h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.2;margin:0 0 12px;color:#fff}}
html body #et-main-area .guides-cta p{{font-size:15px;line-height:1.6;color:rgba(255,255,255,.92);margin:0 0 24px}}
html body #et-main-area .guides-cta .btn{{display:inline-block;background:#fff;color:#0085c9;font-size:14px;font-weight:600;letter-spacing:.02em;padding:14px 32px;text-decoration:none;border-radius:2px;transition:opacity .2s}}
html body #et-main-area .guides-cta .btn:hover{{opacity:.9}}

@media (max-width:640px){{
  html body #et-main-area .guides-hero{{padding:36px 0 28px}}
  html body #et-main-area .guides-list{{padding:28px 0 44px}}
  html body #et-main-area .guides-list .card{{padding:22px 24px}}
}}
{CSS_END}
"""


def build_schema():
    breadcrumbs = {
        "@type": "BreadcrumbList",
        "@id": f"{PAGE_URL}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BIZ_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": PAGE_URL},
        ],
    }
    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "Custom Home Building Guides for Kelowna and the Okanagan",
        "description": "In-depth guides on custom home costs, timelines, contracts, hillside builds, and choosing a builder in Kelowna, West Kelowna, and the Okanagan Valley.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }
    # Also include a CollectionPage listing all guides
    item_list = {
        "@type": "ItemList",
        "@id": f"{PAGE_URL}#guides-list",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "url": f"{BIZ_URL}/guides/{g['slug']}/",
                "name": g["title"],
            }
            for i, g in enumerate(GUIDES)
        ],
    }
    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, item_list]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Custom Home Building Guides for Kelowna | Palermo Homes"
META_DESC = "In-depth guides on custom home costs, timelines, contracts, and choosing a builder in Kelowna, West Kelowna, and the Okanagan."
CANONICAL = PAGE_URL


def build_cards():
    if not GUIDES:
        return '<p class="empty">More guides coming soon.</p>'
    cards = []
    for g in GUIDES:
        cards.append(f'''
        <a class="card" href="/guides/{g["slug"]}/">
          <p class="cat">{g["category"]}</p>
          <h2>{g["title"]}</h2>
          <p>{g["desc"]}</p>
          <span class="read-more">Read the guide <span class="arrow">&rarr;</span></span>
        </a>''')
    return '\n'.join(cards)


MAIN_HTML_TEMPLATE = """
<div class="guides-hub">
  <section class="guides-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">·</span>Guides</p>
      <h1>Custom Home Building Guides for Kelowna and the Okanagan.</h1>
      <p class="sub">Straight-answer articles on custom home costs, timelines, contracts, hillside builds, and how to choose a builder in Kelowna, West Kelowna, Lake Country, Peachland, Penticton, Vernon, and the surrounding Okanagan Valley.</p>
    </div>
  </section>

  <section class="guides-list">
    <div class="wrap">
      <div class="grid">
        __CARDS__
      </div>
    </div>
  </section>

  <section class="guides-cta">
    <div class="wrap">
      <h2>Ready to start planning?</h2>
      <p>Tell us about your lot. We'll book a no-pressure consultation.</p>
      <a class="btn" href="/contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""


def render():
    schema_block = build_schema()
    main_html = MAIN_HTML_TEMPLATE.replace("__CARDS__", build_cards())
    html = SHELL_HEAD + main_html + SHELL_FOOT
    # remove any prior GUIDES-HUB CSS block
    html = re.sub(r"/\* ==== GUIDES-HUB CSS START ==== \*/.*?/\* ==== GUIDES-HUB CSS END ==== \*/", "", html, flags=re.DOTALL)
    # remove any prior ABOUT-V2 CSS block (from the shell)
    html = re.sub(r"/\* ==== ABOUT-V2 CSS START ==== \*/.*?/\* ==== ABOUT-V2 CSS END ==== \*/", "", html, flags=re.DOTALL)
    # inject hub CSS
    html = html.replace("</head>", f"<style>{HUB_CSS}</style></head>", 1)
    # title, meta, canonical
    html = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', html, count=1)
    # Strip any existing meta description (any attribute order), inject fresh
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{META_DESC}"/>\n</head>', 1)
    # Strip any existing canonical tag (any attribute order), inject fresh
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{CANONICAL}"/>\n</head>', 1)
    # Overwrite stale OG + Twitter tags inherited from the About shell
    import datetime as _dt
    _iso = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    _og_image = f"{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-02.jpg"
    html = re.sub(
        r'<meta content="[^"]*" property="og:title"/>',
        f'<meta content="{TITLE.replace(" | Palermo Homes", "")}" property="og:title"/>', html, count=1,
    )
    html = re.sub(
        r'<meta content="[^"]*" property="og:url"/>',
        f'<meta content="{CANONICAL}" property="og:url"/>', html, count=1,
    )
    # Remove article:modified_time entirely (no reliable per-page edit date)
    html = re.sub(r'<meta[^>]*property="article:modified_time"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:data1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:label1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:description"/>\n?', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:image"/>\n?', '', html)
    html = re.sub(
        r'(<meta content="[^"]*" property="og:site_name"/>)',
        r'\1' + f'\n<meta content="{META_DESC}" property="og:description"/>\n<meta content="{_og_image}" property="og:image"/>',
        html, count=1,
    )
    # Strip the Yoast About-page schema (conflicts with our hub schema)
    html = re.sub(r'<script class="yoast-schema-graph"[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    # Replace stale preload image
    html = re.sub(
        r'<link rel="preload" as="image" href="[^"]*" fetchpriority="high">',
        f'<link rel="preload" as="image" href="{_og_image}" fetchpriority="high">',
        html, count=1,
    )
    # inject schema before </head>
    html = html.replace("</head>", schema_block + "</head>", 1)

    out = SITE / "guides" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built /guides/ hub page.")
