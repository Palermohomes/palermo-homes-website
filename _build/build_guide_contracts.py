"""Build /guides/fixed-price-vs-cost-plus-custom-home-kelowna/
Guide #4 - "Fixed-Price vs Cost-Plus Contracts for Custom Homes in BC."
Targets money queries: "fixed price contract custom home", "cost plus contract bc",
"custom home contract types kelowna", "fixed price vs cost plus construction".
Full E-E-A-T stack: Person-schema authorship (Jas), FAQPage, Article, Breadcrumb.
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
PAGE_URL = f"{BIZ_URL}/guides/fixed-price-vs-cost-plus-custom-home-kelowna/"
PUBLISH_DATE = "2026-10-06"
MODIFIED_DATE = datetime.date.today().isoformat()
ISO_MODIFIED = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

CSS_START = "/* ==== GUIDE-CONTRACTS CSS START ==== */"
CSS_END = "/* ==== GUIDE-CONTRACTS CSS END ==== */"

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
html body #et-main-area .guide-body table th{{text-align:left;padding:12px 14px;background:#f4f9fc;border:1px solid #e2ddd0;color:#1a1d21;font-weight:600;font-size:14px;vertical-align:top}}
html body #et-main-area .guide-body table td{{padding:12px 14px;border:1px solid #e2ddd0;color:#3a4048;line-height:1.55;vertical-align:top}}
html body #et-main-area .guide-body table td strong{{color:#1a1d21;font-weight:600}}
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
  html body #et-main-area .guide-body table th,html body #et-main-area .guide-body table td{{padding:9px 10px}}
}}
{CSS_END}
"""

