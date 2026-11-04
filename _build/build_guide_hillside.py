"""Build /guides/hillside-custom-home-kelowna/
Guide #5 - "Hillside Custom Home Builds in Kelowna and the Okanagan."
Targets high-intent + low-competition queries: "hillside home builder kelowna",
"custom home sloped lot okanagan", "geotechnical report cost BC",
"retaining wall cost kelowna", "steep lot custom home west kelowna".
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
PAGE_URL = f"{BIZ_URL}/guides/hillside-custom-home-kelowna/"
PUBLISH_DATE = "2026-10-13"
MODIFIED_DATE = datetime.date.today().isoformat()

CSS_START = "/* ==== GUIDE-HILLSIDE CSS START ==== */"
CSS_END = "/* ==== GUIDE-HILLSIDE CSS END ==== */"

GUIDE_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .guide{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .guide *{{box-sizing:border-box}}
html body #et-main-area .guide .wrap{{max-width:760px;margin:0 auto;padding:0 clamp(20px,4vw,32px)}}
html body #et-main-area .guide-hero{{background:#fff;color:#1a1d21;border-bottom:1px solid #e2ddd0;padding:56px 0 44px}}
html body #et-main-area .guide-hero .crumb{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 22px;padding:0}}
html body #et-main-area .guide-hero .crumb a{{color:#0085c9;text-decoration:none;opacity:.75;transition:opacity .2s}}
html body #et-main-area .guide-hero .crumb a:hover{{opacity:1}}
html body #et-main-area .guide-hero .crumb .sep{{margin:0 10px;opacity:.5}}
html body #et-main-area .guide-hero h1{{font-size:clamp(28px,3.4vw,42px);font-weight:700;letter-spacing:-0.02em;line-height:1.15;margin:0 0 18px;padding:0;color:#1a1d21}}
html body #et-main-area .guide-hero .sub{{font-size:clamp(15px,1.15vw,17px);line-height:1.55;color:#3a4048;margin:0;padding:0}}
html body #et-main-area .guide-hero .meta{{font-size:12px;color:#8a8f97;letter-spacing:.02em;margin:22px 0 0;padding-top:22px;border-top:1px solid #ece8df}}
html body #et-main-area .guide-body{{background:#fff;padding:40px 0 56px}}
html body #et-main-area .guide-body p{{font-size:16px;line-height:1.75;color:#3a4048;margin:0 0 20px;letter-spacing:-0.005em}}
html body #et-main-area .guide-body p strong{{color:#1a1d21;font-weight:600}}
html body #et-main-area .guide-body .lede{{background:#f4f9fc;border-left:3px solid #0085c9;padding:22px 24px;margin:0 0 28px;border-radius:0 4px 4px 0}}
html body #et-main-area .guide-body .lede p{{margin:0;font-size:16px;line-height:1.7;color:#1a1d21;font-weight:500}}
html body #et-main-area .guide-body h2{{font-size:clamp(22px,2.2vw,28px);font-weight:600;letter-spacing:-0.015em;line-height:1.25;color:#1a1d21;margin:44px 0 18px;padding:0}}
html body #et-main-area .guide-body h3{{font-size:clamp(17px,1.55vw,20px);font-weight:600;letter-spacing:-0.01em;line-height:1.3;color:#1a1d21;margin:32px 0 12px;padding:0}}
html body #et-main-area .guide-body ul,html body #et-main-area .guide-body ol{{margin:0 0 20px;padding:0 0 0 22px}}
html body #et-main-area .guide-body ul li,html body #et-main-area .guide-body ol li{{font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 8px}}
html body #et-main-area .guide-body a{{color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1;font-weight:500;transition:border-color .2s}}
html body #et-main-area .guide-body a:hover{{border-bottom-color:#0085c9}}
html body #et-main-area .guide-body hr{{border:0;border-top:1px solid #e2ddd0;margin:36px 0}}
html body #et-main-area .guide-body .footer-note{{font-size:14px;color:#6a7078;font-style:italic;margin:24px 0 0;line-height:1.6}}
html body #et-main-area .guide-body table{{width:100%;border-collapse:collapse;margin:0 0 24px;font-size:15px}}
html body #et-main-area .guide-body table th{{text-align:left;padding:10px 14px;background:#f4f9fc;border:1px solid #e2ddd0;color:#1a1d21;font-weight:600;font-size:14px}}
html body #et-main-area .guide-body table td{{padding:10px 14px;border:1px solid #e2ddd0;color:#3a4048;line-height:1.55}}
html body #et-main-area .guide-about{{background:#fff;padding:36px 0 40px;border-top:1px solid #e2ddd0}}
html body #et-main-area .guide-about h2{{font-size:clamp(20px,2vw,24px);font-weight:600;letter-spacing:-0.01em;color:#1a1d21;margin:0 0 14px}}
html body #et-main-area .guide-about p{{font-size:15px;line-height:1.65;color:#3a4048;margin:0 0 14px}}
html body #et-main-area .guide-about a{{color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1;font-weight:500}}
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
  html body #et-main-area .guide-body table{{font-size:14px}}
  html body #et-main-area .guide-body table th,html body #et-main-area .guide-body table td{{padding:8px 10px}}
}}
{CSS_END}
"""

