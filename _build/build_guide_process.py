"""Build /guides/custom-home-building-process-kelowna/
Guide #8 - "The Custom Home Building Process in Kelowna."
Targets top-of-funnel queries: "custom home process", "how to build custom home",
"custom home steps", "building a house kelowna", "new home construction process bc".
Narrative walkthrough of 8 phases. Each phase: what happens, duration, who's
involved, what client delivers, what delays appear.
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
PAGE_URL = f"{BIZ_URL}/guides/custom-home-building-process-kelowna/"
PUBLISH_DATE = "2026-10-13"
MODIFIED_DATE = datetime.date.today().isoformat()

CSS_START = "/* ==== GUIDE-PROCESS CSS START ==== */"
CSS_END = "/* ==== GUIDE-PROCESS CSS END ==== */"

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
html body #et-main-area .guide-body .phase{{margin:36px 0 0;padding:24px 26px;background:#fff;border:1px solid #e2ddd0;border-radius:4px}}
html body #et-main-area .guide-body .phase-num{{font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 8px}}
html body #et-main-area .guide-body .phase h3{{margin:0 0 10px}}
html body #et-main-area .guide-body .phase .duration{{display:inline-block;font-size:13px;color:#6a7078;background:#f4f9fc;border:1px solid #cfe6f1;padding:3px 10px;border-radius:999px;margin:0 0 14px}}
html body #et-main-area .guide-body .phase p{{font-size:15px;line-height:1.65;margin:0 0 14px}}
html body #et-main-area .guide-body .phase .meta-row{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0 0;padding-top:14px;border-top:1px solid #ece8df;font-size:13px}}
html body #et-main-area .guide-body .phase .meta-row .label{{color:#8a8f97;letter-spacing:.02em;font-weight:600;text-transform:uppercase;font-size:11px;margin:0 0 4px}}
html body #et-main-area .guide-body .phase .meta-row .value{{color:#3a4048;line-height:1.5}}
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
  html body #et-main-area .guide-body .phase{{padding:20px 20px}}
  html body #et-main-area .guide-body .phase .meta-row{{grid-template-columns:1fr}}
  html body #et-main-area .guide-body table{{font-size:14px}}
  html body #et-main-area .guide-body table th,html body #et-main-area .guide-body table td{{padding:8px 10px}}
}}
{CSS_END}
"""

