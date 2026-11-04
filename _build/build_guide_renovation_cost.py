"""Build /guides/whole-home-renovation-cost-okanagan/
Guide #7 - "Whole-Home Renovation Cost in Kelowna and the Okanagan."
Targets high-volume cost queries: "home renovation cost kelowna", "whole house
renovation cost bc", "kitchen renovation cost kelowna", "bathroom renovation
cost okanagan", "basement finish cost kelowna".
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
PAGE_URL = f"{BIZ_URL}/guides/whole-home-renovation-cost-okanagan/"
PUBLISH_DATE = "2026-10-13"
MODIFIED_DATE = datetime.date.today().isoformat()

CSS_START = "/* ==== GUIDE-RENO CSS START ==== */"
CSS_END = "/* ==== GUIDE-RENO CSS END ==== */"

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
        "q": "How much does a whole-home renovation cost in Kelowna?",
        "a": "A whole-home renovation in Kelowna typically runs $150 to $400 per square foot in 2026, depending on scope and finish level. For a 2,000 square foot home, that works out to roughly $300,000 for a cosmetic refresh at the lower end and $800,000 for a full gut-and-rebuild with high-end finishes. Costs in the Central Okanagan currently run about 5% above the Canadian national average, driven by local labour rates and demand for skilled trades. Scope is the single biggest variable: a cosmetic refresh and a full gut renovation can live in the same 2,000 square foot shell at very different numbers."
    },
    {
        "q": "What is the difference between a cosmetic refresh, mid-range renovation, and gut renovation?",
        "a": "A cosmetic refresh keeps all walls, systems, and layout in place and updates finishes only (paint, flooring, light fixtures, maybe cabinet fronts). Typical cost: $100 to $150 per square foot. A mid-range renovation updates finishes, replaces appliances and plumbing fixtures, and may change kitchen or bathroom layout, but keeps structural walls and most systems. Typical cost: $150 to $250 per square foot. A full gut renovation strips the home back to studs, replaces mechanical, electrical, plumbing, insulation, drywall, and often reconfigures the floor plan. Typical cost: $250 to $400+ per square foot."
    },
    {
        "q": "How much does a kitchen renovation cost in Kelowna?",
        "a": "A Kelowna kitchen renovation typically runs $30,000 to $85,000, with an average around $50,000 in 2026. Entry-level cabinet-refresh projects start near $18,000; full custom kitchens with imported stone, premium appliances, and layout changes can exceed $115,000. The main cost drivers are cabinet type (stock, semi-custom, or full custom), countertop material (laminate, quartz, natural stone), appliance package, and whether the layout changes (plumbing and electrical relocations add significantly)."
    },
    {
        "q": "How much does a bathroom renovation cost in Kelowna?",
        "a": "A Kelowna bathroom renovation typically runs $20,000 to $45,000, with an average around $23,000 to $25,000 in 2026. Simple refreshes can land near $8,500; a full gut-and-reconfigure of a primary ensuite with custom tile, double vanity, freestanding tub, and glass shower enclosure can exceed $55,000. Moving plumbing (relocating a toilet, shower, or vanity) is the single biggest cost multiplier in bathroom work."
    },
    {
        "q": "How much does it cost to finish a basement in Kelowna?",
        "a": "Basement finishing in Kelowna ranges from $25,000 for basic finishing (framing, drywall, basic electrical, simple flooring) to $100,000+ for a fully legal secondary suite with separate entrance, kitchen, bathroom, and services. An average full basement finish including a 3-piece bathroom, bedroom with egress window, and main living area runs around $64,000 in 2026. Legal secondary suites require additional permits, fire separation, egress compliance, and typically dedicated HVAC and electrical service."
    },
    {
        "q": "Do I need permits for a home renovation in Kelowna?",
        "a": "Yes, in almost all cases. The City of Kelowna requires building permits for structural changes, additions, decks, new or altered walls, plumbing work, electrical work, HVAC changes, changes to window or door openings, and secondary suite creation. Purely cosmetic work (paint, floor refinishing, cabinet refacing without changing plumbing or electrical) generally does not require a permit. When in doubt, confirm with the municipality before starting. Building and plumbing permits are issued by the City of Kelowna; electrical permits are issued by Technical Safety BC."
    },
    {
        "q": "How long does a whole-home renovation take in Kelowna?",
        "a": "Timeline depends heavily on scope. A cosmetic refresh across a full home typically runs 2 to 4 months. A mid-range renovation runs 4 to 8 months. A full gut renovation of a 2,000+ square foot home typically runs 8 to 14 months from design through final punch list. Design and permits usually take 2 to 4 months before construction starts. Occupied renovations (where the owner remains in the home) extend the timeline because trades work around daily use."
    },
    {
        "q": "What hidden costs commonly appear during a Kelowna renovation?",
        "a": "The most common surprises in Okanagan renovations: knob-and-tube or aluminum wiring in older homes (full rewire adds $15,000 to $40,000+), outdated plumbing that must be replaced once walls are opened (adds $10,000 to $30,000+), asbestos in insulation or drywall mud on homes pre-1990 (abatement adds $5,000 to $25,000), foundation moisture or structural issues revealed during demolition, and inadequate electrical service requiring a panel upgrade ($3,000 to $8,000). A proper pre-renovation assessment identifies most of these before contract."
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
        "headline": "Whole-Home Renovation Cost in Kelowna and the Okanagan: 2026 Pricing Guide",
        "description": "What a whole-home renovation really costs in Kelowna and the Central Okanagan in 2026. Pricing by scope level, by room, by renovation type, plus the hidden costs that catch most homeowners off guard.",
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
            {"@type": "Thing", "name": "Home Renovation Cost"},
            {"@type": "Thing", "name": "Whole-Home Renovation"},
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
            {"@type": "ListItem", "position": 3, "name": "Whole-Home Renovation Cost in the Okanagan", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "Whole-Home Renovation Cost in Kelowna and the Okanagan: 2026 Pricing Guide",
        "description": "A complete 2026 pricing guide for whole-home renovations in Kelowna and the Central Okanagan. Costs by scope, by room, timeline, permit rules, and hidden expenses.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, article, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Whole-Home Renovation Cost Kelowna & Okanagan 2026 | Palermo Homes"
META_DESC = "A complete 2026 pricing guide for whole-home renovations in Kelowna and the Okanagan. Costs by scope, by room, permits, timeline, and hidden expenses."
CANONICAL = PAGE_URL

MAIN_HTML = """
<div class="guide">
  <section class="guide-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">&middot;</span><a href="/guides/">Guides</a><span class="sep">&middot;</span>Whole-Home Renovation Cost in the Okanagan</p>
      <h1>Whole-Home Renovation Cost in Kelowna and the Okanagan: 2026 Pricing Guide</h1>
      <p class="sub">What a whole-home renovation actually costs in Kelowna, West Kelowna, Lake Country, Peachland, Vernon, and Penticton in 2026. Pricing by scope level, by room, by renovation type, plus the hidden costs that catch most homeowners off guard.</p>
      <p class="meta">Published October 2026 &middot; By <a href="/about/jas-sidhu/" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1">Jas Sidhu</a>, Owner of Palermo Homes &middot; Custom Home Builder and Renovator in West Kelowna, BC</p>
    </div>
  </section>

  <section class="guide-body">
    <div class="wrap">
      <div class="lede">
        <p>Whole-home renovations in Kelowna currently run $150 to $400 per square foot in 2026, depending on scope. For a 2,000 square foot home, that works out to roughly $300,000 for a cosmetic refresh at the lower end and $800,000 for a full gut-and-rebuild with high-end finishes. Costs in the Central Okanagan run about 5% above the Canadian national average. Scope and finish level are far bigger cost drivers than square footage alone.</p>
      </div>

      <figure style="margin:28px 0 32px;padding:0">
        <img src="/wp-content/uploads/2025/12/Cabernet-02.jpg" alt="Completed custom renovation project by Palermo Homes in the Okanagan, showing modern finishes typical of a mid-to-high range Kelowna renovation" style="width:100%;height:auto;display:block;border-radius:4px" loading="lazy" width="1200" height="800">
        <figcaption style="font-size:13px;color:#6a7078;margin:10px 0 0;line-height:1.5;font-style:italic">A completed Palermo Homes project. Renovation finish levels in the Central Okanagan now routinely match new-construction custom home standards.</figcaption>
      </figure>

      <p>Renovation is the question we get asked about more than any other, usually by homeowners who love their lot and location but want a home that lives like the ones being built new. The honest answer involves scope ranges, not a single number, because the same square footage can be renovated for a quarter of the top-end number depending on what the project actually touches.</p>

      <p>This guide covers what a Kelowna whole-home renovation runs by scope level, by room type, how renovation compares to new construction, permit requirements, timeline, and the hidden costs that reliably appear once walls open up.</p>

      <h2>Cost per square foot by scope level</h2>

      <p>Most Kelowna renovations fit into one of three scope buckets. Picking which bucket you are in before you start pricing is the single most important decision in setting a realistic budget.</p>

      <table>
        <thead>
          <tr><th>Scope level</th><th>Per sq ft</th><th>2,000 sq ft total</th><th>What it includes</th></tr>
        </thead>
        <tbody>
          <tr><td>Cosmetic refresh</td><td>$100 to $150</td><td>$200,000 to $300,000</td><td>Paint, flooring, light fixtures, cabinet fronts, minor finish updates</td></tr>
          <tr><td>Mid-range renovation</td><td>$150 to $250</td><td>$300,000 to $500,000</td><td>New cabinets, countertops, appliances, plumbing fixtures, some layout changes</td></tr>
          <tr><td>Full gut renovation</td><td>$250 to $400+</td><td>$500,000 to $800,000+</td><td>Strip to studs, new mechanical/electrical/plumbing, structural changes, new layout, high-end finishes</td></tr>
        </tbody>
      </table>

      <p>The 5% Okanagan premium over the Canadian national average applies across all three scope levels. Trades, materials, and transportation into the valley all cost slightly more than in Lower Mainland or Calgary metros.</p>

      <h2>Cost by room</h2>

      <p>Whole-home renovations rarely touch every room at the same intensity. Breaking down expected cost per room helps allocate budget to the spaces that matter most.</p>

      <h3>Kitchen</h3>

      <p>Kitchens are consistently the most expensive room in a Kelowna renovation. Typical ranges:</p>

      <table>
        <thead>
          <tr><th>Kitchen tier</th><th>Cost range</th><th>Typical scope</th></tr>
        </thead>
        <tbody>
          <tr><td>Refresh</td><td>$18,000 to $30,000</td><td>Cabinet refacing, new counters, backsplash, hardware, minor appliance updates</td></tr>
          <tr><td>Mid-range</td><td>$30,000 to $60,000</td><td>Semi-custom cabinets, quartz counters, full appliance package, same layout</td></tr>
          <tr><td>Custom</td><td>$60,000 to $115,000+</td><td>Full custom cabinets, natural stone, premium appliances, layout changes, custom millwork</td></tr>
        </tbody>
      </table>

      <p>Average Kelowna kitchen project in 2026 runs approximately $50,000. The biggest cost multiplier is moving plumbing or gas (relocating a sink, dishwasher, or range), which triggers subfloor work, drywall patching, and inspection sign-offs on each affected trade.</p>

      <h3>Bathrooms</h3>

      <p>Primary ensuite and shared bathrooms are typically the next-largest line items after the kitchen.</p>

      <table>
        <thead>
          <tr><th>Bathroom tier</th><th>Cost range</th><th>Typical scope</th></tr>
        </thead>
        <tbody>
          <tr><td>Refresh</td><td>$8,500 to $15,000</td><td>Vanity swap, new fixtures, tile paint, new mirror and lighting</td></tr>
          <tr><td>Mid-range</td><td>$15,000 to $30,000</td><td>New vanity, tile floor and shower, new tub or shower, some fixture relocations</td></tr>
          <tr><td>Custom</td><td>$30,000 to $55,000+</td><td>Custom vanity, natural stone, freestanding tub, large glass enclosure, full layout change</td></tr>
        </tbody>
      </table>

      <p>Average Kelowna bathroom in 2026 runs approximately $23,000 to $25,000. Moving the toilet is the single most expensive change in a bathroom renovation because it requires relocating the drain through the subfloor.</p>

      <h3>Basement finishing</h3>

      <p>Basements come in three distinct tiers depending on whether the finished space is a legal secondary suite.</p>

      <table>
        <thead>
          <tr><th>Basement scope</th><th>Cost range</th><th>Typical includes</th></tr>
        </thead>
        <tbody>
          <tr><td>Basic finish</td><td>$25,000 to $40,000</td><td>Framing, drywall, basic electrical, simple flooring, no bathroom</td></tr>
          <tr><td>Full finish</td><td>$55,000 to $80,000</td><td>3-piece bathroom, bedroom with egress window, main living area, finished flooring</td></tr>
          <tr><td>Legal secondary suite</td><td>$75,000 to $100,000+</td><td>Separate entrance, kitchen, bathroom, dedicated HVAC, fire separation, egress compliance, permits</td></tr>
        </tbody>
      </table>

      <p>Average Kelowna full basement finish in 2026 runs approximately $64,000. Legal secondary suites require specific permit review and inspection sign-offs that the City handles differently from standard renovation work.</p>

      <h3>Other rooms</h3>

      <ul>
        <li><strong>Bedrooms:</strong> $40 to $100 per sq ft depending on scope (refresh vs full new flooring, trim, closet rebuild)</li>
        <li><strong>Living and family rooms:</strong> $50 to $150 per sq ft (fireplace rework, built-ins, feature walls add quickly)</li>
        <li><strong>Mudroom and laundry:</strong> $15,000 to $50,000 depending on cabinetry and fixture scope</li>
        <li><strong>Home office:</strong> $10,000 to $35,000 with built-in cabinetry and lighting</li>
      </ul>

      <h2>When renovation makes sense vs new construction</h2>

      <p>The question every Okanagan homeowner should ask before committing to a whole-home renovation: at what point does the renovation cost approach new-construction cost? Here is the rough comparison:</p>

      <table>
        <thead>
          <tr><th>Approach</th><th>Typical cost range</th><th>What you keep</th><th>What you get</th></tr>
        </thead>
        <tbody>
          <tr><td>Cosmetic refresh</td><td>$100 to $150 per sq ft</td><td>Everything structural + systems + layout</td><td>Visual update only</td></tr>
          <tr><td>Mid-range renovation</td><td>$150 to $250 per sq ft</td><td>Structure, most systems, most layout</td><td>Updated finishes + partial system update</td></tr>
          <tr><td>Full gut renovation</td><td>$250 to $400+ per sq ft</td><td>Structure, lot, possibly facade</td><td>Essentially new interior with current layout flexibility</td></tr>
          <tr><td>New custom build</td><td>$600 to $1,500+ per sq ft</td><td>Lot only</td><td>Fully new, current code, Step Code 3+ efficiency, layout freedom</td></tr>
        </tbody>
      </table>

      <p>Renovation wins when the existing home has strong bones (sound foundation, good roof, appropriate layout for current needs) and when the location is irreplaceable. New construction wins when the existing home has structural issues, when the layout cannot be made to work without moving load-bearing walls, or when the finished product needs to meet modern energy code and current layout expectations across the board. On a per-square-foot basis, full gut renovations approach the lower end of new-build cost, which is often the moment to re-ask the question.</p>

      <p>For context on new-build cost comparison, see our <a href="/guides/custom-home-cost-kelowna/">2026 custom home cost guide</a>.</p>

      <h2>What permits are required for a Kelowna renovation</h2>

      <p>The City of Kelowna requires building permits for:</p>

      <ul>
        <li>Structural changes (removing or altering walls, beams, posts)</li>
        <li>Additions of any kind</li>
        <li>Decks</li>
        <li>New or altered walls (even non-structural)</li>
        <li>Plumbing work (new fixtures or fixture relocations)</li>
        <li>Electrical work (handled by Technical Safety BC permits)</li>
        <li>HVAC changes (ducting modifications, equipment upgrades)</li>
        <li>Changes to window or door openings</li>
        <li>Secondary suite creation or legalization</li>
      </ul>

      <p>Purely cosmetic work (paint, carpet, cabinet refacing without plumbing or electrical changes) generally does not require a permit. When in doubt, confirm with the municipality before any work begins. West Kelowna, Lake Country, Peachland, Penticton, and Vernon all have similar permit triggers with municipality-specific fee schedules.</p>

      <p>For the full permit cost and process breakdown, see our <a href="/guides/custom-home-permits-okanagan/">Okanagan permits guide</a>.</p>

      <h2>Timeline: how long a whole-home renovation takes</h2>

      <p>Renovation timelines vary more than most people expect, because scope varies more than most people expect.</p>

      <table>
        <thead>
          <tr><th>Scope level</th><th>Design + permits</th><th>Construction</th><th>Total</th></tr>
        </thead>
        <tbody>
          <tr><td>Cosmetic refresh</td><td>2 to 6 weeks</td><td>6 to 12 weeks</td><td>2 to 4 months</td></tr>
          <tr><td>Mid-range renovation</td><td>6 to 12 weeks</td><td>12 to 24 weeks</td><td>4 to 8 months</td></tr>
          <tr><td>Full gut renovation</td><td>8 to 16 weeks</td><td>24 to 40 weeks</td><td>8 to 14 months</td></tr>
        </tbody>
      </table>

      <p>Occupied renovations (where the owner remains in the home during construction) typically add 2 to 4 months to the construction timeline because trades work around daily use, dust containment is more complex, and critical systems need to stay operational.</p>

      <h2>The hidden costs that reliably show up</h2>

      <p>Every renovation reveals surprises once walls open. The five we see most often in Okanagan homes:</p>

      <ol>
        <li><strong>Outdated wiring.</strong> Knob-and-tube in pre-1950s homes or aluminum wiring in some 1960s-70s homes requires full rewire. Cost: $15,000 to $40,000+ for a typical 2,000 square foot home.</li>
        <li><strong>Outdated plumbing.</strong> Galvanized steel supply lines, cast iron drains, or poly-B lines often fail inspection once exposed. Full replumb: $10,000 to $30,000+ depending on access.</li>
        <li><strong>Asbestos.</strong> Common in insulation, drywall mud, floor tile adhesive, and some pipe wrap on homes built before approximately 1990. Testing is required before demolition in BC; abatement adds $5,000 to $25,000 depending on scope.</li>
        <li><strong>Foundation moisture or structural issues.</strong> Previously hidden by finished walls, these can require waterproofing, structural reinforcement, or in rare cases underpinning.</li>
        <li><strong>Inadequate electrical service.</strong> Older homes with 60-amp or 100-amp service often need to upgrade to 200-amp to support modern renovations. Panel upgrade: $3,000 to $8,000, plus any required service upgrade from BC Hydro.</li>
      </ol>

      <p>A pre-renovation assessment that includes a walk-through by the builder, electrician, and plumber (ideally with target wall sections opened for inspection) catches most of these before contract and lets them be priced accurately rather than appearing as change orders mid-construction.</p>

      <h2>What drives the final number up or down</h2>

      <p>Two homes of identical square footage can come in at very different totals. The main variables:</p>

      <ul>
        <li><strong>Finish level.</strong> Builder-grade vs mid-range vs premium can swing per-square-foot cost by 50% or more</li>
        <li><strong>Cabinet selection.</strong> Stock vs semi-custom vs full custom is a 2-3x cost multiplier on a typical kitchen</li>
        <li><strong>Appliance package.</strong> Entry-level vs premium vs commercial-style can add $20,000 to $50,000+ in a single room</li>
        <li><strong>Layout changes.</strong> Moving plumbing, electrical, and HVAC adds significantly beyond pure finish work</li>
        <li><strong>Structural changes.</strong> Removing load-bearing walls requires engineering, beams, and inspection sign-offs</li>
        <li><strong>Age of home.</strong> Older homes almost always surface more hidden costs during demolition</li>
        <li><strong>Access.</strong> Steep driveways, narrow sites, and limited material staging all add labour hours</li>
      </ul>

      <h2>What we have seen on real Okanagan renovations</h2>

      <p>On a 2,400 square foot full-gut renovation we completed in Kelowna, the final number landed at $720,000 (approximately $300/sq ft). The project included complete rewire, replumb, HVAC replacement, new kitchen, three bathroom renovations, basement finish with 3-piece bath, new flooring throughout, and significant layout change on the main floor. The home was built in 1978; the budget absorbed roughly $85,000 in hidden-cost discoveries (full rewire, aluminum wiring replacement, foundation moisture remediation).</p>

      <p>A mid-range renovation of a 1990s-era 3,200 square foot home in West Kelowna came in at $540,000 (approximately $170/sq ft). Scope was kitchen, three bathrooms, flooring, paint, trim, and minor layout changes. Original mechanical and electrical were in good condition and did not need full replacement.</p>

      <blockquote style="border-left:3px solid #0085c9;padding:14px 20px;margin:28px 0;background:#f4f9fc;font-style:italic;color:#1a1d21;font-size:16px;line-height:1.65">
        <p style="margin:0">"The number is almost always higher than what the homeowner initially pictures, and it is almost always because the scope grows as the project is designed. A cosmetic refresh becomes a mid-range renovation becomes a gut. If the scope is going to grow, better to know that before the first wall comes down than halfway through demolition." Jas Sidhu, Owner, Palermo Homes</p>
      </blockquote>

      <h2>How to budget realistically before signing anything</h2>

      <ol>
        <li>Pick a scope level based on what the home actually needs, not what feels affordable</li>
        <li>Get a professional pre-renovation walk-through with any contractor you are considering</li>
        <li>Request itemized pricing (not a single number) covering demo, mechanical, electrical, plumbing, finishes, and project management separately</li>
        <li>Build in a 15% contingency on top of the quoted number for hidden-cost discoveries</li>
        <li>Confirm what permits will be required and factor fees + Development Cost Charges where applicable</li>
        <li>Clarify whether the home will be occupied during construction and factor that into timeline + daily rate</li>
      </ol>

      <p class="footer-note">This guide reflects current renovation cost conditions and permit requirements in the Central Okanagan as of 2026. Material costs, labour rates, and municipal fee schedules change. Verify current specifics with the relevant municipality and any contractor you interview before finalizing a budget.</p>
    </div>
  </section>

  <section class="guide-about">
    <div class="wrap">
      <h2>About Palermo Homes</h2>
      <p>Palermo Homes is a custom home builder and whole-home renovator based in West Kelowna, BC (BC Corporate Registration BC1017682, BC Housing Licensed Residential Builder Number 42812). We build to the same standard whether the project is a new custom home or a whole-home renovation, which is why most of our renovation clients come from referrals by past custom-home clients.</p>
      <p>We renovate across <a href="/service-areas/kelowna/">Kelowna</a>, <a href="/service-areas/west-kelowna/">West Kelowna</a>, <a href="/service-areas/lake-country/">Lake Country</a>, <a href="/service-areas/peachland/">Peachland</a>, <a href="/service-areas/penticton/">Penticton</a>, <a href="/service-areas/vernon/">Vernon</a>, and select Lower Mainland communities.</p>
      <p>For new-build cost comparison, see our <a href="/guides/custom-home-cost-kelowna/">custom home cost guide</a>. For permits that apply to renovations as well as new builds, see our <a href="/guides/custom-home-permits-okanagan/">Okanagan permits guide</a>. For how long a renovation vs new build takes, see the <a href="/guides/how-long-to-build-custom-home-kelowna/">timeline guide</a>.</p>
    </div>
  </section>

  <section class="guide-cta">
    <div class="wrap">
      <h2>Planning a whole-home renovation in the Okanagan?</h2>
      <p>We offer no-pressure pre-renovation walk-throughs and itemized budgeting before any contract. The best time to catch surprises is before the first wall comes down.</p>
      <a class="btn" href="/contact/">Book a consultation</a>
    </div>
  </section>
</div>
"""


OG_IMAGE = f"{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-02.jpg"
OG_TITLE = "Whole-Home Renovation Cost in Kelowna and the Okanagan: 2026 Pricing Guide"


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    html = re.sub(r"/\* ==== GUIDE-RENO CSS START ==== \*/.*?/\* ==== GUIDE-RENO CSS END ==== \*/", "", html, flags=re.DOTALL)
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

    out = SITE / "guides" / "whole-home-renovation-cost-okanagan" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built Guide #7: Whole-Home Renovation Cost in the Okanagan.")
