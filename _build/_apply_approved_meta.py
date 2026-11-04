"""Batch apply approved title + description changes across remaining build scripts.
Idempotent. One-off; delete after use."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

files_and_changes = {
    "_build/build_services.py": [
        ('        meta_desc="Palermo Homes offers custom homes, home renovations, and full-service general contracting across Kelowna, West Kelowna, Lake Country, and the Okanagan Valley.",',
         '        meta_desc="Palermo Homes offers custom homes, home renovations, and full-service general contracting across Kelowna and the Okanagan Valley.",'),
        ('        meta_desc="Custom-quality home renovations in Kelowna, West Kelowna, Lake Country, and the Lower Mainland. Whole-home, kitchen, bathroom, and additions. 15+ years of hands-on building.",',
         '        meta_desc="Custom-quality home renovations by Palermo Homes in Kelowna, West Kelowna, Lake Country, and the Lower Mainland. Whole-home, kitchen, bath.",'),
    ],
    "_build/build_project_communities.py": [
        ('    hub_title = "Our Communities | Palermo Homes | Custom Home Builder in Kelowna, BC"',
         '    hub_title = "Our Project Communities | Palermo Homes, Kelowna"'),
        ("    hub_desc = f\"See {sum(len(c['homes']) for c in COMMUNITIES)} completed custom homes by Palermo Homes across Kelowna and the Okanagan. Browse by community: Eagle Mountain, Cabernet Way, Malbec Place, Vineyard Estates, Touriga Place, Ledgestone, and the Fraser Valley.\"",
         '    hub_desc = "Browse custom homes by Palermo Homes across Kelowna, West Kelowna, Lake Country, Abbotsford, and the Lower Mainland."'),
    ],
    "_build/build_guide_timeline.py": [
        ('TITLE = "How Long to Build a Custom Home in Kelowna? 2026 Timeline Guide | Palermo Homes"',
         'TITLE = "How Long to Build a Custom Home in Kelowna | Palermo Homes"'),
        ('META_DESC = "A realistic month-by-month timeline for building a custom home in Kelowna. Design, permits, construction, and the factors that extend or compress each phase."',
         'META_DESC = "A realistic month-by-month timeline for building a custom home in Kelowna. Design, permits, construction, and what extends each phase."'),
    ],
    "_build/build_guide_choose_builder.py": [
        ('TITLE = "How to Choose a Custom Home Builder in Kelowna: 2026 Guide | Palermo Homes"',
         'TITLE = "Choosing a Custom Home Builder in Kelowna | Palermo Homes"'),
        ('META_DESC = "A step-by-step guide to choosing a custom home builder in Kelowna. Seven verification criteria, red flags to avoid, and how to compare bids before signing any contract."',
         'META_DESC = "A step-by-step guide to choosing a custom home builder in Kelowna. Seven verification criteria, red flags, and how to compare bids."'),
    ],
    "_build/build_guide_contracts.py": [
        ('TITLE = "Fixed-Price vs Cost-Plus Contracts for Custom Homes in BC: 2026 Guide | Palermo Homes"',
         'TITLE = "Fixed-Price vs Cost-Plus Home Contracts BC | Palermo Homes"'),
        ('META_DESC = "A plain-English comparison of fixed-price and cost-plus construction contracts for custom homes in Kelowna and BC. Which protects you, when each makes sense, and how to spot the risks in both."',
         'META_DESC = "A plain-English comparison of fixed-price and cost-plus construction contracts for custom homes in Kelowna and BC."'),
    ],
    "_build/build_guide_cost.py": [
        ('META_DESC = "The typical cost to build a custom home in Kelowna in 2026 ranges from $500 to $900 per square foot. Complete cost breakdown by size, tier, and hillside premium."',
         'META_DESC = "A complete breakdown of what it costs to build a custom home in Kelowna. Size tiers, hillside premiums, and hidden costs."'),
    ],
    "_build/build_author_jas.py": [
        ('TITLE = "Jaspal Sidhu, Owner of Palermo Homes | Custom Home Builder in Kelowna, BC"',
         'TITLE = "Jaspal Sidhu, Owner | Custom Home Builder | Palermo Homes"'),
        ('META_DESC = "Jaspal Sidhu is the owner of Palermo Homes, a custom home builder in West Kelowna, BC. BC Housing Licensed Builder 42812. Over 15 years of Okanagan custom home experience."',
         'META_DESC = "Jaspal Sidhu is the owner of Palermo Homes, a custom home builder in West Kelowna, BC. BC Housing Licensed Residential Builder 42812."'),
    ],
    "_build/build_faq.py": [
        ('META_DESC = "Answers to the most common questions about custom home building in Kelowna, West Kelowna, and the Okanagan. Cost, timelines, warranty, process, and service areas."',
         'META_DESC = "Common questions about custom home building in Kelowna, West Kelowna, and the Okanagan: cost, timelines, warranty, process, service areas."'),
    ],
    "_build/redesign_about.py": [
        ("_desc = 'Palermo Homes is a custom home builder based in Kelowna, BC. 15+ years building custom homes and renovations across Kelowna, West Kelowna, Lake Country, and the Okanagan.'",
         "_desc = 'Palermo Homes is a custom home builder based in Kelowna, BC. 15+ years building custom homes and renovations across the Okanagan.'"),
    ],
    "_build/redesign_awards.py": [
        ("'<title>Awards | Palermo Homes | Award-Winning Custom Home Builder in Kelowna, BC</title>'",
         "'<title>Awards | Palermo Homes | Kelowna Custom Home Builder</title>'"),
        ("_desc = 'Palermo Homes is an award-winning custom home builder in Kelowna, BC, recognized by CHBA Fraser Valley for our custom home builds across the Okanagan.'",
         "_desc = 'Palermo Homes is an award-winning custom home builder in Kelowna, BC, recognized by CHBA Fraser Valley for our custom home builds.'"),
    ],
    "_build/redesign_media.py": [
        ("'<title>Media &amp; Press | Palermo Homes | Award-Winning Custom Home Builder in Kelowna, BC</title>'",
         "'<title>Media Coverage &amp; Press | Palermo Homes, Kelowna</title>'"),
        ("_desc = 'Palermo Homes featured on Hometown Heroes Lottery, West Coast Homes, and Live Like a Millionaire. Custom home builder in Kelowna, BC, across the Okanagan and Fraser Valley.'",
         "_desc = 'Palermo Homes featured on Hometown Heroes Lottery, West Coast Homes, and Live Like a Millionaire. Custom home builder in Kelowna, BC.'"),
    ],
    "_build/build_guides_hub.py": [
        ('META_DESC = "In-depth guides on custom home costs, timelines, contracts, hillside builds, and choosing a builder in Kelowna, West Kelowna, and the Okanagan Valley."',
         'META_DESC = "In-depth guides on custom home costs, timelines, contracts, and choosing a builder in Kelowna, West Kelowna, and the Okanagan."'),
    ],
}

total = 0
missed = 0
for path, changes in files_and_changes.items():
    f = ROOT / path
    html = f.read_text(encoding="utf-8")
    applied = 0
    for old, new in changes:
        if old in html:
            html = html.replace(old, new, 1)
            applied += 1
        else:
            missed += 1
            print(f"  MISS in {path}: {old[:70]}...")
    f.write_text(html, encoding="utf-8")
    total += applied
    print(f"{path}: {applied} changes")
print(f"TOTAL: {total} applied, {missed} missed")
