"""Build /guides/bc-2-5-10-new-home-warranty-explained/
Guide #10 - "BC's 2-5-10 New Home Warranty Explained."
Targets high-intent queries: "2-5-10 warranty bc", "bc new home warranty",
"home warranty insurance british columbia", "homeowner protection act bc".
Structural variation: coverage-tier cards (3 big cards for 2-yr, 5-yr, 10-yr)
with visual year ribbons.
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
PAGE_URL = f"{BIZ_URL}/guides/bc-2-5-10-new-home-warranty-explained/"
PUBLISH_DATE = "2026-10-15"
MODIFIED_DATE = datetime.date.today().isoformat()

CSS_START = "/* ==== GUIDE-WARRANTY CSS START ==== */"
CSS_END = "/* ==== GUIDE-WARRANTY CSS END ==== */"

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
html body #et-main-area .guide-body .tier-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:30px 0 32px}}
html body #et-main-area .guide-body .tier{{background:#fff;border:1px solid #e2ddd0;border-radius:4px;padding:22px 22px;position:relative;overflow:hidden}}
html body #et-main-area .guide-body .tier .ribbon{{position:absolute;top:0;right:0;background:#0085c9;color:#fff;padding:5px 12px;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;border-radius:0 4px 0 4px}}
html body #et-main-area .guide-body .tier .years{{font-size:40px;font-weight:700;color:#0085c9;letter-spacing:-0.03em;line-height:1;margin:0 0 4px}}
html body #et-main-area .guide-body .tier .label{{font-size:13px;font-weight:600;color:#1a1d21;letter-spacing:.02em;margin:0 0 14px}}
html body #et-main-area .guide-body .tier .scope{{font-size:14px;line-height:1.5;color:#3a4048;margin:0;padding-top:14px;border-top:1px solid #ece8df}}
html body #et-main-area .guide-body .callout{{background:#fef9f0;border-left:3px solid #d4a01a;padding:18px 22px;margin:24px 0;border-radius:0 4px 4px 0}}
html body #et-main-area .guide-body .callout .label{{font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:#8f6b11;font-weight:700;margin:0 0 8px}}
html body #et-main-area .guide-body .callout p{{margin:0;font-size:15px;line-height:1.65;color:#1a1d21}}
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
  html body #et-main-area .guide-body .tier-grid{{grid-template-columns:1fr;gap:12px}}
  html body #et-main-area .guide-body table{{font-size:14px}}
  html body #et-main-area .guide-body table th,html body #et-main-area .guide-body table td{{padding:8px 10px}}
}}
{CSS_END}
"""

