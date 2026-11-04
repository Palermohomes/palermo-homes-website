"""Hybrid alt-text enhancement:
1) Hero images get specific descriptions based on what is actually visible in the photo
   (reviewed by hand, no invented details).
2) All other project gallery images get a positional index appended to the project+city label
   so each image on the same page has a unique alt.
3) Everything else (brand logos, badges, etc.) kept as-is.
Idempotent. Safe to rerun.
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

# Hero image overrides. Keyed by image path substring (unique enough to match).
# Each description is factual, based on what the image shows.
HERO_ALTS: dict[str, str] = {
    "2025/12/Cabernet-02.jpg":
        "Modern two-storey hillside custom home exterior at dusk by Palermo Homes on Cabernet Way, West Kelowna, with stone and black cladding and Okanagan Lake in the background",
    "2025/12/Touriga-109.jpg":
        "Single-storey modern custom home exterior at dusk by Palermo Homes on Touriga Place, West Kelowna, with glass garage doors and a panoramic Okanagan Lake view",
    "2025/12/1587-Malbec-14.jpg":
        "Two-storey modern custom home exterior at dusk by Palermo Homes on Malbec Place, West Kelowna, with stone and wood cladding and lit interior windows",
    "2026/01/1583-Malbec-13.jpg":
        "Two-storey modern custom home exterior at dusk by Palermo Homes on Malbec Place, West Kelowna, with white stucco and wood cladding and a glass garage door",
    "2026/01/1556-Cabernet-nate-42.jpg":
        "Modern two-storey hillside custom home exterior by Palermo Homes on Cabernet Way, West Kelowna, with a triple garage and clear blue sky",
    "2026/01/fplNrDJA.jpeg":
        "Modern two-storey hillside custom home exterior at dusk by Palermo Homes on Cabernet Way, West Kelowna, with wood and stucco cladding and a mountain backdrop",
    "2022/04/PAL_220411_Main2.jpg":
        "Modern two-storey walkout custom home exterior by Palermo Homes on Ledgestone Road, Lakestone, Lake Country, with wood and stucco cladding and a forested hillside backdrop",
    "2023/08/095-1524-Cabernet-Wy-95_2.jpg":
        "Luxury two-storey custom home exterior at dusk by Palermo Homes in Vineyard Estates, West Kelowna, with stone columns, a wide double garage, and warm interior lighting",
    "2023/08/Vineyard-Estates-3-Re-Sized-Photo_2.jpg":
        "Minimalist white kitchen interior by Palermo Homes in a Vineyard Estates custom home, West Kelowna, with three cylindrical pendant lights, a white marble island, walnut cabinetry base, and white oak flooring",
    "2020/05/PAL_Projects_NewHouse_FEATURE.jpg":
        "Modern two-storey custom home exterior by Palermo Homes on Eagle Summit Drive, Abbotsford, with dark grey siding, white stucco, stone accents, and a long concrete driveway",
    "2019/06/PAL_Projects_Mahogany_FEATURE.jpg":
        "Two-storey hillside custom home exterior by Palermo Homes on Mahogany Drive, Eagle Mountain, Abbotsford, with stone and shingle cladding, a wood beam entry, and boulder landscaping",
    "2019/06/PAL_Projects_Mahogany2_FEATURE.jpg":
        "Two-storey modern custom home exterior by Palermo Homes on Mahogany Drive, Eagle Mountain, Abbotsford, with grey board-and-batten siding, a shed roof, and a glass garage door",
    "2019/06/2773-Aquila-Drive-Abbotsford-1.jpg":
        "Luxury two-storey modern custom home exterior at dusk by Palermo Homes on Aquila Drive, Eagle Mountain, Abbotsford, with stone columns, wood cladding, glass railings, and a forested hillside backdrop",
    "2019/06/PAL_Projects_EagleSummit_FEATURE.jpg":
        "Three-storey modern custom home exterior at dusk by Palermo Homes on Montana Place, Eagle Mountain, Abbotsford, with grey siding, stone accents, glass railings, and wood beam entry",
    "2019/06/35624-Eagle-Peak-Drive-5.jpg":
        "Two-storey craftsman custom home exterior by Palermo Homes on Eagle Peak Drive, Eagle Mountain, Abbotsford, with grey siding, stone accents, triangular rooflines, and well-landscaped yard",
    "2019/07/PAL_Projects_GreenChairs_Row1a.jpg":
        "Craftsman-modern two-storey custom home exterior at dusk by Palermo Homes on Eagle Summit Drive, Abbotsford, with grey siding, cedar shingles, wood post entry, and a stone-faced glass garage",
    "2023/08/WhatsApp-Image-2026-01-22-at-22.41.31-6.jpeg":
        "Modern two-storey custom home exterior at dusk by Palermo Homes on Verado Court, Eagle Mountain, Abbotsford, with wood plank cladding, stone columns, and a glass garage door",
    "2021/10/PAL_Projects_Verado_FEATURE211005.jpg":
        "Two-storey modern custom home exterior at sunset by Palermo Homes on Verado Court, Eagle Mountain, Abbotsford, with orange cedar cladding, a wood entry door, and glass garage",
    "2019/06/PAL_Projects_Cambie_FEATURE-e1571985525124.jpg":
        "Two-storey craftsman custom home exterior by Palermo Homes in West Abbotsford, with grey siding, stone accents, bay window, gabled roof, and flower gardens in bloom",
}

# Project slug -> (project name, city) for positional alts on project pages
PROJECT_META = {
    "1252":                ("Modern Lakeview Custom Home on Cabernet Way",      "West Kelowna"),
    "713":                 ("Custom Home on Eagle Summit Drive",                "Abbotsford"),
    "cabernet-2":          ("Luxury Modern Custom Home on Cabernet Way",        "West Kelowna"),
    "cabernet-3":          ("Modern Hillside Custom Home on Cabernet Way",      "West Kelowna"),
    "eagle-mountain-1":    ("Modern Custom Home on Mahogany Drive",             "Eagle Mountain, Abbotsford"),
    "eagle-mountain-2":    ("Luxury Mountain View Custom Home on Mahogany Drive","Eagle Mountain, Abbotsford"),
    "eagle-mountain-3":    ("Custom Home on Aquila Drive",                      "Eagle Mountain, Abbotsford"),
    "eagle-mountain-4":    ("Executive Modern Custom Home on Montana Place",    "Eagle Mountain, Abbotsford"),
    "eagle-mountain-5":    ("Hillside Walkout Custom Home on Eagle Peak Drive", "Eagle Mountain, Abbotsford"),
    "eagle-mountain-6":    ("Modern Family Custom Home on Eagle Summit Drive",  "Abbotsford"),
    "eagle-mountain-9":    ("Modern Valley View Custom Home on Verado Court",   "Eagle Mountain, Abbotsford"),
    "lakestone":           ("Custom Home on Ledgestone Road",                   "Lake Country"),
    "malbec-2":            ("Luxury Modern Custom Home on Malbec Place",        "West Kelowna"),
    "malbec-place-1":      ("Modern Lakeview Custom Home on Malbec Place",      "West Kelowna"),
    "touriga-place-1":     ("Modern Lakeview Custom Home on Touriga Place",     "West Kelowna"),
    "verado-court":        ("Custom Home on Verado Court",                      "Eagle Mountain, Abbotsford"),
    "vineyard-estates-3":  ("Luxury Custom Home in Vineyard Estates",           "West Kelowna"),
    "vineyard-estates-4":  ("Modern Hillside Custom Home in Vineyard Estates",  "West Kelowna"),
    "west-abbotsford":     ("Custom Home in West Abbotsford",                   "Abbotsford"),
}

LOGO_PATTERNS = ("palermo-logo", "logolockup", "pal_logo")


def hero_alt_for(src: str) -> str | None:
    """Return the specific hero description if this src matches one we reviewed."""
    low = src.lower()
    for key, alt in HERO_ALTS.items():
        if key.lower() in low:
            return alt
    return None


def process(path: Path) -> tuple[int, int]:
    """Returns (heroes_applied, positional_applied)."""
    html = path.read_text(encoding="utf-8")
    body_m = re.search(r"<body[^>]*>", html)
    if not body_m:
        return (0, 0)
    body_start = body_m.end()
    body = html[body_start:]

    parts = path.relative_to(SITE).parts
    project_slug = parts[1] if len(parts) >= 2 and parts[0] == "project" else None

    heroes = [0]
    positional = [0]
    counter = [0]  # per-page counter for non-hero project images

    def fix(m):
        tag = m.group(0)
        src_m = re.search(r'src="([^"]+)"', tag)
        if not src_m:
            return tag
        src = src_m.group(1)
        low_src = src.lower()
        # Skip logos
        if any(p in low_src for p in LOGO_PATTERNS):
            return tag

        # 1) Hero override (highest priority)
        hero = hero_alt_for(src)
        if hero:
            # Replace existing alt attribute
            if 'alt="' in tag:
                tag = re.sub(r'alt="[^"]*"', f'alt="{hero}"', tag, count=1)
            else:
                tag = tag.replace("<img", f'<img alt="{hero}"', 1)
            heroes[0] += 1
            return tag

        # 2) Positional alt for /project/<slug>/ gallery images (non-hero)
        if project_slug and project_slug in PROJECT_META:
            name, city = PROJECT_META[project_slug]
            counter[0] += 1
            new_alt = f"{name} by Palermo Homes in {city}, gallery view {counter[0]}"
            if 'alt="' in tag:
                # Replace if the alt is the generic repeated one OR already a prior positional variant
                current_alt_m = re.search(r'alt="([^"]*)"', tag)
                if current_alt_m:
                    curr = current_alt_m.group(1)
                    base = f"{name} by Palermo Homes in {city}"
                    if curr == base or curr.startswith(f"{base},") or curr.startswith(f"{base} , "):
                        tag = re.sub(r'alt="[^"]*"', f'alt="{new_alt}"', tag, count=1)
                        positional[0] += 1
            else:
                tag = tag.replace("<img", f'<img alt="{new_alt}"', 1)
                positional[0] += 1
        return tag

    new_body = re.sub(r"<img\b[^>]*>", fix, body)
    if new_body != body:
        path.write_text(html[:body_start] + new_body, encoding="utf-8")
    return (heroes[0], positional[0])


def main():
    total_h = 0
    total_p = 0
    files = 0
    for p in SITE.rglob("index.html"):
        h, pos = process(p)
        if h or pos:
            files += 1
            total_h += h
            total_p += pos
    print(f"Processed {files} pages. Hero alts applied: {total_h}. Positional alts applied: {total_p}.")


if __name__ == "__main__":
    main()
