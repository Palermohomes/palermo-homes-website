"""Compress services hero image: desktop + mobile versions with sharp quality."""
from pathlib import Path
from PIL import Image, ImageOps

SITE = Path(__file__).resolve().parent.parent / "site"
SRC = SITE / "services" / "Cabernet-46.jpg"
OUT_DIR = SITE / "services"

img = Image.open(SRC)
img = ImageOps.exif_transpose(img)  # respect EXIF orientation
print(f"Source: {SRC.name}  {img.size}  {SRC.stat().st_size/1024:.0f} KB")

variants = [
    ("Cabernet-46-desktop.jpg", 1920),
    ("Cabernet-46-mobile.jpg", 960),
]

for name, target_w in variants:
    ratio = target_w / img.width
    if ratio >= 1:
        out = img.copy()
    else:
        new_size = (target_w, round(img.height * ratio))
        out = img.resize(new_size, Image.LANCZOS)
    out_path = OUT_DIR / name
    # save as high-quality JPEG with progressive encoding + subsampling
    out.convert("RGB").save(
        out_path,
        "JPEG",
        quality=82,
        optimize=True,
        progressive=True,
        subsampling=1,  # 4:2:2. Sharper than default 4:2:0
    )
    print(f"  wrote {out_path.name}  {out.size}  {out_path.stat().st_size/1024:.0f} KB")
