"""Build /guides/how-to-choose-custom-home-builder-kelowna/
Guide #2 ,  "How to Choose a Custom Home Builder in Kelowna."
Targets PAA + money queries: "how to choose a custom home builder", "best custom
home builder kelowna", "what to look for in a kelowna home builder".
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
PAGE_URL = f"{BIZ_URL}/guides/how-to-choose-custom-home-builder-kelowna/"
PUBLISH_DATE = "2026-10-03"
MODIFIED_DATE = datetime.date.today().isoformat()

CSS_START = "/* ==== GUIDE-CHOOSE CSS START ==== */"
CSS_END = "/* ==== GUIDE-CHOOSE CSS END ==== */"

# Same CSS as cost guide for design consistency
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
}}
{CSS_END}
"""

# FAQ entries this guide answers (for schema)
FAQ_ITEMS = [
    {
        "q": "How do I choose a custom home builder in Kelowna?",
        "a": "To choose a custom home builder in Kelowna, verify seven things before signing any contract: BC Housing license number, BC Corporate Registry status, fixed-price contract availability, documented change order process, three callable references, 2-5-10 New Home Warranty coverage, and senior on-site project management. Interview at least three builders and compare fixed-price bids on identical scope. The right builder matches your budget, communication style, design goals, and site conditions."
    },
    {
        "q": "What should I look for in a Kelowna custom home builder?",
        "a": "Look for a BC Housing-licensed builder with a transparent, fixed-price contract (not cost-plus), documented change order process, verifiable references from similar projects, active liability and WorkSafeBC insurance, and senior project management rather than a stretched-thin junior PM. Verify their BC Housing license number and BC Corporate Registry at orgbook.gov.bc.ca before any deposit."
    },
    {
        "q": "What are red flags when hiring a custom home builder in Kelowna?",
        "a": "Red flags include lowball bids 30 to 50 percent below competitors (missing scope), vague contracts without specifications or allowances, resistance to fixed-price contracts, pressure to sign quickly, no proof of insurance when asked, and refusal to share BC Housing license numbers. Any builder unable to produce current liability insurance, WorkSafeBC coverage, and course-of-construction insurance certificates should be eliminated from consideration."
    },
    {
        "q": "Is BC Housing registration required for Kelowna custom home builders?",
        "a": "Yes. Every residential home builder in British Columbia must be licensed by BC Housing under the Homeowner Protection Act. BC Housing licensing is mandatory, not optional. You can verify any builder's license status at the BC Housing Registered Builders directory. An unlicensed builder cannot legally construct a new home in BC."
    },
    {
        "q": "How many Kelowna custom home builders should I interview?",
        "a": "Interview at least three Kelowna custom home builders before deciding. Three allows meaningful comparison of pricing, communication style, project approach, and references. Fewer than three limits comparison. More than four or five becomes unproductive. Prepare the same scope and specifications for each builder so the comparison is apples-to-apples."
    },
    {
        "q": "What is the difference between fixed-price and cost-plus contracts for custom homes?",
        "a": "A fixed-price contract commits the builder to a specific total price for defined scope, protecting the homeowner from cost overruns. A cost-plus contract bills the homeowner for actual material and labor costs plus a builder markup, exposing the homeowner to open-ended cost escalation. Fixed-price is standard for most residential custom builds in Kelowna and is strongly preferred for budget predictability."
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
        "headline": "How to Choose a Custom Home Builder in Kelowna: A 2026 Guide",
        "description": "A step-by-step guide to choosing a custom home builder in Kelowna, including seven verification criteria, red flags, interview questions, and how to compare bids.",
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
            {"@type": "Thing", "name": "Custom Home Builder Selection"},
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
            {"@type": "ListItem", "position": 3, "name": "How to Choose a Custom Home Builder in Kelowna", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "WebPage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "How to Choose a Custom Home Builder in Kelowna: A 2026 Guide",
        "description": "A step-by-step guide to choosing a custom home builder in Kelowna, including seven verification criteria, red flags, interview questions, and how to compare bids.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "inLanguage": "en",
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, article, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Choosing a Custom Home Builder in Kelowna | Palermo Homes"
META_DESC = "A step-by-step guide to choosing a custom home builder in Kelowna. Seven verification criteria, red flags, and how to compare bids."
CANONICAL = PAGE_URL

MAIN_HTML = """
<div class="guide">
  <section class="guide-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">·</span><a href="/guides/">Guides</a><span class="sep">·</span>How to Choose a Custom Home Builder in Kelowna</p>
      <h1>How to Choose a Custom Home Builder in Kelowna: A 2026 Guide</h1>
      <p class="sub">A step-by-step guide to choosing a custom home builder in Kelowna and the Okanagan, including seven verification criteria, red flags to avoid, and how to compare bids before signing any contract.</p>
      <p class="meta">Published October 2026 · By <a href="/about/jas-sidhu/" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1">Jas Sidhu</a>, Owner of Palermo Homes · Custom Home Builder in West Kelowna, BC</p>
    </div>
  </section>

  <section class="guide-body">
    <div class="wrap">
      <div class="lede">
        <p>To choose a custom home builder in Kelowna, verify seven things before signing any contract: BC Housing license number, BC Corporate Registry status, fixed-price contract availability, documented change order process, three callable references, 2-5-10 New Home Warranty coverage, and senior on-site project management. Interview at least three builders and compare fixed-price bids on identical scope.</p>
      </div>

      <figure style="margin:28px 0 32px;padding:0">
        <img src="/wp-content/uploads/2025/12/Touriga-109.jpg" alt="Completed custom home by Palermo Homes on Touriga Place in West Kelowna, Licensed BC Housing Residential Builder 42812" style="width:100%;height:auto;display:block;border-radius:4px" loading="lazy" width="1200" height="800">
        <figcaption style="font-size:13px;color:#6a7078;margin:10px 0 0;line-height:1.5;font-style:italic">A completed Palermo Homes custom build on Touriga Place in West Kelowna. BC Housing Licensed Residential Builder number 42812.</figcaption>
      </figure>

      <p>Building a custom home is one of the biggest financial and emotional investments most people ever make. In Kelowna and the greater Okanagan, where lot prices routinely exceed $500,000 and build costs run into the millions, choosing the right custom home builder is not a decision to make lightly.</p>

      <p>This guide covers what genuinely matters when choosing a Kelowna custom home builder in 2026, what most homeowners get wrong, and how to protect yourself from expensive mistakes.</p>

      <h2>What does "custom home" actually mean?</h2>
      <p>The term custom home gets used loosely in Kelowna. Some builders call a home "custom" if you can pick your paint colours and countertop material. That is not custom. That is a spec home with options.</p>
      <p>A true custom home is designed and built specifically for you, on your lot, to your specifications. Every architectural decision, layout choice, finish selection, and structural feature is yours. The floor plan is not pulled from a template. The kitchen is not laid out for a hypothetical buyer. Everything is designed around how you actually live.</p>
      <p>This distinction matters because pricing, timeline, and process differ dramatically between a true custom build and a lightly-customized spec home. If a builder cannot articulate the difference clearly, that is a warning sign.</p>

      <h2>Seven things to verify in any Kelowna custom home builder</h2>

      <h3>1. BC Housing licensing</h3>
      <p>Every legitimate residential builder in British Columbia must be licensed by BC Housing under the Homeowner Protection Act. Ask for the builder's license number and verify it directly at the BC Housing Registered Builders directory. Any hesitation on this question means walking away.</p>

      <h3>2. BC Corporate Registry status</h3>
      <p>Confirm the business is registered with the BC Corporate Registry. This tells you the company is a legal entity in good standing, when it was incorporated, and who the officers are. You can look this up for free at OrgBook BC at orgbook.gov.bc.ca. A builder unwilling to share their registration number is a red flag.</p>

      <h3>3. Fixed-price contracts</h3>
      <p>Cost-plus contracts (where you pay whatever the trades and materials end up costing plus a builder markup) are how people end up hundreds of thousands over budget. Fixed-price contracts with documented allowances for tile, plumbing, appliances, and other variables protect you. If a builder resists fixed-price, ask why. There are legitimate reasons in rare cases, but for most residential custom builds in Kelowna, fixed-price is the standard.</p>

      <h3>4. Documented change order process</h3>
      <p>Every custom build has changes during construction. What separates good Kelowna builders from bad ones is how those changes get handled. A proper change order is written, priced, dated, and signed by both parties before work begins. Verbal change orders lead to disputes and cost overruns.</p>

      <h3>5. Real references you can actually call</h3>
      <p>Ask for at least three references from past clients with similar project scope to yours. Actually call them. Ask specific questions: Was communication clear? Did they finish on budget? Were deficiencies resolved? Would you build with them again? A builder with no references or vague answers is a builder to avoid.</p>

      <h3>6. Warranty coverage</h3>
      <p>Every new home built in BC is covered by the mandatory 2-5-10 New Home Warranty program: 2 years for labour and materials, 5 years for the building envelope, and 10 years for major structural defects. This is backed by a third-party warranty provider registered with BC Housing, not by the builder alone, so coverage is enforceable even if a builder goes out of business. Confirm which provider your builder uses.</p>

      <h3>7. On-site project management</h3>
      <p>Ask who your day-to-day point of contact will be during construction. Some Kelowna builders sell you on the owner's involvement, then hand you off to a junior project manager who is stretched across too many jobs. A builder with clear, senior-level project management on every build delivers a smoother experience.</p>

      <h2>Red flags that mean walk away</h2>

      <p><strong>The lowball estimate.</strong> If one builder's bid comes in 30 to 50 percent below competitors on the same scope, it usually means missing scope, hidden allowances, or a plan to nickel-and-dime you with change orders during construction. Bids should be in a reasonably similar range for the same scope.</p>

      <p><strong>Vague contracts.</strong> If the contract does not specify finish specifications, allowances, timeline, and payment schedule in detail, you are signing up for disputes.</p>

      <p><strong>No permit paperwork.</strong> Legitimate Kelowna builders manage permits and can show you their process. Anyone offering to build without proper permits is exposing you to enormous risk.</p>

      <p><strong>Pressure to sign quickly.</strong> "This price is only good for 48 hours" is a sales tactic, not a building strategy. Custom home builders who care about long-term reputation do not pressure customers.</p>

      <p><strong>Lack of active insurance.</strong> Ask for proof of current liability insurance, WorkSafeBC coverage, and course-of-construction insurance. Ask to see certificates. If a builder cannot produce these quickly, that is a warning.</p>

      <h2>How to compare bids from multiple Kelowna builders</h2>

      <p>Request bids from at least three builders on identical scope. This means giving each builder the same specifications, same lot information, same finish allowances, same square footage, and same inclusions. Only then can you meaningfully compare prices.</p>

      <p>When reviewing bids, ask what is and is not included:</p>
      <ul>
        <li>Does the price include design fees and permits?</li>
        <li>Does it include landscaping and driveway?</li>
        <li>What are the specific allowances for cabinets, tile, plumbing fixtures, and appliances?</li>
        <li>What happens if actual costs exceed allowances?</li>
        <li>Is GST included in the price?</li>
        <li>Who handles geotechnical and site surveys?</li>
      </ul>

      <p>A $600 per square foot quote that excludes finishes may end up costing more than a $750 per square foot quote that includes everything. The lowest number does not always mean the lowest total cost.</p>

      <h2>Neighborhood considerations for Kelowna custom builds</h2>

      <p>Kelowna's custom home neighborhoods each have their own architectural guidelines, design review processes, and site conditions. Working with a builder who knows the specific neighborhood you are building in saves months of design bounces and reduces surprises at permit time.</p>

      <p><strong><a href="/neighborhoods/upper-mission/">Upper Mission</a></strong> (Kettle Valley, The Ponds, Southridge, Crawford Estates): Each sub-community has its own architectural guidelines, material palette, and colour approvals.</p>

      <p><strong>West Kelowna</strong> (<a href="/neighborhoods/lakeview-heights/">Lakeview Heights</a>, Boucherie, Rose Valley): Lake views drive design priorities. Hillside lots common.</p>

      <p><strong><a href="/neighborhoods/wilden/">Wilden</a></strong>: Master-planned community north of downtown Kelowna with strong architectural review.</p>

      <p><strong>McKinley Beach</strong>: Lakefront living with distinctive contemporary design guidelines.</p>

      <p><strong>Lake Country</strong> (Lakestone, Coral Beach, Carr's Landing): Waterfront and vineyard views. Distinct from Kelowna in permitting.</p>

      <p><strong><a href="/neighborhoods/predator-ridge/">Predator Ridge</a></strong> (Vernon area): Golf and lakefront properties with strong design covenants.</p>

      <p>A builder who has completed projects in your target neighborhood already understands its quirks. Ask specifically.</p>

      <h2>How many Kelowna builders should you interview?</h2>

      <p>Interview at least three Kelowna custom home builders before deciding. Three allows meaningful comparison of pricing, communication style, project approach, and references. Fewer than three limits comparison. More than four or five becomes unproductive. Prepare the same scope and specifications for each builder so the comparison is apples-to-apples.</p>

      <h2>What we have seen on real Kelowna projects</h2>

      <p>Over 15 years building across the Okanagan, a few patterns show up repeatedly. On our <a href="/project/cabernet-2/">Cabernet Way project</a> in West Kelowna, the client interviewed six builders before selecting us. Three of the six would not provide fixed-price contracts. One refused to share BC Housing license numbers until a deposit was placed. The ones with the cheapest initial bid later tried to adjust pricing upward after design was locked in.</p>

      <p>On our <a href="/project/malbec-place-1/">Malbec Place project</a>, the homeowners had already received a bid from another builder that was approximately 25 percent lower than ours. When we broke down the scope line by line, the lower bid excluded the finished basement, used lower-tier cabinetry allowances, and did not include landscaping. The actual delivered cost on the other bid, had they proceeded, would have exceeded ours by about $140,000.</p>

      <p>These are not unusual stories. The homeowners who do best are the ones who ask the hard questions before signing, request itemized bids on identical scope, and verify every credential independently rather than trusting what a builder says in a sales meeting.</p>

      <blockquote style="border-left:3px solid #0085c9;padding:14px 20px;margin:28px 0;background:#f4f9fc;font-style:italic;color:#1a1d21;font-size:16px;line-height:1.65">
        <p style="margin:0">"The best clients I work with come in with a list of questions. They want to see the BC Housing license. They want references. They want to understand the change order process. That due diligence is a good thing. It protects both of us and sets the project up for success.". Jas Sidhu, Owner, Palermo Homes</p>
      </blockquote>

      <h2>How to get started with a Kelowna custom home</h2>

      <ol style="padding:0 0 0 22px;margin:0 0 24px">
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Determine your budget realistically, including a 10 to 15 percent contingency.</li>
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Understand your lot situation (owned, considering, or still searching).</li>
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Prepare a list of your must-haves versus nice-to-haves.</li>
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Contact three Kelowna builders for initial consultations.</li>
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Ask each the verification questions in this guide.</li>
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Request references and actually call them.</li>
        <li style="font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 10px">Compare fixed-price bids on identical scope.</li>
      </ol>

      <p>Custom home building is a two-year relationship, not a transaction. The time you spend finding the right builder shapes your experience for decades. Take it seriously.</p>

      <p class="footer-note">This guide reflects current standards in the Central Okanagan as of 2026. Regulations, warranty programs, and licensing requirements change. Verify current specifics with BC Housing and any builder you interview.</p>
    </div>
  </section>

  <section class="guide-about">
    <div class="wrap">
      <h2>About Palermo Homes</h2>
      <p>Palermo Homes is a custom home builder based in West Kelowna, BC (BC Corporate Registration BC1017682, BC Housing Licensed Residential Builder Number 42812). We have been building custom homes and whole-home renovations across the Okanagan Valley and Lower Mainland for over 15 years.</p>
      <p>Our approach uses fixed-price contracts with transparent line-item budgeting, documented change orders, and senior on-site project management on every build. We build in <a href="/service-areas/kelowna/">Kelowna</a>, <a href="/service-areas/west-kelowna/">West Kelowna</a>, <a href="/service-areas/lake-country/">Lake Country</a>, <a href="/service-areas/peachland/">Peachland</a>, <a href="/service-areas/penticton/">Penticton</a>, <a href="/service-areas/vernon/">Vernon</a>, and select Lower Mainland communities.</p>
      <p>For more detail on cost specifically, see our <a href="/guides/custom-home-cost-kelowna/">2026 custom home cost guide</a>. Our <a href="/faq/">FAQ page</a> answers common questions about process, timeline, warranty, and contracts.</p>
    </div>
  </section>

  <section class="guide-cta">
    <div class="wrap">
      <h2>Interviewing custom home builders in Kelowna?</h2>
      <p>We welcome the verification questions in this guide. Book a no-pressure consultation.</p>
      <a class="btn" href="/contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""


OG_IMAGE = f"{BIZ_URL}/wp-content/uploads/2025/12/Touriga-109.jpg"
OG_TITLE = "How to Choose a Custom Home Builder in Kelowna: A 2026 Guide"
READING_TIME = "9 minutes"
ISO_MODIFIED = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    html = re.sub(r"/\* ==== GUIDE-CHOOSE CSS START ==== \*/.*?/\* ==== GUIDE-CHOOSE CSS END ==== \*/", "", html, flags=re.DOTALL)
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
    html = html.replace("</head>", schema_block + "</head>", 1)

    out = SITE / "guides" / "how-to-choose-custom-home-builder-kelowna" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built Guide #2: How to Choose a Custom Home Builder in Kelowna.")
