"""Build /guides/custom-home-permits-okanagan/
Guide #6 - "Custom Home Permits in Kelowna and the Okanagan."
Targets high-intent queries: "building permit kelowna", "building permit cost",
"west kelowna building permit", "custom home permits bc", "energy step code bc",
"bc home warranty requirements".
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
PAGE_URL = f"{BIZ_URL}/guides/custom-home-permits-okanagan/"
PUBLISH_DATE = "2026-10-13"
MODIFIED_DATE = datetime.date.today().isoformat()

CSS_START = "/* ==== GUIDE-PERMITS CSS START ==== */"
CSS_END = "/* ==== GUIDE-PERMITS CSS END ==== */"

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
        "q": "How much does a building permit cost for a custom home in Kelowna?",
        "a": "The City of Kelowna charges building permit fees based on construction value, with a standard rate of approximately 1.14% of construction value (minimum $100). For a $1.5 million custom home, that works out to roughly $17,000 in building permit fees alone. On top of the base permit, expect additional fees for plumbing permits, electrical permits (via Technical Safety BC), gas permits, and Development Cost Charges (DCCs) that vary by lot location. Total permit-related costs on a Kelowna custom home typically run $18,000 to $40,000 or more once all municipal and provincial charges are included."
    },
    {
        "q": "How much does a building permit cost in West Kelowna?",
        "a": "The District of West Kelowna uses the same 1.14% of actual construction value formula as Kelowna (minimum $100), plus a non-refundable application fee with a minimum of $150 due at the time of application. For a $1.2 million custom home, the base permit fee is approximately $13,700. West Kelowna adds its own Development Cost Charges which vary by neighborhood and lot."
    },
    {
        "q": "How long does it take to get a building permit for a custom home in the Okanagan?",
        "a": "Permit review times vary significantly across the Central Okanagan. The District of West Kelowna publishes a 15 business day target for complete single-family or duplex applications. The City of Penticton targets 21 business days standard or 1 to 14 business days through its Residential Xpress program for eligible applications. The District of Peachland cites approximately 2 weeks per their published FAQ. The City of Kelowna does not publish a formal day-count target; industry estimates run 4 to 6 weeks for complete applications. These targets assume a complete application; incomplete submissions or files requiring revisions restart the clock on affected sections."
    },
    {
        "q": "What documents do I need to submit for a custom home building permit in BC?",
        "a": "A typical BC single-family building permit application requires: a Building Permit Application Form, a current legal survey plan, a coordinated site plan showing final construction, architectural drawings (floor plans with dimensions, foundation details, structural components, door and window sizes, plumbing fixtures, mechanical layout), structural engineering stamped drawings, a BC Energy Step Code Pre-Construction Report, Home Warranty Insurance confirmation via BC Housing (New Home Registration), a Property Declaration Form, and any Development Permit documentation if the lot falls in a DP area. Hillside lots additionally require a geotechnical report. Lakefront or waterfront lots may require archaeological assessment and provincial foreshore review."
    },
    {
        "q": "Is BC Energy Step Code required for new custom homes?",
        "a": "Yes. New residential construction in BC must comply with the BC Energy Step Code, with Step 3 as the minimum level required for most new homes in Central Okanagan municipalities. The code requires a pre-construction report from a qualified Energy Advisor confirming the design meets Step 3 performance (airtightness, insulation, mechanical efficiency). An as-built verification is required at completion. The pre-construction report typically runs $800 to $2,500 depending on home size and complexity; the as-built verification adds another $600 to $1,500."
    },
    {
        "q": "Do I need Home Warranty Insurance to get a building permit in BC?",
        "a": "Yes. New Home Warranty Insurance under BC's 2-5-10 program is a Provincial BC Housing requirement for all new homes built by a licensed residential builder. The builder registers the home with BC Housing, who then issues a New Home Registration certificate that is required for building permit issuance. Owner-builders who are building for personal occupancy (not for sale) can apply for an Owner-Builder Exemption instead, but this limits the ability to sell the home for the first year of occupancy and comes with other restrictions."
    },
    {
        "q": "What are Development Cost Charges (DCCs) on a Kelowna custom home?",
        "a": "Development Cost Charges are municipal fees collected at building permit issuance to pay for off-site infrastructure improvements (roads, water, sewer, parks, drainage) attributable to new development. DCCs are separate from building permit fees and can be substantial. In Kelowna, DCCs for a single-family home vary by sector but commonly run $15,000 to $35,000+ depending on the location of the lot and the sector-specific infrastructure needs. West Kelowna, Peachland, Lake Country, Vernon, and Penticton each have their own DCC schedules."
    },
    {
        "q": "What are the most common causes of building permit delays in the Okanagan?",
        "a": "The top five causes of permit delays we see: incomplete applications (missing drawings, missing engineering, missing Step Code report), structural comments requiring revisions during review (adds 2 to 6 weeks), referrals to other departments (planning, environmental, servicing) that trigger additional review cycles, Development Permit requirements that weren't factored into the schedule (hillside, DP area, architectural guidelines), and lot-specific overlays like riparian area regulations on waterfront properties. A well-prepared application drawn by a designer who regularly builds in the specific municipality usually clears first review with minor comments only."
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
        "headline": "Custom Home Permits in Kelowna and the Okanagan: A 2026 Guide to Fees, Timelines, and Requirements",
        "description": "Everything you need to know about building permits for a custom home in Kelowna, West Kelowna, and the Okanagan. Fees by municipality, required documents, Energy Step Code, Home Warranty, Development Cost Charges, and realistic review timelines.",
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
            {"@type": "Thing", "name": "Building Permits"},
            {"@type": "Thing", "name": "Custom Home Construction"},
            {"@type": "Thing", "name": "BC Energy Step Code"},
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
            {"@type": "ListItem", "position": 3, "name": "Custom Home Permits in Kelowna", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "Custom Home Permits in Kelowna and the Okanagan: A 2026 Guide",
        "description": "A complete guide to building permits for a custom home in Kelowna, West Kelowna, and the Okanagan: fees, timelines, required documents, Energy Step Code, Home Warranty, and DCCs.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, article, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Custom Home Permits Kelowna & Okanagan: Fees + Timelines | Palermo Homes"
META_DESC = "A complete guide to custom home building permits in Kelowna and the Okanagan: fees by municipality, required documents, Step Code, Home Warranty, and timelines."
CANONICAL = PAGE_URL

MAIN_HTML = """
<div class="guide">
  <section class="guide-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">&middot;</span><a href="/guides/">Guides</a><span class="sep">&middot;</span>Custom Home Permits in the Okanagan</p>
      <h1>Custom Home Permits in Kelowna and the Okanagan: A 2026 Guide to Fees, Timelines, and Requirements</h1>
      <p class="sub">A plain-English walk-through of the building permit process for a custom home in Kelowna, West Kelowna, Lake Country, Peachland, Penticton, and Vernon. What it costs, what you need to submit, how long each municipality takes, and the hidden charges most homeowners do not budget for.</p>
      <p class="meta">Published October 2026 &middot; By <a href="/about/jas-sidhu/" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1">Jas Sidhu</a>, Owner of Palermo Homes &middot; Custom Home Builder in West Kelowna, BC</p>
    </div>
  </section>

  <section class="guide-body">
    <div class="wrap">
      <div class="lede">
        <p>Building permit fees in Kelowna and West Kelowna are calculated at approximately 1.14% of construction value (minimum $100), which puts the base permit for a $1.5 million custom home at around $17,000. On top of that, expect $15,000 to $35,000+ in Development Cost Charges, $2,000 to $4,000 for Energy Step Code reporting, mandatory Home Warranty registration, and separate permits for plumbing, electrical, and gas. Review times range from 15 business days in West Kelowna to 4 to 6 weeks or longer in Kelowna depending on application completeness and whether a Development Permit is required.</p>
      </div>

      <figure style="margin:28px 0 32px;padding:0">
        <img src="/wp-content/uploads/2025/12/Cabernet-02.jpg" alt="Completed Palermo Homes custom build on Cabernet Way in West Kelowna, representing a project that went through the full BC permit and inspection process" style="width:100%;height:auto;display:block;border-radius:4px" loading="lazy" width="1200" height="800">
        <figcaption style="font-size:13px;color:#6a7078;margin:10px 0 0;line-height:1.5;font-style:italic">A completed custom home that went through the full District of West Kelowna permit process. Pre-permit documentation (geotech, Step Code, architectural stamps, Home Warranty) was prepared and submitted together to clear first review.</figcaption>
      </figure>

      <p>Permits are the phase of a Kelowna custom home where projects most commonly stall. Not because the municipalities are difficult but because applications arrive incomplete, drawings miss required details, or the applicant did not know a Development Permit or environmental review would apply to their lot. The permit itself is not the obstacle. The preparation is.</p>

      <p>This guide walks through what the permit process actually looks like in the Central Okanagan, what you have to submit, what each municipality charges, how long each one takes, and the hidden fees that catch most first-time custom home buyers off guard.</p>

      <h2>The four phases of the custom home permit process</h2>

      <p>Every custom home in BC runs through the same four permit phases. Each has a typical duration, a set of required documents, and a set of things that can delay it.</p>

      <table>
        <thead>
          <tr><th>Phase</th><th>Typical duration</th><th>What happens</th></tr>
        </thead>
        <tbody>
          <tr><td>Pre-application</td><td>2 to 6 weeks</td><td>Drawings finalized, engineering stamped, Step Code report completed, Home Warranty registration, geotech if required</td></tr>
          <tr><td>Development Permit (if required)</td><td>4 to 10 weeks</td><td>Design-guideline review for hillside, hazardous conditions, or planned community lots</td></tr>
          <tr><td>Building Permit review</td><td>2 to 6 weeks</td><td>Municipal technical review, revisions, issuance</td></tr>
          <tr><td>Trade permits + inspections</td><td>Ongoing through construction</td><td>Plumbing, electrical (Technical Safety BC), gas, and construction-phase inspections</td></tr>
        </tbody>
      </table>

      <p>The compound total ranges from 6 weeks on a straightforward flat-lot build in West Kelowna with a complete submission, to 4+ months on a hillside lot in Kelowna with a Development Permit, Step Code revisions, and structural review comments.</p>

      <h2>Building permit fees by municipality</h2>

      <p>Most Central Okanagan municipalities calculate building permit fees as a percentage of construction value. The percentages are similar across jurisdictions, but each municipality publishes its own fee bylaw with specific minimums and application fees.</p>

      <h3>City of Kelowna</h3>

      <p>Kelowna's current fee structure is tiered by construction value, with a standard rate of approximately 1.14% of construction value and a minimum of $100. For higher-value custom homes the actual bylaw tiers are:</p>

      <ul>
        <li>$1 to $10,000: $175.00 minimum</li>
        <li>$10,001 to $100,000: $175.00 plus $9.55 per $1,000</li>
        <li>$100,001 to $500,000: $1,034.50 plus $8.05 per $1,000 over $100,000</li>
        <li>$500,001 and up: $4,254.50 plus $7.20 per $1,000 over $500,000</li>
      </ul>

      <p>For a $1.5 million custom home that works out to approximately $11,500 using the tiered structure, or about $17,000 using the 1.14% calculation. Builders should confirm the current applicable rate directly with the City at application.</p>

      <h3>District of West Kelowna</h3>

      <p>West Kelowna uses the same 1.14% of actual construction value calculation (minimum $100), plus a non-refundable application fee with a minimum of $150 due at the time of application. The permit fee itself is due at the time of permit issuance. For a $1.2 million custom home, the base permit fee runs approximately $13,700 on top of the $150+ application fee.</p>

      <h3>District of Peachland, City of Penticton, City of Vernon, District of Lake Country</h3>

      <p>These municipalities each publish their own fee schedules. The percentage-of-construction-value model is common across BC but the specific percentage, minimum fee, and tier breakpoints vary. For current rates in these jurisdictions, consult the municipality's current Fees and Charges Bylaw before submission.</p>

      <h2>Required documents checklist</h2>

      <p>A typical complete single-family application in BC requires:</p>

      <ul>
        <li><strong>Building Permit Application Form:</strong> municipality-specific form</li>
        <li><strong>Current legal survey plan:</strong> recent, stamped by a BC Land Surveyor</li>
        <li><strong>Site plan:</strong> final design with building footprint, setbacks, grades, drainage, driveway, and services</li>
        <li><strong>Architectural drawings:</strong> floor plans, elevations, sections, dimensions, door and window sizes and locations</li>
        <li><strong>Structural engineering:</strong> stamped drawings from a Professional Engineer (P.Eng.) for foundations, framing, load paths</li>
        <li><strong>Mechanical, electrical, plumbing layout:</strong> showing fixtures, mechanical equipment locations, panel locations</li>
        <li><strong>BC Energy Step Code Pre-Construction Report:</strong> signed by a qualified Energy Advisor</li>
        <li><strong>Home Warranty Insurance confirmation:</strong> New Home Registration from BC Housing, or Owner-Builder Exemption</li>
        <li><strong>Property Declaration Form:</strong> ownership and intended use</li>
        <li><strong>Geotechnical Report:</strong> required for hillside lots, slope-adjacent lots, or lots with known soil issues (see our <a href="/guides/hillside-custom-home-kelowna/">hillside guide</a>)</li>
        <li><strong>Development Permit documentation:</strong> if the lot is in a DP Area (hillside, hazardous conditions, waterfront, architectural guideline community)</li>
      </ul>

      <p>Waterfront or lakefront lots on Okanagan Lake, Kalamalka Lake, or Wood Lake typically require additional provincial reviews including Riparian Areas Protection Regulation (RAPR) compliance and in some cases archaeological assessment.</p>

      <h2>BC Energy Step Code: what it is and what it costs</h2>

      <p>The BC Energy Step Code is a performance-based energy efficiency standard that applies to new construction across the province. Central Okanagan municipalities currently require most new homes to meet Step 3 at minimum. The code sets specific targets for airtightness, insulation levels, and mechanical system efficiency.</p>

      <p>Compliance requires two reports from a qualified Energy Advisor:</p>

      <ul>
        <li><strong>Pre-Construction Report</strong> ($800 to $2,500 depending on home size and complexity). Demonstrates the design will meet the required Step at completion. Required at building permit application.</li>
        <li><strong>Mid-construction airtightness test:</strong> blower door test performed after framing and air barrier are complete</li>
        <li><strong>As-built verification report</strong> ($600 to $1,500). Confirms the completed home meets Step requirements. Required at occupancy.</li>
      </ul>

      <p>Clients who want to exceed Step 3 (for example to qualify for CleanBC rebates or future-proof against stricter future requirements) can target Step 4 or 5. Higher Steps add construction cost but can significantly reduce lifetime energy bills.</p>

      <h2>Home Warranty Insurance (2-5-10)</h2>

      <p>BC's 2-5-10 New Home Warranty, administered through BC Housing, is a Provincial requirement for all new homes built by a licensed residential builder in BC. The warranty provides:</p>

      <ul>
        <li><strong>2 years</strong> on labour and materials for defects</li>
        <li><strong>5 years</strong> on building envelope (walls, roof, windows against water penetration)</li>
        <li><strong>10 years</strong> on structural defects</li>
      </ul>

      <p>The builder is responsible for registering the home with BC Housing and issuing the New Home Registration certificate that is required for building permit issuance. The warranty premium is typically in the range of $1,500 to $4,000 depending on home value and builder record.</p>

      <p><strong>Palermo Homes is BC Housing Licensed Residential Builder Number 42812.</strong> Every home we build is registered under our license and covered by 2-5-10 warranty automatically.</p>

      <p>Owner-builders who intend to live in the home personally (not build-for-sale) can apply for an Owner-Builder Exemption through BC Housing. This waives the mandatory warranty but adds restrictions, including the ability to only build one owner-exempt home every 18 months and restrictions on selling the home for the first year after occupancy.</p>

      <h2>Development Cost Charges (DCCs) and other hidden fees</h2>

      <p>Development Cost Charges are the fee most first-time custom home buyers do not budget for. DCCs are municipal fees collected at building permit issuance to fund off-site infrastructure improvements (roads, water, sewer, parks, drainage) attributable to new development. They are separate from and in addition to the building permit fee itself.</p>

      <p>DCCs vary by municipality and by lot location within the municipality (sector-based pricing). In Kelowna, DCCs for a single-family home commonly run $15,000 to $35,000+ depending on the sector. West Kelowna, Peachland, Lake Country, Vernon, and Penticton each publish their own DCC bylaws with sector-specific rates.</p>

      <p>Other charges that stack on top of base permit fees include:</p>

      <ul>
        <li><strong>Plumbing permit:</strong> municipal, typically a flat or per-fixture fee</li>
        <li><strong>Electrical permit:</strong> issued by Technical Safety BC, not the municipality</li>
        <li><strong>Gas permit:</strong> if gas appliances are installed</li>
        <li><strong>Water and sewer connection fees:</strong> if the lot is not already serviced</li>
        <li><strong>Driveway and curb cut permits:</strong> if a new driveway accesses a municipal road</li>
        <li><strong>Tree protection or removal fees:</strong> some municipalities require tree surveys and preservation deposits</li>
      </ul>

      <p>Total permit-related costs on a Kelowna or West Kelowna custom home typically land between $18,000 and $40,000+ once all municipal and provincial charges are added together. That is a line item worth getting a full breakdown on from your builder before the budget is finalized.</p>

      <h2>Realistic review timelines by municipality</h2>

      <p>Permit review times across the Central Okanagan vary significantly. These are the current published targets or best-available estimates by municipality:</p>

      <ul>
        <li><strong>District of West Kelowna:</strong> 15 business days (about 3 weeks) for a complete single-family or duplex application. Published municipal target. Housing Incentive Program projects target 5 business days.</li>
        <li><strong>City of Penticton:</strong> 21 business days (about 4 weeks) standard, or 1 to 14 business days for eligible applications through the Residential Xpress program. Published municipal target.</li>
        <li><strong>District of Peachland:</strong> Approximately 2 weeks per the municipal building department FAQ, first-come first-served, dependent on application completeness.</li>
        <li><strong>City of Kelowna:</strong> No published day-count target. Industry estimates run 4 to 6 weeks for complete applications; complex files take longer. The city operates a Fast Track program for eligible applications.</li>
        <li><strong>City of Vernon:</strong> No published day-count target. Recent council reporting has indicated permit processing in the "green zone" with past averages under 4 weeks.</li>
        <li><strong>District of Lake Country:</strong> No current day-count target published. Historical news coverage has noted periodic backlogs. Confirm current status directly with the municipality.</li>
      </ul>

      <p>These targets assume complete applications. Revisions during review, incomplete submissions, or files that trigger referrals to other departments (planning, engineering, environmental, servicing) all extend the timeline. Our full breakdown of how permits fit into the overall custom home schedule is in the <a href="/guides/how-long-to-build-custom-home-kelowna/">timeline guide</a>.</p>

      <h2>The five most common permit delays</h2>

      <p>Across hundreds of permit applications over 15+ years, these are the delays we see most often:</p>

      <ol>
        <li><strong>Incomplete application submission.</strong> Missing survey, missing Step Code report, missing structural stamp, missing warranty registration. Each triggers a hold and often a resubmission.</li>
        <li><strong>Structural comments requiring revisions.</strong> If the municipal reviewer flags structural concerns, the structural engineer must revise, re-stamp, and resubmit. Each round adds 2 to 6 weeks.</li>
        <li><strong>Development Permit requirement discovered mid-review.</strong> Hillside, Hazardous Conditions, or architectural guideline requirements that were not identified upfront can add 4 to 10 weeks.</li>
        <li><strong>Referrals to other departments.</strong> Planning, environmental, servicing, or engineering referrals trigger additional review cycles.</li>
        <li><strong>Property-specific overlays.</strong> Riparian areas (lakefront or stream-adjacent), archaeological overlays, agricultural land reserve adjacencies, or tree preservation requirements that were not factored into the application.</li>
      </ol>

      <p>A well-prepared application assembled by a builder and design team who regularly build in the specific municipality usually clears first review with minor comments only. Permit speed is largely about preparation quality, not about advocacy or expediting.</p>

      <h2>What we have seen on real Okanagan permit submissions</h2>

      <p>On our <a href="/project/cabernet-2/">Cabernet Way project</a> in West Kelowna, the complete building permit package was issued in 11 business days from submission (inside the District's published 15-day target). The hillside site required a geotechnical report and additional structural review for the stepped foundation, but because every required document was in the package at submission, the review ran clean.</p>

      <p>Our <a href="/project/malbec-place-1/">Malbec Place project</a> in a straightforward flat-lot West Kelowna neighborhood went through permit in 9 business days with no revisions.</p>

      <p>The longest permit cycle we have seen in recent years ran 14 weeks, on a hillside lot in Kelowna where mid-review the file was referred to planning for a Development Permit the applicant did not know applied, triggering a 7-week DP review on top of the standard building permit review.</p>

      <blockquote style="border-left:3px solid #0085c9;padding:14px 20px;margin:28px 0;background:#f4f9fc;font-style:italic;color:#1a1d21;font-size:16px;line-height:1.65">
        <p style="margin:0">"Permits are not where projects should lose time. If a permit takes 10 weeks instead of 3, almost always the reason is something that was missing from the application. Pay for the prep work. Submit a complete package. The permit timeline follows from the quality of the submission." Jas Sidhu, Owner, Palermo Homes</p>
      </blockquote>

      <h2>How to prepare for a clean first review</h2>

      <p>If you want your Kelowna or West Kelowna custom home permit to clear first review:</p>

      <ol>
        <li>Confirm with the municipality whether a Development Permit applies to your lot before design finalizes</li>
        <li>Commission the geotechnical report early if the lot has any slope or soil complexity</li>
        <li>Engage a qualified Energy Advisor before design is complete so Step Code targets inform the design, not retrofit it</li>
        <li>Have your structural engineer coordinate directly with the architectural team on load paths, not after drawings are complete</li>
        <li>Submit the full package in one application, not in stages</li>
        <li>Choose a builder who regularly builds in the specific municipality and knows that municipality's reviewer preferences</li>
      </ol>

      <p>None of these prevent revisions entirely. They do prevent the preventable ones.</p>

      <p class="footer-note">This guide reflects current permit requirements, fees, and processes in the Central Okanagan as of 2026. Municipal fee bylaws, published review targets, DCC schedules, and Step Code requirements change over time. Verify current specifics with the relevant municipality and any builder you interview.</p>
    </div>
  </section>

  <section class="guide-about">
    <div class="wrap">
      <h2>About Palermo Homes</h2>
      <p>Palermo Homes is a custom home builder based in West Kelowna, BC (BC Corporate Registration BC1017682, BC Housing Licensed Residential Builder Number 42812). We have been managing custom home permit submissions across the Central Okanagan for over 15 years. Our in-house process coordinates architectural, structural, mechanical, geotechnical, and Step Code deliverables before a single page gets submitted to the municipality, which is why most of our files clear first review with minor comments only.</p>
      <p>We build in <a href="/service-areas/kelowna/">Kelowna</a>, <a href="/service-areas/west-kelowna/">West Kelowna</a>, <a href="/service-areas/lake-country/">Lake Country</a>, <a href="/service-areas/peachland/">Peachland</a>, <a href="/service-areas/penticton/">Penticton</a>, <a href="/service-areas/vernon/">Vernon</a>, and select Lower Mainland communities.</p>
      <p>For how permits fit into the overall custom home schedule, see our <a href="/guides/how-long-to-build-custom-home-kelowna/">timeline guide</a>. For hillside-specific permit and geotech requirements, see the <a href="/guides/hillside-custom-home-kelowna/">hillside builds guide</a>. For how to pick a builder who knows the local permit process, see the <a href="/guides/how-to-choose-custom-home-builder-kelowna/">builder selection guide</a>.</p>
    </div>
  </section>

  <section class="guide-cta">
    <div class="wrap">
      <h2>Planning a custom home build in the Okanagan?</h2>
      <p>We handle the full permit coordination in-house. Fewer surprises, faster review cycles.</p>
      <a class="btn" href="/contact/">Book a consultation</a>
    </div>
  </section>
</div>
"""


OG_IMAGE = f"{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-02.jpg"
OG_TITLE = "Custom Home Permits in Kelowna and the Okanagan: A 2026 Guide to Fees, Timelines, and Requirements"


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    html = re.sub(r"/\* ==== GUIDE-PERMITS CSS START ==== \*/.*?/\* ==== GUIDE-PERMITS CSS END ==== \*/", "", html, flags=re.DOTALL)
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

    out = SITE / "guides" / "custom-home-permits-okanagan" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built Guide #6: Custom Home Permits in Kelowna and the Okanagan.")
