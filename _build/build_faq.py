"""Build /faq/ page. Clean accordion layout inspired by wedocustomgyms, white theme.
25 questions optimized for Google SEO and AI answer engines (GEO/AEO).
FAQPage + BreadcrumbList + WebPage schema. No street address anywhere.
Idempotent. Safe to rerun."""
import re
import json
from pathlib import Path

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

CSS_START = "/* ==== FAQ-V2 CSS START ==== */"
CSS_END = "/* ==== FAQ-V2 CSS END ==== */"

FAQ_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .faq{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .faq *{{box-sizing:border-box}}
html body #et-main-area .faq .wrap{{max-width:1080px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}

/* Hero. Matches ct-top pattern from contact page: white bg, blue H1, blue crumbs. */
html body #et-main-area .faq-hero{{background:#fff;color:#1a1d21;border-bottom:1px solid #e2ddd0;padding:64px 0 52px}}
html body #et-main-area .faq-hero .wrap{{max-width:1080px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .faq-hero .crumb{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 24px;padding:0}}
html body #et-main-area .faq-hero .crumb a{{color:#0085c9;text-decoration:none;opacity:.75;transition:opacity .2s}}
html body #et-main-area .faq-hero .crumb a:hover{{opacity:1}}
html body #et-main-area .faq-hero .crumb .sep{{margin:0 10px;opacity:.5}}
html body #et-main-area .faq-hero h1{{font-size:clamp(28px,3.4vw,46px);font-weight:700;letter-spacing:-0.015em;line-height:1;margin:0 0 22px;padding:0;color:#0085c9;text-transform:uppercase;white-space:nowrap}}
html body #et-main-area .faq-hero .sub{{font-size:clamp(14px,1.05vw,16px);line-height:1.6;color:#3a4048;margin:0;padding:0;max-width:52ch}}
html body #et-main-area .faq-hero .sub a{{color:#0085c9;text-decoration:none;border-bottom:1px solid #0085c9;font-weight:600;transition:opacity .2s}}
html body #et-main-area .faq-hero .sub a:hover{{opacity:.75}}
@media (max-width:820px){{
  html body #et-main-area .faq-hero{{padding:44px 0 32px}}
  html body #et-main-area .faq-hero h1{{font-size:clamp(20px,5vw,30px)}}
}}
@media (max-width:420px){{
  html body #et-main-area .faq-hero h1{{font-size:clamp(16px,4.5vw,22px)}}
}}

/* Category label between groups */
html body #et-main-area .faq-cat{{padding:32px 0 8px;background:#fff}}
html body #et-main-area .faq-cat .lbl{{font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0}}

/* List container */
html body #et-main-area .faq-list{{background:#fff;padding:0 0 8px}}

/* Individual Q&A row */
html body #et-main-area .faq-row{{border-bottom:1px solid #ece8df}}
html body #et-main-area .faq-row summary{{cursor:pointer;display:flex;align-items:flex-start;justify-content:space-between;gap:24px;padding:26px 0;list-style:none;font-size:clamp(16px,1.5vw,19px);font-weight:600;color:#1a1d21;line-height:1.35;letter-spacing:-0.01em;transition:color .2s}}
html body #et-main-area .faq-row summary::-webkit-details-marker{{display:none}}
html body #et-main-area .faq-row summary:hover{{color:#0085c9}}
html body #et-main-area .faq-row summary .icon{{flex-shrink:0;width:24px;height:24px;position:relative;margin-top:2px}}
html body #et-main-area .faq-row summary .icon::before,
html body #et-main-area .faq-row summary .icon::after{{content:'';position:absolute;background:#1a1d21;transition:transform .25s ease,background .2s}}
html body #et-main-area .faq-row summary .icon::before{{top:50%;left:0;right:0;height:1.5px;transform:translateY(-50%)}}
html body #et-main-area .faq-row summary .icon::after{{top:0;bottom:0;left:50%;width:1.5px;transform:translateX(-50%)}}
html body #et-main-area .faq-row[open] summary .icon::after{{transform:translateX(-50%) rotate(90deg);opacity:0}}
html body #et-main-area .faq-row summary:hover .icon::before,
html body #et-main-area .faq-row summary:hover .icon::after{{background:#0085c9}}
html body #et-main-area .faq-row .ans{{padding:0 48px 28px 0;font-size:15px;line-height:1.7;color:#3a4048;max-width:80ch}}
html body #et-main-area .faq-row .ans p{{margin:0 0 12px}}
html body #et-main-area .faq-row .ans p:last-child{{margin:0}}
html body #et-main-area .faq-row .ans a{{color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1;font-weight:500;transition:border-color .2s}}
html body #et-main-area .faq-row .ans a:hover{{border-bottom-color:#0085c9}}

/* CTA. Matches site-wide svc-cta pattern (padding:56px 0). */
html body #et-main-area .faq-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center;margin-top:48px}}
html body #et-main-area .faq-cta h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 14px;color:#fff !important}}
html body #et-main-area .faq-cta p{{color:rgba(255,255,255,.92) !important;font-size:16px;margin:0 0 26px}}
html body #et-main-area .faq-cta a.btn{{display:inline-block;background:#fff;color:#0085c9;padding:14px 30px;border-radius:999px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;text-decoration:none;transition:background .2s,color .2s}}
html body #et-main-area .faq-cta a.btn:hover{{background:#141821;color:#fff}}
{CSS_END}
"""


# ============================================================
# FAQ CONTENT
# ============================================================
CATEGORIES = [
    {
        "id": "cost",
        "label": "Cost & Budgeting",
        "items": [
            {
                "q": "How much does a custom home cost in Kelowna?",
                "a": "Custom homes in Kelowna typically range from $1.5 million to $5 million and up for the home alone, not including land. The current market runs approximately $500 to $900 per square foot depending on finish level, site conditions, and structural complexity. A mid-range 3,500 square foot Palermo custom home usually lands between $2.0M and $3.2M. Hillside lots with retaining, deep pilings, or complex geotech can add $100,000 to $400,000 over a comparable flat lot. Palermo Homes provides transparent line-item budgeting from the first conversation so you see exactly where your investment goes."
            },
            {
                "q": "What is included in a Palermo custom home price?",
                "a": "Every Palermo build includes complete architectural design coordination, engineering, permit management, all trades and materials, project management, site supervision, on-site cleanup, final commissioning, and the full BC 2-5-10 New Home Warranty. Standard specifications include 8 foot doors, engineered hardwood, quartz countertops, custom cabinetry, tile-lined showers, and premium appliances. Upgrades like wine rooms, elevators, indoor pools, or bespoke millwork are quoted separately. What is not included: land purchase, landscaping beyond the basic package, custom furniture, and appliances outside the standard specification."
            },
            {
                "q": "What is the price per square foot for a custom home in the Okanagan?",
                "a": "Custom home pricing in the Okanagan currently runs between $500 and $900 per square foot for above-grade finished space, plus $200 to $350 per square foot for finished basement space. Entry level custom builds start around $500 to $600 per square foot. Mid-range projects with premium finishes run $650 to $800 per square foot. High-end custom builds with imported materials, complex geometry, or specialty systems can exceed $900 per square foot. Kelowna, West Kelowna, and Lake Country pricing is typically 10 to 15 percent higher than Vernon or Penticton due to labour costs and lot values. See our detailed <a href=\"/guides/custom-home-cost-kelowna/\">2026 cost guide for custom homes in Kelowna</a> for a full breakdown by home size and tier."
            },
            {
                "q": "Do you offer financing options?",
                "a": "Palermo Homes does not provide in-house financing directly. However, we work regularly with construction lenders and mortgage specialists across the Okanagan who understand custom builds. We can refer you to lenders who offer draw-based construction mortgages structured around the project's build schedule. We also coordinate with your lender throughout the project by providing progress reports, invoices, and draw requests directly, which keeps your financing on track without extra work on your end."
            },
            {
                "q": "How do you handle change orders and cost overruns?",
                "a": "Palermo uses fixed-price contracts where possible, with clearly documented allowances for items like tile, plumbing fixtures, and appliances. Any change requested during the build is written up as a formal change order with material cost, labour cost, and schedule impact, then approved by you before work begins. We do not proceed with any change without your written sign-off. This keeps you fully in control of the budget and eliminates end-of-project surprises. Our typical projects finish within 3 to 5 percent of the original contract price."
            },
        ]
    },
    {
        "id": "process",
        "label": "Process & Timeline",
        "items": [
            {
                "q": "How long does it take to build a custom home in Kelowna?",
                "a": "A typical Palermo custom home takes 14 to 20 months from your first design meeting to move-in. This breaks down roughly as: 3 to 5 months for architectural design and interior finishes, 2 to 3 months for permits and geotechnical assessment (longer on hillside lots), and 9 to 12 months of actual construction. Hillside sites in Upper Mission, Kettle Valley, McKinley Beach, or Predator Ridge often add 4 to 8 weeks for retaining, drainage, and foundation stepping. Excavation and framing move fastest in Okanagan summers, so we schedule critical exterior phases to hit the right months."
            },
            {
                "q": "What is the design-build process at Palermo Homes?",
                "a": "Our process runs in five phases. Phase 1 is discovery, where we understand your lifestyle, budget, and site. Phase 2 is design development with our architect, where we create schematics and refine to construction drawings. Phase 3 is permits and pre-construction, including geotech, engineering, and city approvals. Phase 4 is construction with weekly site meetings and monthly progress updates. Phase 5 is final commissioning, deficiency walk-through, and hand-over including all warranty documents. You have one point of contact from Palermo throughout every phase."
            },
            {
                "q": "Can I use my own architect or existing house plans?",
                "a": "Yes. Palermo works both as a design-build firm and as a construction partner for owners who already have their own architect or completed plans. If you bring existing plans, we review them for constructability, cost efficiency, and code compliance, then provide a detailed line-item bid. If you want us to handle design, we work with our in-house architectural partners who specialize in West Coast contemporary and mountain modern styles suited to the Okanagan. Either path gets you the same fixed-price contract and quality standards."
            },
            {
                "q": "When can I move in after construction starts?",
                "a": "Most Palermo custom homes are ready for occupancy 9 to 12 months after excavation begins, assuming standard weather and no major scope changes. Complex hillside builds or homes with specialty features like indoor pools or elevators can run 13 to 15 months of construction. We provide a detailed schedule at contract signing that shows all major milestones (foundation, framing, mechanical rough-in, drywall, cabinetry, final finishes) so you can plan your move with confidence. Weekly progress updates keep the schedule visible to you at all times."
            },
            {
                "q": "What happens during the permit and design phase?",
                "a": "The design and permit phase typically runs 5 to 8 months before ground-break. During design, we develop the architectural drawings, structural engineering, interior finish selections, and detailed specifications. During permitting, we submit to the City of Kelowna, West Kelowna, or the relevant municipality, and coordinate any required geotechnical assessments, hillside development permits, sub-community design review (Upper Mission, Predator Ridge, etc.), and building code approvals. Palermo manages every submission and follow-up on your behalf, so you are not chasing paperwork."
            },
        ]
    },
    {
        "id": "lot",
        "label": "Lot & Design",
        "items": [
            {
                "q": "Do I need to own a lot before contacting Palermo Homes?",
                "a": "No. Many Palermo clients contact us before they have a lot, and we help evaluate potential properties for buildability, cost implications, and design suitability. If you already have a lot, we can begin design immediately after our first consultation. If you are still searching, we work with local real estate agents who specialize in custom home lots across Kelowna, West Kelowna, Lake Country, and the Okanagan. Getting our input before purchasing a lot often saves tens of thousands of dollars by flagging site issues (slope, drainage, geotech, servicing) that affect build cost."
            },
            {
                "q": "Can Palermo help me find the right lot in Kelowna or West Kelowna?",
                "a": "Yes. We regularly refer clients to lot listings that suit their budget and design goals across the Okanagan. We know most active custom home neighborhoods including <a href=\"/neighborhoods/upper-mission/\">Upper Mission</a>, <a href=\"/neighborhoods/kettle-valley/\">Kettle Valley</a>, <a href=\"/neighborhoods/wilden/\">Wilden</a>, <a href=\"/neighborhoods/mckinley-beach/\">McKinley Beach</a>, <a href=\"/neighborhoods/lakestone/\">Lakestone</a>, and <a href=\"/neighborhoods/predator-ridge/\">Predator Ridge</a>. Before you commit to a lot, we walk the site with you, review the geotech, servicing, and any design covenants, and provide a realistic build cost range specific to that lot. This turns lot purchases from a gamble into an informed decision."
            },
            {
                "q": "What is the difference between a custom home and a spec home?",
                "a": "A custom home is designed and built specifically for you, on your lot, to your specifications. Every architectural decision, finish selection, layout choice, and feature is yours. A spec home is built by a developer on speculation, meaning they design and build it hoping to sell it to a future buyer. Spec homes offer faster occupancy but limited customization. Palermo Homes builds exclusively custom homes because it delivers a home tailored to how you actually live, with your lifestyle, family, and aesthetic in mind, and gives you full control over quality throughout the build."
            },
        ]
    },
    {
        "id": "areas",
        "label": "Service Areas",
        "items": [
            {
                "q": "What areas of BC do you serve?",
                "a": "Palermo Homes builds custom homes and renovations across the Central Okanagan, North Okanagan, and Lower Mainland. Our primary service areas include <a href=\"/service-areas/kelowna/\">Kelowna</a>, <a href=\"/service-areas/west-kelowna/\">West Kelowna</a>, <a href=\"/service-areas/lake-country/\">Lake Country</a>, <a href=\"/service-areas/peachland/\">Peachland</a>, <a href=\"/service-areas/vernon/\">Vernon</a>, and <a href=\"/service-areas/penticton/\">Penticton</a>. We also take select projects in the <a href=\"/service-areas/lower-mainland/\">Lower Mainland</a> and Fraser Valley including Abbotsford, Chilliwack, Langley, Vancouver, and West Vancouver. If you are outside these areas, contact us and we will let you know if we can help."
            },
            {
                "q": "Do you build in West Kelowna, Lake Country, and Peachland?",
                "a": "Yes. Palermo Homes actively builds in <a href=\"/service-areas/west-kelowna/\">West Kelowna</a> (including Lakeview Heights, Boucherie, and Rose Valley), <a href=\"/service-areas/lake-country/\">Lake Country</a> (including Lakestone, Coral Beach, and Carr's Landing), and <a href=\"/service-areas/peachland/\">Peachland</a> (including Ponderosa and Trepanier). We are BC-registered as company BC1017682 and hold BC Housing license number 42812, which covers new home construction across all of British Columbia. Our project managers are familiar with each municipality's building codes, permit processes, and design review requirements."
            },
            {
                "q": "Do you build in the Lower Mainland and Fraser Valley?",
                "a": "Yes, on a select basis. Palermo Homes has built custom homes in the <a href=\"/service-areas/lower-mainland/\">Lower Mainland</a> including Abbotsford, Chilliwack, Langley, Vancouver, and West Vancouver. Because our head office is in the Okanagan, we take Lower Mainland projects when the scope justifies the travel and site management. Existing Palermo clients who want to build a second home or renovation in the Lower Mainland get priority. If you are considering a Lower Mainland project, contact us and we will assess feasibility and provide an honest answer on whether we can serve you well."
            },
            {
                "q": "Can you build in specific neighborhoods like Upper Mission or Wilden?",
                "a": "Yes. Palermo Homes builds in every major Kelowna and West Kelowna custom home neighborhood, including <a href=\"/neighborhoods/upper-mission/\">Upper Mission</a> (Kettle Valley, The Ponds, Southridge, Crawford Estates), <a href=\"/neighborhoods/wilden/\">Wilden</a>, <a href=\"/neighborhoods/mckinley-beach/\">McKinley Beach</a>, <a href=\"/neighborhoods/kettle-valley/\">Kettle Valley</a>, <a href=\"/neighborhoods/lakestone/\">Lakestone</a> in Lake Country, and <a href=\"/neighborhoods/predator-ridge/\">Predator Ridge</a> near Vernon. We work inside each sub-community's architectural guidelines, colour palettes, and design review processes from the first sketch, which means fewer bounces and no surprises at permit time."
            },
        ]
    },
    {
        "id": "warranty",
        "label": "Warranty & Quality",
        "items": [
            {
                "q": "What warranty do you offer on new custom homes?",
                "a": "Every Palermo custom home is covered by British Columbia's mandatory 2-5-10 New Home Warranty program. The coverage breaks down as: 2 years for labour and materials (workmanship defects), 5 years for the building envelope (water penetration, moisture protection), and 10 years for major structural defects (load-bearing elements, foundation). This is the highest standard warranty available for new construction in Canada. Our warranty is backed by a third-party provider registered with BC Housing, not by Palermo alone, so coverage is enforceable even if a builder went out of business."
            },
            {
                "q": "Are you a licensed builder in BC?",
                "a": "Yes. Palermo Homes Ltd. is a fully licensed residential builder in British Columbia. Our BC Housing licensed builder number is 42812. Our corporate registration with the BC Corporate Registry is BC1017682, incorporated October 29, 2014. You can verify our license status at any time through the BC Housing Registered Builders directory or through the BC OrgBook at orgbook.gov.bc.ca. BC law requires all new home builders to be licensed and registered, and we maintain full compliance."
            },
            {
                "q": "What certifications and industry memberships do you have?",
                "a": "Palermo Homes is a licensed BC Housing residential builder (license #42812), a BuildZoom verified contractor with a BZ Score of 92, and a Canadian Home Builders Association member. We have received multiple awards including the CHBA Fraser Valley Housing Award of Excellence. Our team members hold current WorkSafeBC clearances, and all sub-trades are verified for licensing and insurance before working on any Palermo project. We also carry full liability insurance and course of construction coverage on every build."
            },
            {
                "q": "How do you ensure quality throughout the build?",
                "a": "Quality on a Palermo build comes from three things: in-house project management, vetted trade partners, and documented inspection points. Every project has a dedicated site supervisor who is on site daily. We use a shared project management system where you can see photos, progress updates, and the schedule in real time. We hold formal inspections at foundation, framing, mechanical rough-in, insulation, drywall, and pre-hand-over stages. Every deficiency is tracked, assigned, and re-inspected before we move to the next phase. This is the same process on a 2,500 square foot family home as on a 7,000 square foot estate."
            },
        ]
    },
    {
        "id": "sustainability",
        "label": "Sustainability & Technology",
        "items": [
            {
                "q": "Do you build energy-efficient or Net Zero homes?",
                "a": "Yes. Palermo Homes builds energy-efficient custom homes that meet or exceed British Columbia's Step Code requirements, which is BC's mandatory energy efficiency framework for new construction. We can build to any Step Code level from Step 3 (basic efficiency) up to Step 5 (Net Zero Ready), with corresponding upgrades to insulation, air sealing, windows, mechanical systems, and heat recovery ventilation. Net Zero Ready homes are pre-wired and structurally prepared for solar panels to eventually produce as much energy as they consume. We discuss energy performance goals early in design so cost and payback are transparent."
            },
            {
                "q": "What smart home technology can Palermo integrate into a custom home?",
                "a": "Palermo Homes integrates smart home technology from the design phase forward. Common integrations include: whole-home lighting control (Lutron, Control4), automated blinds, smart thermostats, security and camera systems, integrated audio-visual, smart locks, irrigation controls, EV charging infrastructure, and centralized network wiring. We work with dedicated AV and low-voltage specialists who wire during the framing stage, which is far cheaper than retrofitting later. Whether you want simple smart-thermostat basics or a fully integrated Control4 system, we scope it into the initial design so it is done properly and future-proofed."
            },
            {
                "q": "Do you build homes with solar panels or geothermal heating systems?",
                "a": "Yes. Solar photovoltaic systems and geothermal heat pumps are increasingly common on Palermo custom homes, especially on larger lots where system payback makes sense. A typical residential solar array in the Okanagan runs $25,000 to $60,000 depending on system size, with payback periods of 8 to 15 years given current BC Hydro rates. Geothermal systems cost $30,000 to $70,000 more than conventional HVAC but offer 40 to 60 percent operating cost reductions and often 20+ year system life. We design homes to be solar-ready even if you install panels later."
            },
        ]
    },
    {
        "id": "renovations",
        "label": "Renovations",
        "items": [
            {
                "q": "Do you do home renovations or only new custom builds?",
                "a": "Palermo Homes does both. Our renovation division handles whole-home renovations, kitchen renovations, bathroom renovations, additions, secondary suites, and structural remodels. We use the same in-house project management, vetted trades, and quality standards as our custom home builds. Renovation projects typically range from $100,000 for a single-room renovation up to $2 million or more for a whole-home renovation with major structural changes. All renovations include a workmanship warranty and full documentation of any structural, mechanical, or electrical modifications for future resale."
            },
            {
                "q": "Can you renovate a home while we live in it?",
                "a": "Yes, in many cases. For kitchen renovations, bathroom renovations, or additions where we can seal off the work area, most families continue living in the home throughout the project. We install dust barriers, protect flooring, and coordinate trades to minimize disruption. For whole-home renovations with major structural work, HVAC changes, or extensive electrical rework, we usually recommend temporary alternate accommodation because the noise, dust, and utility interruptions are significant. We discuss this openly at the estimating stage so you know what to expect."
            },
            {
                "q": "What types of renovations do you specialize in?",
                "a": "Palermo Homes specializes in high-end whole-home renovations, kitchen renovations, bathroom renovations, additions, garage conversions, and heritage home restorations. We are especially known for open-concept renovations of older Okanagan homes where we remove load-bearing walls to create modern living spaces, and for hillside home additions where site access and structural engineering matter. We handle everything from design through permits, construction, and final finishes. If your renovation involves structural changes, foundation work, or significant scope, we are typically a strong fit."
            },
        ]
    },
    {
        "id": "about",
        "label": "About Palermo",
        "items": [
            {
                "q": "How long has Palermo Homes been building?",
                "a": "Palermo Homes Ltd. was incorporated on October 29, 2014, and has been actively building custom homes and renovations in British Columbia for over 15 years including the owners' pre-incorporation project history. We have completed dozens of custom homes and renovation projects across the Central Okanagan, North Okanagan, and Lower Mainland. Our project portfolio includes lakeview homes in West Kelowna, hillside custom homes in Upper Mission, waterfront properties in Lake Country, and estate homes in Vernon and Peachland. See our <a href=\"/projects/\">projects page</a> for recent builds."
            },
            {
                "q": "Who owns Palermo Homes and what is the team like?",
                "a": "Palermo Homes is owned by Jas Sidhu, a hands-on builder who is on site regularly across active projects. Our team includes in-house project managers, site supervisors, dedicated administrative staff, and long-standing relationships with a curated group of trade partners across framing, mechanical, electrical, cabinetry, and finish trades. We deliberately keep our project load moderate so every client gets senior attention. You are not one of dozens of active files. When you call Palermo, you reach someone who knows your project."
            },
            {
                "q": "What makes Palermo Homes different from other Kelowna builders?",
                "a": "Three things distinguish Palermo Homes from other Kelowna custom home builders. First, transparent line-item pricing from day one, with fixed-price contracts and formal change order documentation. Second, a single point of contact throughout the project, so you never chase multiple people for answers. Third, moderate project load by design, which means senior team members are actively involved on your build instead of stretched across too many jobs. Combined with our BC 2-5-10 warranty coverage and 15+ years of Okanagan build experience, this delivers a smoother, more predictable custom home experience."
            },
            {
                "q": "How do I get started with Palermo Homes?",
                "a": "Getting started is simple. Call us at (604) 897-9390 or use our <a href=\"/contact/\">contact form</a> to schedule an initial consultation. The first conversation is free and takes about 45 minutes. We discuss your project scope, budget range, timeline, and whether you have a lot or are still searching. If it is a good fit on both sides, we book a site visit or design meeting to move to the next step. There is no pressure, no obligation, and no cost until we sign a formal design or construction contract."
            },
            {
                "q": "Can you provide references from past Palermo Homes clients?",
                "a": "Yes. Palermo Homes provides client references on request, typically after an initial consultation once we know your project is a serious fit. We share contact details for past clients with similar project types (custom home, whole-home renovation, hillside build, etc.) so their feedback is relevant to your situation. We recommend calling multiple references and asking specific questions about communication, budget accuracy, timeline adherence, and quality of finished work. You can also see our <a href=\"/projects/\">recent projects</a> and third-party verifications through BC Housing, BuildZoom, and Houzz."
            },
        ]
    },
]


def build_body():
    """Produce the accordion body. Categories emit a small label + their rows."""
    out = []
    first = True
    for c in CATEGORIES:
        out.append(f'''
  <section class="faq-cat"><div class="wrap"><p class="lbl">{c["label"]}</p></div></section>
  <section class="faq-list"><div class="wrap">''')
        for item in c["items"]:
            open_attr = " open" if first else ""
            first = False
            out.append(f'''
    <details class="faq-row"{open_attr}>
      <summary>{item["q"]}<span class="icon"></span></summary>
      <div class="ans"><p>{item["a"]}</p></div>
    </details>''')
        out.append("\n  </div></section>")
    return "".join(out)


def build_schema():
    entities = []
    for c in CATEGORIES:
        for item in c["items"]:
            plain = re.sub(r'<[^>]+>', '', item["a"])
            entities.append({
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": plain},
            })
    faq = {"@type": "FAQPage", "mainEntity": entities}
    breadcrumbs = {
        "@type": "BreadcrumbList",
        "@id": f"{BIZ_URL}/faq/#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BIZ_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "FAQ", "item": f"{BIZ_URL}/faq/"},
        ],
    }
    webpage = {
        "@type": "WebPage",
        "@id": f"{BIZ_URL}/faq/",
        "url": f"{BIZ_URL}/faq/",
        "name": "Frequently Asked Questions",
        "description": "Common questions about custom home building, renovations, cost, timelines, warranty, and service areas answered by Palermo Homes in Kelowna, BC.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{BIZ_URL}/faq/#breadcrumb"},
        "inLanguage": "en",
    }
    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, faq]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Custom Home Builder FAQ | Palermo Homes Kelowna"
META_DESC = "Common questions about custom home building in Kelowna, West Kelowna, and the Okanagan: cost, timelines, warranty, process, service areas."
CANONICAL = f"{BIZ_URL}/faq/"

MAIN_HTML = f"""
<div class="faq">
  <section class="faq-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">·</span>FAQ</p>
      <h1>Frequently Asked Questions.</h1>
      <p class="sub">Everything you need to know before starting your custom home or renovation. Something not covered here? <a href="/contact/">Reach out directly.</a></p>
    </div>
  </section>
  {build_body()}
  <section class="faq-cta">
    <div class="wrap">
      <h2>Still have a question?</h2>
      <p>Ask us directly. We answer every inquiry within one business day.</p>
      <a class="btn" href="/contact/">Contact Palermo Homes</a>
    </div>
  </section>
</div>
"""


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    # remove any prior FAQ-V1/V2 CSS block
    html = re.sub(r"/\* ==== FAQ-V[12] CSS START ==== \*/.*?/\* ==== FAQ-V[12] CSS END ==== \*/", "", html, flags=re.DOTALL)
    # remove any prior ABOUT-V2 CSS block
    html = re.sub(r"/\* ==== ABOUT-V2 CSS START ==== \*/.*?/\* ==== ABOUT-V2 CSS END ==== \*/", "", html, flags=re.DOTALL)
    # inject FAQ CSS
    html = html.replace("</head>", f"<style>{FAQ_CSS}</style></head>", 1)
    # title
    html = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', html, count=1)
    # Strip existing canonical (any attribute order), inject fresh
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{CANONICAL}"/>\n</head>', 1)
    # Strip existing meta description (any attribute order), inject fresh
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{META_DESC}"/>\n</head>', 1)
    # Overwrite stale OG tags inherited from the About shell
    _og_image = f"{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-02.jpg"
    html = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{TITLE.replace(" | Palermo Homes", "")}" property="og:title"/>', html, count=1)
    html = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{CANONICAL}" property="og:url"/>', html, count=1)
    # Remove article:modified_time entirely (no reliable per-page edit date)
    html = re.sub(r'<meta[^>]*property="article:modified_time"[^>]*/?>\s*', '', html)
    # Remove stale twitter data (reading-time) inherited from About
    html = re.sub(r'<meta[^>]*name="twitter:data1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:label1"[^>]*/?>\s*', '', html)
    # Add og:description + og:image after og:site_name (idempotent)
    html = re.sub(r'<meta content="[^"]*" property="og:description"/>\n?', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:image"/>\n?', '', html)
    html = re.sub(
        r'(<meta content="[^"]*" property="og:site_name"/>)',
        r'\1' + f'\n<meta content="{META_DESC}" property="og:description"/>\n<meta content="{_og_image}" property="og:image"/>',
        html, count=1,
    )
    # Strip Yoast About-page schema (we inject our own)
    html = re.sub(r'<script class="yoast-schema-graph"[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    # Fix stale preload image
    html = re.sub(
        r'<link rel="preload" as="image" href="[^"]*" fetchpriority="high">',
        f'<link rel="preload" as="image" href="{_og_image}" fetchpriority="high">',
        html, count=1,
    )
    # inject schema before </head>
    html = html.replace("</head>", schema_block + "</head>", 1)

    out = SITE / "faq" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built FAQ page.")
