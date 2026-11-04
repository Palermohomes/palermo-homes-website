"""Replace Divi's messy footer with a clean, aligned, professional custom footer.
Idempotent. Safe to rerun after content changes.
Runs on every HTML page across the site."""
import os
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

FOOTER_CSS_START = "/* ==== SITE-FOOTER-V2 CSS START ==== */"
FOOTER_CSS_END = "/* ==== SITE-FOOTER-V2 CSS END ==== */"
FOOTER_HTML_START = "<!-- SITE-FOOTER-V2 START -->"
FOOTER_HTML_END = "<!-- SITE-FOOTER-V2 END -->"

FOOTER_CSS = f"""
{FOOTER_CSS_START}
html body #site-footer{{background:#f6f4ef;color:#1a1d21;font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;border-top:1px solid #ece8df;padding:64px 0 24px;margin-top:0}}
html body #site-footer .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #site-footer .cols{{display:grid;grid-template-columns:1.1fr .85fr 1.5fr .8fr 1.15fr;gap:48px;align-items:start}}
html body #site-footer h4{{font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 22px}}
html body #site-footer .brand-col img.wordmark{{height:36px;width:auto;display:block;margin:0 0 18px -4px}}
html body #site-footer .brand-col p{{font-size:14px;font-weight:400;letter-spacing:0;line-height:1.4;color:#6a7078;margin:0;max-width:26ch}}
html body #site-footer .social-links{{display:flex;gap:10px;margin:18px 0 0}}
html body #site-footer .social-links a{{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border:1px solid #d9d3c4;border-radius:6px;color:#6a7078;transition:color .2s,border-color .2s,background .2s}}
html body #site-footer .social-links a:hover{{color:#0085c9;border-color:#0085c9}}
/* Menu + Contact columns share identical dim, low-weight typography (wedogyms-style) */
html body #site-footer ul.links,
html body #site-footer .contact-col{{font-size:14px;line-height:1.4;color:#6a7078}}
html body #site-footer ul.links{{list-style:none;margin:0;padding:0}}
html body #site-footer ul.links.two-col{{column-count:2;column-gap:24px}}
html body #site-footer ul.links li,
html body #site-footer .contact-col p{{margin:0 0 11px;break-inside:avoid;font-size:14px;font-weight:400;letter-spacing:0;text-transform:none;line-height:1.4;color:#6a7078}}
html body #site-footer ul.links a,
html body #site-footer .contact-col a{{color:#6a7078;text-decoration:none;font-size:14px;font-weight:400;letter-spacing:0;text-transform:none;transition:color .2s}}
html body #site-footer .contact-col .ct-phone,
html body #site-footer .contact-col .ct-email{{margin:0 0 8px;font-size:14px;font-weight:400;line-height:1.5;color:#6a7078}}
html body #site-footer .contact-col .ct-email{{margin-bottom:0}}
html body #site-footer .contact-col .ct-phone a,
html body #site-footer .contact-col .ct-email a{{font-size:14px;font-weight:400;line-height:1.5;color:#6a7078}}
html body #site-footer ul.links a:hover,
html body #site-footer .contact-col a:hover{{color:#0085c9}}
html body #site-footer .assoc-col .badges{{display:block;padding:6px 0}}
html body #site-footer .assoc-col .badges img{{width:100%;height:auto;display:block;max-height:80px;object-fit:contain}}
html body #site-footer .bottom{{margin-top:56px;padding-top:20px;border-top:1px solid #ece8df;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;font-size:12px;color:#7a828c;letter-spacing:.02em}}
html body #site-footer .bottom .tag{{color:#7a828c}}

/* Hide Divi's original footer entirely (any template-footer section, regardless of index) */
html body #et-footer-nav,html body #footer-bottom,html body .et-l--footer,html body #main-footer,html body footer#et-l--footer,html body [class*="_tb_footer"]{{display:none !important}}

@media (max-width:960px){{
  html body #site-footer{{padding:48px 0 20px}}
  html body #site-footer .cols{{grid-template-columns:1fr 1fr;gap:36px}}
  html body #site-footer .assoc-col{{grid-column:1 / -1}}
  html body #site-footer ul.links.two-col{{column-count:1}}
}}
@media (max-width:600px){{
  html body #site-footer .cols{{grid-template-columns:1fr;gap:32px}}
  html body #site-footer .bottom{{justify-content:flex-start}}
}}
{FOOTER_CSS_END}
"""

