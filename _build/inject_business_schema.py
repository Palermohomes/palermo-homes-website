"""Inject site-wide LocalBusiness + Organization schema into every HTML page.
Adds rich business signals (address, hours, geo, social, price, image, etc.) that
apply to every page. Homepage, services, about, projects, all of them.
Idempotent. Safe to rerun."""
import os
import re
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

SCHEMA_START = "<!-- SITE-BUSINESS-SCHEMA START -->"
SCHEMA_END = "<!-- SITE-BUSINESS-SCHEMA END -->"

BIZ_URL = "https://palermohomes.com"
BIZ_NAME = "Palermo Homes"
BIZ_LEGAL_NAME = "Palermo Homes Ltd."
BIZ_PHONE = "+1-778-760-4113"
BIZ_EMAIL = "info@palermohomes.com"
BIZ_STREET = "1523 Pinot Gris Drive"
BIZ_CITY = "West Kelowna"
BIZ_REGION = "BC"
BIZ_POSTAL = "V4T 2Y6"
BIZ_COUNTRY = "CA"
BIZ_LAT = 49.8397
BIZ_LON = -119.4884
BIZ_IMAGE = f"{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-07.jpg"
BIZ_LOGO = f"{BIZ_URL}/wp-content/uploads/brand/palermo-logo-blue.png"
BIZ_DESCRIPTION = "Custom home builder based in West Kelowna, BC. 15+ years building custom homes and whole-home renovations across the Okanagan and Lower Mainland."
BIZ_FOUNDED = "2014"

# sameAs: authoritative entity references + social profiles + owned content platforms
# Wikidata URL anchors the entity graph (critical for AI engines + Knowledge Graph)
SOCIAL = [
    "https://www.wikidata.org/wiki/Q141539061",
    "https://www.facebook.com/PalermoHomes",
    "https://www.instagram.com/palermohomesltd/",
    "https://www.linkedin.com/company/palermo-homes-ltd",
    "https://www.houzz.com/professionals/home-builders/palermo-homes-pfvwus-pf~1452287384",
    "https://palermohomes.substack.com",
]

SERVICE_AREAS = ["Kelowna", "West Kelowna", "Lake Country", "Peachland", "Vernon", "Penticton", "Lower Mainland"]

KNOWS_ABOUT = [
    "Custom Home Construction",
    "Home Renovations",
    "General Contracting",
    "Kitchen Renovations",
    "Bathroom Renovations",
    "Whole-Home Renovations",
    "Custom Cabinetry",
    "Finish Carpentry",
]


def build_schema():
    organization = {
        "@type": "Organization",
        "@id": f"{BIZ_URL}/#organization",
        "name": BIZ_LEGAL_NAME,
        "alternateName": BIZ_NAME,
        "url": BIZ_URL,
        "logo": {
            "@type": "ImageObject",
            "url": BIZ_LOGO,
        },
        "sameAs": SOCIAL,
        "foundingDate": BIZ_FOUNDED,
        "identifier": [
            {"@type": "PropertyValue", "propertyID": "BC Corporate Registry", "value": "BC1017682"},
            {"@type": "PropertyValue", "propertyID": "BC Housing License", "value": "42812"},
        ],
    }
    business = {
        "@type": "HomeAndConstructionBusiness",
        "@id": f"{BIZ_URL}/#business",
        "name": BIZ_NAME,
        "legalName": BIZ_LEGAL_NAME,
        "url": BIZ_URL,
        "telephone": BIZ_PHONE,
        "email": BIZ_EMAIL,
        "description": BIZ_DESCRIPTION,
        "image": BIZ_IMAGE,
        "logo": BIZ_LOGO,
        "priceRange": "$$$$",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": BIZ_CITY,
            "addressRegion": BIZ_REGION,
            "addressCountry": BIZ_COUNTRY,
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "08:00",
            "closes": "17:00",
        }],
        "areaServed": [{"@type": "City", "name": area} for area in SERVICE_AREAS],
        "knowsAbout": KNOWS_ABOUT,
        "sameAs": SOCIAL,
        "foundingDate": BIZ_FOUNDED,
    }
    graph = {
        "@context": "https://schema.org",
        "@graph": [organization, business],
    }
    return json.dumps(graph, ensure_ascii=False)


SCHEMA_BLOCK = f'{SCHEMA_START}\n<script type="application/ld+json">{build_schema()}</script>\n{SCHEMA_END}'


def process_page(page_path: Path) -> bool:
    html = page_path.read_text(encoding="utf-8")

    # Remove any prior injected block (idempotent)
    if SCHEMA_START in html:
        html = re.sub(re.escape(SCHEMA_START) + r".*?" + re.escape(SCHEMA_END), "", html, flags=re.DOTALL)

    # Inject right after <head> so it never interferes with build scripts that use </style></head> markers
    if "<head>" not in html:
        return False
    html = html.replace("<head>", f"<head>\n{SCHEMA_BLOCK}", 1)

    page_path.write_text(html, encoding="utf-8")
    return True


def main():
    count = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = Path(root) / f
            if process_page(p):
                count += 1
    print(f"Injected business schema on {count} pages")


if __name__ == "__main__":
    main()
