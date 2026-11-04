"""One-time (idempotent) SEO title/H1 updater for individual project detail pages.
Data-driven: edit the MAP dict, rerun to apply. Safe to run multiple times."""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

# slug -> (detail_title, detail_h1)
# Detail title pattern: {descriptor} Custom Home on/in {street/community}, {city} | Palermo Homes
MAP = {
    '1252'                : ('Lakeview Home on Cabernet Way, West Kelowna | Palermo Homes',
                              'Modern Lakeview Custom Home on Cabernet Way'),
    'cabernet-2'          : ('Luxury Home on Cabernet Way, West Kelowna | Palermo Homes',
                                    'Luxury Modern Custom Home on Cabernet Way'),
    'cabernet-3'          : ('Hillside Home on Cabernet Way, West Kelowna | Palermo Homes',
                                    'Modern Hillside Custom Home on Cabernet Way'),
    'malbec-place-1'      : ('Lakeview Home on Malbec Place, West Kelowna | Palermo Homes',
                                        'Modern Lakeview Custom Home on Malbec Place'),
    'malbec-2'            : ('Luxury Home on Malbec Place, West Kelowna | Palermo Homes',
                                  'Luxury Modern Custom Home on Malbec Place'),
    'touriga-place-1'     : ('Lakeview Home on Touriga Place, West Kelowna | Palermo Homes',
                                         'Modern Lakeview Custom Home on Touriga Place'),
    'vineyard-estates-3'  : ('Luxury Home in Vineyard Estates, West Kelowna | Palermo Homes',
                                            'Luxury Custom Home in Vineyard Estates'),
    'vineyard-estates-4'  : ('Hillside Home, Vineyard Estates, West Kelowna | Palermo Homes',
                                            'Modern Hillside Custom Home in Vineyard Estates'),
    'eagle-mountain-1'    : ('Custom Home, Mahogany Dr, Eagle Mountain, Abbotsford | Palermo',
                                          'Modern Custom Home on Mahogany Drive, Eagle Mountain'),
    'eagle-mountain-2'    : ('Luxury Home, Mahogany Dr, Eagle Mountain, Abbotsford | Palermo',
                                          'Luxury Mountain View Custom Home on Mahogany Drive, Eagle Mountain'),
    'eagle-mountain-3'    : ('Custom Home on Aquila Dr, Eagle Mountain, Abbotsford | Palermo',
                                          'Custom Home on Aquila Drive, Eagle Mountain'),
    'eagle-mountain-4'    : ('Custom Home, Montana Pl, Eagle Mountain, Abbotsford | Palermo',
                                          'Executive Modern Custom Home on Montana Place, Eagle Mountain'),
    'eagle-mountain-5'    : ('Hillside Walkout Home, Eagle Mountain, Abbotsford | Palermo',
                                          'Hillside Walkout Custom Home on Eagle Peak Drive, Eagle Mountain'),
    'eagle-mountain-6'    : ('Family Home on Eagle Summit Dr, Abbotsford | Palermo Homes',
                                          'Modern Family Custom Home on Eagle Summit Drive'),
    'verado-court'        : ('Custom Home on Verado Ct, Eagle Mountain, Abbotsford | Palermo',
                                      'Custom Home on Verado Court, Eagle Mountain'),
    '713'                 : ('Custom Home on Eagle Summit Dr, Abbotsford | Palermo Homes',
                             'New Build Custom Home on Eagle Summit Drive'),
    'eagle-mountain-9'    : ('Valley View Home, Eagle Mountain, Abbotsford | Palermo',
                                          'Modern Valley View Custom Home on Verado Court, Eagle Mountain'),
    'lakestone'           : ('Custom Home on Ledgestone Road, Lake Country | Palermo Homes',
                                   'Custom Home on Ledgestone Road, Lake Country'),
    'west-abbotsford'     : ('Modern Custom Home in West Abbotsford, BC | Palermo Homes',
                                         'Modern Custom Home in West Abbotsford'),
}

TITLE_RE   = re.compile(r'<title>.*?</title>', re.DOTALL)
OGTITLE_RE = re.compile(r'(<meta\s+content=")[^"]*("\s+property="og:title"/>)')
H1_RE      = re.compile(r'<h1\s+class="entry-title">.*?</h1>', re.DOTALL)
# JSON-LD WebPage.name: "name":"XYZ &#8211; Palermo Homes"
WEBPAGE_NAME_RE = re.compile(r'("@type":"WebPage"[^{}]*?"name":")[^"]*?(&#8211; Palermo Homes")')
# JSON-LD last BreadcrumbList item (ends with "}])
BREADCRUMB_LAST_RE = re.compile(r'("@type":"ListItem","position":\d+,"name":")[^"]*("\}\])')


def update_page(slug: str, title: str, h1: str) -> bool:
    p = SITE / "project" / slug / "index.html"
    if not p.exists():
        print(f"  MISSING: {slug}")
        return False
    html = p.read_text(encoding="utf-8")
    original = html

    html = TITLE_RE.sub(f"<title>{title}</title>", html, count=1)
    html = OGTITLE_RE.sub(lambda m: f'{m.group(1)}{title}{m.group(2)}', html, count=1)
    html = H1_RE.sub(f'<h1 class="entry-title">{h1}</h1>', html, count=1)
    # Schema: WebPage.name. Use H1 for readability
    html = WEBPAGE_NAME_RE.sub(lambda m: f'{m.group(1)}{h1} {m.group(2)}', html, count=1)
    # Schema: last breadcrumb item. Use H1
    html = BREADCRUMB_LAST_RE.sub(lambda m: f'{m.group(1)}{h1}{m.group(2)}', html, count=1)

    if html != original:
        p.write_text(html, encoding="utf-8")
        print(f"  updated: {slug}")
        return True
    print(f"  no-op:   {slug}")
    return False


def main():
    print("Applying SEO titles/H1s to project detail pages...")
    for slug, (title, h1) in MAP.items():
        update_page(slug, title, h1)
    print("Done.")


if __name__ == "__main__":
    main()
