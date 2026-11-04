"""Apply remaining description shortenings per user approval + banned-fact removal."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

replacements = {
    "_build/build_service_areas.py": [
        ('"meta_desc": "Palermo Homes is a custom home builder in Kelowna, BC. Custom home design and construction across Upper Mission, Kettle Valley, Glenmore, Lower Mission, and the Central Okanagan. 15+ years hands-on.",',
         '"meta_desc": "Custom home builder in Kelowna, BC. Design and construction across Upper Mission, Kettle Valley, Glenmore, and the Central Okanagan.",'),
        ('"meta_desc": "Palermo Homes builds custom lakeview homes across West Kelowna\'s wine district. Cabernet Way, Malbec Place, Touriga Place, Vineyard Estates. 15+ years, commercial-grade construction.",',
         '"meta_desc": "Palermo Homes builds custom lakeview homes across West Kelowna\'s wine district: Cabernet Way, Malbec Place, Touriga Place, Vineyard Estates.",'),
        ('"meta_desc": "Palermo Homes builds custom homes across Lake Country, BC. Lakestone, Ledgestone Road, Oyama, Carr\'s Landing. Lakefront and orchard-view expertise. 15+ years hands-on.",',
         '"meta_desc": "Palermo Homes builds custom homes across Lake Country, BC, including Lakestone, Ledgestone Road, Oyama, and Carr\'s Landing.",'),
        ('"meta_desc": "Palermo Homes builds custom homes across Vernon, BC and the North Okanagan. The Rise, Predator Ridge, Middleton Mountain, Okanagan Landing. 15+ years of hands-on experience.",',
         '"meta_desc": "Palermo Homes builds custom homes across Vernon, BC and the North Okanagan, including The Rise, Predator Ridge, and Middleton Mountain.",'),
        ('"meta_desc": "Palermo Homes takes on select custom home and renovation projects across the Lower Mainland. Abbotsford, Chilliwack, Langley. Eagle Mountain, West Abbotsford, Verado Court portfolio.",',
         '"meta_desc": "Palermo Homes takes on select custom home and renovation projects across the Lower Mainland, including Eagle Mountain and West Abbotsford.",'),
    ],
    "_build/build_project_communities.py": [],  # handled below with dict rebuild
    "site/contact/index.html": [
        ('<meta content="Contact Palermo Homes to plan a custom home, renovation, or general-contracting project in Kelowna, West Kelowna, Lake Country, and across the Okanagan. Call (604) 897-9390 or send a message." name="description"/>',
         '<meta content="Contact Palermo Homes about a custom home, renovation, or general contracting project in Kelowna and the Okanagan. (604) 897-9390." name="description"/>'),
    ],
}

total = 0
miss = 0
for path, pairs in replacements.items():
    f = ROOT / path
    if not pairs:
        continue
    src = f.read_text(encoding="utf-8")
    applied = 0
    for old, new in pairs:
        if old in src:
            src = src.replace(old, new, 1)
            applied += 1
        else:
            miss += 1
            print(f"  MISS in {path}: {old[:70]}...")
    f.write_text(src, encoding="utf-8")
    total += applied
    print(f"{path}: {applied} changes")

# Now shorten the project community descriptions (they use c["tagline"] + c["intro"][:140]).
# Easier to override the hub_desc + the per-community desc construction.
pc = ROOT / "_build" / "build_project_communities.py"
src = pc.read_text(encoding="utf-8")

# Change the community meta_desc construction to use a shorter formula + strip banned facts.
old_desc_build = 'desc = f\'{c["tagline"]} {c["intro"][:140]}\''
new_desc_build = ('# Shortened per 155-char limit; use first ~140 chars of a cleaned combined string\n'
                  '        combined = f\'{c["tagline"]} {c["intro"]}\'.replace("\\n", " ")\n'
                  '        desc = combined[:152].rstrip() + ("..." if len(combined) > 152 else "")')
if old_desc_build in src:
    src = src.replace(old_desc_build, new_desc_build, 1)
    total += 1
    print(f"_build/build_project_communities.py: community desc generator updated")
else:
    print(f"  MISS: community desc generator pattern not found")
    miss += 1

pc.write_text(src, encoding="utf-8")

print(f"TOTAL: {total} applied, {miss} missed")
