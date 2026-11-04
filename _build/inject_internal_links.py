"""Post-build pass: strengthen internal linking on 24 weak pages.
Approved by user with corrections:
- Only link pages in the same real geographic area
- Eagle Mountain community includes ALL 9 projects (em-1 through -6, em-9, verado-court, 713)
- Vineyard Estates is in Lakeview Heights (confirmed in Lakeview Heights page content)
- Cabernet is NOT in Upper Mission (removed)
- Guides cross-link to sibling guides
Uses natural, descriptive anchor text. Injects into a bounded block so reruns replace cleanly.
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

START = "<!-- INTERNAL-LINKS START -->"
END = "<!-- INTERNAL-LINKS END -->"

# Each key = source page. Value = list of (href, anchor_text) pairs to inject at end of main content.
LINKS: dict[str, list[tuple[str, str]]] = {
    # --- Service area pages: link to each matching project community + project detail + relevant guides
    "service-areas/kelowna/index.html": [
        ("/guides/custom-home-building-process-kelowna/", "The 8-phase custom home building process in Kelowna"),
        ("/guides/custom-home-permits-okanagan/", "Kelowna building permits: fees, timelines, requirements"),
        ("/guides/hillside-custom-home-kelowna/", "Hillside custom home builds in Kelowna"),
        ("/guides/custom-home-cost-kelowna/", "What a custom home costs in Kelowna in 2026"),
    ],
    "service-areas/west-kelowna/index.html": [
        ("/projects/cabernet/", "See all three Cabernet Way builds"),
        ("/projects/malbec/", "View our Malbec Place custom builds"),
        ("/projects/touriga/", "The Touriga Place custom build"),
        ("/projects/vineyard-estates/", "Our Vineyard Estates homes"),
        ("/project/malbec-2/", "A luxury Malbec Place home we completed"),
        ("/project/vineyard-estates-4/", "A hillside home we built in Vineyard Estates"),
        ("/guides/hillside-custom-home-kelowna/", "Hillside custom home builds in West Kelowna"),
        ("/guides/custom-home-permits-okanagan/", "West Kelowna building permits: 15-day target"),
    ],
    "service-areas/lake-country/index.html": [
        ("/projects/ledgestone/", "The Ledgestone Road grand-prize home"),
        ("/neighborhoods/lakestone/", "Custom home builder in Lakestone"),
        ("/guides/custom-home-building-process-kelowna/", "The Kelowna-area custom home building process"),
        ("/guides/custom-home-permits-okanagan/", "Okanagan building permits by municipality"),
    ],
    "service-areas/vernon/index.html": [
        ("/neighborhoods/the-rise/", "The Rise golf-course community in Vernon"),
        ("/neighborhoods/adventure-bay/", "Custom homes in Adventure Bay, Vernon"),
        ("/guides/hillside-custom-home-kelowna/", "Hillside custom home builds in Vernon"),
        ("/guides/custom-home-permits-okanagan/", "Vernon building permit timeline and fees"),
    ],
    "service-areas/penticton/index.html": [
        ("/neighborhoods/naramata-bench/", "Naramata Bench wine country"),
        ("/neighborhoods/skaha-hills/", "Skaha Hills vineyard community"),
        ("/guides/custom-home-permits-okanagan/", "Penticton Residential Xpress permit program"),
        ("/guides/custom-home-building-process-kelowna/", "The 8-phase custom home process"),
    ],
    "service-areas/peachland/index.html": [
        ("/guides/custom-home-permits-okanagan/", "Peachland building permit process (approx 2 weeks)"),
        ("/guides/hillside-custom-home-kelowna/", "Hillside builds on Beach Avenue and Somerset Reach"),
        ("/guides/custom-home-building-process-kelowna/", "The 8-phase custom home building process"),
    ],
    "service-areas/lower-mainland/index.html": [
        ("/projects/eagle-mountain/", "All nine Eagle Mountain builds in Abbotsford"),
        ("/projects/west-abbotsford/", "Our West Abbotsford legacy build"),
        ("/project/713/", "An Eagle Summit Drive custom home in Abbotsford"),
        ("/guides/hillside-custom-home-kelowna/", "Hillside builds on Eagle Mountain and similar grades"),
        ("/guides/custom-home-building-process-kelowna/", "Our 8-phase custom home building process"),
    ],

    # --- Neighborhood pages: link to sibling neighborhoods in same city + the community page + hillside guide where relevant
    "neighborhoods/eagle-mountain/index.html": [
        ("/projects/eagle-mountain/", "See all nine Eagle Mountain custom builds"),
        ("/project/eagle-mountain-1/", "Mahogany Drive custom home"),
        ("/project/eagle-mountain-5/", "Hillside Walkout on Eagle Peak Drive"),
        ("/project/verado-court/", "Custom home on Verado Court"),
        ("/guides/hillside-custom-home-kelowna/", "What hillside builds like Eagle Mountain really cost"),
    ],
    "neighborhoods/lakeview-heights/index.html": [
        ("/projects/vineyard-estates/", "Our Vineyard Estates custom homes"),
        ("/project/vineyard-estates-3/", "Luxury home in Vineyard Estates"),
        ("/project/vineyard-estates-4/", "Hillside home in Vineyard Estates"),
        ("/guides/hillside-custom-home-kelowna/", "Hillside builds in Lakeview Heights: cost and process"),
    ],
    "neighborhoods/upper-mission/index.html": [
        ("/guides/hillside-custom-home-kelowna/", "Hillside builds in Upper Mission: geotech, permits, cost"),
        ("/guides/custom-home-permits-okanagan/", "Kelowna building permit process and fees"),
    ],
    "neighborhoods/kettle-valley/index.html": [
        ("/projects/cabernet/", "Our Cabernet Way custom builds (Kettle Valley)"),
        ("/project/cabernet-2/", "A completed Cabernet Way home"),
        ("/guides/hillside-custom-home-kelowna/", "Hillside builds in Kettle Valley: cost and permits"),
    ],
    "neighborhoods/wilden/index.html": [
        ("/guides/hillside-custom-home-kelowna/", "Hillside builds in Wilden: geotech, DP review, cost"),
        ("/guides/custom-home-building-process-kelowna/", "The 8-phase process for custom builds"),
    ],
    "neighborhoods/the-rise/index.html": [
        ("/neighborhoods/predator-ridge/", "Predator Ridge resort community in Vernon"),
        ("/neighborhoods/adventure-bay/", "Adventure Bay above Okanagan Lake"),
    ],
    "neighborhoods/adventure-bay/index.html": [
        ("/neighborhoods/the-rise/", "The Rise hillside golf community in Vernon"),
        ("/neighborhoods/predator-ridge/", "Predator Ridge resort community in Vernon"),
    ],
    "neighborhoods/predator-ridge/index.html": [
        ("/neighborhoods/the-rise/", "The Rise hillside community in Vernon"),
        ("/neighborhoods/adventure-bay/", "Adventure Bay above Okanagan Lake"),
    ],
    "neighborhoods/naramata-bench/index.html": [
        ("/neighborhoods/skaha-hills/", "Skaha Hills vineyard community in Penticton"),
    ],
    "neighborhoods/skaha-hills/index.html": [
        ("/neighborhoods/naramata-bench/", "Naramata Bench wine country near Penticton"),
    ],
    "neighborhoods/lakestone/index.html": [
        ("/project/lakestone/", "The Ledgestone Road custom home in Lakestone"),
        ("/projects/ledgestone/", "Our Ledgestone Road grand-prize project"),
    ],

    # --- Guides cross-link to sibling guides (older guides get links to newer ones)
    "guides/custom-home-cost-kelowna/index.html": [
        ("/guides/fixed-price-vs-cost-plus-custom-home-kelowna/", "fixed-price vs cost-plus contracts"),
        ("/guides/custom-home-building-process-kelowna/", "the 8-phase custom home building process"),
        ("/guides/financing-custom-home-bc/", "how construction financing works in BC"),
        ("/guides/whole-home-renovation-cost-okanagan/", "whole-home renovation cost comparison"),
        ("/guides/hillside-custom-home-kelowna/", "what hillside builds really cost"),
    ],
    "guides/how-to-choose-custom-home-builder-kelowna/index.html": [
        ("/guides/fixed-price-vs-cost-plus-custom-home-kelowna/", "fixed-price vs cost-plus contracts"),
        ("/guides/custom-home-building-process-kelowna/", "the full 8-phase process your builder manages"),
        ("/guides/custom-home-permits-okanagan/", "permit process your builder should handle"),
    ],
    "guides/how-long-to-build-custom-home-kelowna/index.html": [
        ("/guides/fixed-price-vs-cost-plus-custom-home-kelowna/", "fixed-price vs cost-plus contracts"),
        ("/guides/custom-home-permits-okanagan/", "permit timelines by municipality"),
        ("/guides/hillside-custom-home-kelowna/", "how hillside lots extend the timeline"),
        ("/guides/custom-home-building-process-kelowna/", "the 8-phase process breakdown"),
    ],
    "guides/fixed-price-vs-cost-plus-custom-home-kelowna/index.html": [
        ("/guides/financing-custom-home-bc/", "why lenders require fixed-price for construction mortgages"),
        ("/guides/custom-home-cost-kelowna/", "custom home cost ranges in Kelowna"),
    ],
    # New guides cross-link to each other + back to foundational guides
    "guides/hillside-custom-home-kelowna/index.html": [
        ("/guides/custom-home-permits-okanagan/", "building permits and Development Permit review"),
        ("/guides/custom-home-cost-kelowna/", "full custom home cost ranges in Kelowna"),
        ("/guides/custom-home-building-process-kelowna/", "the 8-phase custom home process"),
    ],
    "guides/custom-home-permits-okanagan/index.html": [
        ("/guides/hillside-custom-home-kelowna/", "hillside lots and Development Permit requirements"),
        ("/guides/custom-home-building-process-kelowna/", "where permits fit in the 8-phase process"),
        ("/guides/financing-custom-home-bc/", "how permits affect construction mortgage approval"),
    ],
    "guides/whole-home-renovation-cost-okanagan/index.html": [
        ("/guides/custom-home-cost-kelowna/", "custom new-build cost comparison"),
        ("/guides/custom-home-permits-okanagan/", "renovation permit requirements and fees"),
        ("/guides/how-long-to-build-custom-home-kelowna/", "renovation vs new-build timeline"),
    ],
    "guides/custom-home-building-process-kelowna/index.html": [
        ("/guides/custom-home-permits-okanagan/", "permit phase deep-dive"),
        ("/guides/hillside-custom-home-kelowna/", "hillside site evaluation details"),
        ("/guides/financing-custom-home-bc/", "financing structure across the process"),
        ("/guides/how-long-to-build-custom-home-kelowna/", "phase-by-phase timeline breakdown"),
    ],
    "guides/financing-custom-home-bc/index.html": [
        ("/guides/fixed-price-vs-cost-plus-custom-home-kelowna/", "fixed-price contracts that lenders require"),
        ("/guides/custom-home-cost-kelowna/", "custom home cost ranges to size your mortgage"),
        ("/guides/custom-home-building-process-kelowna/", "the 8-phase process your draws support"),
    ],

    # --- Services pages: link to all relevant guides
    "services/custom-homes/index.html": [
        ("/guides/custom-home-building-process-kelowna/", "The 8-phase custom home building process"),
        ("/guides/custom-home-cost-kelowna/", "What a custom home costs in Kelowna in 2026"),
        ("/guides/how-long-to-build-custom-home-kelowna/", "How long a custom home takes to build"),
        ("/guides/custom-home-permits-okanagan/", "Permit fees and timelines by municipality"),
        ("/guides/financing-custom-home-bc/", "Construction mortgages and progress draws in BC"),
        ("/guides/hillside-custom-home-kelowna/", "Hillside custom home builds in the Okanagan"),
        ("/guides/fixed-price-vs-cost-plus-custom-home-kelowna/", "Fixed-price vs cost-plus contracts"),
        ("/guides/how-to-choose-custom-home-builder-kelowna/", "How to choose a Kelowna custom home builder"),
    ],
    "services/renovations/index.html": [
        ("/guides/whole-home-renovation-cost-okanagan/", "Whole-home renovation cost in the Okanagan"),
        ("/guides/custom-home-permits-okanagan/", "Renovation permit requirements"),
        ("/guides/how-long-to-build-custom-home-kelowna/", "Renovation and build timelines"),
        ("/guides/fixed-price-vs-cost-plus-custom-home-kelowna/", "Renovation contract structures"),
    ],
    "services/general-contracting/index.html": [
        ("/guides/custom-home-building-process-kelowna/", "The custom home process we coordinate"),
        ("/guides/custom-home-permits-okanagan/", "Permits we handle on your behalf"),
        ("/guides/fixed-price-vs-cost-plus-custom-home-kelowna/", "Contract structures we work with"),
        ("/guides/financing-custom-home-bc/", "Lender-ready documentation we provide"),
    ],
    "services/index.html": [
        ("/guides/custom-home-building-process-kelowna/", "The 8-phase custom home building process"),
        ("/guides/whole-home-renovation-cost-okanagan/", "Whole-home renovation cost guide"),
        ("/guides/custom-home-cost-kelowna/", "Custom home cost ranges in Kelowna"),
        ("/guides/custom-home-permits-okanagan/", "Permits and approvals in the Okanagan"),
    ],

    # --- Core pages that benefit from guide links
    "faq/index.html": [
        ("/guides/custom-home-building-process-kelowna/", "The 8-phase custom home building process"),
        ("/guides/custom-home-cost-kelowna/", "What a custom home costs in Kelowna"),
        ("/guides/custom-home-permits-okanagan/", "Permit fees and timelines by municipality"),
        ("/guides/financing-custom-home-bc/", "Construction mortgages and progress draws"),
        ("/guides/hillside-custom-home-kelowna/", "Hillside custom home builds"),
        ("/guides/whole-home-renovation-cost-okanagan/", "Whole-home renovation cost"),
    ],
    "projects/index.html": [
        ("/guides/custom-home-building-process-kelowna/", "The 8-phase custom home process behind every project"),
        ("/guides/custom-home-cost-kelowna/", "Custom home cost ranges"),
        ("/guides/hillside-custom-home-kelowna/", "Hillside builds like Cabernet Way and Eagle Mountain"),
    ],
}


def build_block(pairs: list[tuple[str, str]], heading: str = "More from Palermo Homes") -> str:
    items = "\n".join(f'    <li><a href="{href}">{text}</a></li>' for href, text in pairs)
    return (
        f'\n{START}\n'
        f'<aside style="max-width:1080px;margin:40px auto 24px;padding:24px clamp(20px,3vw,32px);background:#f6f4ef;border-top:1px solid #e2ddd0;border-bottom:1px solid #e2ddd0;font-family:\'Inter\',system-ui,sans-serif">\n'
        f'  <p style="font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 14px">{heading}</p>\n'
        f'  <ul style="list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:14px 32px;font-size:15px;line-height:1.5">\n'
        f'{items}\n'
        f'  </ul>\n'
        f'</aside>\n'
        f'{END}\n'
    )


def process(rel_path: str, pairs: list[tuple[str, str]]) -> bool:
    p = SITE / rel_path
    if not p.exists():
        print(f"  MISS: {rel_path} not found")
        return False
    html = p.read_text(encoding="utf-8")
    # Strip prior block (idempotent)
    html = re.sub(re.escape(START) + ".*?" + re.escape(END) + r"\n?", "", html, flags=re.DOTALL)
    block = build_block(pairs)
    # Insert right before closing </div> that ends the main content, which is right before <footer>
    footer_m = re.search(r"<footer\b", html)
    if not footer_m:
        print(f"  MISS: no <footer> in {rel_path}")
        return False
    insert_at = footer_m.start()
    html = html[:insert_at] + block + html[insert_at:]
    p.write_text(html, encoding="utf-8")
    return True


def main():
    ok = 0
    for rel, pairs in LINKS.items():
        if process(rel, pairs):
            ok += 1
    print(f"Injected internal-link block on {ok}/{len(LINKS)} pages.")


if __name__ == "__main__":
    main()
