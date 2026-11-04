"""Build /guides/how-long-to-build-custom-home-kelowna/
Guide #3 - "How Long Does It Take to Build a Custom Home in Kelowna."
Targets PAA + money queries: "how long does it take to build a custom home",
"custom home timeline kelowna", "how long to build a house kelowna".
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
PAGE_URL = f"{BIZ_URL}/guides/how-long-to-build-custom-home-kelowna/"
PUBLISH_DATE = "2026-10-05"
MODIFIED_DATE = datetime.date.today().isoformat()

CSS_START = "/* ==== GUIDE-TIMELINE CSS START ==== */"
CSS_END = "/* ==== GUIDE-TIMELINE CSS END ==== */"

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
html body #et-main-area .guide-body ul{{margin:0 0 20px;padding:0 0 0 22px}}
html body #et-main-area .guide-body ul li{{font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 8px}}
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
        "q": "How long does it take to build a custom home in Kelowna?",
        "a": "A typical custom home in Kelowna takes 14 to 20 months from first design meeting to move-in. That includes 3 to 6 months for design, 6 weeks to 3 months for permits (varies by municipality), 8 to 14 months for construction, and 1 to 2 months for deficiency work and occupancy. Hillside lots, larger homes over 5,000 square feet, and custom structural features extend the timeline. Flat lots with a locked-in design and standard specifications can complete in 12 to 14 months total."
    },
    {
        "q": "How long is the design phase for a custom home in Kelowna?",
        "a": "Design takes 3 to 6 months for most Kelowna custom homes. This includes initial consultations, concept drawings, floor plan refinement, architectural detailing, structural engineering, and finish selections. Homeowners who come in with a clear vision and decisive selections finish design in 3 to 4 months. Those who change direction or add scope mid-design often take 5 to 6 months or longer."
    },
    {
        "q": "How long does the permit process take in Kelowna?",
        "a": "Building permit review times vary significantly across the Okanagan. The District of West Kelowna publishes a 15 business day target for complete single-family applications. The City of Penticton targets 21 business days standard or 1 to 14 business days through its Residential Xpress program. The District of Peachland FAQ states approximately 2 weeks. The City of Kelowna does not publish a formal day-count target; industry estimates for a complete application run 4 to 6 weeks. District of Lake Country does not publish current review times. Hillside lots requiring a Development Permit review add weeks on top of the building permit timeline. Allow 6 weeks to 3 months total for permits depending on municipality and whether a Development Permit is required."
    },
    {
        "q": "How long does construction take for a custom home in Kelowna?",
        "a": "Active construction takes 8 to 14 months for a typical Kelowna custom home. A 3,000 square foot home on a flat lot with straightforward foundations runs 8 to 10 months. A 5,000 square foot home with hillside structural work, custom millwork, and complex mechanical systems can take 12 to 14 months. Weather, trade availability, and change orders during construction all extend this window."
    },
    {
        "q": "What factors extend a custom home build timeline in Kelowna?",
        "a": "The main delays are hillside site work (adds 2 to 4 months), permit revisions during review (adds 1 to 3 months), change orders during construction (each major one adds 2 to 6 weeks), custom imported finishes with long lead times (adds 1 to 2 months), and labour shortages for specialty trades like custom millwork or heritage-style stonework. Winter concrete pours in the Okanagan can also compress a schedule if timed poorly."
    },
    {
        "q": "Can a custom home be built faster than 14 months in Kelowna?",
        "a": "A smaller custom home under 2,500 square feet on a flat lot with a pre-designed plan can complete in 10 to 12 months total. Pushing faster than that typically means compromising on either design detail, finish quality, or construction oversight. Builders who promise 6 to 8 month timelines on a true custom home are usually selling a modified spec home or cutting corners that show up later as deficiencies."
    },
    {
        "q": "When should I start the custom home process if I want to move in by a specific date?",
        "a": "Work backward from your target move-in date and allow at least 18 months buffer. If you want to be in your custom Kelowna home by summer 2028, start initial design meetings by January 2027 at the latest. Starting earlier is better. Rushing design to meet a tight move-in date almost always costs more in change orders and leads to decisions you regret later."
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
        "headline": "How Long Does It Take to Build a Custom Home in Kelowna? 2026 Timeline Guide",
        "description": "A realistic month-by-month timeline for building a custom home in Kelowna and the Okanagan, including design, permits, construction, and the factors that extend or compress each phase.",
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
            {"@type": "Thing", "name": "Custom Home Construction Timeline"},
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
            {"@type": "ListItem", "position": 3, "name": "How Long to Build a Custom Home in Kelowna", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "How Long Does It Take to Build a Custom Home in Kelowna? 2026 Timeline Guide",
        "description": "A realistic month-by-month timeline for building a custom home in Kelowna and the Okanagan, including design, permits, construction, and the factors that extend or compress each phase.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, article, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "How Long to Build a Custom Home in Kelowna | Palermo Homes"
META_DESC = "A realistic month-by-month timeline for building a custom home in Kelowna. Design, permits, construction, and what extends each phase."
CANONICAL = PAGE_URL

MAIN_HTML = """
<div class="guide">
  <section class="guide-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">&middot;</span><a href="/guides/">Guides</a><span class="sep">&middot;</span>How Long to Build a Custom Home in Kelowna</p>
      <h1>How Long Does It Take to Build a Custom Home in Kelowna? A 2026 Timeline Guide</h1>
      <p class="sub">A realistic month-by-month timeline for designing, permitting, and building a custom home in Kelowna and the Okanagan, plus the factors that extend or compress each phase.</p>
      <p class="meta">Published October 2026 &middot; By <a href="/about/jas-sidhu/" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1">Jas Sidhu</a>, Owner of Palermo Homes &middot; Custom Home Builder in West Kelowna, BC</p>
    </div>
  </section>

  <section class="guide-body">
    <div class="wrap">
      <div class="lede">
        <p>A typical custom home in Kelowna takes 14 to 20 months from first design meeting to move-in. That breaks down as 3 to 6 months for design, 6 weeks to 3 months for permits (varies by municipality), 8 to 14 months for construction, and 1 to 2 months for deficiency work and occupancy. Hillside lots, larger homes over 5,000 square feet, and complex custom features extend the timeline. Flat lots with a locked design and a Development Permit-free site finish faster.</p>
      </div>

      <figure style="margin:28px 0 32px;padding:0">
        <img src="/wp-content/uploads/2025/12/Cabernet-02.jpg" alt="Completed custom home by Palermo Homes on Cabernet Way in West Kelowna, built on a hillside lot" style="width:100%;height:auto;display:block;border-radius:4px" loading="lazy" width="1200" height="800">
        <figcaption style="font-size:13px;color:#6a7078;margin:10px 0 0;line-height:1.5;font-style:italic">A completed custom home on Cabernet Way, West Kelowna. This hillside build ran approximately 18 months from first design meeting to move-in.</figcaption>
      </figure>

      <p>Timeline is the question almost every Kelowna custom home client asks first, often before cost. The honest answer involves ranges, not a single number, because every build has its own site conditions, scope, and sequence of decisions. This guide walks through each phase of a Kelowna custom home with realistic durations, where delays actually come from, and how to plan a move-in date that holds up.</p>

      <h2>The four phases of a Kelowna custom home</h2>

      <p>Every custom build in the Okanagan runs through the same four phases. Each one has a typical duration and a set of things that can stretch it.</p>

      <table>
        <thead>
          <tr><th>Phase</th><th>Typical duration</th><th>What happens</th></tr>
        </thead>
        <tbody>
          <tr><td>Design</td><td>3 to 6 months</td><td>Concept, floor plans, architectural detailing, engineering, finish selections</td></tr>
          <tr><td>Permits</td><td>6 weeks to 3 months</td><td>Building permit application, review, revisions, issuance. Faster in West Kelowna, Peachland, Penticton; variable in Kelowna.</td></tr>
          <tr><td>Construction</td><td>8 to 14 months</td><td>Site prep, foundation, framing, mechanical, finishes, exterior</td></tr>
          <tr><td>Deficiency and occupancy</td><td>1 to 2 months</td><td>Final inspections, deficiency list, occupancy permit, move-in</td></tr>
        </tbody>
      </table>

      <p>Added together, that is a realistic 14 to 20 months. Shorter is possible on a simple build. Longer is common on anything with meaningful site complexity or scope that evolves during design.</p>

      <h2>Phase 1: Design (3 to 6 months)</h2>

      <p>Design is the phase most homeowners underestimate. It is also the phase where decisions have the biggest downstream impact on both cost and construction speed.</p>

      <h3>What design actually includes</h3>

      <ul>
        <li>Initial consultations and site walk</li>
        <li>Concept drawings and floor plan options</li>
        <li>Floor plan refinement and client sign-off</li>
        <li>Architectural detailing (exterior elevations, window placements, roof lines)</li>
        <li>Structural engineering stamped drawings</li>
        <li>Mechanical, electrical, and plumbing layout</li>
        <li>Interior finish selections (flooring, tile, cabinetry, plumbing fixtures, lighting)</li>
      </ul>

      <h3>What extends design</h3>

      <p>The most common cause of a long design phase is changing direction mid-stream. A client who signs off on a floor plan, then two months later asks to move the kitchen or add a second-floor wing, resets the clock on structural and mechanical work.</p>

      <p>Finish selections also stall more projects than most people expect. Choosing between three tile options takes an afternoon. Choosing between three thousand takes months. Builders who provide curated allowance ranges keep this phase moving.</p>

      <h2>Phase 2: Permits (6 weeks to 3 months)</h2>

      <p>Building permit review times vary significantly across the Okanagan. These are the current published targets or best-available estimates by municipality:</p>

      <ul>
        <li><strong>District of West Kelowna:</strong> 15 business days (about 3 weeks) for a complete single-family or duplex application. <a href="https://www.westkelownacity.ca/building-business-development/building-permits-and-inspections/" rel="noopener">Published municipal target.</a></li>
        <li><strong>City of Penticton:</strong> 21 business days (about 4 weeks) standard, or 1 to 14 business days for eligible applications through the Residential Xpress program. <a href="https://www.penticton.ca/business-building/building-permits/building-permit-timelines" rel="noopener">Published municipal target.</a></li>
        <li><strong>District of Peachland:</strong> Approximately 2 weeks per the municipal building department FAQ, first-come first-served, dependent on application completeness. <a href="https://www.peachland.ca/departments/building-department/building-permit-faqs" rel="noopener">Published municipal estimate.</a></li>
        <li><strong>City of Kelowna:</strong> No published day-count target. Industry estimates run 4 to 6 weeks for a complete application; complex files take longer. The city operates a Fast Track program for eligible applications.</li>
        <li><strong>City of Vernon:</strong> No published day-count target. Recent council reporting has flagged permit processing in the "green zone" with no significant delays, with past averages under 4 weeks.</li>
        <li><strong>District of Lake Country:</strong> No current municipal day-count target published. Historical news coverage has flagged backlogs. Expect to confirm current status directly with the municipality.</li>
      </ul>

      <p>These targets assume a complete application. Incomplete submissions, revisions during review, or files that trigger additional department referrals (planning, engineering, environmental) extend the timeline. Properties with foreshore work on Okanagan Lake or Kalamalka Lake add a provincial review that can extend weeks or months beyond municipal timelines.</p>

      <p>Hillside lots requiring a Development Permit (DP) review add time on top of the standard building permit timeline. Specific DP durations are not published by most Okanagan municipalities, so plan for additional weeks on any hillside build.</p>

      <h3>What extends permits</h3>

      <p>Revisions during review are the single biggest cause of permit delays. If the municipality requests structural or code changes, that portion of the review restarts. A well-prepared permit set drawn by professionals who build in the specific municipality often usually clears first review with minor comments only.</p>

      <h2>Phase 3: Construction (8 to 14 months)</h2>

      <p>Active construction is the longest phase and the most visible one. For a 3,000 square foot home on a flat lot with straightforward specifications, 8 to 10 months is realistic. A 5,000 square foot home with hillside structural work, custom millwork, imported stone, or complex mechanical systems runs 12 to 14 months.</p>

      <h3>Construction stages and timing</h3>

      <ul>
        <li><strong>Site prep and excavation:</strong> 2 to 4 weeks</li>
        <li><strong>Foundation and underslab mechanical:</strong> 4 to 6 weeks</li>
        <li><strong>Framing:</strong> 6 to 10 weeks</li>
        <li><strong>Roof, windows, exterior envelope:</strong> 4 to 8 weeks</li>
        <li><strong>Mechanical, electrical, plumbing rough-in:</strong> 4 to 6 weeks</li>
        <li><strong>Insulation and drywall:</strong> 3 to 5 weeks</li>
        <li><strong>Interior finishes (flooring, tile, cabinets, paint):</strong> 10 to 16 weeks</li>
        <li><strong>Final mechanical, plumbing, electrical:</strong> 3 to 5 weeks</li>
        <li><strong>Exterior landscaping, driveway, final site:</strong> 3 to 6 weeks</li>
      </ul>

      <p>These stages overlap. Framing finishes before windows are installed. Insulation starts in some rooms while mechanical rough-in continues in others. A good construction schedule sequences trades so that each one has a clear path and no one is waiting on another.</p>

      <h3>What extends construction</h3>

      <ul>
        <li><strong>Change orders.</strong> Each major change during construction adds 2 to 6 weeks and often more. Moving a wall, adding a bathroom, upgrading finishes beyond allowance all push the schedule.</li>
        <li><strong>Weather.</strong> Okanagan winters can delay concrete pours, roofing, and exterior work. A well-planned build schedules weather-sensitive work for the right season.</li>
        <li><strong>Specialty trade availability.</strong> Custom millwork, heritage-style stonework, and specialized metal fabrication have long lead times in the Okanagan. Ordering early matters.</li>
        <li><strong>Imported materials.</strong> Italian tile, European windows, specialty appliances. Lead times of 12 to 20 weeks are not uncommon.</li>
        <li><strong>Hidden site conditions.</strong> Unexpected rock on a hillside lot, poor soil requiring additional engineering, utility conflicts underground.</li>
      </ul>

      <h2>Phase 4: Deficiency and occupancy (1 to 2 months)</h2>

      <p>Once construction is substantially complete, final inspections begin. Building, plumbing, electrical, gas, and in some cases fire inspections all need to pass. Deficiencies identified during inspections get fixed, re-inspected, and signed off.</p>

      <p>The deficiency list that the homeowner walks through with the builder usually takes 2 to 4 weeks to resolve. Occupancy permit issuance from the municipality is typically 1 to 2 weeks after the final inspection passes.</p>

      <h2>How Kelowna-specific factors change the timeline</h2>

      <h3>Hillside lots</h3>

      <p>Hillside builds in neighborhoods like <a href="/neighborhoods/upper-mission/">Upper Mission</a>, <a href="/neighborhoods/lakeview-heights/">Lakeview Heights</a>, <a href="/neighborhoods/wilden/">Wilden</a>, and <a href="/neighborhoods/predator-ridge/">Predator Ridge</a> add 2 to 4 months to the overall timeline. The extra work includes geotechnical investigation, retaining walls, drainage engineering, Development Permit review, and more complex foundation work.</p>

      <h3>Waterfront and lakefront builds</h3>

      <p>Builds on Okanagan Lake, Kalamalka Lake, or Wood Lake with any foreshore work add provincial review. Riparian area regulations, archaeological assessments, and Transport Canada approvals for anything over the water each add weeks or months.</p>

      <h3>Architectural guideline communities</h3>

      <p>Master-planned communities with design review (Wilden, <a href="/neighborhoods/kettle-valley/">Kettle Valley</a>, Upper Mission sub-communities, <a href="/neighborhoods/mckinley-beach/">McKinley Beach</a>) add 4 to 10 weeks for architectural review before building permit submission. Working with a builder who knows the specific guidelines prevents design bounces.</p>

      <h3>Rural and acreage lots</h3>

      <p>Acreage builds in Lake Country, outer West Kelowna, or beyond municipal boundaries often require septic design, well drilling, hydro service installation, and sometimes road access improvements. Each of these adds weeks and can run in parallel with other design work if planned early.</p>

      <h2>What we have seen on real Kelowna projects</h2>

      <p>On our <a href="/project/cabernet-2/">Cabernet Way project</a> in West Kelowna, design ran 4 months, permits came through in 10 weeks, construction took 11 months, and deficiency plus occupancy was 6 weeks. Total: approximately 18 months from first meeting to move-in. The hillside site added about 2 months to what a flat-lot build of the same size would have taken.</p>

      <p>Our <a href="/project/malbec-place-1/">Malbec Place project</a> ran faster, approximately 15 months total, because the client arrived with a near-finalized concept, made decisive finish selections, and did not change scope during construction. The lot was also flat with straightforward foundations.</p>

      <p>The longest project we have run in recent years went 24 months, driven primarily by three major scope changes during construction and a long-lead imported stone package. None of those delays were surprises in hindsight. Each was a decision the client made, understood, and accepted at the time.</p>

      <blockquote style="border-left:3px solid #0085c9;padding:14px 20px;margin:28px 0;background:#f4f9fc;font-style:italic;color:#1a1d21;font-size:16px;line-height:1.65">
        <p style="margin:0">"The clients who finish on schedule are the ones who make decisions in design and stop making them in construction. Every change during framing is weeks and dollars. We do not discourage changes when they matter, but clients should understand what they cost before they request them." Jas Sidhu, Owner, Palermo Homes</p>
      </blockquote>

      <h2>How to plan a realistic move-in date</h2>

      <p>Work backward from your target move-in and add buffer:</p>

      <ol style="padding:0 0 0 22px;margin:0 0 24px">
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Pick a realistic move-in month. Avoid committing to specific school start dates or wedding events on the same month as projected occupancy.</li>
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Subtract 18 months as a baseline. That gets you to the "start of design" month.</li>
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Add 2 to 4 months buffer for anything hillside, complex, or on a tight lot.</li>
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Start builder conversations 1 to 2 months before design begins.</li>
      </ol>

      <p>For a summer 2028 move-in, that means builder conversations by late 2026, design starting by early 2027, and permits in-hand by late 2027.</p>

      <h2>How to compress the timeline (safely)</h2>

      <p>Pushing a Kelowna custom home faster than 14 months is possible but requires giving something up. Realistic ways to save time without cutting corners:</p>

      <ul>
        <li>Start with a near-complete concept rather than exploring options during paid design time</li>
        <li>Lock in finish selections before construction starts, not during</li>
        <li>Choose domestic materials over imported wherever possible</li>
        <li>Build on a flat lot in a non-hillside neighborhood</li>
        <li>Avoid architectural review communities if speed matters more than guidelines</li>
        <li>Submit permits in late fall when queues are shorter</li>
      </ul>

      <p>Compressing below 10 months on a true custom home usually means buying a modified spec home instead. There is nothing wrong with that path, but it is a different product than a true custom build.</p>

      <p class="footer-note">This guide reflects current permit and construction conditions in the Central Okanagan as of 2026. Municipal review times, trade availability, and material lead times change. Verify current specifics with the relevant municipality and any builder you interview.</p>
    </div>
  </section>

  <section class="guide-about">
    <div class="wrap">
      <h2>About Palermo Homes</h2>
      <p>Palermo Homes is a custom home builder based in West Kelowna, BC (BC Corporate Registration BC1017682, BC Housing Licensed Residential Builder Number 42812). We have been building custom homes and whole-home renovations across the Okanagan Valley and Lower Mainland for over 15 years.</p>
      <p>We build in <a href="/service-areas/kelowna/">Kelowna</a>, <a href="/service-areas/west-kelowna/">West Kelowna</a>, <a href="/service-areas/lake-country/">Lake Country</a>, <a href="/service-areas/peachland/">Peachland</a>, <a href="/service-areas/penticton/">Penticton</a>, <a href="/service-areas/vernon/">Vernon</a>, and select Lower Mainland communities.</p>
      <p>For cost specifically, see our <a href="/guides/custom-home-cost-kelowna/">2026 custom home cost guide</a>. For how to choose a builder before signing anything, see our <a href="/guides/how-to-choose-custom-home-builder-kelowna/">builder selection guide</a>. Common process questions are answered on our <a href="/faq/">FAQ page</a>.</p>
    </div>
  </section>

  <section class="guide-cta">
    <div class="wrap">
      <h2>Planning a custom home build in the Okanagan?</h2>
      <p>Start the conversation early. The best outcomes come from clients who plan 18 months ahead.</p>
      <a class="btn" href="/contact/">Book a consultation</a>
    </div>
  </section>