FAQ_ITEMS = [
    {
        "q": "What is BC's 2-5-10 New Home Warranty?",
        "a": "BC's 2-5-10 is the mandatory new home warranty required by the Homeowner Protection Act for every new home built by a licensed residential builder in British Columbia. It is the strongest construction defect insurance in Canada. The 2-5-10 refers to the three coverage periods: 2 years on labour and materials, 5 years on the building envelope, and 10 years on structural defects. The warranty is sold by BC Housing-authorized third-party insurers and is non-optional for licensed builds."
    },
    {
        "q": "What exactly does the 2-year coverage include?",
        "a": "The 2-year coverage is layered. For the first 12 months (15 months for common property in multi-unit buildings), it covers general defects in labour and materials across the whole home. For the full 24 months, it covers defects in major systems: electrical, plumbing, heating, ventilation, air conditioning, exterior cladding, windows, exterior doors, and anything that makes the home unfit to live in. This is the broadest coverage period and catches most workmanship issues homeowners experience in year one and two."
    },
    {
        "q": "What does the 5-year building envelope coverage cover?",
        "a": "The 5-year period covers defects that cause unintended water penetration into the home. This includes exterior walls, roof systems, foundations below grade, flashings, membranes, and anything in the building envelope that is supposed to keep water out. If water intrudes due to a construction defect within 5 years of occupancy, the warranty covers both the repair of the defect and any resulting damage to the home."
    },
    {
        "q": "What does the 10-year structural coverage cover?",
        "a": "The 10-year period is the narrowest but longest. It covers defects in the load-bearing components of the home (foundation, beams, columns, structural framing) that affect structural integrity, as well as any defect that makes the home unfit to live in. It does not cover cosmetic issues, minor performance problems, or anything that is not genuinely structural. In practice, 10-year claims are rare because serious structural issues on a properly built home from a licensed builder are rare."
    },
    {
        "q": "What is NOT covered by the 2-5-10 warranty?",
        "a": "Common exclusions include normal wear and tear, damage caused by homeowner negligence or failure to maintain the home, landscaping and site grading, non-residential structures (sheds, detached garages depending on policy), roads, curbs, driveways, materials supplied by the owner rather than the builder, damage caused by others or by natural events (earthquake, flood, fire, windstorm), and secondary damage from issues the homeowner delayed reporting. Each warranty provider has specific exclusions listed in the policy document, which should be read carefully at closing."
    },
    {
        "q": "Who provides the 2-5-10 warranty, and does the builder choose?",
        "a": "The warranty is issued by a third-party insurer that is authorized by BC Housing. Current authorized providers include Travelers Canada, National Home Warranty, Pacific Home Warranty, and WBI Home Warranty. The licensed builder registers the home with their chosen warranty provider, pays the warranty premium (typically $1,500 to $4,000+ depending on home value and builder record), and the policy is issued to the homeowner at closing. The homeowner does not choose the provider, the builder does, but all BC Housing-authorized providers meet the same minimum coverage requirements under the Act."
    },
    {
        "q": "How do I make a warranty claim?",
        "a": "The standard process: first contact the builder in writing with a clear description of the defect, photos, and the date you discovered it. The builder typically has an opportunity to inspect and remedy the issue directly. If the builder does not respond, disputes the claim, or no longer operates, the homeowner escalates to the warranty insurance provider directly. The provider sends an adjuster to assess, and if coverage applies, authorizes repair. Document everything in writing from day one. Keep all warranty documents, inspection reports, and photos together in one file."
    },
    {
        "q": "What happens if the builder goes out of business?",
        "a": "The warranty continues to protect the homeowner even if the builder dissolves or ceases operations. This is one of the main reasons the 2-5-10 is backed by third-party insurance rather than the builder directly. If the builder is no longer available to perform warranty repairs, the warranty provider steps in. This is a critical protection, especially for structural (10-year) and envelope (5-year) coverage periods that extend well beyond typical builder tenure in some cases."
    },
    {
        "q": "Does the warranty transfer to subsequent owners if I sell the home?",
        "a": "Yes. The 2-5-10 warranty attaches to the home, not the original purchaser. All remaining coverage periods transfer automatically to new owners at resale. This increases the home's resale value, particularly within the first 5 years when envelope coverage still applies. Make sure to pass all warranty documentation to the new owner at closing."
    },
    {
        "q": "What is the Owner-Builder Exemption and how does it affect warranty?",
        "a": "BC Housing allows an Owner-Builder Exemption for homeowners who want to act as their own general contractor on a home they will personally occupy (not build-for-sale). The exemption waives the mandatory 2-5-10 warranty requirement, which reduces upfront cost but eliminates the warranty protection. Owner-builder exemptions also carry restrictions: typically only one exempt build per 18 months and limits on reselling the home within the first year of occupancy. For most buyers, hiring a licensed builder with mandatory warranty coverage provides significantly stronger long-term protection."
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
        "headline": "BC's 2-5-10 New Home Warranty Explained: What's Covered, What Isn't, and How to Claim",
        "description": "A plain-English guide to British Columbia's mandatory 2-5-10 New Home Warranty. Coverage periods, exclusions, how to make a claim, what happens if the builder closes, and how the warranty transfers at resale.",
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
            {"@type": "Thing", "name": "2-5-10 New Home Warranty"},
            {"@type": "Thing", "name": "Homeowner Protection Act BC"},
            {"@type": "Thing", "name": "BC Housing"},
            {"@type": "Place", "name": "British Columbia, Canada"},
            {"@type": "Place", "name": "Kelowna, BC"},
        ],
    }

    breadcrumbs = {
        "@type": "BreadcrumbList",
        "@id": f"{PAGE_URL}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BIZ_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{BIZ_URL}/guides/"},
            {"@type": "ListItem", "position": 3, "name": "BC's 2-5-10 New Home Warranty Explained", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "BC's 2-5-10 New Home Warranty Explained: What's Covered, What Isn't, and How to Claim",
        "description": "A plain-English 2026 guide to British Columbia's mandatory 2-5-10 New Home Warranty. Coverage, exclusions, claims process, and resale transfer.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, article, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "BC's 2-5-10 New Home Warranty Explained | Palermo Homes"
META_DESC = "A plain-English guide to BC's mandatory 2-5-10 New Home Warranty. What is covered in each period, exclusions, how to claim, resale transfer."
CANONICAL = PAGE_URL

MAIN_HTML = """
<div class="guide">
  <section class="guide-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">&middot;</span><a href="/guides/">Guides</a><span class="sep">&middot;</span>BC's 2-5-10 New Home Warranty Explained</p>
      <h1>BC's 2-5-10 New Home Warranty Explained: What's Covered, What Isn't, and How to Claim</h1>
      <p class="sub">A plain-English walk-through of British Columbia's mandatory new home warranty. Three coverage periods, what each one covers in practice, the exclusions nobody mentions until you need them, and the exact process for making a claim.</p>
      <p class="meta">Published October 2026 &middot; By <a href="/about/jas-sidhu/" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1">Jas Sidhu</a>, Owner of Palermo Homes &middot; BC Housing Licensed Residential Builder 42812</p>
    </div>
  </section>

  <section class="guide-body">
    <div class="wrap">
      <div class="lede">
        <p>BC's 2-5-10 New Home Warranty is mandatory for every new home built by a licensed residential builder in British Columbia under the Homeowner Protection Act. It is the strongest construction defect insurance in Canada. The three numbers refer to three coverage periods: 2 years on labour and materials, 5 years on the building envelope, 10 years on load-bearing structure. The warranty is backed by a BC Housing-authorized third-party insurer, which means coverage continues even if the builder closes down.</p>
      </div>

      <figure style="margin:28px 0 32px;padding:0">
        <img src="/wp-content/uploads/2025/12/Cabernet-02.jpg" alt="A completed Palermo Homes custom build on Cabernet Way in West Kelowna, protected by BC's mandatory 2-5-10 New Home Warranty" style="width:100%;height:auto;display:block;border-radius:4px" loading="lazy" width="1200" height="800">
        <figcaption style="font-size:13px;color:#6a7078;margin:10px 0 0;line-height:1.5;font-style:italic">Every Palermo Homes custom build is registered under BC Housing License 42812 and automatically covered by the mandatory 2-5-10 warranty.</figcaption>
      </figure>

      <div class="tier-grid">
        <div class="tier">
          <span class="ribbon">Year 1 to 2</span>
          <p class="years">2</p>
          <p class="label">Labour and materials</p>
          <p class="scope">General defects for 12 months (15 months for multi-unit common property). Major systems (electrical, plumbing, HVAC, cladding, windows, doors) and anything making the home unfit to live in: full 24 months.</p>
        </div>
        <div class="tier">
          <span class="ribbon">Year 1 to 5</span>
          <p class="years">5</p>
          <p class="label">Building envelope</p>
          <p class="scope">Defects causing unintended water penetration. Exterior walls, roofs, foundations below grade, flashings, membranes. Covers both the defect repair and any resulting damage.</p>
        </div>
        <div class="tier">
          <span class="ribbon">Year 1 to 10</span>
          <p class="years">10</p>
          <p class="label">Load-bearing structure</p>
          <p class="scope">Defects in load-bearing components (foundation, beams, columns, framing) that affect structural integrity, or any defect making the home unfit to live in. Narrow but long.</p>
        </div>
      </div>

      <p>Those three periods run concurrently, not consecutively. The clock starts ticking on all three at the same moment, which is the earlier of the home's first occupancy date or the first owner's title transfer date. By year 3, your 2-year period has expired but 5-year envelope and 10-year structure continue. By year 6, only 10-year structure continues. This is why the 10-year period is the narrowest in scope: it only kicks in for issues that genuinely require the long tail.</p>

      <h2>What the 2-year coverage actually includes</h2>

      <p>The 2-year period is where most warranty claims happen. It is the broadest coverage and catches typical workmanship issues that show up as the home settles and the systems break in.</p>

      <h3>First 12 months: everything</h3>

      <p>During the first 12 months of occupancy (15 months for common property in multi-unit buildings like townhouses or stratas), the warranty covers general defects in labour and materials across the whole home. This includes drywall cracks, paint issues, trim gaps, door and window operation problems, caulking failures, flooring defects, cabinet alignment, hardware function, and general finish quality.</p>

      <h3>Full 24 months: major systems + habitability</h3>

      <p>For the full two years, these specific categories remain covered:</p>

      <ul>
        <li><strong>Electrical systems:</strong> wiring, panels, fixtures, outlets, switches</li>
        <li><strong>Plumbing systems:</strong> supply lines, drains, fixtures, water heater, pressure</li>
        <li><strong>Heating, ventilation, and air conditioning:</strong> furnace, ducting, air handlers, thermostats</li>
        <li><strong>Exterior cladding:</strong> siding, stone, brick, stucco (installation defects, not weathering)</li>
        <li><strong>Windows and exterior doors:</strong> defects in installation, operation, or sealing</li>
        <li><strong>Any defect making the home unfit to live in:</strong> safety hazards, major system failures</li>
      </ul>

      <h2>What the 5-year envelope coverage actually includes</h2>

      <p>The 5-year building envelope period covers one specific issue: water getting into the home where it is not supposed to. The envelope is everything that separates conditioned interior space from the exterior. Walls, roofs, and foundations below grade are the primary components. Supporting elements include flashings, roofing membranes, window and door seals, air and vapour barriers, and penetrations through the envelope.</p>

      <p>A 5-year claim typically starts with visible water damage inside the home (stains, mold, swollen drywall, rotted wood) or an active leak. The warranty covers investigation, repair of the defective component, and remediation of any damage the leak caused. This is one of the most financially significant warranty periods because water intrusion repairs can run tens of thousands of dollars on a single incident.</p>

      <h2>What the 10-year structural coverage actually includes</h2>

      <p>The 10-year structural period is intentionally narrow. It covers only two things:</p>

      <ol>
        <li>Defects in the load-bearing components of the home that affect structural integrity</li>
        <li>Defects making the home unfit to live in</li>
      </ol>

      <p>Load-bearing components include the foundation, structural framing (floor and roof systems that carry loads), beams, columns, load-bearing walls, and in some cases roof trusses. The defect must be serious enough that it affects the building's structural performance, not just something that looks concerning.</p>

      <p>In practice, 10-year structural claims are rare on homes built by licensed builders. Modern engineering requirements and inspection stops during construction catch most structural issues long before they would manifest as a 10-year warranty claim. When they do occur, they are typically settling-related foundation issues on hillside or complex sites.</p>

      <h2>What is NOT covered</h2>

      <p>Every warranty provider publishes a specific exclusions list in the policy document. Common exclusions across all BC-authorized providers include:</p>

      <ul>
        <li>Normal wear and tear from use over time</li>
        <li>Damage caused by homeowner negligence or failure to maintain the home</li>
        <li>Landscaping, site grading, and anything outside the foundation footprint</li>
        <li>Non-residential structures (depending on policy, may include detached garages or sheds)</li>
        <li>Roads, curbs, driveways, and site services</li>
        <li>Materials supplied by the owner rather than the builder</li>
        <li>Damage caused by others or by natural events: earthquake, flood, fire, windstorm, lightning</li>
        <li>Secondary damage from issues the homeowner knew about but delayed reporting</li>
        <li>Owner-installed modifications, additions, or renovations after original construction</li>
        <li>Appliances (typically covered by manufacturer warranty instead)</li>
      </ul>

      <div class="callout">
        <p class="label">Important</p>
        <p>Read your specific policy document carefully at closing. Each BC Housing-authorized provider has small variations in exclusion wording. The policy, not any summary, is what controls what is covered when you file a claim.</p>
      </div>

      <h2>Who provides the warranty, and does the builder choose?</h2>

      <p>The warranty is issued by a third-party insurer authorized by BC Housing to sell new home warranty insurance in British Columbia. Current authorized providers include:</p>

      <ul>
        <li>Travelers Canada</li>
        <li>National Home Warranty</li>
        <li>Pacific Home Warranty</li>
        <li>WBI Home Warranty</li>
      </ul>

      <p>The licensed builder registers each home with their chosen warranty provider before building permit issuance. The builder pays the warranty premium (typically $1,500 to $4,000+ depending on home value, builder record, and risk profile), and the policy is issued to the homeowner at closing. The homeowner does not choose the provider, the builder does, but all authorized providers must meet the same minimum coverage requirements under the Homeowner Protection Act.</p>

      <h2>How to make a warranty claim</h2>

      <p>The standard claims process:</p>

      <ol>
        <li><strong>Document the issue.</strong> Photos, video, written description of what you observed, when it started, and current condition. Be specific.</li>
        <li><strong>Contact the builder in writing.</strong> Email is best because it creates a dated record. Include the documentation. Request an inspection and remedy.</li>
        <li><strong>Give the builder reasonable time to respond.</strong> Most builders have an internal warranty response window, typically 10 to 30 business days depending on severity.</li>
        <li><strong>If the builder responds and offers repair, document the work.</strong> Keep records of what was done, by whom, and when.</li>
        <li><strong>If the builder does not respond, disputes the claim, or no longer operates, escalate to the warranty provider directly.</strong> Policy documents include claim submission instructions. The provider sends an adjuster to assess.</li>
        <li><strong>If the provider authorizes coverage, repair proceeds.</strong> If the provider denies, the policy includes a dispute resolution process (often an independent arbitrator).</li>
      </ol>

      <p>Document everything in writing from the first observation of the issue. Keep all warranty documents, inspection reports, and photos together in one organized file. If a claim becomes contested, the paper trail is what matters.</p>

      <h2>What happens if the builder goes out of business</h2>

      <p>The warranty continues to protect the homeowner even if the builder dissolves or ceases operations. This is the single most important feature of the BC 2-5-10 structure. Because the warranty is backed by third-party insurance (not the builder's own balance sheet), coverage survives the builder's failure.</p>

      <p>If the builder is no longer available to perform warranty repairs, the warranty provider steps in. The homeowner contacts the provider directly, the provider assesses the claim, and if coverage applies, the provider either authorizes a contractor to perform the repair or reimburses the homeowner for the cost. This protection is especially valuable for the 5-year envelope and 10-year structural periods, which can extend well beyond the operational tenure of some smaller builders.</p>

      <h2>Does the warranty transfer when the home is sold?</h2>

      <p>Yes. The 2-5-10 warranty attaches to the home itself, not the original purchaser. All remaining coverage periods transfer automatically to new owners at resale. A home sold in year 3 of its life still has 2 years of envelope coverage and 7 years of structural coverage remaining when it changes hands.</p>

      <p>Resale homes within the first 5 years especially benefit from this. Buyers of newer homes should always confirm the warranty status at offer and ensure the seller provides all original policy documents at closing. If the policy document is lost, the warranty provider can reissue a copy using the home's registration details.</p>

      <h2>Owner-Builder Exemption: what it costs you</h2>

      <p>BC Housing allows an Owner-Builder Exemption for homeowners who want to act as their own general contractor on a home they will personally occupy (not build-for-sale). The exemption waives the mandatory 2-5-10 warranty, which saves the $1,500 to $4,000+ premium upfront but eliminates the long-term protection.</p>

      <p>Exemption restrictions typically include:</p>

      <ul>
        <li>Only one owner-exempt build allowed per 18 months</li>
        <li>Owner must personally occupy the home (not build-for-sale)</li>
        <li>Restrictions on reselling the home within the first year of occupancy</li>
        <li>No warranty protection for the first 10 years, which can affect resale value</li>
      </ul>

      <p>For most buyers, hiring a licensed builder with mandatory warranty coverage provides significantly stronger long-term protection, especially for the 5-year envelope and 10-year structural periods that would be hardest to self-fund.</p>

      <h2>Why warranty-backed builders typically cost more</h2>

      <p>Licensed builders carry costs that owner-builders avoid: warranty premiums, BC Housing licensing fees, insurance coverage during construction, bonding requirements in some cases, and ongoing training and compliance costs. These costs are built into the fixed-price contract. They are also what gives you access to the warranty protection, the dispute resolution process, and the regulatory oversight that comes with licensing.</p>

      <blockquote style="border-left:3px solid #0085c9;padding:14px 20px;margin:28px 0;background:#f4f9fc;font-style:italic;color:#1a1d21;font-size:16px;line-height:1.65">
        <p style="margin:0">"The 2-5-10 is not just a piece of paper. It is the mechanism that makes a BC licensed builder different from an unlicensed one. If something goes wrong 7 years after move-in and we are still in business, we fix it. If we are not, the warranty provider does. That is the trade-off homeowners should understand when comparing bids." Jas Sidhu, Owner, Palermo Homes</p>
      </blockquote>

      <h2>What to confirm about warranty before signing a contract</h2>

      <ol>
        <li>Confirm the builder is BC Housing-licensed and ask for the license number</li>
        <li>Ask which warranty provider the builder uses (Travelers, National, Pacific, WBI)</li>
        <li>Confirm the warranty is included in the quoted price (it typically is on licensed builds)</li>
        <li>Ask when during construction the New Home Registration is submitted (should be before building permit issuance)</li>
        <li>Ask for a sample warranty policy document before signing so you can read the specific exclusions</li>
        <li>Confirm the builder has had no recent warranty disputes or BC Housing disciplinary actions (public searchable on BC Housing website)</li>
      </ol>

      <p class="footer-note">This guide reflects current 2-5-10 New Home Warranty requirements in British Columbia as of 2026 and is based on BC Housing published materials and the Homeowner Protection Act. Specific coverage terms, exclusions, and claim procedures vary by warranty provider and policy. Always read the specific policy document issued with your home. Nothing in this guide constitutes legal advice.</p>
    </div>
  </section>

  <section class="guide-about">
    <div class="wrap">
      <h2>About Palermo Homes</h2>
      <p>Palermo Homes is a BC Housing Licensed Residential Builder (License 42812, Corporate Registration BC1017682) based in West Kelowna. Every custom home we build is registered with BC Housing and automatically covered by the mandatory 2-5-10 New Home Warranty. We have been building across the Central Okanagan for over 15 years and maintain long-term warranty relationships with our completed homes.</p>
      <p>We build in <a href="/service-areas/kelowna/">Kelowna</a>, <a href="/service-areas/west-kelowna/">West Kelowna</a>, <a href="/service-areas/lake-country/">Lake Country</a>, <a href="/service-areas/peachland/">Peachland</a>, <a href="/service-areas/penticton/">Penticton</a>, <a href="/service-areas/vernon/">Vernon</a>, and select Lower Mainland communities.</p>
      <p>For how warranty fits with the contract structure, see our <a href="/guides/fixed-price-vs-cost-plus-custom-home-kelowna/">fixed-price vs cost-plus guide</a>. For how lenders view warranty on construction mortgages, see the <a href="/guides/financing-custom-home-bc/">financing guide</a>. For how to verify a licensed builder before signing anything, see <a href="/guides/how-to-choose-custom-home-builder-kelowna/">how to choose a Kelowna builder</a>.</p>
    </div>
  </section>

  <section class="guide-cta">
    <div class="wrap">
      <h2>Planning a custom home build in the Okanagan?</h2>
      <p>Every Palermo build is registered with BC Housing and covered by the mandatory 2-5-10 warranty from day one.</p>
      <a class="btn" href="/contact/">Book a consultation</a>
    </div>
  </section>
</div>
"""


OG_IMAGE = f"{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-02.jpg"
OG_TITLE = "BC's 2-5-10 New Home Warranty Explained: What's Covered, What Isn't, and How to Claim"


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    html = re.sub(r"/\* ==== GUIDE-WARRANTY CSS START ==== \*/.*?/\* ==== GUIDE-WARRANTY CSS END ==== \*/", "", html, flags=re.DOTALL)
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

    out = SITE / "guides" / "bc-2-5-10-new-home-warranty-explained" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built Guide #10: BC's 2-5-10 New Home Warranty Explained.")
