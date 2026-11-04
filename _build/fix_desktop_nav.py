"""Force horizontal desktop nav. Divi mirror is defaulting to mobile hamburger on desktop.
Idempotent. Safe to rerun."""
import os
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

CSS_START = "/* ==== NAV-FIX START ==== */"
CSS_END = "/* ==== NAV-FIX END ==== */"

NAV_CSS = f"""
{CSS_START}
@media (min-width: 981px) {{
  html body #top-menu {{ display: block !important; }}
  html body #top-menu li {{ display: inline-block !important; }}
  html body #et_mobile_nav_menu {{ display: none !important; }}
  html body .mobile_menu_bar,
  html body .mobile_menu_bar.et_pb_header_toggle {{ display: none !important; }}
  html body #et-top-navigation {{ padding-top: 24px !important; }}
}}
{CSS_END}
"""


def process(html: str) -> tuple[str, bool]:
    # remove prior injection
    if CSS_START in html:
        html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.DOTALL)
    # inject before </style></head>
    if "</style></head>" not in html:
        return html, False
    return html.replace("</style></head>", NAV_CSS + "</style></head>", 1), True


def main():
    count = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = Path(root) / f
            html = p.read_text(encoding="utf-8")
            new_html, ok = process(html)
            if ok and new_html != html:
                p.write_text(new_html, encoding="utf-8")
                count += 1
    print(f"Injected nav-fix CSS into {count} pages")


if __name__ == "__main__":
    main()
