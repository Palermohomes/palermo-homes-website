"""Replace the project title MAP in update_project_seo_titles.py with ≤62-char versions.
All titles keep city per user's rules."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
f = ROOT / "_build" / "update_project_seo_titles.py"
src = f.read_text(encoding="utf-8")

NEW_MAP = {
    # Cabernet Way (West Kelowna)
    '1252':         ('Lakeview Home on Cabernet Way, West Kelowna | Palermo Homes',
                     'Modern Lakeview Custom Home on Cabernet Way'),
    'cabernet-2':   ('Luxury Home on Cabernet Way, West Kelowna | Palermo Homes',
                     'Luxury Modern Custom Home on Cabernet Way'),
    'cabernet-3':   ('Hillside Home on Cabernet Way, West Kelowna | Palermo Homes',
                     'Modern Hillside Custom Home on Cabernet Way'),
    # Malbec Place
    'malbec-place-1': ('Lakeview Home on Malbec Place, West Kelowna | Palermo Homes',
                       'Modern Lakeview Custom Home on Malbec Place'),
    'malbec-2':       ('Luxury Home on Malbec Place, West Kelowna | Palermo Homes',
                       'Luxury Modern Custom Home on Malbec Place'),
    # Touriga Place
    'touriga-place-1': ('Lakeview Home on Touriga Place, West Kelowna | Palermo Homes',
                        'Modern Lakeview Custom Home on Touriga Place'),
    # Vineyard Estates
    'vineyard-estates-3': ('Luxury Home in Vineyard Estates, West Kelowna | Palermo Homes',
                           'Luxury Custom Home in Vineyard Estates'),
    'vineyard-estates-4': ('Hillside Home, Vineyard Estates, West Kelowna | Palermo Homes',
                           'Modern Hillside Custom Home in Vineyard Estates'),
    # Eagle Mountain (Abbotsford) - all must keep Abbotsford per user
    'eagle-mountain-1': ('Custom Home, Mahogany Dr, Eagle Mountain, Abbotsford | Palermo',
                         'Modern Custom Home on Mahogany Drive, Eagle Mountain'),
    'eagle-mountain-2': ('Luxury Home, Mahogany Dr, Eagle Mountain, Abbotsford | Palermo',
                         'Luxury Mountain View Custom Home on Mahogany Drive, Eagle Mountain'),
    'eagle-mountain-3': ('Custom Home on Aquila Dr, Eagle Mountain, Abbotsford | Palermo',
                         'Custom Home on Aquila Drive, Eagle Mountain'),
    'eagle-mountain-4': ('Custom Home, Montana Pl, Eagle Mountain, Abbotsford | Palermo',
                         'Executive Modern Custom Home on Montana Place, Eagle Mountain'),
    'eagle-mountain-5': ('Hillside Walkout Home, Eagle Mountain, Abbotsford | Palermo',
                         'Hillside Walkout Custom Home on Eagle Peak Drive, Eagle Mountain'),
    'eagle-mountain-6': ('Family Home on Eagle Summit Dr, Abbotsford | Palermo Homes',
                         'Modern Family Custom Home on Eagle Summit Drive'),
    'verado-court':     ('Custom Home on Verado Ct, Eagle Mountain, Abbotsford | Palermo',
                         'Custom Home on Verado Court, Eagle Mountain'),
    '713':              ('Custom Home on Eagle Summit Dr, Abbotsford | Palermo Homes',
                         'New Build Custom Home on Eagle Summit Drive'),
    'eagle-mountain-9': ('Valley View Home, Eagle Mountain, Abbotsford | Palermo',
                         'Modern Valley View Custom Home on Verado Court, Eagle Mountain'),
    # Ledgestone Road (Lake Country) - Option A, drop award
    'lakestone': ('Custom Home on Ledgestone Road, Lake Country | Palermo Homes',
                  'Custom Home on Ledgestone Road, Lake Country'),
    # West Abbotsford
    'west-abbotsford': ('Modern Custom Home in West Abbotsford, BC | Palermo Homes',
                        'Modern Custom Home in West Abbotsford'),
}

# Find start/end of MAP block manually
start = src.find("MAP = {")
assert start != -1, "MAP = { not found"
# Find the matching closing brace at start of a line
end_idx = src.find("\n}\n", start)
assert end_idx != -1, "closing } not found"
end = end_idx + 3

new_map_src = "MAP = {\n"
for slug, (title, h1) in NEW_MAP.items():
    new_map_src += f"    {slug!r:<22}: ({title!r},\n"
    new_map_src += " " * (24 + len(slug) + 2) + f"{h1!r}),\n"
new_map_src += "}\n"
new_src = src[:start] + new_map_src + src[end:]
# Sanity: all titles ≤62
for slug, (title, _) in NEW_MAP.items():
    assert len(title) <= 62, f"TOO LONG {slug}: {len(title)} chars"

f.write_text(new_src, encoding="utf-8")
print(f"Replaced MAP with {len(NEW_MAP)} project titles. All <= 62 chars.")
