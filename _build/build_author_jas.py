"""Build /about/jas-sidhu/. Standalone author/owner bio page.
Max E-E-A-T play: Person schema, verifiable credentials, links to every piece
Jas has authored or been quoted in across the site. Every guide's author
attribution should point here.
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
PAGE_URL = f"{BIZ_URL}/about/jas-sidhu/"
PHOTO_URL = f"{BIZ_URL}/wp-content/uploads/2020/03/TCP_1620.jpg"
PUBLISH_DATE = "2026-10-05"
MODIFIED_DATE = datetime.date.today().isoformat()
ISO_MODIFIED = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

CSS_START = "/* ==== AUTHOR-BIO CSS START ==== */"
CSS_END = "/* ==== AUTHOR-BIO CSS END ==== */"

# Design: mirrors About page tokens exactly for site-wide consistency.
CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .bio{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .bio *{{box-sizing:border-box}}
html body #et-main-area .bio img{{display:block;max-width:100%;height:auto}}
html body #et-main-area .bio .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .bio .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}

/* Hero. Tighter, text only, no background image (clean portrait follows in split). */
html body #et-main-area .bio-hero{{background:#fff;color:#1a1d21;border-bottom:1px solid #e2ddd0;padding:48px 0 36px}}
html body #et-main-area .bio-hero .crumb{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 22px;padding:0}}
html body #et-main-area .bio-hero .crumb a{{color:#0085c9;text-decoration:none;opacity:.75;transition:opacity .2s}}
html body #et-main-area .bio-hero .crumb a:hover{{opacity:1}}
html body #et-main-area .bio-hero .crumb .sep{{margin:0 10px;opacity:.5}}
html body #et-main-area .bio-hero h1{{font-size:clamp(30px,3.6vw,44px);font-weight:500;letter-spacing:-0.02em;line-height:1.1;margin:0 0 10px;padding:0;color:#1a1d21}}
html body #et-main-area .bio-hero .role{{font-size:clamp(15px,1.2vw,18px);color:#0085c9;font-weight:600;margin:0 0 16px;letter-spacing:.01em}}
html body #et-main-area .bio-hero .sub{{font-size:clamp(15px,1.15vw,17px);line-height:1.55;color:#3a4048;margin:0;padding:0;max-width:70ch}}
html body #et-main-area .bio-hero .top-cta{{display:inline-block;margin:22px 0 0;color:#0085c9;text-decoration:none;font-size:clamp(15px,1.15vw,17px);font-weight:600;letter-spacing:.01em;border-bottom:1px solid #cfe6f1;transition:border-color .2s,color .2s}}
html body #et-main-area .bio-hero .top-cta:hover{{color:#0a5c8a;border-bottom-color:#0085c9}}

/* Split: portrait left, bio text right. Mirrors about-split. */
html body #et-main-area .bio-split{{padding:40px 0 44px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .bio-split .grid{{display:grid;grid-template-columns:1fr 1.3fr;gap:48px;align-items:stretch}}
html body #et-main-area .bio-split .photo{{overflow:hidden;background:#f6f4ef;min-height:100%;border-radius:4px}}
html body #et-main-area .bio-split .photo img{{width:100%;height:100%;object-fit:cover;display:block}}
html body #et-main-area .bio-split .copy{{display:flex;flex-direction:column}}
html body #et-main-area .bio-split h2{{font-size:clamp(20px,2.2vw,26px);font-weight:600;letter-spacing:-0.015em;line-height:1.2;margin:0 0 16px;color:#1a1d21}}
html body #et-main-area .bio-split p{{font-size:16px;line-height:1.7;color:#3a4048;margin:0 0 16px}}
html body #et-main-area .bio-split p:last-child{{margin:0}}

/* Credentials strip (verifiable facts). Blue brand band, matches about-coverage style. */
html body #et-main-area .bio-creds{{background:#0085c9;padding:40px 0;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .bio-creds .eyebrow{{text-align:center;margin:0 0 24px;color:rgba(255,255,255,.9) !important}}
html body #et-main-area .bio-creds .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;max-width:1080px;margin:0 auto}}
html body #et-main-area .bio-creds .item{{text-align:center;padding:0 10px}}
html body #et-main-area .bio-creds .item .num{{font-size:clamp(22px,2.4vw,32px);font-weight:500;color:#fff;letter-spacing:-0.02em;line-height:1;margin-bottom:10px}}
html body #et-main-area .bio-creds .item .lab{{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.85);font-weight:600;line-height:1.4}}

/* Expertise + method section. Clean content block. */
html body #et-main-area .bio-method{{padding:48px 0;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .bio-method .inner{{max-width:800px;margin:0 auto}}
html body #et-main-area .bio-method h2{{font-size:clamp(22px,2.4vw,30px);font-weight:600;letter-spacing:-0.015em;line-height:1.2;margin:0 0 20px;color:#1a1d21}}
html body #et-main-area .bio-method h3{{font-size:clamp(17px,1.6vw,20px);font-weight:600;letter-spacing:-0.01em;line-height:1.3;color:#1a1d21;margin:28px 0 10px}}
html body #et-main-area .bio-method p{{font-size:16px;line-height:1.7;color:#3a4048;margin:0 0 16px}}
html body #et-main-area .bio-method ul{{margin:0 0 16px;padding:0 0 0 22px}}
html body #et-main-area .bio-method ul li{{font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 8px}}
html body #et-main-area .bio-method a{{color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1;font-weight:500;transition:border-color .2s}}
html body #et-main-area .bio-method a:hover{{border-bottom-color:#0085c9}}

/* Published writing + press (E-E-A-T boost: links to every piece he authored). */
html body #et-main-area .bio-pubs{{padding:40px 0;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .bio-pubs .inner{{max-width:1080px;margin:0 auto}}
html body #et-main-area .bio-pubs .head{{margin:0 0 24px}}
html body #et-main-area .bio-pubs h2{{font-size:clamp(20px,2.2vw,26px);font-weight:600;letter-spacing:-0.015em;line-height:1.2;margin:0;color:#1a1d21}}
html body #et-main-area .bio-pubs .cols{{display:grid;grid-template-columns:1fr 1fr;gap:40px}}
html body #et-main-area .bio-pubs .col h3{{font-size:14px;letter-spacing:.1em;text-transform:uppercase;color:#5a6069;font-weight:600;margin:0 0 14px;padding:0 0 10px;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .bio-pubs ul{{list-style:none;margin:0;padding:0}}
html body #et-main-area .bio-pubs li{{padding:10px 0;border-bottom:1px solid #e2ddd0;font-size:15px;line-height:1.5}}
html body #et-main-area .bio-pubs li:last-child{{border-bottom:0}}
html body #et-main-area .bio-pubs li a{{color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1;font-weight:500;transition:color .2s,border-color .2s}}
html body #et-main-area .bio-pubs li a:hover{{color:#0a5c8a;border-bottom-color:#0085c9}}
html body #et-main-area .bio-pubs li .src{{display:block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#7a828c;margin-top:4px;font-weight:500}}

/* Projects led (links to indexed project pages = internal linking boost). */
html body #et-main-area .bio-projects{{padding:40px 0;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .bio-projects .inner{{max-width:1080px;margin:0 auto}}
html body #et-main-area .bio-projects h2{{font-size:clamp(20px,2.2vw,26px);font-weight:600;letter-spacing:-0.015em;line-height:1.2;margin:0 0 20px;color:#1a1d21}}
html body #et-main-area .bio-projects p.lead{{font-size:16px;line-height:1.65;color:#3a4048;margin:0 0 20px;max-width:60ch}}
html body #et-main-area .bio-projects .chips{{display:flex;flex-wrap:wrap;gap:4px 0;margin:0;line-height:2.2}}
html body #et-main-area .bio-projects .chips a{{display:inline-block;color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1;font-size:16px;font-weight:500;padding:0 2px;transition:border-color .2s,color .2s}}
html body #et-main-area .bio-projects .chips a:hover{{border-bottom-color:#0085c9;color:#0a5c8a}}
html body #et-main-area .bio-projects .chips .sep{{color:#c5cbd2;margin:0 14px;user-select:none;font-weight:400}}

/* CTA (matches guide-cta on other pages for consistency). */
html body #et-main-area .bio-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center}}
html body #et-main-area .bio-cta h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.2;margin:0 0 12px;color:#fff}}
html body #et-main-area .bio-cta p{{font-size:15px;line-height:1.6;color:rgba(255,255,255,.92);margin:0 0 24px;max-width:52ch;margin-left:auto;margin-right:auto}}
html body #et-main-area .bio-cta .btn{{display:inline-block;background:#fff;color:#0085c9;font-size:14px;font-weight:600;letter-spacing:.02em;padding:14px 32px;text-decoration:none;border-radius:2px;transition:opacity .2s}}
html body #et-main-area .bio-cta .btn:hover{{opacity:.9}}

/* Mobile */
@media (max-width:900px){{
  html body #et-main-area .bio-split .grid{{grid-template-columns:1fr;gap:28px}}
  html body #et-main-area .bio-split .photo{{max-height:420px}}
  html body #et-main-area .bio-creds .grid{{grid-template-columns:repeat(2,1fr);gap:24px}}
  html body #et-main-area .bio-pubs .cols{{grid-template-columns:1fr;gap:28px}}
}}
@media (max-width:640px){{
  html body #et-main-area .bio-hero{{padding:32px 0 24px}}
  html body #et-main-area .bio-split{{padding:28px 0 32px}}
  html body #et-main-area .bio-creds{{padding:28px 0}}
  html body #et-main-area .bio-method{{padding:32px 0}}
  html body #et-main-area .bio-pubs{{padding:32px 0}}
  html body #et-main-area .bio-projects{{padding:32px 0}}
}}
{CSS_END}
"""