FAQ_ITEMS = [
    {
        "q": "What are the main phases of building a custom home in Kelowna?",
        "a": "A Kelowna custom home moves through 8 distinct phases: initial consultation and feasibility (2 to 4 weeks), lot evaluation and feasibility study (2 to 4 weeks if a lot is already owned, longer if lot hunting is active), design and architectural development (3 to 6 months), permits and approvals (6 weeks to 3 months), site preparation and foundation (6 to 10 weeks), framing and envelope (10 to 18 weeks), mechanical, electrical, plumbing, and interior finishing (24 to 40 weeks), and final inspections, deficiencies, and occupancy (4 to 8 weeks). From first conversation to move-in, a typical build runs 14 to 20 months."
    },
    {
        "q": "What does the initial consultation phase involve?",
        "a": "The initial consultation is a 60 to 90 minute conversation covering your vision, lot (if you own one), budget range, timeline target, and style direction. A good builder uses this meeting to assess whether the project is realistic for your lot and budget, flag any obvious constraints (hillside, size limits, permit complexity), and give you an honest first opinion on cost range. No fees are charged for this meeting at Palermo Homes. If both sides want to move forward, a feasibility study or design agreement follows."
    },
    {
        "q": "Do I need to own a lot before starting the custom home process?",
        "a": "No. Many clients engage a custom builder before purchasing a lot, specifically to evaluate lots during the shopping phase. A builder's pre-purchase walk-through can identify slope issues, access constraints, servicing problems, geotechnical concerns, Development Permit requirements, and architectural guideline restrictions that affect buildability and cost. This 90-minute step before you offer is almost always worth more than any inspection commissioned after the deal closes. We offer pre-purchase lot walks across the Central Okanagan."
    },
    {
        "q": "How long is the design phase on a custom home in Kelowna?",
        "a": "Design typically runs 3 to 6 months for a Kelowna custom home. The phase includes initial concept drawings, floor plan refinement, architectural detailing (exterior elevations, roof lines, window placements), structural engineering, mechanical, electrical, and plumbing layout, and interior finish selections. Homeowners who arrive with a clear vision and make decisive selections finish design in 3 to 4 months. Those who explore multiple directions or change scope mid-design often take 5 to 6 months or longer."
    },
    {
        "q": "What happens during the permit phase?",
        "a": "During the permit phase, the complete application package (architectural, structural, mechanical, Step Code report, Home Warranty registration, geotechnical where required) is submitted to the municipality for building permit review. Review times vary by municipality: 15 business days in West Kelowna, 2 weeks in Peachland, 21 business days in Penticton, and 4 to 6 weeks typically in Kelowna. Development Permits (required on hillside and some other sites) add additional review time. The permit phase is where most delays happen when applications are incomplete."
    },
    {
        "q": "What should a client expect to be doing during the construction phase?",
        "a": "During construction, the client's main responsibilities are responding to selection decisions (confirming tile, plumbing fixtures, lighting, hardware when samples are presented), attending scheduled site walks (typically every 2 to 4 weeks), reviewing weekly or bi-weekly photo updates, and making timely decisions on any change requests. A well-managed build minimizes the number of decisions dropped on the client mid-construction by locking selections before the first wall goes up. The client is not expected to be on-site daily or to manage trades directly."
    },
    {
        "q": "How is a custom home different from buying a spec home or a production builder's house?",
        "a": "A custom home is designed from scratch for your specific lot, lifestyle, and budget. You choose the floor plan, the finishes, the systems, and the structural details. A spec home is designed by a builder, built on speculation, and sold as-is or with limited finish choices. A production builder's home is one of a handful of pre-designed plans built repeatedly across a development with limited customization. True custom builds take longer (14 to 20 months vs 6 to 10 months for a spec or production home) and cost more per square foot, but produce a home specifically shaped around how you actually live."
    },
    {
        "q": "When should I start the custom home process if I want to move in by a specific date?",
        "a": "Work backward from your target move-in and add 18 months as a baseline, plus 2 to 4 months buffer for anything hillside, complex, or on a tight lot. For a summer 2028 move-in, that means builder conversations by late 2026, design starting by early 2027, and permits submitted by late 2027. Rushing design to meet a tight move-in date almost always costs more in change orders and leads to decisions you regret later. Our full timeline breakdown is in the <a href='/guides/how-long-to-build-custom-home-kelowna/'>timeline guide</a>."
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
        "headline": "The Custom Home Building Process in Kelowna: A Phase-by-Phase 2026 Guide",
        "description": "Everything that happens when you build a custom home in Kelowna, from first consultation to move-in. Each phase explained in plain English: what happens, how long it takes, who is involved, and what the client is responsible for.",
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
            {"@type": "Thing", "name": "Custom Home Building Process"},
            {"@type": "Thing", "name": "New Home Construction"},
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
            {"@type": "ListItem", "position": 3, "name": "The Custom Home Building Process in Kelowna", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "The Custom Home Building Process in Kelowna: A Phase-by-Phase 2026 Guide",
        "description": "A plain-English walkthrough of the full custom home building process in Kelowna, from first consultation to move-in. Each of the 8 phases explained.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, article, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Custom Home Building Process Kelowna: 8-Phase Guide | Palermo Homes"
META_DESC = "Everything that happens when you build a custom home in Kelowna, from first consultation to move-in. 8 phases explained in plain English with durations."
CANONICAL = PAGE_URL

MAIN_HTML = """
<div class="guide">
  <section class="guide-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">&middot;</span><a href="/guides/">Guides</a><span class="sep">&middot;</span>The Custom Home Building Process in Kelowna</p>
      <h1>The Custom Home Building Process in Kelowna: A Phase-by-Phase 2026 Guide</h1>
      <p class="sub">Everything that happens when you build a custom home in Kelowna, from first consultation to move-in. Each of the 8 phases explained in plain English: what happens, how long it takes, who is involved, and what you as the client are responsible for.</p>
      <p class="meta">Published October 2026 &middot; By <a href="/about/jas-sidhu/" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1">Jas Sidhu</a>, Owner of Palermo Homes &middot; Custom Home Builder in West Kelowna, BC</p>
    </div>
  </section>

  <section class="guide-body">
    <div class="wrap">
      <div class="lede">
        <p>Building a custom home in Kelowna moves through 8 distinct phases over 14 to 20 months: initial consultation, lot evaluation, design, permits, site prep and foundation, framing and envelope, mechanical and interior finishing, and final inspections and occupancy. Each phase has a typical duration, a defined set of professionals involved, and specific things the client is responsible for. Understanding the sequence before you start prevents the two most common mistakes: starting with the wrong lot and starting design before scope is clear.</p>
      </div>

      <figure style="margin:28px 0 32px;padding:0">
        <img src="/wp-content/uploads/2025/12/Cabernet-02.jpg" alt="Completed Palermo Homes custom home on Cabernet Way in West Kelowna, representing the final result of the full 8-phase custom home building process" style="width:100%;height:auto;display:block;border-radius:4px" loading="lazy" width="1200" height="800">
        <figcaption style="font-size:13px;color:#6a7078;margin:10px 0 0;line-height:1.5;font-style:italic">A completed custom home on Cabernet Way, West Kelowna. The full process from first consultation to this photograph ran approximately 18 months.</figcaption>
      </figure>

      <p>Most first-time custom home clients walk into the process with a general idea of the finished product and almost no picture of what happens between first conversation and move-in. The gap between the two is what makes custom home building feel opaque. This guide pulls that gap apart into 8 sequential phases that happen on every build, in the same order, with similar durations across similar projects.</p>

      <p>The phases are a sequence, not a checklist to rush through. Each one has decisions that lock the next one in place. Shortcutting earlier phases almost always creates problems in later phases that cost more to fix than the time saved up front.</p>

      <h2>The 8 phases at a glance</h2>

      <table>
        <thead>
          <tr><th>Phase</th><th>Typical duration</th><th>What locks at the end</th></tr>
        </thead>
        <tbody>
          <tr><td>1. Initial consultation and feasibility</td><td>2 to 4 weeks</td><td>Decision to proceed, builder selected</td></tr>
          <tr><td>2. Lot evaluation and site study</td><td>2 to 4 weeks (if lot owned)</td><td>Buildable envelope, site constraints identified</td></tr>
          <tr><td>3. Design and architectural development</td><td>3 to 6 months</td><td>Final construction drawings</td></tr>
          <tr><td>4. Permits and approvals</td><td>6 weeks to 3 months</td><td>Building permit in-hand</td></tr>
          <tr><td>5. Site preparation and foundation</td><td>6 to 10 weeks</td><td>Foundation poured and backfilled</td></tr>
          <tr><td>6. Framing and envelope</td><td>10 to 18 weeks</td><td>Weather-tight shell</td></tr>
          <tr><td>7. Mechanical, electrical, plumbing, and interior finishing</td><td>24 to 40 weeks</td><td>Substantially complete home</td></tr>
          <tr><td>8. Final inspections, deficiencies, and occupancy</td><td>4 to 8 weeks</td><td>Occupancy permit, keys handed over</td></tr>
        </tbody>
      </table>

      <h2>Phase 1: Initial consultation and feasibility</h2>

      <div class="phase">
        <p class="phase-num">Phase 1</p>
        <h3>What this phase actually looks like</h3>
        <span class="duration">2 to 4 weeks</span>
        <p>The first conversation is a 60 to 90 minute meeting with the builder, usually in person at their office or on your lot if you own one. The topics covered are your vision, your lot or lot-shopping status, your budget range, your timeline target, and your style direction.</p>
        <p>A good builder uses this meeting to assess whether the project is realistic for the budget, flag any obvious lot or scope constraints, and give you a candid first opinion on cost range. If both sides want to move forward, a feasibility study or design agreement follows.</p>
        <div class="meta-row">
          <div><p class="label">Who is involved</p><p class="value">Builder (owner or senior PM), you</p></div>
          <div><p class="label">What the client delivers</p><p class="value">Lot information (if owned), rough budget range, must-have list</p></div>
        </div>
      </div>

      <h2>Phase 2: Lot evaluation and site study</h2>

      <div class="phase">
        <p class="phase-num">Phase 2</p>
        <h3>Understanding what the lot can actually support</h3>
        <span class="duration">2 to 4 weeks (if lot owned); longer if actively lot hunting</span>
        <p>Before any serious design work, the lot needs to be evaluated for buildability. The builder walks the site, reviews zoning and setbacks, assesses slope and access, and identifies anything that will drive cost or constrain design.</p>
        <p>If the lot has not been purchased yet, this phase can run as pre-purchase walk-throughs on candidate lots. The 90 minutes spent on a lot before you offer almost always catches issues that would cost tens of thousands to work around after the deal closes. Hillside status, Development Permit requirements, servicing constraints, soil issues, ridgeline or ravine proximity, and architectural guideline restrictions all get flagged here.</p>
        <p>For hillside lots specifically, a geotechnical engineer may be engaged in this phase or at the start of design. See our <a href="/guides/hillside-custom-home-kelowna/">hillside builds guide</a> for the full breakdown of what sloped lots add to cost and timeline.</p>
        <div class="meta-row">
          <div><p class="label">Who is involved</p><p class="value">Builder, geotech engineer (if hillside), municipal planning (informational calls)</p></div>
          <div><p class="label">What the client delivers</p><p class="value">Lot title, any existing surveys, any municipal correspondence</p></div>
        </div>
      </div>

      <h2>Phase 3: Design and architectural development</h2>

      <div class="phase">
        <p class="phase-num">Phase 3</p>
        <h3>Translating vision into construction drawings</h3>
        <span class="duration">3 to 6 months</span>
        <p>Design is the phase most homeowners underestimate. It is also the phase where decisions have the biggest downstream impact on both cost and construction speed. The phase includes initial concept drawings, floor plan options, floor plan refinement and sign-off, architectural detailing (exterior elevations, window placements, roof lines), structural engineering, mechanical/electrical/plumbing layout, and interior finish selections.</p>
        <p>The clients who finish design in 3 to 4 months are the ones who arrive with a clear vision and make decisive selections. The clients who take 5 to 6+ months are the ones who explore multiple directions, change scope, or struggle with finish decisions. Both are valid approaches, but the longer path adds design cost and delays construction.</p>
        <p>Interior finish selections stall more projects than most people expect. Choosing between three tile options takes an afternoon. Choosing between three thousand takes months. Builders who provide curated allowance ranges keep this phase moving.</p>
        <div class="meta-row">
          <div><p class="label">Who is involved</p><p class="value">Architect or designer, structural engineer, Energy Advisor, interior designer, mechanical consultants, builder as project coordinator</p></div>
          <div><p class="label">What the client delivers</p><p class="value">Timely feedback on options, decisions on finish selections, approvals at each design milestone</p></div>
        </div>
      </div>

      <h2>Phase 4: Permits and approvals</h2>

      <div class="phase">
        <p class="phase-num">Phase 4</p>
        <h3>Clearing the municipal review</h3>
        <span class="duration">6 weeks to 3 months</span>
        <p>Once design is complete and all consulting work is stamped and ready, the full package is submitted to the municipality for building permit review. For hillside lots or lots in Development Permit areas, a DP review runs separately and often precedes the building permit submission.</p>
        <p>Permit review times vary by municipality: 15 business days target in West Kelowna, 2 weeks in Peachland, 21 business days standard in Penticton, 4 to 6 weeks typical in Kelowna. Complete, well-prepared applications clear first review with minor comments only. Incomplete applications or complex files trigger revision cycles that add weeks or months.</p>
        <p>For the full fee and process breakdown by municipality, see the <a href="/guides/custom-home-permits-okanagan/">Okanagan permits guide</a>.</p>
        <div class="meta-row">
          <div><p class="label">Who is involved</p><p class="value">Builder (as applicant), municipal plans examiner, BC Housing (for warranty registration), Technical Safety BC (for electrical permits)</p></div>
          <div><p class="label">What the client delivers</p><p class="value">Signatures on application forms, payment of DCCs and permit fees</p></div>
        </div>
      </div>

      <h2>Phase 5: Site preparation and foundation</h2>

      <div class="phase">
        <p class="phase-num">Phase 5</p>
        <h3>Breaking ground and establishing the base</h3>
        <span class="duration">6 to 10 weeks</span>
        <p>Site prep covers clearing, grading, excavation, and installation of underslab services (water, sewer, drainage, sometimes radon mitigation). On hillside lots this phase includes retaining wall installation and more complex drainage. Foundation work follows: footings, foundation walls, waterproofing, perimeter drainage, and backfill.</p>
        <p>This is the first visible phase, which creates a false sense that the project is now moving fast. The reality is that months of preparation lead to a few weeks of ground work, and construction then settles into the longer phases that follow.</p>
        <div class="meta-row">
          <div><p class="label">Who is involved</p><p class="value">Excavation contractor, concrete contractor, surveyor (foundation layout), municipal inspector, plumbing contractor (underslab)</p></div>
          <div><p class="label">What the client delivers</p><p class="value">Nothing specific; the client observes and approves foundation layout before pour</p></div>
        </div>
      </div>

      <h2>Phase 6: Framing and envelope</h2>

      <div class="phase">
        <p class="phase-num">Phase 6</p>
        <h3>The shell goes up</h3>
        <span class="duration">10 to 18 weeks</span>
        <p>Framing is the phase where the home starts to look like itself. Floors, walls, roof structure, windows, exterior doors, roofing, and exterior sheathing all happen here. By the end of this phase, the shell is weather-tight and the interior is protected from the elements.</p>
        <p>Clients often want to make design changes during framing because it is the first phase where spaces feel real. Changes at this point are expensive. Moving a wall after framing requires re-engineering, re-permit review in some cases, and ripple effects through mechanical and electrical layouts. The decisions locked in design phase should stay locked.</p>
        <div class="meta-row">
          <div><p class="label">Who is involved</p><p class="value">Framing crew, structural engineer (site inspections), window installer, roofing contractor, exterior finish crews</p></div>
          <div><p class="label">What the client delivers</p><p class="value">Attend first site walk after framing is complete, confirm no last-minute changes</p></div>
        </div>
      </div>

      <h2>Phase 7: Mechanical, electrical, plumbing, and interior finishing</h2>

      <div class="phase">
        <p class="phase-num">Phase 7</p>
        <h3>The longest phase, by far</h3>
        <span class="duration">24 to 40 weeks</span>
        <p>This is the longest and most complex phase in the entire build. It covers rough-in of mechanical, electrical, and plumbing systems, insulation, drywall, interior trim and millwork, cabinets, flooring, tile, paint, lighting fixtures, plumbing fixtures, appliances, and all exterior finishing (siding, soffits, decks, driveway).</p>
        <p>The phase includes many simultaneous trade sequences. Framing of mechanical in one room while drywall finishes in another. Cabinet installation in the kitchen while tile crews work in a bathroom. Good construction management sequences trades so each one has a clear path and no one is waiting on another.</p>
        <p>Clients should expect bi-weekly site walks during this phase, weekly or bi-weekly progress photo updates, and periodic selection confirmations as specific finish decisions come up (tile grout colour, hardware specifics, final paint sheen).</p>
        <div class="meta-row">
          <div><p class="label">Who is involved</p><p class="value">Mechanical, electrical, plumbing, insulation, drywall, trim, cabinet, flooring, tile, paint, siding, deck, and landscape trades. The builder coordinates all of them.</p></div>
          <div><p class="label">What the client delivers</p><p class="value">Timely selection confirmations, attendance at scheduled site walks, response to any change requests within agreed timeframes</p></div>
        </div>
      </div>

      <h2>Phase 8: Final inspections, deficiencies, and occupancy</h2>

      <div class="phase">
        <p class="phase-num">Phase 8</p>
        <h3>From "substantially complete" to keys in hand</h3>
        <span class="duration">4 to 8 weeks</span>
        <p>Once construction is substantially complete, final inspections begin: building, plumbing, electrical, gas, and in some cases fire. Each inspection may surface deficiencies that need to be corrected and re-inspected.</p>
        <p>The homeowner walks through the home with the builder for a formal deficiency list review. Most lists have 20 to 60 items on a typical build: paint touch-ups, trim adjustments, hardware tweaks, minor cosmetic issues. The builder resolves these over 2 to 4 weeks. Occupancy permit is issued once the final inspection sign-offs are complete, typically 1 to 2 weeks after the final inspection passes.</p>
        <p>Keys are handed over, the Home Warranty becomes active, and the project transitions to post-occupancy support. Palermo Homes maintains a direct communication channel with every client for warranty questions and ongoing support.</p>
        <div class="meta-row">
          <div><p class="label">Who is involved</p><p class="value">Municipal inspectors (building, plumbing, electrical, gas, fire), builder, client, Energy Advisor (final verification), warranty provider</p></div>
          <div><p class="label">What the client delivers</p><p class="value">Participation in deficiency walk, timely decisions on any remaining selections (e.g. landscape plants), final payment</p></div>
        </div>
      </div>

      <h2>What happens in parallel across phases</h2>

      <p>The 8-phase structure above is sequential at the high level but many activities run in parallel inside and across phases. Finish selections continue into early construction. Structural engineering continues during permit review. Trade scheduling begins before site prep finishes. A good project manager maintains a master schedule that keeps every parallel activity moving without creating bottlenecks.</p>

      <p>What should not run in parallel: major scope decisions and active construction. Clients who change scope during framing or finishing almost always see weeks of delay and significant change-order cost. The design phase is the place to make scope decisions.</p>

      <h2>What a client actually does across all 8 phases</h2>

      <p>Over 14 to 20 months, the client's time commitment averages 2 to 6 hours per week during active phases, concentrated in the design phase and in site walks during construction. Specifically:</p>

      <ul>
        <li><strong>Design phase (3 to 6 months):</strong> 4 to 8 hours per week on finish selections, floor plan reviews, meetings with the design team</li>
        <li><strong>Permit phase:</strong> Minimal client involvement; the builder manages submission and response to municipal comments</li>
        <li><strong>Site prep and foundation:</strong> 1 to 2 site visits, otherwise observational</li>
        <li><strong>Framing and envelope:</strong> First site walk after framing complete; otherwise observe photo updates</li>
        <li><strong>Finishing (longest phase):</strong> Bi-weekly site walks, selection confirmations as needed</li>
        <li><strong>Final phase:</strong> Deficiency walk, final payment, move-in</li>
      </ul>

      <p>A well-run custom home does not require the client to be on-site daily or to manage trades directly. That is the builder's job. The client's job is to make clear decisions in design, show up for the key milestones, and let the builder run the construction.</p>

      <blockquote style="border-left:3px solid #0085c9;padding:14px 20px;margin:28px 0;background:#f4f9fc;font-style:italic;color:#1a1d21;font-size:16px;line-height:1.65">
        <p style="margin:0">"The best custom home clients are the ones who understand what phase we are in and make phase-appropriate decisions. Design decisions during design. Finish decisions before trades arrive. Nothing after framing except colour and hardware tweaks. The projects that go over budget are almost always the ones where the client treats construction as an extension of design." Jas Sidhu, Owner, Palermo Homes</p>
      </blockquote>

      <h2>Common mistakes to avoid</h2>

      <ol>
        <li><strong>Starting design before the lot is confirmed.</strong> Design decisions depend on the specific lot. Design developed for one lot rarely transfers cleanly to another.</li>
        <li><strong>Rushing design to meet a move-in date.</strong> Shortcutting design almost always costs more in change orders than it saves in weeks.</li>
        <li><strong>Submitting an incomplete permit application.</strong> Permit review restarts on affected sections every time revisions are required.</li>
        <li><strong>Making major scope changes during construction.</strong> Each change during framing adds 2 to 6 weeks and significant cost.</li>
        <li><strong>Choosing a builder based on the lowest bid.</strong> Final cost is far more about builder capability than initial quote. See the <a href="/guides/how-to-choose-custom-home-builder-kelowna/">builder selection guide</a>.</li>
      </ol>

      <h2>What this looks like on a real Kelowna build</h2>

      <p>Our <a href="/project/cabernet-2/">Cabernet Way project</a> ran the full 8-phase process over approximately 18 months. Initial consultation and lot evaluation took 3 weeks. Design ran 4 months. Permits came through in 10 weeks. Site prep, foundation, framing, and finishing ran 11 months of active construction. Final inspections and deficiency work took 6 weeks. Total: approximately 18 months from first meeting to keys-in-hand.</p>

      <p class="footer-note">This guide reflects the current process, timelines, and requirements for custom home building in the Central Okanagan as of 2026. Municipal review times, trade availability, and specific requirements change. Verify current specifics with any builder you interview.</p>
    </div>
  </section>

  <section class="guide-about">
    <div class="wrap">
      <h2>About Palermo Homes</h2>
      <p>Palermo Homes is a custom home builder based in West Kelowna, BC (BC Corporate Registration BC1017682, BC Housing Licensed Residential Builder Number 42812). We walk every client through the same 8-phase process described above, with transparent timelines, defined decision points, and in-house coordination of design, permits, and construction.</p>
      <p>We build in <a href="/service-areas/kelowna/">Kelowna</a>, <a href="/service-areas/west-kelowna/">West Kelowna</a>, <a href="/service-areas/lake-country/">Lake Country</a>, <a href="/service-areas/peachland/">Peachland</a>, <a href="/service-areas/penticton/">Penticton</a>, <a href="/service-areas/vernon/">Vernon</a>, and select Lower Mainland communities.</p>
      <p>For cost context across the process, see our <a href="/guides/custom-home-cost-kelowna/">cost guide</a>. For how long each phase takes, see the <a href="/guides/how-long-to-build-custom-home-kelowna/">timeline guide</a>. For the permit specifics in Phase 4, see the <a href="/guides/custom-home-permits-okanagan/">permits guide</a>. For contract structure before you start design, see the <a href="/guides/fixed-price-vs-cost-plus-custom-home-kelowna/">fixed-price vs cost-plus guide</a>.</p>
    </div>
  </section>

  <section class="guide-cta">
    <div class="wrap">
      <h2>Thinking about starting the process?</h2>
      <p>The first conversation is a 60 to 90 minute meeting. No fees, no pressure. We will give you a realistic assessment of what your project looks like end-to-end.</p>
      <a class="btn" href="/contact/">Book a consultation</a>
    </div>
  </section>
</div>
"""


OG_IMAGE = f"{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-02.jpg"
OG_TITLE = "The Custom Home Building Process in Kelowna: A Phase-by-Phase 2026 Guide"


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    html = re.sub(r"/\* ==== GUIDE-PROCESS CSS START ==== \*/.*?/\* ==== GUIDE-PROCESS CSS END ==== \*/", "", html, flags=re.DOTALL)
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

    out = SITE / "guides" / "custom-home-building-process-kelowna" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built Guide #8: The Custom Home Building Process in Kelowna.")