</div>
"""


OG_IMAGE = f"{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-02.jpg"
OG_TITLE = "How Long Does It Take to Build a Custom Home in Kelowna? 2026 Timeline Guide"
READING_TIME = "10 minutes"
ISO_MODIFIED = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "+00:00")


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    html = re.sub(r"/\* ==== GUIDE-TIMELINE CSS START ==== \*/.*?/\* ==== GUIDE-TIMELINE CSS END ==== \*/", "", html, flags=re.DOTALL)
    html = re.sub(r"/\* ==== ABOUT-V2 CSS START ==== \*/.*?/\* ==== ABOUT-V2 CSS END ==== \*/", "", html, flags=re.DOTALL)
    html = html.replace("</head>", f"<style>{GUIDE_CSS}</style></head>", 1)
    html = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', html, count=1)
    # Strip any existing meta description (any attribute order), inject fresh
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{META_DESC}"/>\n</head>', 1)
    # Strip any existing canonical tag (any attribute order), inject fresh
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{CANONICAL}"/>\n</head>', 1)
    # Overwrite stale OG + Twitter tags inherited from the About shell
    # Note: in this shell content="..." comes BEFORE property="..."
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
    # Replace the stale preload image (not self-closing in source)
    html = re.sub(
        r'<link rel="preload" as="image" href="[^"]*" fetchpriority="high">',
        f'<link rel="preload" as="image" href="{OG_IMAGE}" fetchpriority="high">',
        html, count=1,
    )
    html = html.replace("</head>", schema_block + "</head>", 1)

    out = SITE / "guides" / "how-long-to-build-custom-home-kelowna" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built Guide #3: How Long to Build a Custom Home in Kelowna.")