NAV_ITEMS = [
    ("Home", "/"),
    ("Projects", "/projects/"),
    ("Services", "/services/"),
    ("About", "/about/"),
    ("Jas Sidhu, Owner", "/about/jas-sidhu/"),
    ("Awards", "/awards/"),
    ("Media", "/media/"),
    ("FAQ", "/faq/"),
    ("Contact", "/contact/"),
]  # kept mixed case to match wedogyms-style dim footer typography

SERVICE_AREAS = [
    ("Kelowna", "/service-areas/kelowna/"),
    ("West Kelowna", "/service-areas/west-kelowna/"),
    ("Lake Country", "/service-areas/lake-country/"),
    ("Peachland", "/service-areas/peachland/"),
    ("Vernon", "/service-areas/vernon/"),
    ("Penticton", "/service-areas/penticton/"),
    ("Lower Mainland", "/service-areas/lower-mainland/"),
]

FOOTER_HTML = f"""{FOOTER_HTML_START}
<footer id="site-footer">
  <div class="wrap">
    <div class="cols">
      <div class="brand-col">
        <img class="wordmark" src="/wp-content/uploads/brand/palermo-logo-blue.png" alt="Palermo Homes">
        <p>Custom home builder based in Kelowna, BC. Building homes and renovations across the Okanagan, the Fraser Valley, and the Lower Mainland for 15+ years.</p>
        <div class="social-links">
          <a href="https://www.facebook.com/PalermoHomes" target="_blank" rel="noopener" aria-label="Palermo Homes on Facebook">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"/></svg>
          </a>
          <a href="https://www.instagram.com/palermohomesltd/" target="_blank" rel="noopener" aria-label="Palermo Homes on Instagram">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
          </a>
        </div>
      </div>
      <div class="links-col">
        <h4>Site</h4>
        <ul class="links two-col">
          {''.join(f'<li><a href="{h}">{l}</a></li>' for l, h in NAV_ITEMS)}
        </ul>
      </div>
      <div class="areas-col">
        <h4>Service Areas</h4>
        <ul class="links two-col">
          {''.join(f'<li><a href="{h}">{l}</a></li>' for l, h in SERVICE_AREAS)}
        </ul>
      </div>
      <div class="contact-col">
        <h4>Contact</h4>
        <p class="ct-phone"><a href="tel:7787604113">(778) 760-4113</a></p>
        <p class="ct-email"><a href="mailto:info@palermohomes.com">info@palermohomes.com</a></p>
      </div>
      <div class="assoc-col">
        <h4>Associated With</h4>
        <div class="badges">
          <img src="/wp-content/uploads/brand/logoLockup-blue.png" alt="Palermo Homes association badges: Millionaire Lottery, CHBA BC, Hometown Heroes Lottery, National Home Warranty, EnerGuide">
        </div>
      </div>
    </div>
    <div class="bottom">
      <div>&copy; <span id="ft-yr"></span> Palermo Homes. All rights reserved.</div>
      <div class="tag">Custom Home Builder · Kelowna & the Okanagan · Lower Mainland</div>
    </div>
  </div>
  <script>document.getElementById('ft-yr').textContent=new Date().getFullYear();</script>
</footer>
{FOOTER_HTML_END}"""


def process_page(page_path: Path) -> bool:
    html = page_path.read_text(encoding="utf-8")

    # 1) Remove any prior CSS block
    if FOOTER_CSS_START in html:
        html = re.sub(re.escape(FOOTER_CSS_START) + r".*?" + re.escape(FOOTER_CSS_END), "", html, flags=re.DOTALL)
    # 2) Remove any prior HTML block
    if FOOTER_HTML_START in html:
        html = re.sub(re.escape(FOOTER_HTML_START) + r".*?" + re.escape(FOOTER_HTML_END), "", html, flags=re.DOTALL)

    # 3) Inject CSS as its own <style> block before </head>
    if "</head>" not in html:
        return False
    html = html.replace("</head>", f"<style>{FOOTER_CSS}</style></head>", 1)

    # 4) Inject footer HTML right before </body>
    if "</body>" not in html:
        return False
    html = html.replace("</body>", FOOTER_HTML + "\n</body>", 1)

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
    print(f"Replaced footer on {count} pages")


if __name__ == "__main__":
    main()
