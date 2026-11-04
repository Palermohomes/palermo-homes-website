"""Build /guides/custom-home-cost-kelowna/. First long-form article page.
Optimized for featured snippet capture on "cost to build custom home Kelowna" query.
Includes FAQPage + Article + BreadcrumbList + WebPage schema.
Idempotent. Safe to rerun."""
import re
import json
from pathlib import Path
import datetime

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
PAGE_URL = f"{BIZ_URL}/guides/custom-home-cost-kelowna/"
PUBLISH_DATE = "2026-09-29"
MODIFIED_DATE = datetime.date.today().isoformat()

CSS_START = "/* ==== GUIDE-COST CSS START ==== */"
CSS_END = "/* ==== GUIDE-COST CSS END ==== */"

GUIDE_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .guide{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .guide *{{box-sizing:border-box}}
html body #et-main-area .guide .wrap{{max-width:760px;margin:0 auto;padding:0 clamp(20px,4vw,32px)}}

/* Hero */
html body #et-main-area .guide-hero{{background:#fff;color:#1a1d21;border-bottom:1px solid #e2ddd0;padding:56px 0 44px}}
html body #et-main-area .guide-hero .crumb{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 22px;padding:0}}
html body #et-main-area .guide-hero .crumb a{{color:#0085c9;text-decoration:none;opacity:.75;transition:opacity .2s}}
html body #et-main-area .guide-hero .crumb a:hover{{opacity:1}}
html body #et-main-area .guide-hero .crumb .sep{{margin:0 10px;opacity:.5}}
html body #et-main-area .guide-hero h1{{font-size:clamp(28px,3.4vw,42px);font-weight:700;letter-spacing:-0.02em;line-height:1.15;margin:0 0 18px;padding:0;color:#1a1d21}}
html body #et-main-area .guide-hero .sub{{font-size:clamp(15px,1.15vw,17px);line-height:1.55;color:#3a4048;margin:0;padding:0}}
html body #et-main-area .guide-hero .meta{{font-size:12px;color:#8a8f97;letter-spacing:.02em;margin:22px 0 0;padding-top:22px;border-top:1px solid #ece8df}}

/* Body */
html body #et-main-area .guide-body{{background:#fff;padding:40px 0 56px}}
html body #et-main-area .guide-body p{{font-size:16px;line-height:1.75;color:#3a4048;margin:0 0 20px;letter-spacing:-0.005em}}
html body #et-main-area .guide-body p strong{{color:#1a1d21;font-weight:600}}
html body #et-main-area .guide-body .lede{{background:#f4f9fc;border-left:3px solid #0085c9;padding:22px 24px;margin:0 0 28px;border-radius:0 4px 4px 0}}
html body #et-main-area .guide-body .lede p{{margin:0;font-size:16px;line-height:1.7;color:#1a1d21;font-weight:500}}
html body #et-main-area .guide-body h2{{font-size:clamp(22px,2.2vw,28px);font-weight:600;letter-spacing:-0.015em;line-height:1.25;color:#1a1d21;margin:44px 0 18px;padding:0}}
html body #et-main-area .guide-body h3{{font-size:clamp(17px,1.55vw,20px);font-weight:600;letter-spacing:-0.01em;line-height:1.3;color:#1a1d21;margin:32px 0 12px;padding:0}}
html body #et-main-area .guide-body ul{{margin:0 0 20px;padding:0 0 0 22px}}
html body #et-main-area .guide-body ul li{{font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 8px}}
html body #et-main-area .guide-body a{{color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1;font-weight:500;transition:border-color .2s}}
html body #et-main-area .guide-body a:hover{{border-bottom-color:#0085c9}}
html body #et-main-area .guide-body hr{{border:0;border-top:1px solid #e2ddd0;margin:36px 0}}
html body #et-main-area .guide-body .footer-note{{font-size:14px;color:#6a7078;font-style:italic;margin:24px 0 0;line-height:1.6}}

/* About Palermo section */
html body #et-main-area .guide-about{{background:#fff;padding:36px 0 40px;border-top:1px solid #e2ddd0}}
html body #et-main-area .guide-about h2{{font-size:clamp(20px,2vw,24px);font-weight:600;letter-spacing:-0.01em;color:#1a1d21;margin:0 0 14px}}
html body #et-main-area .guide-about p{{font-size:15px;line-height:1.65;color:#3a4048;margin:0 0 14px}}
html body #et-main-area .guide-about a{{color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1;font-weight:500}}

/* CTA */
html body #et-main-area .guide-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center}}
html body #et-main-area .guide-cta h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.2;margin:0 0 12px;color:#fff}}
html body #et-main-area .guide-cta p{{font-size:15px;line-height:1.6;color:rgba(255,255,255,.92);margin:0 0 24px}}
html body #et-main-area .guide-cta .btn{{display:inline-block;background:#fff;color:#0085c9;font-size:14px;font-weight:600;letter-spacing:.02em;padding:14px 32px;text-decoration:none;border-radius:2px;transition:opacity .2s}}
html body #et-main-area .guide-cta .btn:hover{{opacity:.9}}

@media (max-width:640px){{
  html body #et-main-area .guide-hero{{padding:36px 0 28px}}
  html body #et-main-area .guide-body{{padding:24px 0 40px}}
  html body #et-main-area .guide-body h2{{margin:32px 0 14px}}
  html body #et-main-area .guide-body h3{{margin:24px 0 10px}}
}}
{CSS_END}
"""

# FAQ entries for schema. These are the questions this article answers
FAQ_ITEMS = [
    {
        "q": "What is the typical cost to build a custom home in Kelowna in 2026?",
        "a": "The typical cost to build a custom home in Kelowna in 2026 ranges from $500 to $900 per square foot for above-grade finished space, plus $200 to $350 per square foot for finished basement space. A standard 3,000 square foot custom home in Kelowna typically costs between $1.5 million and $2.7 million for the home alone, not including land."
    },
    {
        "q": "What is the typical cost to build a 2,000 square foot house in BC?",
        "a": "A 2,000 square foot custom home in Kelowna typically costs $1 million to $1.8 million for the home alone. Add $400,000 to $700,000 for a comparable finished basement, and $100,000 to $400,000 for hillside site conditions."
    },
    {
        "q": "What is the typical cost to build a 3,000 square foot house in BC?",
        "a": "A 3,000 square foot custom home in Kelowna typically costs $1.5 million to $2.7 million for the home alone. Add $600,000 to $1.05 million if you finish the basement."
    },
    {
        "q": "What is the typical cost to build a 4,000 square foot house in BC?",
        "a": "A 4,000 square foot custom home in Kelowna typically costs $2 million to $3.6 million for the home alone. Add $800,000 to $1.4 million for a finished basement, common at this size."
    },
    {
        "q": "How long does it take to build a custom home in Kelowna?",
        "a": "A typical custom home in Kelowna takes 14 to 20 months from your first design meeting to move-in. This breaks down as 3 to 5 months for architectural design and interior selections, 2 to 3 months for permits and geotechnical assessment (longer on hillside lots), and 9 to 12 months for actual construction."
    },
    {
        "q": "How much does a hillside lot add to construction cost in Kelowna?",
        "a": "Building on a hillside lot in Kelowna adds $100,000 to $400,000 over a comparable flat lot. This applies to popular neighborhoods including Upper Mission, Kettle Valley, McKinley Beach, Lakeview Heights in West Kelowna, and Predator Ridge near Vernon. Costs include retaining walls, deep pilings, drainage systems, geotechnical assessments, additional excavation, and access road construction."
    },
]


def build_schema():
    faq_entities = []
    for item in FAQ_ITEMS:
        faq_entities.append({
            "@type": "Question",
            "name": item["q"],
            "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
        })

    faq = {"@type": "FAQPage", "mainEntity": faq_entities}

    article = {
        "@type": "Article",
        "@id": f"{PAGE_URL}#article",
        "headline": "What Is the Typical Cost to Build a Custom Home in Kelowna in 2026?",
        "description": "A complete cost breakdown for custom homes in Kelowna and the Okanagan, including per-square-foot pricing, hidden costs, hillside build premiums, and how to budget realistically.",
        "author": {
            "@type": "Person",
            "@id": f"{BIZ_URL}/about/jas-sidhu/#person",
            "name": "Jas Sidhu",
            "url": f"{BIZ_URL}/about/jas-sidhu/",
            "jobTitle": "Owner, Palermo Homes",
        },
        "publisher": {
            "@type": "Organization",
            "@id": f"{BIZ_URL}/#organization",
            "name": "Palermo Homes",
        },
        "datePublished": PUBLISH_DATE,
        "dateModified": MODIFIED_DATE,
        "mainEntityOfPage": PAGE_URL,
        "url": PAGE_URL,
        "articleSection": "Guides",
        "about": [
            {"@type": "Thing", "name": "Custom Home Construction"},
            {"@type": "Place", "name": "Kelowna, BC"},
            {"@type": "Place", "name": "Okanagan Valley"},
        ],
    }

    breadcrumbs = {
        "@type": "BreadcrumbList",
        "@id": f"{PAGE_URL}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BIZ_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{BIZ_URL}/guides/"},
            {"@type": "ListItem", "position": 3, "name": "Cost to Build a Custom Home in Kelowna", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "What Is the Typical Cost to Build a Custom Home in Kelowna in 2026?",
        "description": "A complete cost breakdown for custom homes in Kelowna and the Okanagan, including per-square-foot pricing, hidden costs, hillside build premiums, and how to budget realistically.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, article, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Cost to Build a Custom Home in Kelowna 2026 | Palermo Homes"
META_DESC = "A complete breakdown of what it costs to build a custom home in Kelowna. Size tiers, hillside premiums, and hidden costs."
CANONICAL = PAGE_URL

MAIN_HTML = """
<div class="guide">
  <section class="guide-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">·</span><a href="/guides/">Guides</a><span class="sep">·</span>Cost to Build a Custom Home in Kelowna</p>
      <h1>What Is the Typical Cost to Build a Custom Home in Kelowna in 2026?</h1>
      <p class="sub">A complete cost breakdown for custom homes in Kelowna and the Okanagan, including per-square-foot pricing, hidden costs, hillside build premiums, and how to budget realistically.</p>
      <p class="meta">Published September 2026 · By <a href="/about/jas-sidhu/" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1">Jas Sidhu</a>, Owner of Palermo Homes · Custom Home Builder in West Kelowna, BC</p>
    </div>
  </section>

  <section class="guide-body">
    <div class="wrap">
      <div class="lede">
        <p>The typical cost to build a custom home in Kelowna in 2026 ranges from $500 to $900 per square foot for above-grade finished space, plus $200 to $350 per square foot for finished basement space. A standard 3,000 square foot custom home in Kelowna typically costs between $1.5 million and $2.7 million for the home alone, not including land.</p>
      </div>

      <figure style="margin:28px 0 32px;padding:0">
        <img src="/wp-content/uploads/2026/01/1583-Malbec-13.jpg" alt="Completed custom home by Palermo Homes on Malbec Place in West Kelowna with imported stone work and premium finishes" style="width:100%;height:auto;display:block;border-radius:4px" loading="lazy" width="1200" height="800">
        <figcaption style="font-size:13px;color:#6a7078;margin:10px 0 0;line-height:1.5;font-style:italic">A completed Palermo Homes custom build on Malbec Place in West Kelowna. Imported stone, custom millwork, and a chef-grade kitchen package landed this project in the high-end per-square-foot band.</figcaption>
      </figure>

      <p>This is the direct answer most people are searching for. The rest of this article explains what changes those numbers, what most builders don't tell you, and how to budget realistically for a custom build in the Okanagan.</p>

      <h2>Cost breakdown by build tier</h2>
      <p>Custom home construction costs in Kelowna fall into three broad tiers based on finishes, architectural complexity, and site conditions.</p>

      <h3>Entry-level custom builds: $500 to $600 per square foot</h3>
      <p>Standard finishes, straightforward architecture, flat lots. A 3,000 square foot entry-level custom home in Kelowna typically costs $1.5 million to $1.8 million.</p>
      <p>Included at this tier:</p>
      <ul>
        <li>Standard cabinets and countertops</li>
        <li>Standard flooring (carpet, laminate, some tile)</li>
        <li>Basic lighting packages</li>
        <li>Standard windows and doors</li>
        <li>Simple rooflines</li>
      </ul>

      <h3>Mid-range custom homes: $650 to $800 per square foot</h3>
      <p>Premium finishes, engineered hardwood, quartz counters, custom cabinetry, moderate architectural complexity. A 3,000 square foot mid-range custom home in Kelowna typically costs $1.95 million to $2.4 million.</p>
      <p>Included at this tier:</p>
      <ul>
        <li>Custom cabinetry throughout</li>
        <li>Engineered hardwood flooring</li>
        <li>Quartz or granite countertops</li>
        <li>Premium plumbing fixtures</li>
        <li>Higher-end lighting</li>
        <li>Better window packages</li>
      </ul>

      <h3>High-end custom builds: $850 to $1,200+ per square foot</h3>
      <p>Imported materials, complex geometry, specialty systems, wine rooms, home theatres, indoor pools, or bespoke millwork. A 3,000 square foot high-end custom home in Kelowna typically costs $2.55 million to $3.6 million or more.</p>
      <p>Included at this tier:</p>
      <ul>
        <li>Fully custom millwork</li>
        <li>Imported stone, tile, and hardwood</li>
        <li>Complex architectural features</li>
        <li>Smart home automation</li>
        <li>Specialty rooms (wine cellars, theatres, gyms)</li>
        <li>Premium appliance packages</li>
      </ul>

      <h2>Hillside and waterfront build premiums</h2>
      <p>Building on a hillside lot in Kelowna adds $100,000 to $400,000 over a comparable flat lot. This applies to popular neighborhoods including <a href="/neighborhoods/upper-mission/">Upper Mission</a>, <a href="/neighborhoods/kettle-valley/">Kettle Valley</a>, McKinley Beach, <a href="/neighborhoods/lakeview-heights/">Lakeview Heights</a> in West Kelowna, and <a href="/neighborhoods/predator-ridge/">Predator Ridge</a> near Vernon.</p>
      <p>Hillside premium costs include:</p>
      <ul>
        <li>Retaining walls and site engineering</li>
        <li>Deep pilings for hillside foundations</li>
        <li>Drainage systems</li>
        <li>Geotechnical assessments</li>
        <li>Additional excavation</li>
        <li>Access road construction</li>
      </ul>
      <p>Waterfront lots on Okanagan Lake, Kalamalka Lake, or Skaha Lake add similar premiums due to shoreline setback requirements, environmental assessments, and specialty foundation work.</p>

      <h2>What is the typical cost to build a 2,000 square foot house in BC?</h2>
      <p>A 2,000 square foot custom home in Kelowna typically costs $1 million to $1.8 million for the home alone. This assumes above-grade finished space at $500 to $900 per square foot, no finished basement included, a flat or gently sloped lot, and mid-range finishes.</p>
      <p>Add $400,000 to $700,000 for a comparable finished basement, and $100,000 to $400,000 for hillside site conditions.</p>

      <h2>What is the typical cost to build a 3,000 square foot house in BC?</h2>
      <p>A 3,000 square foot custom home in Kelowna typically costs $1.5 million to $2.7 million for the home alone. Add $600,000 to $1.05 million if you finish the basement.</p>

      <h2>What is the typical cost to build a 4,000 square foot house in BC?</h2>
      <p>A 4,000 square foot custom home in Kelowna typically costs $2 million to $3.6 million for the home alone. Add $800,000 to $1.4 million for a finished basement, common at this size.</p>

      <h2>How long does it take to build a custom home in Kelowna?</h2>
      <p>A typical custom home in Kelowna takes 14 to 20 months from your first design meeting to move-in:</p>
      <ul>
        <li>3 to 5 months for architectural design and interior selections</li>
        <li>2 to 3 months for permits and geotechnical assessment (longer on hillside lots)</li>
        <li>9 to 12 months for actual construction</li>
      </ul>
      <p>Hillside builds and homes with specialty features often add 4 to 8 weeks to the total timeline.</p>

      <h2>Costs most Kelowna builders don't include upfront</h2>
      <p>The published per-square-foot rate is only part of the story. Real total budgets for custom home construction in Kelowna also need to account for:</p>
      <p><strong>Land costs:</strong> $500,000 to $2.5 million for a Central Okanagan lot. Waterfront and hillside lots cost significantly more.</p>
      <p><strong>Design fees:</strong> $30,000 to $80,000 for architectural design. Some builders include this in the per-square-foot price; others charge separately.</p>
      <p><strong>Permits and development cost charges:</strong> $15,000 to $50,000 depending on the city (Kelowna, West Kelowna, Lake Country, Peachland, Penticton, Vernon all have different fee structures).</p>
      <p><strong>Landscaping and driveway:</strong> $30,000 to $150,000 depending on scope.</p>
      <p><strong>GST:</strong> 5% on the finished home value (this is significant on a $2 million home).</p>
      <p><strong>Contingency:</strong> 10 to 15% of construction cost is standard for unforeseen conditions.</p>

      <h2>How to budget realistically</h2>
      <p>Add up the following to get a realistic total budget for a custom home in Kelowna:</p>
      <ul>
        <li>Land cost</li>
        <li>Design and permits ($50,000 to $130,000)</li>
        <li>Construction cost (square footage times per-square-foot rate)</li>
        <li>Hillside/waterfront premium if applicable</li>
        <li>Landscaping ($50,000+)</li>
        <li>GST (5% of home value)</li>
        <li>10 to 15% contingency</li>
      </ul>
      <p>For a mid-range 3,000 square foot custom home on a flat lot in Kelowna, this typically totals $2.5 million to $3.5 million all-in, including land.</p>

      <h2>Real cost data from recent Palermo projects</h2>

      <p>Numbers in isolation do not tell the whole story. Here is what the ranges above look like applied to actual Okanagan builds we have delivered.</p>

      <p>Our <a href="/project/cabernet-2/">Cabernet Way project</a> in <a href="/neighborhoods/wilden/">Wilden</a> is a mid-range custom home on a hillside lot. The lot alone required additional geotechnical work and a retaining wall system that added roughly $185,000 over a comparable flat lot. Finishes were mid-range to upper-mid-range: engineered hardwood throughout, quartz counters, custom cabinetry, and a feature stone wall. The all-in build cost came in at the upper end of the mid-range per-square-foot band described earlier.</p>

      <p>Our <a href="/project/malbec-place-1/">Malbec Place project</a> in West Kelowna was built on a flat lot. The homeowners prioritized interior architectural detail and a chef-grade kitchen package. The resulting cost per square foot landed in the high-end band because of imported stone work, specialty millwork, and upgraded mechanical systems rather than site conditions.</p>

      <p>Two homes, similar scale, very different per-square-foot numbers. This is why asking for a rate alone is insufficient. The honest conversation starts with your lot, your design priorities, and your finish preferences, then arrives at a number.</p>

      <blockquote style="border-left:3px solid #0085c9;padding:14px 20px;margin:28px 0;background:#f4f9fc;font-style:italic;color:#1a1d21;font-size:16px;line-height:1.65">
        <p style="margin:0">"Clients often ask us for a per-square-foot number before we have seen the lot or discussed finishes. We can give a range, but the real number depends on dozens of decisions that have not been made yet. The builders who quote confidently before those conversations usually adjust pricing later.". Jas Sidhu, Owner, Palermo Homes</p>
      </blockquote>

      <h2>Why per-square-foot rates alone are misleading</h2>
      <p>Different builders include different things in their per-square-foot rate. Some quote a "shell" price that excludes cabinets, appliances, and finishes. Others quote a fully finished, turnkey price. When comparing bids from Kelowna custom home builders, always ask what is and is not included.</p>
      <p>A $600 per square foot quote that excludes finishes may end up costing more than a $750 per square foot quote that includes everything.</p>

      <p class="footer-note">Custom home cost expectations should always be discussed in the context of your specific lot, design, and finish preferences. The ranges in this article reflect current 2026 market conditions in the Central Okanagan.</p>
    </div>
  </section>

  <section class="guide-about">
    <div class="wrap">
      <h2>About Palermo Homes</h2>
      <p>Palermo Homes is a custom home builder based in West Kelowna, BC (BC Corporate Registration BC1017682, BC Housing Licensed Residential Builder Number 42812). We have been building custom homes and whole-home renovations across the Okanagan Valley and Lower Mainland for over 15 years.</p>
      <p>Our approach uses fixed-price contracts with transparent line-item budgeting, documented change orders, and senior on-site project management on every build. We build in <a href="/service-areas/kelowna/">Kelowna</a>, <a href="/service-areas/west-kelowna/">West Kelowna</a>, <a href="/service-areas/lake-country/">Lake Country</a>, <a href="/service-areas/peachland/">Peachland</a>, <a href="/service-areas/penticton/">Penticton</a>, <a href="/service-areas/vernon/">Vernon</a>, and select Lower Mainland communities.</p>
      <p>Our detailed <a href="/faq/">FAQ page</a> answers the most common questions we get about cost, timeline, contracts, warranty, and process.</p>
    </div>
  </section>

  <section class="guide-cta">
    <div class="wrap">
      <h2>Planning a custom home in the Okanagan?</h2>
      <p>Tell us about your lot and design goals. We'll book a no-pressure consultation.</p>
      <a class="btn" href="/contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""


OG_IMAGE = f"{BIZ_URL}/wp-content/uploads/2026/01/1583-Malbec-13.jpg"
OG_TITLE = "What Is the Typical Cost to Build a Custom Home in Kelowna in 2026?"
READING_TIME = "9 minutes"
ISO_MODIFIED = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    # remove any prior guide CSS block
    html = re.sub(r"/\* ==== GUIDE-COST CSS START ==== \*/.*?/\* ==== GUIDE-COST CSS END ==== \*/", "", html, flags=re.DOTALL)
    # remove any prior ABOUT-V2 CSS block (from the shell)
    html = re.sub(r"/\* ==== ABOUT-V2 CSS START ==== \*/.*?/\* ==== ABOUT-V2 CSS END ==== \*/", "", html, flags=re.DOTALL)
    # inject guide CSS
    html = html.replace("</head>", f"<style>{GUIDE_CSS}</style></head>", 1)
    # title, meta, canonical
    html = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', html, count=1)
    # Strip any existing meta description (any attribute order), inject fresh
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{META_DESC}"/>\n</head>', 1)
    # Strip any existing canonical tag (any attribute order), inject fresh
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{CANONICAL}"/>\n</head>', 1)
    # Overwrite stale OG + Twitter tags inherited from the About shell
    html = re.sub(
        r'<meta content="[^"]*" property="og:title"/>',
        f'<meta content="{OG_TITLE}" property="og:title"/>', html, count=1,
    )
    html = re.sub(
        r'<meta content="[^"]*" property="og:url"/>',
        f'<meta content="{CANONICAL}" property="og:url"/>', html, count=1,
    )
    # Remove article:modified_time entirely (no reliable per-page edit date)
    html = re.sub(r'<meta[^>]*property="article:modified_time"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:data1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:label1"[^>]*/?>\s*', '', html)
    # Add og:description + og:image after og:site_name (idempotent)
    html = re.sub(r'<meta content="[^"]*" property="og:description"/>\n?', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:image"/>\n?', '', html)
    html = re.sub(
        r'(<meta content="[^"]*" property="og:site_name"/>)',
        r'\1' + f'\n<meta content="{META_DESC}" property="og:description"/>\n<meta content="{OG_IMAGE}" property="og:image"/>',
        html, count=1,
    )
    # Strip the Yoast schema graph (About page JSON-LD that conflicts with ours)
    html = re.sub(r'<script class="yoast-schema-graph"[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    # Replace the stale preload image
    html = re.sub(
        r'<link rel="preload" as="image" href="[^"]*" fetchpriority="high">',
        f'<link rel="preload" as="image" href="{OG_IMAGE}" fetchpriority="high">',
        html, count=1,
    )
    # inject schema before </head>
    html = html.replace("</head>", schema_block + "</head>", 1)

    out = SITE / "guides" / "custom-home-cost-kelowna" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built featured-snippet-optimized cost guide page.")