FAQ_ITEMS = [
    {
        "q": "How much more does it cost to build a custom home on a hillside lot in Kelowna?",
        "a": "A hillside lot typically adds $80,000 to $250,000 to the total project cost of a Kelowna custom home. That premium covers geotechnical investigation ($3,500 to $10,000), engineered retaining walls ($300 to $1,000 per linear foot), stepped foundations, upgraded drainage, excavation, and the additional engineering fees required for sloped sites. The exact number depends on slope angle, soil conditions, lot access, and how aggressively the home design works with or against the existing grade."
    },
    {
        "q": "What qualifies as a hillside lot under City of Kelowna rules?",
        "a": "The City of Kelowna's 2040 Official Community Plan defines hillside development as lands with a natural slope of 10% or greater over at least a 6-metre horizontal distance. Lots with portions exceeding 20% slope fall into a Hillside Development Permit (DP) Area, which requires a design-guideline review before building permit. Slopes of 30% or more trigger the Hazardous Conditions DP Area, with additional geotechnical and setback requirements. West Kelowna uses similar thresholds and in some cases stricter monitoring requirements."
    },
    {
        "q": "Do I need a geotechnical report to build on a sloped lot in the Okanagan?",
        "a": "Yes. Any lot with meaningful slope, soil instability, high water table, or proximity to a ridgeline or cliff requires a geotechnical report signed by a qualified professional engineer. For straightforward Okanagan sloped lots, geotechnical reports typically run $3,500 to $6,000. More complex sites with steep grade, variable soils, or deep investigation needs run $6,000 to $10,000 or more. The report drives foundation design, retaining wall engineering, drainage, and in some cases the allowable building setback."
    },
    {
        "q": "How much do engineered retaining walls cost on a Kelowna custom home?",
        "a": "Engineered retaining walls typically cost $300 to $700 per linear foot for standard applications and $400 to $1,000 per linear foot for engineered concrete walls common in the Lower Mainland and steeper Okanagan hillside sites. Any retaining wall over 1.2 metres (approximately 4 feet) in height requires a building permit and must be designed by a geotechnical engineer, with engineering and permit fees adding $1,500 to $3,500 on top of material and installation. A home requiring 60 linear feet of engineered wall is looking at $18,000 to $42,000 for the wall alone, before related drainage and backfill work."
    },
    {
        "q": "What are the setback rules for building near a slope, cliff, or ridgeline in Kelowna?",
        "a": "City of Kelowna requires a minimum 10-metre setback from the top of ridgelines, cliffs, and ravines on properties within the Hazardous Conditions Development Permit Area. A reduced setback is possible if a geotechnical report by a qualified professional justifies it. West Kelowna applies similar setbacks and in recent years has tightened monitoring and geotechnical documentation requirements. For specific setback calculations on a particular lot, the geotechnical engineer coordinates directly with the municipality."
    },
    {
        "q": "How much longer does a hillside custom home take to build in Kelowna?",
        "a": "Hillside builds add approximately 2 to 4 months to the overall timeline of a Kelowna custom home. The added time covers geotechnical investigation and report, Development Permit review (where required), additional structural engineering for stepped foundations and retaining walls, slower excavation on sloped access, and more complex site drainage installation. For a build that would run 14 to 18 months on a flat lot, allow 16 to 22 months on a comparable hillside lot."
    },
    {
        "q": "Can I avoid some of the hillside cost by designing the home to follow the grade?",
        "a": "Yes. Homes designed to step with the existing grade (walk-out basements, split-level entries, cantilevered decks instead of extensive retaining) often cost significantly less than homes that force a flat building pad through heavy cut-and-fill. City of Kelowna's hillside design guidelines explicitly encourage minimizing cut and fill to preserve natural topography. Working with a builder and designer experienced in Okanagan hillside sites from day one usually saves more money than any single construction decision made later."
    },
    {
        "q": "What should I check before buying a sloped lot in the Okanagan?",
        "a": "Before committing to a hillside purchase, walk the lot with an experienced builder and ideally a geotechnical engineer. Verify the slope percentage and whether it falls in a Hillside or Hazardous Conditions DP area, confirm access for construction equipment, check for ridgelines or ravines that trigger setbacks, look for drainage patterns and signs of past water or soil movement, and ask the municipality about any site-specific overlays. Palermo Homes offers pre-purchase lot walks for buyers considering hillside properties in Upper Mission, Kettle Valley, Wilden, Lakeview Heights, Predator Ridge, and other Okanagan hillside neighborhoods."
    },
]


