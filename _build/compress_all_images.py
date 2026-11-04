"""Bulk compress every JPEG in site/ over 300KB.

Rules:
- Resize width to max 2000px (keeps quality at retina viewing)
- Re-encode JPEG at quality 82, progressive, 4:2:2 subsampling
- Skip if output would be larger than input
- Skip PNGs (logos, transparent UI)
- Skip files already under 300KB
- Handle EXIF orientation before resize
"""
from pathlib import Path
from PIL import Image, ImageOps

SITE = Path(__file__).resolve().parent.parent / "site"
MAX_WIDTH = 2000
QUALITY = 82
MIN_SIZE_BYTES = 300 * 1024  # only touch files > 300KB


def compress(path: Path) -> tuple[int, int, bool]:
    """Returns (before, after, touched)."""
    before = path.stat().st_size
    if before < MIN_SIZE_BYTES:
        return before, before, False

    try:
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)
    except Exception as e:
        print(f"  SKIP  {path.relative_to(SITE)}  ({e})")
        return before, before, False

    # Resize if wider than MAX_WIDTH
    if img.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img.width
        new_size = (MAX_WIDTH, round(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    # Re-encode to a temp path, compare, then swap
    tmp = path.with_suffix(path.suffix + ".tmp")
    img.convert("RGB").save(
        tmp,
        "JPEG",
        quality=QUALITY,
        optimize=True,
        progressive=True,
        subsampling=1,
    )
    after = tmp.stat().st_size

    if after < before:
        tmp.replace(path)
        return before, after, True
    else:
        tmp.unlink()
        return before, before, False


def main():
    total_before = 0
    total_after = 0
    n_touched = 0
    n_scanned = 0
    biggest_wins = []

    for path in SITE.rglob("*.jpg"):
        n_scanned += 1
        before, after, touched = compress(path)
        total_before += before
        total_after += after
        if touched:
            n_touched += 1
            saved = before - after
            biggest_wins.append((saved, path.relative_to(SITE)))
            print(f"  {before/1024:>6.0f} KB -> {after/1024:>6.0f} KB   {path.relative_to(SITE)}")

    for path in SITE.rglob("*.jpeg"):
        n_scanned += 1
        before, after, touched = compress(path)
        total_before += before
        total_after += after
        if touched:
            n_touched += 1
            saved = before - after
            biggest_wins.append((saved, path.relative_to(SITE)))
            print(f"  {before/1024:>6.0f} KB -> {after/1024:>6.0f} KB   {path.relative_to(SITE)}")

    print()
    print(f"Scanned:  {n_scanned} JPEGs")
    print(f"Touched:  {n_touched} files")
    print(f"Before:   {total_before/1024/1024:.1f} MB")
    print(f"After:    {total_after/1024/1024:.1f} MB")
    print(f"Saved:    {(total_before-total_after)/1024/1024:.1f} MB  ({100*(1-total_after/max(1,total_before)):.0f}%)")


if __name__ == "__main__":
    main()
