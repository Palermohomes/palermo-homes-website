"""Build /guides/financing-custom-home-bc/
Guide #9 - "Financing a Custom Home in BC."
Targets high-intent money queries: "construction mortgage bc", "custom home
financing bc", "progress draw mortgage", "construction loan canada",
"builders lien act bc holdback".
Positioned as educator, not lender. Builders Lien Act section is unique
BC-specific content that most national guides miss.
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
PAGE_URL = f"{BIZ_URL}/guides/financing-custom-home-bc/"
PUBLISH_DATE = "2026-10-13"
MODIFIED_DATE = datetime.date.today().isoformat()

CSS_START = "/* ==== GUIDE-FINANCING CSS START ==== */"
CSS_END = "/* ==== GUIDE-FINANCING CSS END ==== */"

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
html body #et-main-area .guide-body .draw-row{{display:grid;grid-template-columns:50px 1fr auto;gap:16px;padding:16px 0;border-bottom:1px solid #ece8df;align-items:center}}
html body #et-main-area .guide-body .draw-row:last-child{{border-bottom:0}}
html body #et-main-area .guide-body .draw-row .num{{width:40px;height:40px;background:#f4f9fc;border:1px solid #cfe6f1;color:#0085c9;font-weight:700;font-size:15px;display:flex;align-items:center;justify-content:center;border-radius:50%}}
html body #et-main-area .guide-body .draw-row .label{{font-size:15px;color:#1a1d21;font-weight:600;margin:0}}
html body #et-main-area .guide-body .draw-row .desc{{font-size:14px;color:#6a7078;line-height:1.5;margin:4px 0 0}}
html body #et-main-area .guide-body .draw-row .pct{{font-size:18px;color:#0085c9;font-weight:600;letter-spacing:-0.01em}}
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
  html body #et-main-area .guide-body .draw-row{{grid-template-columns:40px 1fr;gap:12px}}
  html body #et-main-area .guide-body .draw-row .pct{{grid-column:2;font-size:16px;margin:4px 0 0}}
  html body #et-main-area .guide-body table{{font-size:14px}}
  html body #et-main-area .guide-body table th,html body #et-main-area .guide-body table td{{padding:8px 10px}}
}}
{CSS_END}
"""