def build_schema():
    faq_entities = [
        {"@type": "Question", "name": item["q"],
         "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
        for item in FAQ_ITEMS
    ]
    faq = {"@type": "FAQPage", "mainEntity": faq_entities}

    article = {
        "@type": "Article",
        "@id": f"{PAGE_URL}#article",
        "headline": "Hillside Custom Home Builds in Kelowna and the Okanagan: Costs, Permits, and Timeline",
        "description": "A complete guide to building a custom home on a sloped lot in Kelowna, West Kelowna, Vernon, and the Okanagan. Geotechnical requirements, Development Permit rules, retaining wall costs, foundation impact, and timeline.",
        "author": {
            "@type": "Person",
            "@id": f"{BIZ_URL}/about/jas-sidhu/#person",
            "name": "Jas Sidhu",
            "url": f"{BIZ_URL}/about/jas-sidhu/",
            "jobTitle": "Owner, Palermo Homes",
        },
        "publisher": {"@type": "Organization", "@id": f"{BIZ_URL}/#organization", "name": "Palermo Homes"},
        "datePublished": PUBLISH_DATE,
        "dateModified": MODIFIED_DATE,
        "mainEntityOfPage": PAGE_URL,
        "url": PAGE_URL,
        "articleSection": "Guides",
        "about": [
            {"@type": "Thing", "name": "Hillside Custom Home Construction"},
            {"@type": "Thing", "name": "Geotechnical Engineering"},
            {"@type": "Place", "name": "Kelowna, BC"},
            {"@type": "Place", "name": "West Kelowna, BC"},
            {"@type": "Place", "name": "Okanagan Valley"},
        ],
    }

    breadcrumbs = {
        "@type": "BreadcrumbList",
        "@id": f"{PAGE_URL}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BIZ_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{BIZ_URL}/guides/"},
            {"@type": "ListItem", "position": 3, "name": "Hillside Custom Home Builds in Kelowna", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "Hillside Custom Home Builds in Kelowna and the Okanagan: Costs, Permits, and Timeline",
        "description": "A complete guide to building a custom home on a sloped lot in Kelowna and the Okanagan. Geotechnical requirements, Development Permit rules, retaining wall costs, and timeline.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, article, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Hillside Custom Home Builds Kelowna: Costs & Permits | Palermo Homes"
META_DESC = "A complete guide to custom home builds on sloped lots in Kelowna and the Okanagan. Geotech, Development Permit rules, retaining walls, costs, and timeline."
CANONICAL = PAGE_URL

MAIN_HTML = """
<div class="guide">
  <section class="guide-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">&middot;</span><a href="/guides/">Guides</a><span class="sep">&middot;</span>Hillside Custom Home Builds in Kelowna</p>
      <h1>Hillside Custom Home Builds in Kelowna and the Okanagan: Costs, Permits, and Timeline</h1>
      <p class="sub">A straight-answer guide to building a custom home on a sloped lot in Kelowna, West Kelowna, Vernon, and across the Okanagan. What geotechnical work really costs, what the municipalities actually require, and how hillside sites change the budget and schedule.</p>
      <p class="meta">Published October 2026 &middot; By <a href="/about/jas-sidhu/" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1">Jas Sidhu</a>, Owner of Palermo Homes &middot; Custom Home Builder in West Kelowna, BC</p>
    </div>
  </section>

  <section class="guide-body">
    <div class="wrap">
      <div class="lede">
        <p>A hillside lot typically adds $80,000 to $250,000 to the total cost of a Kelowna custom home and 2 to 4 months to the timeline. The premium covers geotechnical investigation ($3,500 to $10,000), Development Permit review, engineered retaining walls ($300 to $1,000 per linear foot), stepped foundations, upgraded drainage, and the additional engineering those elements require. The size of the premium depends almost entirely on the slope, the soil, and how aggressively the home design works with or against the natural grade.</p>
      </div>

      <figure style="margin:28px 0 32px;padding:0">
        <img src="/wp-content/uploads/2025/12/Cabernet-02.jpg" alt="Completed hillside custom home by Palermo Homes on Cabernet Way in West Kelowna, overlooking Okanagan Lake" style="width:100%;height:auto;display:block;border-radius:4px" loading="lazy" width="1200" height="800">
        <figcaption style="font-size:13px;color:#6a7078;margin:10px 0 0;line-height:1.5;font-style:italic">A completed hillside custom home on Cabernet Way, West Kelowna. Stepped foundations and engineered retaining allowed the home to follow the natural grade with minimal cut and fill.</figcaption>
      </figure>

      <p>Almost every desirable view lot in the Central Okanagan is on a slope. Upper Mission, Kettle Valley, Wilden, Lakeview Heights, McKinley Beach, Predator Ridge, Eagle Mountain in Abbotsford, and most of the valley benches sit on grades steep enough to trigger Hillside Development Permit review and engineered foundation work. For buyers evaluating a sloped lot, the question is not whether the premium exists. The question is how large it will be, where it comes from, and what the design choices can do to control it.</p>

      <p>This guide walks through the real cost drivers, the specific municipal rules in Kelowna and West Kelowna, the engineering work that gets added, and how an experienced hillside builder scopes a build before you sign anything.</p>

      <h2>What qualifies as a "hillside" lot in Kelowna and West Kelowna</h2>

      <p>Both City of Kelowna and the District of West Kelowna use slope thresholds to classify when a lot requires hillside design review. The thresholds matter because they determine whether a Development Permit (DP) is required on top of the standard building permit.</p>

      <table>
        <thead>
          <tr><th>Slope condition</th><th>Classification</th><th>What it triggers</th></tr>
        </thead>
        <tbody>
          <tr><td>10% or greater over 6+ metres</td><td>Hillside land (per Kelowna OCP definition)</td><td>Hillside design considerations apply</td></tr>
          <tr><td>20% or greater on any portion of lot</td><td>Hillside Development Permit Area</td><td>DP review required before building permit</td></tr>
          <tr><td>30% or greater</td><td>Hazardous Conditions DP Area</td><td>Geotechnical review, setback rules, preserved open space</td></tr>
          <tr><td>Any ridgeline, cliff, or ravine on or adjacent to lot</td><td>Hazardous Conditions</td><td>Minimum 10-metre setback from top of feature</td></tr>
        </tbody>
      </table>

      <p>West Kelowna uses similar slope thresholds and in recent years has added stricter monitoring requirements for hillside builds, with more site inspections during construction and more documentation from the geotechnical engineer.</p>

      <p>A property can fall into more than one category. A hillside lot in Upper Mission that includes a ravine edge, for example, will trigger both the Hillside DP and Hazardous Conditions DP, with the setback rules applying on top of the general hillside design guidelines.</p>

      <h2>The real cost drivers on a hillside build</h2>

      <p>Hillside premium is not one line item. It is five or six separate costs that stack on top of what a comparable flat-lot build would run.</p>

      <table>
        <thead>
          <tr><th>Cost item</th><th>Typical range</th><th>What drives the number</th></tr>
        </thead>
        <tbody>
          <tr><td>Geotechnical investigation and report</td><td>$3,500 to $10,000+</td><td>Slope angle, soil variability, depth of investigation required</td></tr>
          <tr><td>Engineered retaining walls (per linear foot)</td><td>$300 to $1,000</td><td>Wall height, material (block, poured, SRW), engineering stamp</td></tr>
          <tr><td>Retaining wall engineering + permits</td><td>$1,500 to $3,500</td><td>Required on any wall over 1.2 m (approx. 4 ft)</td></tr>
          <tr><td>Site drainage system</td><td>$100 to $200 per linear foot</td><td>French drains, perforated pipe, backfill, outlets</td></tr>
          <tr><td>Excavation and site prep uplift</td><td>$20,000 to $80,000</td><td>Equipment access, haul distance, rock removal, slope stability</td></tr>
          <tr><td>Stepped foundation and structural uplift</td><td>$30,000 to $120,000</td><td>Multi-level footings, deeper piers, engineered steel, cantilevered sections</td></tr>
          <tr><td>Development Permit review and professional fees</td><td>$5,000 to $20,000</td><td>Architect, geotech, civil, DP application fees</td></tr>
        </tbody>
      </table>

      <p>Added together, the floor on a modest hillside premium is around $80,000. Steep lots with significant retaining, rock removal, or long engineered walls routinely push past $200,000. On the extreme end, lakefront or ridge-top lots with major grade changes and bedrock excavation can exceed $350,000 in hillside-specific premium.</p>

      <h3>Geotechnical investigation: what you are paying for</h3>

      <p>The geotechnical report is almost always the first spend on a hillside lot. A qualified professional engineer (P.Eng.) visits the site, performs test holes or boreholes, analyses soil samples, and produces a stamped report that covers soil bearing capacity, groundwater conditions, slope stability, recommended foundation type, drainage requirements, and in some cases a specific setback from any slope hazard.</p>

      <p>For standard residential sloped lots in BC, the report runs $3,500 to $6,000. Mid-complexity sites (variable soils, steeper grade, close to known hazards) run $5,000 to $10,000. Severely complex sites, deep investigation requirements, or multiple test locations can run $10,000 to $15,000 or more.</p>

      <p>Do not skip this step or try to use a geotechnical report commissioned by a previous owner from years ago. Municipalities require a current report, and the design decisions that follow (foundation type, retaining wall engineering, setbacks) all depend on the report's findings.</p>

      <h3>Retaining walls: usually the biggest surprise</h3>

      <p>Engineered retaining walls are typically the single largest hillside cost item on a per-foot basis. Standard residential walls run $300 to $700 per linear foot. Engineered concrete walls common in the Lower Mainland and steeper Okanagan sites run $400 to $1,000 per linear foot.</p>

      <p>Any retaining wall over 1.2 metres (approximately 4 feet) in height requires a building permit and must be designed by a geotechnical or structural engineer. Engineering plus permit fees add $1,500 to $3,500 on top of material and installation. Walls that step down the lot (common on hillside builds) often total 100 to 200+ linear feet of retaining across the full site, which puts the retaining line item alone between $30,000 and $150,000+ before drainage.</p>

      <p>A hidden sub-cost: every properly built wall requires crushed gravel backfill, perforated drain pipe, and often a French drain system, which adds another $10 to $30 per linear foot. On a 150-linear-foot wall system, drainage alone can add $1,500 to $4,500.</p>

      <h3>Stepped foundations and structural uplift</h3>

      <p>Hillside homes rarely sit on a single flat footing. Stepped foundations, where the footing drops at different elevations to follow the grade, require more concrete, more rebar, more formwork, and more inspection stops. Deep piers to reach competent bearing soil may be required where fill is present or soils are variable.</p>

      <p>For homes that cantilever over a steep drop (common in Lakeview Heights and McKinley Beach), engineered steel structure replaces simple post-and-beam wood framing, which can add $30,000 to $80,000 on a mid-size home. Walk-out basements, which are often the best design solution for a sloped lot, come with their own costs for retaining wall integration, waterproofing, and drainage behind the foundation.</p>

      <h2>Setback rules: what the municipalities actually require</h2>

      <h3>City of Kelowna</h3>

      <p>The City of Kelowna's 2040 Official Community Plan requires a minimum 10-metre setback from the top of ridgelines, cliffs, and ravines on any property within the Hazardous Conditions Development Permit Area. The setback can be reduced only if a geotechnical report by a qualified professional engineer justifies the reduction with specific site analysis.</p>

      <p>The hillside design guidelines also require that areas with natural slopes of 30% or more be preserved as natural open space, which limits where the building envelope can go on steeply graded lots. Cut-and-fill must be minimized, with design encouraged to step with the grade rather than force a flat building pad.</p>

      <h3>District of West Kelowna</h3>

      <p>West Kelowna applies similar setback and design principles and in recent years has tightened its hillside building rules. Current requirements include more technical information from geotechnical engineers at application, more monitoring during construction, and in some cases greater setbacks from slope crests than the Kelowna baseline. Property owners on hillside sites are typically required to retain the services of a geotechnical engineer throughout construction to confirm all recommendations are followed.</p>

      <h3>Other Okanagan municipalities</h3>

      <p>Lake Country, Peachland, Penticton, and Vernon each have their own slope and hazard provisions. The common thread across all five municipalities: any sloped lot with slope exceeding 20%, any lot near a ridgeline or ravine, and any lot with known geotechnical concerns will require a stamped geotechnical report and additional design review before building permit issuance. Confirm specifics with the municipality before offering on a lot.</p>

      <h2>Timeline impact: how much longer a hillside build takes</h2>

      <p>Hillside builds add approximately 2 to 4 months to the overall timeline of a Kelowna custom home. The added time breaks down as:</p>

      <ul>
        <li><strong>Geotechnical investigation and report:</strong> 2 to 6 weeks before design can lock</li>
        <li><strong>Development Permit review (where required):</strong> 4 to 10 weeks on top of standard building permit timeline</li>
        <li><strong>Additional structural engineering:</strong> 2 to 4 weeks for stepped foundations, retaining walls, and cantilevered elements</li>
        <li><strong>Slower excavation and site prep:</strong> 1 to 3 extra weeks on-site</li>
        <li><strong>Drainage installation and backfill:</strong> 1 to 2 extra weeks</li>
      </ul>

      <p>A flat-lot build that would run 14 to 18 months from design to move-in typically becomes 16 to 22 months on a comparable hillside lot. Our full breakdown of custom home timelines in Kelowna is in the <a href="/guides/how-long-to-build-custom-home-kelowna/">timeline guide</a>.</p>

      <h2>How design choices control the hillside premium</h2>

      <p>The homes that go over budget on hillside premium are usually the ones that fight the grade. The homes that come in on budget work with it. A few of the biggest design decisions:</p>

      <ul>
        <li><strong>Step with the grade rather than cutting a flat pad.</strong> Walk-out basements, split-level entries, and cantilevered decks all let the home follow the slope with less retaining.</li>
        <li><strong>Keep the building footprint narrow in the slope direction.</strong> A long rectangle running parallel to contour lines retains far less than a square that cuts across the slope.</li>
        <li><strong>Design the retaining as site features, not emergency fixes.</strong> Integrated hardscape walls doubling as planters, seating, or driveway edging usually cost less than ad-hoc engineered walls added mid-build.</li>
        <li><strong>Access drainage early.</strong> A proper site-wide drainage plan designed before excavation costs far less than remedial drainage work after construction reveals a water problem.</li>
        <li><strong>Pick finishes that tolerate movement.</strong> Materials and joints that forgive the small settlement that happens on any new fill save repair cost in years 3 to 10.</li>
      </ul>

      <h2>What we have seen on real hillside projects</h2>

      <p>On our <a href="/project/cabernet-2/">Cabernet Way project</a> in West Kelowna, the hillside premium came in at approximately $110,000 on a mid-size custom home. The site required 85 linear feet of engineered retaining, a stepped foundation across three elevations, a full French drain system, and a geotechnical report that drove the specific setback from the upslope bank. Design followed the grade with a walk-out lower level and a cantilevered deck, which kept the premium from pushing higher.</p>

      <p>On an Eagle Mountain project in Abbotsford, a steeper site with more variable soils, the hillside premium ran closer to $185,000. The additional costs came from deeper piers, more extensive retaining (160+ linear feet), rock removal in two zones, and a longer DP review process.</p>

      <blockquote style="border-left:3px solid #0085c9;padding:14px 20px;margin:28px 0;background:#f4f9fc;font-style:italic;color:#1a1d21;font-size:16px;line-height:1.65">
        <p style="margin:0">"The number people land on for a hillside premium is almost always lower than reality until they see the geotech report. The report drives everything downstream. Clients who commission the geotech early, before they commit to a specific design, save tens of thousands by designing with the findings instead of around them." Jas Sidhu, Owner, Palermo Homes</p>
      </blockquote>

      <h2>What to check before buying a sloped lot in the Okanagan</h2>

      <p>If you are evaluating a hillside lot in Kelowna, West Kelowna, Lake Country, Peachland, Vernon, or Penticton, walk the lot with an experienced hillside builder before any offer. Items to confirm:</p>

      <ol>
        <li>Slope percentage across the lot (eye estimate, then professional confirmation)</li>
        <li>Whether any portion falls in a Hillside DP or Hazardous Conditions DP area</li>
        <li>Setback distance from any ridgeline, cliff, or ravine edge</li>
        <li>Vehicle and equipment access for construction (not just finished-home driveway access)</li>
        <li>Drainage patterns and signs of past water movement</li>
        <li>Rock outcrops that may require blasting or specialist removal</li>
        <li>Neighboring builds and how they handled the same grade</li>
        <li>Any site-specific overlays, covenants, or architectural guidelines from the development or municipality</li>
      </ol>

      <p>We offer pre-purchase lot walks for buyers considering hillside properties across the Central Okanagan. The 90 minutes on-site before you offer is almost always more valuable than any inspection commissioned after the deal closes.</p>

      <p class="footer-note">This guide reflects current municipal rules, geotechnical practice, and construction cost conditions in the Central Okanagan as of 2026. Specific setback distances, DP triggers, and cost ranges change over time and vary by site. Verify current specifics with the relevant municipality and any builder you interview.</p>
    </div>
  </section>

  <section class="guide-about">
    <div class="wrap">
      <h2>About Palermo Homes</h2>
      <p>Palermo Homes is a custom home builder based in West Kelowna, BC (BC Corporate Registration BC1017682, BC Housing Licensed Residential Builder Number 42812). We have built hillside custom homes across the Central Okanagan for over 15 years, including projects in <a href="/neighborhoods/upper-mission/">Upper Mission</a>, <a href="/neighborhoods/kettle-valley/">Kettle Valley</a>, <a href="/neighborhoods/lakeview-heights/">Lakeview Heights</a>, <a href="/neighborhoods/wilden/">Wilden</a>, <a href="/neighborhoods/predator-ridge/">Predator Ridge</a>, and Eagle Mountain in Abbotsford.</p>
      <p>We build in <a href="/service-areas/kelowna/">Kelowna</a>, <a href="/service-areas/west-kelowna/">West Kelowna</a>, <a href="/service-areas/lake-country/">Lake Country</a>, <a href="/service-areas/peachland/">Peachland</a>, <a href="/service-areas/penticton/">Penticton</a>, <a href="/service-areas/vernon/">Vernon</a>, and select Lower Mainland communities.</p>
      <p>For general cost context, see our <a href="/guides/custom-home-cost-kelowna/">2026 custom home cost guide</a>. For how long a build takes, see our <a href="/guides/how-long-to-build-custom-home-kelowna/">timeline guide</a>. For contract structure before you sign anything, see the <a href="/guides/fixed-price-vs-cost-plus-custom-home-kelowna/">fixed-price vs cost-plus guide</a>.</p>
    </div>
  </section>

  <section class="guide-cta">
    <div class="wrap">
      <h2>Thinking about a hillside build in the Okanagan?</h2>
      <p>We offer pre-purchase lot walks and no-pressure consultations. The best time to involve a builder is before you offer, not after.</p>
      <a class="btn" href="/contact/">Book a consultation</a>
    </div>
  </section>
</div>
"""


OG_IMAGE = f"{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-02.jpg"
OG_TITLE = "Hillside Custom Home Builds in Kelowna and the Okanagan: Costs, Permits, and Timeline"


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    html = re.sub(r"/\* ==== GUIDE-HILLSIDE CSS START ==== \*/.*?/\* ==== GUIDE-HILLSIDE CSS END ==== \*/", "", html, flags=re.DOTALL)
    html = re.sub(r"/\* ==== ABOUT-V2 CSS START ==== \*/.*?/\* ==== ABOUT-V2 CSS END ==== \*/", "", html, flags=re.DOTALL)
    html = html.replace("</head>", f"<style>{GUIDE_CSS}</style></head>", 1)
    html = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', html, count=1)
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{META_DESC}"/>\n</head>', 1)
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{CANONICAL}"/>\n</head>', 1)
    html = re.sub(
        r'<meta content="[^"]*" property="og:title"/>',
        f'<meta content="{OG_TITLE}" property="og:title"/>', html, count=1,
    )
    html = re.sub(
        r'<meta content="[^"]*" property="og:url"/>',
        f'<meta content="{CANONICAL}" property="og:url"/>', html, count=1,
    )
    html = re.sub(r'<meta[^>]*property="article:modified_time"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:data1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:label1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:description"/>\n?', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:image"/>\n?', '', html)
    html = re.sub(
        r'(<meta content="[^"]*" property="og:site_name"/>)',
        r'\1' + f'\n<meta content="{META_DESC}" property="og:description"/>\n<meta content="{OG_IMAGE}" property="og:image"/>',
        html, count=1,
    )
    html = re.sub(r'<script class="yoast-schema-graph"[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(
        r'<link rel="preload" as="image" href="[^"]*" fetchpriority="high">',
        f'<link rel="preload" as="image" href="{OG_IMAGE}" fetchpriority="high">',
        html,
    )
    html = html.replace("</head>", schema_block + "</head>", 1)

    out = SITE / "guides" / "hillside-custom-home-kelowna" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built Guide #5: Hillside Custom Home Builds in Kelowna.")
