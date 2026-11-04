"""Remove title="..." from <img> tags when the value is a file name or "default".
Keep every other title. Report count removed. Idempotent."""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
FILENAME_RE = re.compile(r"\.(jpe?g|png|webp|gif|svg|bmp|tiff?)$", re.IGNORECASE)


def should_strip(title_value: str) -> bool:
    """Strip titles that look auto-generated (filename-derived), keep human-written ones."""
    t = title_value.strip()
    if not t:
        return True
    if t.lower() == "default":
        return True
    # Any image extension in the string
    if FILENAME_RE.search(t):
        return True
    # Contains underscore (humans don't title with underscores)
    if "_" in t:
        return True
    # Looks like a slug: no spaces OR hyphen-separated word+digits combo like "1556-Cabernet-nate-42"
    if " " not in t and len(t) <= 40:
        return True
    # Pattern like "1556 Cabernet nate-42" or "PAL_hm_AwardsPic". Digit + alpha mix without sentence case
    if re.match(r"^[A-Za-z]+[A-Z][a-z]*[A-Z]", t):  # CamelCase-ish gibberish like "fplNrDJA"
        return True
    # Contains a hyphen-dash and digit pattern typical of file stems ("1587-Malbec-14", "1556 Cabernet nate-42")
    if re.search(r"\b\d{3,}\b.*[-A-Za-z]", t) and len(t.split()) <= 5:
        return True
    # WhatsApp / phone export patterns ("WhatsApp Image 2026-01-22 at 22.41.31 (6)")
    if "whatsapp" in t.lower():
        return True
    # Any ISO date + time pattern = auto-generated filename
    if re.search(r"\d{4}-\d{2}-\d{2}.*\d{2}[.:]\d{2}", t):
        return True
    return False


def process(page: Path) -> tuple[int, list[str]]:
    """Returns (count_removed, sample_removed_values)."""
    html = page.read_text(encoding="utf-8")
    body_m = re.search(r"<body[^>]*>", html)
    if not body_m:
        return (0, [])
    body_start = body_m.end()
    body = html[body_start:]

    removed = [0]
    samples: list[str] = []

    def fix(m):
        tag = m.group(0)
        title_m = re.search(r'\stitle="([^"]*)"', tag)
        if not title_m:
            return tag
        value = title_m.group(1)
        if should_strip(value):
            removed[0] += 1
            if len(samples) < 5:
                samples.append(value)
            return re.sub(r'\stitle="[^"]*"', '', tag, count=1)
        return tag

    new_body = re.sub(r"<img\b[^>]*>", fix, body)
    if new_body != body:
        page.write_text(html[:body_start] + new_body, encoding="utf-8")
    return (removed[0], samples)


def main():
    total = 0
    files_changed = 0
    sample_pool: list[tuple[str, str]] = []
    for p in sorted(SITE.rglob("index.html")):
        n, samples = process(p)
        if n:
            files_changed += 1
            total += n
            for s in samples:
                if len(sample_pool) < 10:
                    sample_pool.append((str(p.relative_to(SITE)).replace("\\", "/"), s))
    print(f"Removed {total} title attributes across {files_changed} pages.")
    print()
    print("Sample of removed title values:")
    for page_rel, val in sample_pool:
        print(f"  {page_rel}: title={val!r}")


if __name__ == "__main__":
    main()