FAQ_ITEMS = [
    {
        "q": "What is a construction mortgage in BC?",
        "a": "A construction mortgage, sometimes called a progress draw mortgage or builder's mortgage, is a loan designed specifically to finance a new home build. Unlike a conventional mortgage where you receive the full amount at closing, a construction mortgage releases funds in stages (called draws) as the home is built, with each draw tied to a completed construction milestone. The loan is short-term, typically 12 to 18 months, and you make interest-only payments on the amounts actually advanced. Once construction is complete and the occupancy permit is issued, the construction mortgage is converted to or replaced by a traditional residential mortgage."
    },
    {
        "q": "How much down payment do I need for a construction mortgage in BC?",
        "a": "Most BC construction mortgages require 20% to 25% down, and some lenders require up to 35% depending on the project, borrower profile, and lender appetite. This is higher than the 5% minimum for insured residential mortgages because lenders carry more risk financing a project in progress. If you already own the lot, the lot value typically counts toward your down payment, which can reduce the cash needed upfront. For a $1.5 million custom build in Kelowna, expect to need $300,000 to $375,000 in equity (lot plus cash) before most lenders will fund the construction mortgage."
    },
    {
        "q": "How does a progress draw schedule work on a BC custom home?",
        "a": "A typical BC construction mortgage has 4 to 5 draws, each tied to a construction milestone. A common schedule: Draw 1 (approximately 15%) at site preparation and foundation complete, Draw 2 (approximately 25%) at framing complete, Draw 3 (approximately 25%) at lock-up (weather-tight shell with rough mechanicals), Draw 4 (approximately 20%) at interior finishing substantially complete, and Draw 5 (approximately 15%) at final inspection and occupancy. Before each draw is released, an inspector or appraiser visits the site to verify the work has been completed. BC's Builders Lien Act requires a 10% holdback on each draw, released after a minimum 45-day holding period after substantial completion."
    },
    {
        "q": "What is the BC Builders Lien Act holdback?",
        "a": "The BC Builders Lien Act requires the owner (or the owner's lender on behalf of the owner) to hold back 10% of every progress payment made to the builder throughout construction. The holdback protects subcontractors and material suppliers who may be owed money by the general contractor; if any party files a lien, the holdback is used to settle the claim before being released to the builder. The holdback is released after a 55-day period following substantial completion (45-day lien period plus a few days for the lender's processing), provided no liens have been filed. This is a BC-specific rule that most national construction financing guides overlook."
    },
    {
        "q": "What is the difference between a construction-to-permanent mortgage and a stand-alone construction loan?",
        "a": "A construction-to-permanent (CTP) mortgage combines the construction loan and the end mortgage into a single loan that converts automatically from draw-mode to amortizing-mortgage-mode once construction is complete. One application, one closing, one set of legal fees. A stand-alone construction loan is a short-term loan that funds construction only; once the home is complete, you pay it off by taking out a separate traditional mortgage. Stand-alone loans sometimes offer slightly better construction-phase rates but add a second round of legal fees and underwriting at the end. For most custom home buyers in BC, construction-to-permanent is the simpler and lower-total-cost option."
    },
    {
        "q": "What interest rate should I expect on a BC construction mortgage?",
        "a": "Construction mortgage rates in Canada typically run 1% to 3% above conventional residential mortgage rates due to the elevated risk profile. Interest is charged only on amounts actually drawn, not on the full approved amount. During a typical 12 to 15 month build, interest costs on the drawn portion accumulate month over month as more funds are released. On a $1.5 million build with a staggered draw schedule, total interest paid during construction commonly runs $25,000 to $55,000 depending on rates, draw timing, and lot equity. Interest-only payments during construction are made from the borrower's own funds, not from the loan."
    },
    {
        "q": "What documents does a lender need to approve a construction mortgage in BC?",
        "a": "A typical BC construction mortgage application requires: proof of income (T4s, Notice of Assessment, pay stubs, self-employed documentation), credit report, bank statements showing down payment source, lot title or purchase agreement, builder's fixed-price construction contract, detailed cost breakdown, architectural plans and engineering stamps, building permit (or confirmation of permit application), BC Energy Step Code Pre-Construction Report, BC Housing Home Warranty confirmation (New Home Registration or Owner-Builder Exemption), and an as-if-complete appraisal from a certified appraiser the lender selects. Most lenders will not fund without a BC-licensed residential builder on the contract or an approved Owner-Builder Exemption."
    },
    {
        "q": "Can I get a construction mortgage if I plan to be an owner-builder in BC?",
        "a": "Yes, but with more lender scrutiny. Owner-builders in BC must apply for and receive an Owner-Builder Exemption from BC Housing (which waives the mandatory 2-5-10 Home Warranty). Lenders view owner-builder projects as higher risk because there is no licensed general contractor managing cost and schedule. Expect higher down payment requirements (often 25% to 35%+), potentially higher interest rates, more conservative appraisals, and more frequent inspection requirements. Some lenders decline owner-builder construction loans entirely. Working with a licensed builder like Palermo Homes (BC Housing License 42812) typically results in better financing terms."
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
        "headline": "Financing a Custom Home in BC: Construction Mortgages, Progress Draws, and Builders Lien Act Holdback",
        "description": "How construction financing actually works in BC. Progress draw schedules, the Builders Lien Act 10% holdback, down payment requirements, construction-to-permanent vs stand-alone loans, interest costs, and what lenders need before approval.",
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
            {"@type": "Thing", "name": "Construction Mortgage"},
            {"@type": "Thing", "name": "Custom Home Financing"},
            {"@type": "Thing", "name": "Builders Lien Act"},
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
            {"@type": "ListItem", "position": 3, "name": "Financing a Custom Home in BC", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "Financing a Custom Home in BC: Construction Mortgages, Progress Draws, and Builders Lien Act Holdback",
        "description": "A plain-English guide to custom home financing in BC: construction mortgages, progress draws, the Builders Lien Act 10% holdback, down payment, interest costs, and documents required.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, article, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Financing a Custom Home in BC: Construction Mortgages Explained | Palermo Homes"
META_DESC = "How custom home construction financing works in BC. Progress draws, Builders Lien Act 10% holdback, down payment, interest costs, and lender requirements."
CANONICAL = PAGE_URL

MAIN_HTML = """
<div class="guide">
  <section class="guide-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">&middot;</span><a href="/guides/">Guides</a><span class="sep">&middot;</span>Financing a Custom Home in BC</p>
      <h1>Financing a Custom Home in BC: Construction Mortgages, Progress Draws, and the Builders Lien Act Holdback</h1>
      <p class="sub">How custom home construction financing actually works in British Columbia. Progress draw schedules, the BC-specific 10% holdback requirement, down payment realities, construction-to-permanent vs stand-alone loan structures, and what lenders need to see before approval.</p>
      <p class="meta">Published October 2026 &middot; By <a href="/about/jas-sidhu/" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1">Jas Sidhu</a>, Owner of Palermo Homes &middot; Custom Home Builder in West Kelowna, BC &middot; <strong>Educational guide only, not financial advice. Consult a licensed mortgage broker or lender for terms specific to your situation.</strong></p>
    </div>
  </section>

  <section class="guide-body">
    <div class="wrap">
      <div class="lede">
        <p>A BC construction mortgage releases funds in 4 to 5 stages (draws) as construction progresses, requires 20% to 25% down (sometimes more), carries interest rates 1% to 3% above conventional mortgages, and runs 12 to 18 months before converting to or being replaced by a permanent mortgage. BC's Builders Lien Act requires a 10% holdback on every draw payment, released about 55 days after substantial completion. Lot equity typically counts toward down payment, and most lenders require a BC-licensed residential builder on the contract.</p>
      </div>

      <figure style="margin:28px 0 32px;padding:0">
        <img src="/wp-content/uploads/2025/12/Cabernet-02.jpg" alt="A completed Palermo Homes custom build on Cabernet Way in West Kelowna, the kind of project that requires a BC construction mortgage structured as progress draws" style="width:100%;height:auto;display:block;border-radius:4px" loading="lazy" width="1200" height="800">
        <figcaption style="font-size:13px;color:#6a7078;margin:10px 0 0;line-height:1.5;font-style:italic">A completed custom home on Cabernet Way, West Kelowna. Built using a standard 5-draw construction mortgage structure through a BC-based lender.</figcaption>
      </figure>

      <p>Financing is often the most confusing part of planning a custom home for buyers who have only ever bought resale properties. A traditional mortgage lands the full purchase price in one closing. A construction mortgage releases funds in stages tied to physical progress, with inspectors verifying the work before each release and a BC-specific holdback requirement that most national financing guides miss entirely.</p>

      <p>This guide walks through how construction financing actually works in British Columbia: the draw schedule, the 10% Builders Lien Act holdback, down payment realities, loan structure choices, interest costs during the build, and the documentation lenders require. It is written as an educator's walkthrough, not financial advice. For specific numbers and terms, work with a licensed BC mortgage broker or your lender.</p>

      <h2>How a construction mortgage is different from a regular mortgage</h2>

      <p>A traditional residential mortgage closes on an existing property. The lender appraises the home as it stands today, and the full loan amount is advanced at closing. The borrower starts making principal and interest payments immediately.</p>

      <p>A construction mortgage closes before the home exists. The lender appraises the home on an "as-if-complete" basis using the design drawings, specification sheet, and builder contract. Funds are advanced in stages as the home is built. The borrower makes interest-only payments on the amounts actually drawn, not on the full approved amount. Once construction is complete and the occupancy permit is issued, the construction mortgage converts to or is replaced by a conventional amortizing mortgage.</p>

      <table>
        <thead>
          <tr><th></th><th>Traditional residential mortgage</th><th>Construction mortgage</th></tr>
        </thead>
        <tbody>
          <tr><td>Advance structure</td><td>Full amount at closing</td><td>Staged draws tied to construction milestones</td></tr>
          <tr><td>Payment type</td><td>Principal + interest from day 1</td><td>Interest-only on drawn amounts during build</td></tr>
          <tr><td>Term</td><td>Typically 1 to 10 years (fixed or variable)</td><td>12 to 18 months, converts or renews at completion</td></tr>
          <tr><td>Minimum down payment</td><td>5% (insured) to 20% (uninsured)</td><td>20% to 35%+</td></tr>
          <tr><td>Interest rate</td><td>Current prime +/- lender spread</td><td>Conventional rate + 1% to 3% premium</td></tr>
          <tr><td>Appraisal basis</td><td>Current market value of existing home</td><td>As-if-complete value based on plans + specs</td></tr>
          <tr><td>Inspections required</td><td>None during the loan</td><td>Draw inspection before each advance</td></tr>
        </tbody>
      </table>

      <h2>The typical BC progress draw schedule</h2>

      <p>Most BC construction mortgages use a 4 or 5 draw schedule tied to defined construction milestones. The exact percentages and milestones vary by lender, but the common structure looks like this:</p>

      <div class="draw-row">
        <div class="num">1</div>
        <div>
          <p class="label">Site preparation + foundation complete</p>
          <p class="desc">Excavation, foundation pour, waterproofing, perimeter drainage, backfill, and underslab services complete. Draw inspector confirms work.</p>
        </div>
        <div class="pct">~15%</div>
      </div>
      <div class="draw-row">
        <div class="num">2</div>
        <div>
          <p class="label">Framing complete</p>
          <p class="desc">Structural framing (floors, walls, roof), roof sheathing, windows and exterior doors installed. House is enclosed to the elements.</p>
        </div>
        <div class="pct">~25%</div>
      </div>
      <div class="draw-row">
        <div class="num">3</div>
        <div>
          <p class="label">Lock-up (weather-tight shell)</p>
          <p class="desc">Exterior finished (siding or stone), roofing complete, insulation and vapour barrier installed, rough mechanical / electrical / plumbing complete.</p>
        </div>
        <div class="pct">~25%</div>
      </div>
      <div class="draw-row">
        <div class="num">4</div>
        <div>
          <p class="label">Interior substantially complete</p>
          <p class="desc">Drywall, flooring, cabinetry, tile, trim, and most fixtures installed. Interior painting complete.</p>
        </div>
        <div class="pct">~20%</div>
      </div>
      <div class="draw-row">
        <div class="num">5</div>
        <div>
          <p class="label">Final completion + occupancy</p>
          <p class="desc">Final inspection passed, occupancy permit issued, exterior and landscape finishing complete.</p>
        </div>
        <div class="pct">~15%</div>
      </div>

      <p>Before each draw is released, the lender sends an inspector or appraiser to the site to verify the work has been completed to the stated milestone. The inspector files a draw report, and the funds are released from the lender to the borrower (or directly to the builder, depending on the arrangement) within a few business days.</p>

      <h2>The BC Builders Lien Act 10% holdback</h2>

      <div class="callout">
        <p class="label">BC-specific rule</p>
        <p>Section 4 of BC's Builders Lien Act requires the owner (or the owner's lender on behalf of the owner) to hold back 10% of every progress payment made to the builder throughout construction. This holdback protects subcontractors and material suppliers who may have unpaid claims. The holdback is released approximately 55 days after substantial completion, provided no liens are filed.</p>
      </div>

      <p>In practical terms, on a $1.5 million construction mortgage with the typical 5-draw structure, the builder actually receives $150,000 less than the gross draw amounts across the build. That $150,000 sits in holdback until the lien period expires. If a subcontractor files a lien during the 45-day lien period after substantial completion, the holdback is used to settle the claim before being released.</p>

      <p>This is a BC-specific requirement that most national construction financing guides either overlook or misdescribe. It affects how the builder structures cash flow, how trades are paid, and in rare cases how long the final draw takes to fully release. A licensed BC builder is familiar with the holdback mechanics and will not be surprised by them. An out-of-province contractor or an owner-builder without construction experience often is.</p>

      <h2>Down payment realities</h2>

      <p>Most BC construction mortgages require 20% to 25% down. Some lenders require up to 35% depending on the project profile, borrower credit, and lender appetite for the specific build type (standard custom home vs hillside vs unusual design vs owner-builder).</p>

      <p>Lot equity counts toward down payment. If you own a lot free and clear worth $500,000 and the total project value is $2,000,000, your lot equity represents 25% of the project. Many lenders will treat that as the down payment and lend the remaining $1,500,000 as the construction mortgage.</p>

      <p>If you still have a mortgage on the lot, the lender will consider the net equity. A $500,000 lot with a $200,000 lot mortgage leaves $300,000 of equity, which may or may not be sufficient depending on lender requirements.</p>

      <p>For buyers purchasing both the lot and funding construction, the down payment is typically a combination of lot purchase cash and additional cash held in reserve. Lenders want to see the down payment is actually in the borrower's bank account at the time of application, not borrowed from another source.</p>

      <h2>Construction-to-permanent vs stand-alone construction loans</h2>

      <h3>Construction-to-permanent (CTP) mortgage</h3>

      <p>A CTP mortgage combines the construction loan and the end mortgage into a single loan. One application, one closing, one set of legal fees. The loan starts in construction mode (interest-only draws), and automatically converts to standard amortizing mortgage mode once the home is complete and the final draw is released. This is the simpler and typically lower-total-cost option for most custom home buyers in BC.</p>

      <h3>Stand-alone construction loan</h3>

      <p>A stand-alone construction loan is a short-term loan that funds only the construction phase. Once the home is complete, the borrower takes out a separate traditional mortgage (potentially from a different lender) to pay off the construction loan. Stand-alone loans sometimes offer slightly better construction-phase rates but require a second round of underwriting, legal fees, and appraisal at the end. They can make sense for borrowers who want to shop multiple lenders for the end mortgage or who expect their borrower profile to change significantly between the start and end of construction.</p>

      <h2>Interest costs during construction</h2>

      <p>Construction mortgage interest is charged only on amounts actually drawn, not on the full approved amount. During a staggered 12 to 15 month build, interest costs accumulate month over month as more funds are released.</p>

      <p>A rough estimate on a $1.5 million construction mortgage with a 5-draw schedule, average interest rate of 7.5%, and a 13 month build:</p>

      <ul>
        <li>Average drawn balance over the build (weighted): approximately $750,000</li>
        <li>Interest at 7.5% on $750,000 over 13 months: approximately $61,000</li>
      </ul>

      <p>Actual interest costs vary significantly with the actual rate at the time, draw timing, project duration, and whether lot equity is used to reduce the drawn amounts. Interest-only payments during construction are made from the borrower's own funds (not from the loan), so budget cash flow accordingly. Some lenders allow interest to be capitalized into the loan, with interest costs added to principal, though this reduces the available construction budget.</p>

      <h2>Documents a lender will ask for</h2>

      <p>A typical BC construction mortgage application requires:</p>

      <ul>
        <li><strong>Income documentation:</strong> T4s, Notice of Assessment, pay stubs, self-employed financial statements, T1 Generals</li>
        <li><strong>Credit report:</strong> pulled by the lender</li>
        <li><strong>Bank statements:</strong> showing down payment source and that funds are seasoned</li>
        <li><strong>Lot title:</strong> if owned, or purchase agreement if being purchased concurrently</li>
        <li><strong>Builder contract:</strong> fixed-price construction contract with a BC-licensed residential builder</li>
        <li><strong>Detailed cost breakdown:</strong> by category (foundation, framing, mechanical, finishes, etc.)</li>
        <li><strong>Architectural and structural drawings:</strong> stamped by qualified professionals</li>
        <li><strong>Building permit or confirmation of permit application</strong></li>
        <li><strong>BC Energy Step Code Pre-Construction Report:</strong> from a qualified Energy Advisor</li>
        <li><strong>BC Housing Home Warranty confirmation:</strong> New Home Registration from the licensed builder, or Owner-Builder Exemption if applicable</li>
        <li><strong>Insurance confirmation:</strong> course-of-construction insurance in place</li>
      </ul>

      <p>The lender's appraiser will perform an as-if-complete appraisal based on the plans, specifications, and local market data to confirm the completed home will be worth at least the loan amount plus the down payment. If the appraisal comes in below expectations, the loan amount may be reduced or additional down payment required.</p>

      <h2>Why most lenders prefer a licensed BC builder</h2>

      <p>Most lenders will not fund a construction mortgage without a BC-licensed residential builder on the contract (or an approved Owner-Builder Exemption). The reasons:</p>

      <ul>
        <li>Licensed builders carry mandatory BC Housing 2-5-10 Home Warranty, protecting the lender's collateral post-completion</li>
        <li>Licensed builders are subject to BC Housing oversight and must meet experience and financial requirements to maintain their license</li>
        <li>Licensed builders typically have established trade relationships, better cost control, and faster schedules, reducing project risk</li>
        <li>Fixed-price contracts with licensed builders provide the lender with a reliable total cost figure to appraise against</li>
      </ul>

      <p><strong>Palermo Homes is BC Housing Licensed Residential Builder Number 42812 and holds BC Corporate Registration BC1017682.</strong> Our contracts, warranty registrations, and documentation are structured to support lender due diligence and typically clear construction mortgage approval conditions without issue.</p>

      <h2>Owner-builder financing in BC</h2>

      <p>Owner-builders in BC must apply for and receive an Owner-Builder Exemption from BC Housing (which waives the mandatory 2-5-10 warranty). Lenders view owner-builder projects as higher risk because there is no licensed general contractor managing cost and schedule. In practice, owner-builder construction loans typically require:</p>

      <ul>
        <li>Higher down payment, often 25% to 35%+</li>
        <li>Potentially higher interest rate premium</li>
        <li>More conservative appraisal</li>
        <li>More frequent inspections</li>
        <li>Detailed personal construction experience documentation</li>
      </ul>

      <p>Some lenders decline owner-builder construction loans entirely. For most buyers, working with a licensed builder results in better financing terms, fewer surprises during the build, and the 2-5-10 warranty protection that follows the home after completion.</p>

      <h2>Timeline: when financing happens relative to the build</h2>

      <p>Here is how construction financing sequences against the overall custom home build phases covered in our <a href="/guides/custom-home-building-process-kelowna/">process guide</a>:</p>

      <table>
        <thead>
          <tr><th>Project phase</th><th>Financing step</th></tr>
        </thead>
        <tbody>
          <tr><td>Initial consultation</td><td>Rough budget range confirmed; initial mortgage broker conversation</td></tr>
          <tr><td>Lot evaluation</td><td>Lot purchase financing or lot equity confirmation</td></tr>
          <tr><td>Design (early)</td><td>Mortgage pre-approval conversation to confirm borrowing capacity</td></tr>
          <tr><td>Design (late) + permit prep</td><td>Formal construction mortgage application submitted with full package</td></tr>
          <tr><td>Permit issuance</td><td>Mortgage approval conditions cleared, financing commits</td></tr>
          <tr><td>Site prep + foundation</td><td>Draw 1 released after inspection</td></tr>
          <tr><td>Framing</td><td>Draw 2 released</td></tr>
          <tr><td>Lock-up</td><td>Draw 3 released</td></tr>
          <tr><td>Interior finishing</td><td>Draw 4 released</td></tr>
          <tr><td>Final inspections + occupancy</td><td>Draw 5 released; CTP mortgage converts to amortizing; or stand-alone loan paid off by new mortgage</td></tr>
          <tr><td>55 days post-completion</td><td>Builders Lien Act holdback released</td></tr>
        </tbody>
      </table>

      <h2>How to prepare before applying</h2>

      <ol>
        <li>Clarify your budget range before builder conversations. Lenders will tell you what you qualify for; a mortgage broker specializing in construction loans can give you specific numbers.</li>
        <li>Keep down payment funds seasoned in a single account for 90+ days before application.</li>
        <li>Confirm lot ownership status and any existing mortgage on the lot.</li>
        <li>Shop lenders through a mortgage broker experienced in BC construction loans. Different banks and credit unions have very different appetites for custom construction.</li>
        <li>Have the builder provide a fixed-price contract with detailed cost breakdown before the mortgage application.</li>
        <li>Confirm your BC Housing New Home Registration (via the builder) before submitting the mortgage application.</li>
        <li>Factor construction-phase interest into your budget as a separate line item.</li>
      </ol>

      <h2>Common mistakes to avoid</h2>

      <ol>
        <li><strong>Applying for a construction mortgage without a fixed-price contract.</strong> Lenders will not fund without a clear total project cost. See our <a href="/guides/fixed-price-vs-cost-plus-custom-home-kelowna/">fixed-price vs cost-plus guide</a>.</li>
        <li><strong>Underestimating the Builders Lien Act holdback effect on builder cash flow.</strong> The builder is funding 10% of each payment until the holdback releases.</li>
        <li><strong>Forgetting to budget interest-only payments during construction.</strong> On a $1.5 million build, this can be $4,000 to $5,000+ per month at peak draw.</li>
        <li><strong>Changing project scope significantly after mortgage approval.</strong> Lenders approve against a specific plan and contract; major changes trigger re-underwriting.</li>
        <li><strong>Hiring an unlicensed builder.</strong> Most BC lenders decline, and the ones that approve impose significant premium rates.</li>
      </ol>

      <p class="footer-note">This guide is educational only and does not constitute financial or lending advice. Specific loan terms, rates, down payment requirements, and documentation vary by lender, borrower profile, project type, and current market conditions. Consult a licensed BC mortgage broker or lender for terms specific to your situation. All interest rate examples and cost estimates are illustrative and reflect general market conditions as of 2026. For current rates and terms, speak with a qualified mortgage professional.</p>
    </div>
  </section>

  <section class="guide-about">
    <div class="wrap">
      <h2>About Palermo Homes</h2>
      <p>Palermo Homes is a custom home builder based in West Kelowna, BC (BC Corporate Registration BC1017682, BC Housing Licensed Residential Builder Number 42812). Our contracts, warranty registrations, cost breakdowns, and construction documentation are structured to support construction mortgage approval and draw administration with BC lenders. We work regularly with mortgage brokers and lending teams across the Central Okanagan.</p>
      <p>We build in <a href="/service-areas/kelowna/">Kelowna</a>, <a href="/service-areas/west-kelowna/">West Kelowna</a>, <a href="/service-areas/lake-country/">Lake Country</a>, <a href="/service-areas/peachland/">Peachland</a>, <a href="/service-areas/penticton/">Penticton</a>, <a href="/service-areas/vernon/">Vernon</a>, and select Lower Mainland communities.</p>
      <p>For the cost side of the equation, see our <a href="/guides/custom-home-cost-kelowna/">custom home cost guide</a>. For how long the project runs across all draws, see the <a href="/guides/how-long-to-build-custom-home-kelowna/">timeline guide</a>. For the step-by-step process financing supports, see the <a href="/guides/custom-home-building-process-kelowna/">process guide</a>. For contract structure (which lenders care about), see the <a href="/guides/fixed-price-vs-cost-plus-custom-home-kelowna/">fixed-price vs cost-plus guide</a>.</p>
    </div>
  </section>

  <section class="guide-cta">
    <div class="wrap">
      <h2>Planning a custom home build and need lender-ready documentation?</h2>
      <p>Our contracts, cost breakdowns, and warranty registrations are structured to clear construction mortgage approval conditions without surprises.</p>
      <a class="btn" href="/contact/">Book a consultation</a>
    </div>
  </section>
</div>
"""


OG_IMAGE = f"{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-02.jpg"
OG_TITLE = "Financing a Custom Home in BC: Construction Mortgages, Progress Draws, and Builders Lien Act Holdback"


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    html = re.sub(r"/\* ==== GUIDE-FINANCING CSS START ==== \*/.*?/\* ==== GUIDE-FINANCING CSS END ==== \*/", "", html, flags=re.DOTALL)
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

    out = SITE / "guides" / "financing-custom-home-bc" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built Guide #9: Financing a Custom Home in BC.")
