"""Add proper <meta name="description"> tags to every individual project page.

Google was falling back to scraping page content (which grabbed leftover Divi
navigation cruft like "← PREV NEXT → ASSOCIATED WITH: +") because these pages
had no meta description. Fixes the sitelinks in search results.
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

# slug -> meta description (target ~130-155 chars, must include location + brand)
DESCRIPTIONS = {
    # Cabernet Way (West Kelowna wine district)
    '1252':         "Modern lakeview custom home on Cabernet Way in West Kelowna. Designed and built by Palermo Homes. View the project gallery.",
    'cabernet-2':   "Luxury modern custom home on Cabernet Way, West Kelowna. Full lakeview siting and in-house finish carpentry by Palermo Homes.",
    'cabernet-3':   "Modern hillside custom home on Cabernet Way in West Kelowna. Terraced build with valley views by Palermo Homes. View the project gallery.",

    # Malbec Place (West Kelowna)
    'malbec-place-1': "Modern lakeview custom home on Malbec Place, West Kelowna. Wine district build by Palermo Homes. View the project gallery.",
    'malbec-2':       "Luxury modern custom home on Malbec Place, West Kelowna. Wine district build by Palermo Homes. See the completed project.",

    # Touriga Place (West Kelowna)
    'touriga-place-1': "Modern lakeview custom home on Touriga Place in West Kelowna's wine district. Designed and built by Palermo Homes. View the gallery.",

    # Vineyard Estates (West Kelowna)
    'vineyard-estates-3': "Luxury custom home in Vineyard Estates, West Kelowna. Modern hillside build by Palermo Homes. View the project.",
    'vineyard-estates-4': "Modern hillside custom home in Vineyard Estates, West Kelowna. Custom design and build by Palermo Homes.",

    # Eagle Mountain (Abbotsford, Fraser Valley)
    'eagle-mountain-1': "Modern custom home on Mahogany Drive in Eagle Mountain, Abbotsford. Designed and built by Palermo Homes. View the full project gallery.",
    'eagle-mountain-2': "Luxury mountain-view custom home on Mahogany Drive, Eagle Mountain, Abbotsford. Custom design and build by Palermo Homes.",
    'eagle-mountain-3': "Custom home on Aquila Drive in Eagle Mountain, Abbotsford. Modern architecture and hillside engineering by Palermo Homes. View the gallery.",
    'eagle-mountain-4': "Executive modern custom home on Montana Place, Eagle Mountain, Abbotsford. Custom build by Palermo Homes. See the completed project.",
    'eagle-mountain-5': "Hillside walkout custom home on Eagle Peak Drive in Eagle Mountain, Abbotsford. Designed and built by Palermo Homes. View the gallery.",
    'eagle-mountain-6': "Modern family custom home on Eagle Summit Drive in Abbotsford. Designed and built by Palermo Homes. See the full project gallery.",
    'eagle-mountain-9': "Modern valley-view custom home on Verado Court, Eagle Mountain, Abbotsford. Custom build by Palermo Homes. View the completed home.",
    'verado-court':     "Custom home on Verado Court in Eagle Mountain, Abbotsford. Designed and built by Palermo Homes. View the project gallery.",
    '713':              "New-build custom home on Eagle Summit Drive in Abbotsford, BC. Custom design and construction by Palermo Homes. See the gallery.",

    # Ledgestone Road (Lake Country) - Hometown Heroes 2022 grand prize
    'lakestone': "Custom home on Ledgestone Road in Lake Country, BC. Grand prize of the Hometown Heroes Lottery 2022. Designed and built by Palermo Homes.",

    # West Abbotsford
    'west-abbotsford': "Modern custom home in West Abbotsford, BC. Designed and built by Palermo Homes. View the completed project gallery.",
}

# Regex helpers
DESC_META_RE   = re.compile(r'<meta[^>]*name="description"[^>]*/?>')
OGDESC_META_RE = re.compile(r'<meta[^>]*property="og:description"[^>]*/?>')
TITLE_END_RE   = re.compile(r'(</title>)')


def apply(slug: str, desc: str) -> bool:
    p = SITE / "project" / slug / "index.html"
    if not p.exists():
        print(f"  MISSING: {slug}")
        return False
    html = p.read_text(encoding="utf-8")
    original = html

    desc_tag   = f'<meta content="{desc}" name="description"/>'
    ogdesc_tag = f'<meta content="{desc}" property="og:description"/>'

    # Handle description
    if DESC_META_RE.search(html):
        html = DESC_META_RE.sub(desc_tag, html, count=1)
    else:
        html = TITLE_END_RE.sub(r'\1\n' + desc_tag, html, count=1)

    # Handle og:description
    if OGDESC_META_RE.search(html):
        html = OGDESC_META_RE.sub(ogdesc_tag, html, count=1)
    else:
        # Insert right after description
        html = html.replace(desc_tag, desc_tag + "\n" + ogdesc_tag, 1)

    if html != original:
        p.write_text(html, encoding="utf-8")
        print(f"  updated: {slug}  ({len(desc)} chars)")
        return True
    print(f"  no-op:   {slug}")
    return False


def main():
    print("Adding meta descriptions to project detail pages...")
    n = 0
    for slug, desc in DESCRIPTIONS.items():
        if apply(slug, desc):
            n += 1
    print(f"Done. Updated {n}/{len(DESCRIPTIONS)} pages.")


if __name__ == "__main__":
    main()
