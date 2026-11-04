"""Strip legacy Divi cruft from all HTML pages:

1) The legacy Divi footer block (`<footer class="et-l et-l--footer">...</footer>`)
  . Every page has both the legacy Divi footer AND our custom `<footer id="site-footer">`.
   Google was reading the legacy one which contains "ASSOCIATED WITH:" and duplicate
   contact info. Remove it, keep only the custom footer.

2) The Divi post-nav "← PREV NEXT →" module on project detail pages.
   Google was surfacing this as sitelink snippets. Kill it.
"""
import re
import pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

# Legacy Divi footer: from <footer class="et-l et-l--footer"> to the matching </footer>
LEGACY_FOOTER_RE = re.compile(
    r'<footer class="et-l et-l--footer">.*?</footer>',
    re.DOTALL
)

# PREV/NEXT post navigation module (project pages only)
POST_NAV_RE = re.compile(
    r'<div class="et_pb_module et_pb_post_nav_0_tb_body[^"]*"[^>]*>.*?</div>',
    re.DOTALL
)

# Empty row/column left after post-nav removal (optional cleanup)
EMPTY_ROW_RE = re.compile(
    r'<div class="et_pb_row et_pb_row_0_tb_body">\s*'
    r'<div class="et_pb_column et_pb_column_4_4 et_pb_column_0_tb_body[^"]*"[^>]*>\s*'
    r'</div>\s*</div>\s*',
    re.DOTALL
)


def clean(path: pathlib.Path) -> tuple[bool, int, int]:
    """Returns (touched, footer_removed_bytes, nav_removed_bytes)."""
    html = path.read_text(encoding="utf-8")
    orig = html
    fb = nb = 0

    m = LEGACY_FOOTER_RE.search(html)
    if m:
        fb = len(m.group(0))
        html = LEGACY_FOOTER_RE.sub("", html, count=1)

    m = POST_NAV_RE.search(html)
    if m:
        nb = len(m.group(0))
        html = POST_NAV_RE.sub("", html, count=1)
        # Also clean up the now-empty wrapper row if present
        html = EMPTY_ROW_RE.sub("", html, count=1)

    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True, fb, nb
    return False, 0, 0


def main():
    total_touched = 0
    total_footer_bytes = 0
    total_nav_bytes = 0
    for p in sorted(SITE.rglob("index.html")):
        touched, fb, nb = clean(p)
        if touched:
            total_touched += 1
            total_footer_bytes += fb
            total_nav_bytes += nb
            rel = p.relative_to(SITE)
            marks = []
            if fb: marks.append(f"footer -{fb}B")
            if nb: marks.append(f"nav -{nb}B")
            print(f"  {rel}  ({', '.join(marks)})")
    print()
    print(f"Cleaned {total_touched} files")
    print(f"Legacy footer bytes removed: {total_footer_bytes/1024:.1f} KB")
    print(f"Post-nav bytes removed:      {total_nav_bytes/1024:.1f} KB")


if __name__ == "__main__":
    main()