FAQ_ITEMS = [
    {
        "q": "What is the difference between fixed-price and cost-plus contracts for custom homes in BC?",
        "a": "A fixed-price contract commits the builder to a specific total price for defined scope, protecting the homeowner from cost overruns. A cost-plus contract bills the homeowner for actual material and labour costs plus a builder markup (typically 15 to 25 percent), exposing the homeowner to open-ended cost escalation. Fixed-price is standard for most residential custom builds in Kelowna and the Okanagan and is strongly preferred for budget predictability."
    },
    {
        "q": "Which is better for a custom home in Kelowna, fixed-price or cost-plus?",
        "a": "For most Kelowna custom home buyers, fixed-price is better. It protects you from cost overruns, forces the builder to scope the project in detail upfront, and gives you a defensible budget to make financing decisions on. Cost-plus can make sense for very large, complex, or unusual builds where scope cannot be fully defined in advance, but these are the exception, not the rule."
    },
    {
        "q": "How does a fixed-price custom home contract work in BC?",
        "a": "A fixed-price custom home contract in BC specifies the total price, the detailed scope of work, finish allowances for items like tile and cabinets, the payment draw schedule, timeline, and the change order process. The builder commits to the price for the defined scope. If the homeowner requests additions or upgrades during construction, those are handled through written change orders with their own pricing. Any items subject to variable cost (allowances) are capped at the contracted amount, with any overage charged separately."
    },
    {
        "q": "What are allowances in a fixed-price construction contract?",
        "a": "Allowances are budget line items for materials where the homeowner has not yet made a final selection. Typical allowance categories include tile, plumbing fixtures, lighting, appliances, flooring, and cabinetry. The contract specifies a dollar amount for each category. If the homeowner selects products within the allowance, there is no change to the contract. If they select higher-priced items, the difference is added as a change order. Transparent allowances protect both the homeowner and the builder from mid-build price surprises."
    },
    {
        "q": "Why do some builders refuse fixed-price contracts?",
        "a": "Some builders refuse fixed-price contracts because fixed-price shifts cost risk from the homeowner to the builder. A builder who cannot or will not accurately scope and price a project in advance avoids fixed-price for self-protection. Legitimate reasons to prefer cost-plus exist for very unusual projects where scope genuinely cannot be defined, but for a standard residential custom build in the Okanagan, resistance to fixed-price is a yellow flag that warrants investigation."
    },
    {
        "q": "What is a reasonable builder markup on a cost-plus contract?",
        "a": "Builder markup on cost-plus contracts in BC typically ranges from 15 to 25 percent of hard costs (materials and labour). Below 15 percent is unusually low and may hide risk. Above 25 percent should prompt questions about what services justify the higher margin. On a $2 million build, the difference between 15 percent and 25 percent markup is $200,000 of pure margin, which is why cost-plus is risky without strict oversight."
    },
    {
        "q": "Can a custom home contract in BC be partially fixed-price?",
        "a": "Yes. Some builders use hybrid contracts that fix the base construction price but leave specific allowance categories (such as interior finishes) as cost-plus or time-and-materials with a cap. This hybrid approach can work when the homeowner wants flexibility on finishes but certainty on the core construction. The important detail is that any cost-plus portion must have a clear cap and transparent reporting, otherwise it reintroduces the cost-overrun risk fixed-price was meant to prevent."
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
        "headline": "Fixed-Price vs Cost-Plus Contracts for Custom Homes in BC: 2026 Guide",
        "description": "A plain-English comparison of fixed-price and cost-plus construction contracts for custom homes in Kelowna and BC. Which protects you, when each makes sense, and how to spot the risks in both.",
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
            {"@type": "Thing", "name": "Construction Contracts"},
            {"@type": "Thing", "name": "Fixed-Price Contract"},
            {"@type": "Thing", "name": "Cost-Plus Contract"},
            {"@type": "Place", "name": "Kelowna, BC"},
            {"@type": "Place", "name": "British Columbia"},
        ],
    }

    breadcrumbs = {
        "@type": "BreadcrumbList",
        "@id": f"{PAGE_URL}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BIZ_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{BIZ_URL}/guides/"},
            {"@type": "ListItem", "position": 3, "name": "Fixed-Price vs Cost-Plus Contracts", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "Fixed-Price vs Cost-Plus Contracts for Custom Homes in BC: 2026 Guide",
        "description": "A plain-English comparison of fixed-price and cost-plus construction contracts for custom homes in Kelowna and BC.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, article, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Fixed-Price vs Cost-Plus Home Contracts BC | Palermo Homes"
META_DESC = "A plain-English comparison of fixed-price and cost-plus construction contracts for custom homes in Kelowna and BC."
CANONICAL = PAGE_URL
OG_IMAGE = f"{BIZ_URL}/wp-content/uploads/2025/12/homepage3.jpg"
OG_TITLE = "Fixed-Price vs Cost-Plus Contracts for Custom Homes in BC: 2026 Guide"
READING_TIME = "9 minutes"

MAIN_HTML = """
<div class="guide">
  <section class="guide-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">&middot;</span><a href="/guides/">Guides</a><span class="sep">&middot;</span>Fixed-Price vs Cost-Plus Contracts</p>
      <h1>Fixed-Price vs Cost-Plus Contracts for Custom Homes in BC: A 2026 Guide</h1>
      <p class="sub">A plain-English comparison of the two main construction contract types for custom homes in Kelowna and the Okanagan, which one protects you from cost overruns, when each makes sense, and the risks hidden in both.</p>
      <p class="meta">Published October 2026 &middot; By <a href="/about/jas-sidhu/" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1">Jas Sidhu</a>, Owner of Palermo Homes &middot; Custom Home Builder in West Kelowna, BC</p>
    </div>
  </section>

  <section class="guide-body">
    <div class="wrap">
      <div class="lede">
        <p>A fixed-price custom home contract commits the builder to a specific total price for defined scope, protecting the homeowner from cost overruns. A cost-plus contract bills the homeowner for actual material and labour costs plus a builder markup (typically 15 to 25 percent), with no price ceiling. For most Kelowna custom builds, fixed-price is the standard and the safer choice for the homeowner.</p>
      </div>

      <figure style="margin:28px 0 32px;padding:0">
        <img src="/wp-content/uploads/2025/12/homepage3.jpg" alt="Custom home built by Palermo Homes on a fixed-price contract in the Okanagan Valley" style="width:100%;height:auto;display:block;border-radius:4px" loading="lazy" width="1200" height="800">
        <figcaption style="font-size:13px;color:#6a7078;margin:10px 0 0;line-height:1.5;font-style:italic">A Palermo Homes custom build in the Okanagan. Every Palermo project runs on a fixed-price contract with transparent allowances and documented change orders.</figcaption>
      </figure>

      <p>Choosing a construction contract type is one of the first real financial decisions a custom home buyer makes, and it is the one that determines whether the final bill resembles the signed quote. The two main contract structures in British Columbia residential construction are fixed-price and cost-plus. The difference between them is who carries the cost risk.</p>

      <h2>Fixed-price contracts, in plain English</h2>

      <p>A fixed-price contract (sometimes called a lump-sum or stipulated-sum contract) commits the builder to deliver a defined scope of work for a specific price. The builder absorbs cost overruns on anything that is in scope and priced. If a trade comes in higher than the builder estimated, that is the builder's problem, not the homeowner's.</p>

      <p>For a fixed-price contract to work fairly, three things need to be true:</p>
      <ul>
        <li><strong>Detailed scope.</strong> Every room, finish, system, and inclusion is specified in writing before the contract is signed. Vague scope is how fixed-price contracts turn into change-order mines.</li>
        <li><strong>Documented allowances.</strong> For items the homeowner has not selected yet (tile, lighting, appliances, plumbing fixtures), the contract carries a dollar allowance. Selections within the allowance cost nothing extra. Selections above the allowance generate a transparent change order.</li>
        <li><strong>A clear change order process.</strong> Every mid-build change is priced, written up, dated, and signed before work starts. No verbal handshakes.</li>
      </ul>

      <p>When these three conditions are met, a fixed-price contract gives the homeowner a defensible budget to make financing, insurance, and planning decisions on.</p>

      <h2>Cost-plus contracts, in plain English</h2>

      <p>A cost-plus contract bills the homeowner for actual costs incurred by the builder (materials, labour, subcontractor invoices) plus a markup, typically expressed as a percentage of those costs. There is no price ceiling. If the actual cost of the build runs 40 percent over initial estimates, the homeowner pays 40 percent over initial estimates. The builder's markup is calculated on the final cost, so the builder's compensation can increase if the project runs over.</p>

      <p>The structural problem with cost-plus is the misaligned incentive. In a fixed-price contract, the builder is motivated to control cost because overruns come out of the builder's margin. In a cost-plus contract, the builder is paid a percentage of total cost, so cost increases can increase the builder's payment.</p>

      <h2>The honest comparison</h2>

      <table>
        <thead>
          <tr><th>Factor</th><th>Fixed-price</th><th>Cost-plus</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Who carries cost overrun risk</strong></td><td>Builder</td><td>Homeowner</td></tr>
          <tr><td><strong>Price certainty before construction</strong></td><td>High (if scope is detailed)</td><td>Low (estimate only, no ceiling)</td></tr>
          <tr><td><strong>Builder incentive on cost control</strong></td><td>Aligned (overruns reduce builder margin)</td><td>Mixed (overruns can increase builder markup dollars)</td></tr>
          <tr><td><strong>Time to prepare the contract</strong></td><td>Longer (detailed scoping required)</td><td>Shorter (less upfront detail)</td></tr>
          <tr><td><strong>Flexibility to change scope mid-build</strong></td><td>Change orders required</td><td>Easier (just invoiced)</td></tr>
          <tr><td><strong>Financing lender comfort</strong></td><td>Strong (fixed total)</td><td>Weaker (no fixed total)</td></tr>
          <tr><td><strong>Best for</strong></td><td>Most residential custom builds</td><td>Highly unusual scope or research-phase builds</td></tr>
        </tbody>
      </table>

      <h2>Common fixed-price contract mistakes</h2>

      <p>Fixed-price is only fair to both sides if the scope and allowances are detailed. The common failure modes:</p>

      <h3>Vague allowances</h3>
      <p>"Flooring allowance: $8,000" with no indication of what quality that buys. The homeowner picks flooring, gets a change order for $14,000 because the quoted allowance covered contractor-grade only. Honest fixed-price contracts specify allowance ranges with examples ("tile allowance $45 per square foot, examples: X, Y, Z product lines").</p>

      <h3>Missing scope items</h3>
      <p>The quote excludes landscaping, driveway, septic, well, geotechnical, or site surveys without flagging it clearly. The homeowner thinks the fixed price covers everything and finds out at completion that it did not.</p>

      <h3>Change order volume</h3>
      <p>A builder who provides a lowball fixed-price and plans to make up margin through change orders during construction has effectively sold a cost-plus contract disguised as fixed-price. Expect every reputable Kelowna builder to issue change orders for genuine mid-build changes, but a build that generates 20 to 30 change orders without the homeowner driving the changes is a bad sign.</p>

      <h2>When cost-plus actually makes sense</h2>

      <p>Cost-plus is not inherently wrong. It is the appropriate structure for a narrow set of situations:</p>
      <ul>
        <li><strong>Highly unusual or custom scope</strong> where the builder cannot reasonably estimate the cost in advance. Examples include heritage restorations with unknown structural conditions, experimental building systems, or research-grade sustainable builds using unproven materials.</li>
        <li><strong>Early design-phase construction</strong> where the homeowner wants to start site work before the full design is complete. Even here, the cost-plus portion should be capped and converted to fixed-price as soon as the design finalizes.</li>
        <li><strong>Owner-contractor builds</strong> where the owner is managing their own project and the "builder" is really a general contractor managing trades on the owner's behalf.</li>
      </ul>

      <p>For a standard residential custom home on a defined lot in the Okanagan, none of these conditions typically apply. If a builder is pushing cost-plus for a standard custom build, ask directly why fixed-price is not an option. A good answer involves specifics about scope that genuinely cannot be scoped. A vague answer is a flag.</p>

      <h2>How to evaluate a fixed-price quote</h2>

      <p>When reviewing a fixed-price custom home quote in Kelowna, run through this checklist before signing:</p>
      <ul>
        <li>Is every room detailed with finishes, fixtures, and dimensions?</li>
        <li>Are all allowances itemized by category with specific dollar amounts?</li>
        <li>Do the allowances come with example products or quality ranges, not just a dollar figure?</li>
        <li>Are landscaping, driveway, septic/well (if rural), geotechnical, and site surveys explicitly included or clearly excluded?</li>
        <li>Is the payment draw schedule tied to construction milestones, not calendar dates?</li>
        <li>Is the change order process documented in writing (how changes get priced, who signs, when work begins)?</li>
        <li>Is GST handled explicitly (included or added)?</li>
        <li>Is the warranty program named (2-5-10 provider)?</li>
        <li>Is there a liquidated damages clause for late completion, and is it reciprocal?</li>
      </ul>

      <p>A quote that answers all of these clearly is a quote you can compare against other quotes meaningfully. A quote that leaves any of them vague is not actually a fixed-price contract. It is a soft estimate dressed up as one.</p>

      <h2>How Palermo Homes handles contracts</h2>

      <p>Every Palermo Homes project in the Okanagan runs on a fixed-price contract with transparent allowances and documented change orders. We do not run cost-plus residential builds. For most of our clients, this means the number signed at contract is the number paid at completion, with any variations coming only from change orders the homeowner specifically requested in writing.</p>

      <p>On our <a href="/project/cabernet-2/">Cabernet Way project</a>, the final cost landed within 2 percent of the signed contract, with the variance driven by a late-stage client request to upgrade the primary bathroom tile package. That change order was priced, written up, and signed before the tile was ordered. On our <a href="/project/malbec-place-1/">Malbec Place project</a>, the final cost matched the signed contract exactly because no mid-build scope changes were requested.</p>

      <blockquote style="border-left:3px solid #0085c9;padding:14px 20px;margin:28px 0;background:#f4f9fc;font-style:italic;color:#1a1d21;font-size:16px;line-height:1.65">
        <p style="margin:0">"We lose some clients because we insist on fixed-price. They go to a builder quoting cost-plus with a lower starting number and come back a year later asking what we would charge to finish. Fixed-price is harder to sell upfront and better to live with for the next 18 months." Jas Sidhu, Owner, Palermo Homes</p>
      </blockquote>

      <h2>Related reading</h2>

      <p>Our <a href="/guides/how-to-choose-custom-home-builder-kelowna/">guide to choosing a custom home builder in Kelowna</a> covers the seven verification criteria to run on any Kelowna builder before signing anything, including the fixed-price versus cost-plus question in context. Our <a href="/guides/custom-home-cost-kelowna/">custom home cost guide</a> explains how to budget for a Kelowna custom home before you request fixed-price quotes. Our <a href="/guides/how-long-to-build-custom-home-kelowna/">timeline guide</a> covers how long the design, permits, and construction phases take.</p>

      <p class="footer-note">This guide reflects standard residential custom home contract practice in the Central Okanagan as of 2026. Contract law and construction industry practice evolve. Verify current specifics with any builder you interview and consult legal counsel before signing any construction contract.</p>
    </div>
  </section>

  <section class="guide-about">
    <div class="wrap">
      <h2>About Palermo Homes</h2>
      <p>Palermo Homes is a custom home builder based in West Kelowna, BC (BC Corporate Registration BC1017682, BC Housing Licensed Residential Builder Number 42812). We have been building custom homes and whole-home renovations across the Okanagan Valley and Lower Mainland for over 15 years. Every project runs on a fixed-price contract with transparent allowances and documented change orders.</p>
      <p>We build in <a href="/service-areas/kelowna/">Kelowna</a>, <a href="/service-areas/west-kelowna/">West Kelowna</a>, <a href="/service-areas/lake-country/">Lake Country</a>, <a href="/service-areas/peachland/">Peachland</a>, <a href="/service-areas/penticton/">Penticton</a>, <a href="/service-areas/vernon/">Vernon</a>, and select Lower Mainland communities. More about the owner and the approach is on the <a href="/about/jas-sidhu/">Jas Sidhu bio page</a>.</p>
    </div>
  </section>

  <section class="guide-cta">
    <div class="wrap">
      <h2>Interested in a fixed-price custom home build in the Okanagan?</h2>
      <p>Tell us about your lot, scope, and finish priorities. We will scope it in detail and give you a defensible fixed-price quote.</p>
      <a class="btn" href="/contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    html = re.sub(r"/\* ==== GUIDE-CONTRACTS CSS START ==== \*/.*?/\* ==== GUIDE-CONTRACTS CSS END ==== \*/", "", html, flags=re.DOTALL)
    html = re.sub(r"/\* ==== ABOUT-V2 CSS START ==== \*/.*?/\* ==== ABOUT-V2 CSS END ==== \*/", "", html, flags=re.DOTALL)
    html = html.replace("</head>", f"<style>{GUIDE_CSS}</style></head>", 1)
    html = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', html, count=1)
    # Strip any existing meta description (any attribute order), inject fresh
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{META_DESC}"/>\n</head>', 1)
    # Strip any existing canonical tag (any attribute order), inject fresh
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{CANONICAL}"/>\n</head>', 1)
    # OG + Twitter tags
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
        html, count=1,
    )
    html = html.replace("</head>", schema_block + "</head>", 1)

    out = SITE / "guides" / "fixed-price-vs-cost-plus-custom-home-kelowna" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built Guide #4: Fixed-Price vs Cost-Plus Contracts.")