def build_schema():
    person = {
        "@type": "Person",
        "@id": f"{PAGE_URL}#person",
        "name": "Jas Sidhu",
        "alternateName": ["J. Sidhu"],
        "jobTitle": "Owner and Custom Home Builder",
        "url": PAGE_URL,
        "image": PHOTO_URL,
        "worksFor": {"@type": "Organization", "@id": f"{BIZ_URL}/#organization", "name": "Palermo Homes"},
        "knowsAbout": [
            "Custom home construction",
            "Whole-home renovation",
            "Fixed-price construction contracts",
            "Hillside residential construction",
            "Geotechnical requirements for sloped lots",
            "BC Housing Residential Builder requirements",
            "2-5-10 New Home Warranty program",
            "BC Energy Step Code compliance",
            "Development Permits and building permits in the Okanagan",
            "Construction mortgages and progress draw financing",
            "BC Builders Lien Act holdback administration",
            "Okanagan Valley custom home design",
            "Lower Mainland custom home construction",
        ],
        "memberOf": [
            {"@type": "Organization", "name": "Canadian Home Builders' Association of British Columbia", "url": "https://chbabc.org/"},
        ],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "West Kelowna",
            "addressRegion": "BC",
            "addressCountry": "CA",
        },
        "telephone": "+1-778-760-4113",
        "hasCredential": [
            {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "license",
                "name": "BC Housing Licensed Residential Builder",
                "identifier": "42812",
                "recognizedBy": {"@type": "Organization", "name": "BC Housing", "url": "https://www.bchousing.org/licensing-consumer-services/for-licensed-builders"},
            },
            {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "registration",
                "name": "BC Corporate Registration",
                "identifier": "BC1017682",
                "recognizedBy": {"@type": "Organization", "name": "BC Registries and Online Services"},
            },
        ],
    }

    breadcrumbs = {
        "@type": "BreadcrumbList",
        "@id": f"{PAGE_URL}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BIZ_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "About", "item": f"{BIZ_URL}/about/"},
            {"@type": "ListItem", "position": 3, "name": "Jas Sidhu", "item": PAGE_URL},
        ],
    }

    webpage = {
        "@type": "ProfilePage",
        "@id": PAGE_URL,
        "url": PAGE_URL,
        "name": "Jas Sidhu, Owner of Palermo Homes | Custom Home Builder in Kelowna, BC",
        "description": "Jas Sidhu is the owner of Palermo Homes, a custom home builder based in West Kelowna, BC. BC Housing Licensed Residential Builder number 42812. Over 15 years of custom home construction experience across the Okanagan, Fraser Valley, and Lower Mainland.",
        "isPartOf": {"@id": f"{BIZ_URL}/#website"},
        "breadcrumb": {"@id": f"{PAGE_URL}#breadcrumb"},
        "mainEntity": {"@id": f"{PAGE_URL}#person"},
        "inLanguage": "en",
        "dateModified": MODIFIED_DATE,
    }

    graph = {"@context": "https://schema.org", "@graph": [webpage, breadcrumbs, person]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


TITLE = "Jas Sidhu, Owner | Custom Home Builder | Palermo Homes"
META_DESC = "Jas Sidhu is the owner of Palermo Homes, a custom home builder in West Kelowna, BC. BC Housing Licensed Residential Builder 42812."
CANONICAL = PAGE_URL
OG_TITLE = "Jas Sidhu, Owner of Palermo Homes"
READING_TIME = "4 minutes"

MAIN_HTML = f"""
<div class="bio">
  <section class="bio-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">Home</a><span class="sep">&middot;</span><a href="/about/">About</a><span class="sep">&middot;</span>Jas Sidhu</p>
      <h1>Jas Sidhu</h1>
      <p class="role">Owner, Palermo Homes</p>
      <p class="sub">Jas is the owner of Palermo Homes, a custom home builder based in West Kelowna, BC. He leads every build from first design meeting to final walkthrough, across the Central Okanagan and Lower Mainland.</p>
      <a class="top-cta" href="tel:+17787604113" aria-label="Call 778-760-4113">(778) 760-4113</a>
    </div>
  </section>

  <section class="bio-split">
    <div class="wrap">
      <div class="grid">
        <div class="photo">
          <img src="/wp-content/uploads/2020/03/TCP_1620.jpg" alt="Jas Sidhu, owner of Palermo Homes, custom home builder in West Kelowna, BC" width="1200" height="852">
        </div>
        <div class="copy">
          <h2>About Jas</h2>
          <p>Jas Sidhu has led Palermo Homes for over 15 years, building custom homes and whole-home renovations across Kelowna, West Kelowna, Lake Country, Peachland, Penticton, Vernon, and the Lower Mainland.</p>
          <p>His approach is grounded in three things: fixed-price contracts with transparent line-item budgeting, documented change orders so clients are never surprised, and senior on-site project management on every build. The result is a track record of homes delivered on budget, on schedule, and with the kind of finish quality that gets referenced in neighbourhood architectural reviews.</p>
          <p>Palermo Homes operates under BC Housing Licensed Residential Builder number 42812 and BC Corporate Registration BC1017682. The company is a member of the Canadian Home Builders' Association of British Columbia.</p>
          <p>Jas lives and works in the Central Okanagan and personally manages site visits across the service area. For a conversation about your lot, your design goals, or your timeline, reach him at <a href="tel:+17787604113" style="color:#0085c9;text-decoration:none;border-bottom:1px solid #cfe6f1;font-weight:600">(778) 760-4113</a>.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="bio-creds">
    <div class="wrap">
      <p class="eyebrow">Verifiable credentials</p>
      <div class="grid">
        <div class="item">
          <div class="num">15+</div>
          <div class="lab">Years building<br>in the Okanagan</div>
        </div>
        <div class="item">
          <div class="num">42812</div>
          <div class="lab">BC Housing<br>Licensed Builder</div>
        </div>
        <div class="item">
          <div class="num">BC1017682</div>
          <div class="lab">BC Corporate<br>Registration</div>
        </div>
        <div class="item">
          <div class="num">7</div>
          <div class="lab">Okanagan + BC<br>service areas</div>
        </div>
      </div>
    </div>
  </section>

  <section class="bio-method">
    <div class="wrap">
      <div class="inner">
        <h2>How Jas builds</h2>
        <p>Every Palermo Homes project runs on the same three operating principles. These are the things Jas insists on with every client before a contract is signed.</p>

        <h3>Fixed-price contracts, not cost-plus</h3>
        <p>Jas does not run cost-plus builds. Every Palermo contract is fixed-price with documented allowances for finishes. Clients know their number before construction starts, and the number does not creep because the builder is incentivized to control cost.</p>

        <h3>Senior on-site project management</h3>
        <p>Jas is personally involved in every project. Clients do not get handed off to a junior PM running six other jobs. Decisions get made, not deferred.</p>

        <h3>Documented change orders</h3>
        <p>If something changes during construction, it gets priced, written up, and signed before work starts. No verbal handshakes that turn into disputes.</p>

        <p>If you want the full version of this philosophy applied to choosing any Kelowna builder, Jas wrote the <a href="/guides/how-to-choose-custom-home-builder-kelowna/">builder selection guide</a> that walks through the seven verification steps every homeowner should run before signing anything.</p>
      </div>
    </div>
  </section>

  <section class="bio-pubs">
    <div class="wrap">
      <div class="inner">
        <div class="head">
          <h2>Published writing and media</h2>
        </div>
        <div class="cols">
          <div class="col">
            <h3>Guides authored on palermohomes.com</h3>
            <ul>
              <li><a href="/guides/custom-home-cost-kelowna/">What Is the Typical Cost to Build a Custom Home in Kelowna in 2026?</a><span class="src">Palermo Homes Guide</span></li>
              <li><a href="/guides/how-to-choose-custom-home-builder-kelowna/">How to Choose a Custom Home Builder in Kelowna: A 2026 Guide</a><span class="src">Palermo Homes Guide</span></li>
              <li><a href="/guides/how-long-to-build-custom-home-kelowna/">How Long Does It Take to Build a Custom Home in Kelowna? 2026 Timeline Guide</a><span class="src">Palermo Homes Guide</span></li>
              <li><a href="/guides/fixed-price-vs-cost-plus-custom-home-kelowna/">Fixed-Price vs Cost-Plus Contracts for Custom Homes in BC: A 2026 Guide</a><span class="src">Palermo Homes Guide</span></li>
              <li><a href="/guides/hillside-custom-home-kelowna/">Hillside Custom Home Builds in Kelowna and the Okanagan: Costs, Permits, and Timeline</a><span class="src">Palermo Homes Guide</span></li>
              <li><a href="/guides/custom-home-permits-okanagan/">Custom Home Permits in Kelowna and the Okanagan: A 2026 Guide to Fees, Timelines, and Requirements</a><span class="src">Palermo Homes Guide</span></li>
              <li><a href="/guides/whole-home-renovation-cost-okanagan/">Whole-Home Renovation Cost in Kelowna and the Okanagan: 2026 Pricing Guide</a><span class="src">Palermo Homes Guide</span></li>
              <li><a href="/guides/custom-home-building-process-kelowna/">The Custom Home Building Process in Kelowna: A Phase-by-Phase 2026 Guide</a><span class="src">Palermo Homes Guide</span></li>
              <li><a href="/guides/financing-custom-home-bc/">Financing a Custom Home in BC: Construction Mortgages, Progress Draws, and Builders Lien Act Holdback</a><span class="src">Palermo Homes Guide</span></li>
            </ul>
          </div>
          <div class="col">
            <h3>External publications</h3>
            <ul>
              <li><a href="https://www.linkedin.com/pulse/building-custom-home-kelowna-what-actually-matters-2026-msiuc/" rel="noopener">Building a Custom Home in Kelowna: What Actually Matters in 2026</a><span class="src">LinkedIn Pulse</span></li>
              <li><a href="https://palermohomes.substack.com/p/the-real-cost-of-building-a-custom" rel="noopener">The Real Cost of Building a Custom Home in the Okanagan</a><span class="src">Palermo Homes Substack</span></li>
              <li><a href="https://medium.com/@jordydhillon2005/how-to-choose-a-custom-home-builder-in-kelowna-a-2026-guide-079e8355d639" rel="noopener">How to Choose a Custom Home Builder in Kelowna: A 2026 Guide</a><span class="src">Medium (industry commentary)</span></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="bio-projects">
    <div class="wrap">
      <div class="inner">
        <h2>Recent projects led by Jas</h2>
        <p class="lead">A selection of custom homes Jas has personally overseen as owner of Palermo Homes. Full project galleries are available on each project page.</p>
        <div class="chips">
          <a href="/project/cabernet-2/">Cabernet Way</a><span class="sep">&middot;</span>
          <a href="/project/malbec-place-1/">Malbec Place</a><span class="sep">&middot;</span>
          <a href="/project/touriga-place-1/">Touriga Place</a><span class="sep">&middot;</span>
          <a href="/project/vineyard-estates-3/">Vineyard Estates</a><span class="sep">&middot;</span>
          <a href="/project/lakestone/">Lakestone</a><span class="sep">&middot;</span>
          <a href="/project/eagle-mountain-1/">Eagle Mountain</a><span class="sep">&middot;</span>
          <a href="/project/verado-court/">Verado Court</a><span class="sep">&middot;</span>
          <a href="/project/west-abbotsford/">West Abbotsford</a><span class="sep">&middot;</span>
          <a href="/projects/">All projects</a>
        </div>
      </div>
    </div>
  </section>

  <section class="bio-cta">
    <div class="wrap">
      <h2>Planning a custom home in the Okanagan?</h2>
      <p>Jas takes the first call personally. Tell him about your lot, your design priorities, and your rough timeline. No pressure, no sales script.</p>
      <a class="btn" href="/contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""


def render():
    schema_block = build_schema()
    html = SHELL_HEAD + MAIN_HTML + SHELL_FOOT
    # Strip prior AUTHOR-BIO CSS block (idempotent)
    html = re.sub(r"/\* ==== AUTHOR-BIO CSS START ==== \*/.*?/\* ==== AUTHOR-BIO CSS END ==== \*/", "", html, flags=re.DOTALL)
    # Strip About shell's own CSS block (we're on a new page, not About)
    html = re.sub(r"/\* ==== ABOUT-V2 CSS START ==== \*/.*?/\* ==== ABOUT-V2 CSS END ==== \*/", "", html, flags=re.DOTALL)
    # Inject our CSS
    html = html.replace("</head>", f"<style>{CSS}</style></head>", 1)
    # Title, meta description, canonical
    html = re.sub(r'<title>[^<]*</title>', f'<title>{TITLE}</title>', html, count=1)
    # Strip any existing meta description (any attribute order), inject fresh
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{META_DESC}"/>\n</head>', 1)
    # Strip any existing canonical tag (any attribute order), inject fresh
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{CANONICAL}"/>\n</head>', 1)
    # OG + Twitter tags (same fix pattern as the guide pages)
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
    # Add og:description + og:image (photo of Jas = perfect social preview)
    html = re.sub(r'<meta content="[^"]*" property="og:description"/>\n?', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:image"/>\n?', '', html)
    html = re.sub(
        r'(<meta content="[^"]*" property="og:site_name"/>)',
        r'\1' + f'\n<meta content="{META_DESC}" property="og:description"/>\n<meta content="{PHOTO_URL}" property="og:image"/>',
        html, count=1,
    )
    # Also set og:type to profile (correct type for a Person page)
    html = re.sub(
        r'<meta content="[^"]*" property="og:type"/>',
        '<meta content="profile" property="og:type"/>', html, count=1,
    )
    # Strip Yoast About-page schema (conflicts with our Person schema)
    html = re.sub(r'<script class="yoast-schema-graph"[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    # Preload the hero portrait so social-click LCP is fast
    html = re.sub(
        r'<link rel="preload" as="image" href="[^"]*" fetchpriority="high">',
        f'<link rel="preload" as="image" href="{PHOTO_URL}" fetchpriority="high">',
        html, count=1,
    )
    # Inject our schema before </head>
    html = html.replace("</head>", schema_block + "</head>", 1)

    out = SITE / "about" / "jas-sidhu" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    render()
    print("Done. Built /about/jas-sidhu/ author bio page.")
