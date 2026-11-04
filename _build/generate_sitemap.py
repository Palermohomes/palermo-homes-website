"""Generate sitemap.xml listing every index.html under site/."""
from pathlib import Path
from datetime import date

SITE = Path(__file__).resolve().parent.parent / "site"
BASE = "https://palermohomes.com"
TODAY = date.today().isoformat()

# Page priority tiers based on business importance
PRIORITY = {
    "/": 1.0,
    "/services/": 0.9,
    "/services/custom-homes/": 0.9,
    "/services/renovations/": 0.9,
    "/services/general-contracting/": 0.9,
    "/projects/": 0.9,
    "/contact/": 0.8,
    "/faq/": 0.8,
    "/about/": 0.7,
    "/awards/": 0.6,
    "/media/": 0.6,
}


def url_for(path: Path) -> str:
    rel = path.parent.relative_to(SITE).as_posix()
    if rel == ".":
        return "/"
    return "/" + rel + "/"


def priority_for(url: str) -> float:
    if url in PRIORITY:
        return PRIORITY[url]
    if url.startswith("/projects/"):
        return 0.7  # project community pages
    if url.startswith("/project/"):
        return 0.6  # individual project detail pages
    if url.startswith("/guides/"):
        return 0.85  # long-form guide articles, high SEO value
    return 0.5


def main():
    urls = []
    for p in sorted(SITE.rglob("index.html")):
        u = url_for(p)
        urls.append(u)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"  <url>")
        lines.append(f"    <loc>{BASE}{u}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <priority>{priority_for(u):.1f}</priority>")
        lines.append(f"  </url>")
    lines.append("</urlset>")

    out = SITE / "sitemap.xml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(SITE.parent)} with {len(urls)} URLs")


if __name__ == "__main__":
    main()
