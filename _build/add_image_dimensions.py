"""Post-build pass: add real width and height attributes to <img> tags that lack them.
Reads image dimensions directly from file bytes (PNG, JPEG, WebP) with no external deps.
Prevents Cumulative Layout Shift (CLS) and feeds Core Web Vitals.
Idempotent. Safe to rerun."""
import re
import struct
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
DIM_CACHE: dict[str, tuple[int, int]] = {}


def read_png(fp) -> tuple[int, int] | None:
    """PNG: bytes 16-24 are width/height (big-endian uint32)."""
    fp.seek(0)
    header = fp.read(24)
    if len(header) < 24 or not header.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    w, h = struct.unpack(">II", header[16:24])
    return (w, h)


def read_jpeg(fp) -> tuple[int, int] | None:
    """JPEG: scan for SOFn markers (0xC0-0xC3, 0xC5-0xC7, 0xC9-0xCB, 0xCD-0xCF)."""
    fp.seek(0)
    data = fp.read(2)
    if data != b"\xff\xd8":
        return None
    while True:
        marker = fp.read(2)
        if len(marker) < 2:
            return None
        if marker[0] != 0xFF:
            return None
        code = marker[1]
        if 0xC0 <= code <= 0xCF and code not in (0xC4, 0xC8, 0xCC):
            fp.read(3)  # length (2) + precision (1)
            hw = fp.read(4)
            if len(hw) < 4:
                return None
            h, w = struct.unpack(">HH", hw)
            return (w, h)
        length_bytes = fp.read(2)
        if len(length_bytes) < 2:
            return None
        length = struct.unpack(">H", length_bytes)[0]
        fp.seek(length - 2, 1)


def read_webp(fp) -> tuple[int, int] | None:
    """WebP: VP8, VP8L, or VP8X chunk header."""
    fp.seek(0)
    header = fp.read(30)
    if len(header) < 30 or not header.startswith(b"RIFF") or header[8:12] != b"WEBP":
        return None
    chunk = header[12:16]
    if chunk == b"VP8X":
        w = int.from_bytes(header[24:27], "little") + 1
        h = int.from_bytes(header[27:30], "little") + 1
        return (w, h)
    if chunk == b"VP8L":
        b = header[21:25]
        w = ((b[1] & 0x3F) << 8 | b[0]) + 1
        h = ((b[3] & 0x0F) << 10 | b[2] << 2 | (b[1] & 0xC0) >> 6) + 1
        return (w, h)
    if chunk == b"VP8 ":
        fp.seek(26)
        tag = fp.read(10)
        if len(tag) < 10:
            return None
        w = struct.unpack("<H", tag[6:8])[0] & 0x3FFF
        h = struct.unpack("<H", tag[8:10])[0] & 0x3FFF
        return (w, h)
    return None


def get_dims(abs_path: Path) -> tuple[int, int] | None:
    key = str(abs_path)
    if key in DIM_CACHE:
        return DIM_CACHE[key]
    if not abs_path.exists():
        DIM_CACHE[key] = None
        return None
    try:
        with abs_path.open("rb") as fp:
            ext = abs_path.suffix.lower()
            dims = None
            if ext == ".png":
                dims = read_png(fp)
            elif ext in (".jpg", ".jpeg"):
                dims = read_jpeg(fp)
            elif ext == ".webp":
                dims = read_webp(fp)
            # Fallback: try all parsers (misnamed files)
            if dims is None:
                for reader in (read_png, read_jpeg, read_webp):
                    dims = reader(fp)
                    if dims:
                        break
            DIM_CACHE[key] = dims
            return dims
    except Exception:
        DIM_CACHE[key] = None
        return None


def resolve_src(page: Path, src: str) -> Path | None:
    """Resolve img src to a local file path."""
    if src.startswith(("http://", "https://", "data:")):
        return None
    if src.startswith("/"):
        candidate = SITE / src.lstrip("/")
    else:
        candidate = (page.parent / src).resolve()
    try:
        candidate.relative_to(SITE)
    except ValueError:
        return None
    return candidate


def process(page: Path) -> int:
    html = page.read_text(encoding="utf-8")
    body_m = re.search(r"<body[^>]*>", html)
    if not body_m:
        return 0
    body_start = body_m.end()
    body = html[body_start:]
    added = [0]

    def fix(m):
        tag = m.group(0)
        if "width=" in tag and "height=" in tag:
            return tag
        src_m = re.search(r'src="([^"]+)"', tag)
        if not src_m:
            return tag
        abs_path = resolve_src(page, src_m.group(1))
        if not abs_path:
            return tag
        dims = get_dims(abs_path)
        if not dims:
            return tag
        w, h = dims
        if "width=" not in tag:
            tag = tag.replace("<img", f'<img width="{w}"', 1)
        if "height=" not in tag:
            tag = tag.replace("<img", f'<img height="{h}"', 1)
        added[0] += 1
        return tag

    new_body = re.sub(r"<img\b[^>]*>", fix, body)
    if new_body != body:
        page.write_text(html[:body_start] + new_body, encoding="utf-8")
    return added[0]


def main():
    files = 0
    total = 0
    for p in SITE.rglob("index.html"):
        n = process(p)
        if n:
            files += 1
            total += n
    print(f"Added width/height to {total} <img> tags across {files} pages.")


if __name__ == "__main__":
    main()
