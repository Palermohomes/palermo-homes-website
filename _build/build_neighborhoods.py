"""Build /neighborhoods/ landing pages using About shell.
Each page: unique title/meta, LocalBusiness+Service+FAQPage schema, editorial layout.
Reuses the .svc design system from build_service_areas.py so every page flows.
Idempotent. Safe to rerun.

Neighborhoods are sub-areas of the parent cities in build_service_areas.py.
Each neighborhood page links back to its parent city page for topical hierarchy.
"""
import re
import json
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BUILD_DATE = datetime.date.today().isoformat()
BUILD_DATE_HUMAN = datetime.date.today().strftime("%B %Y")
ABOUT = SITE / "about" / "index.html"
base = ABOUT.read_text(encoding="utf-8")

open_marker = '<div id="et-main-area">'
close_marker = '<footer'
open_idx = base.find(open_marker)
inner_start = base.find('>', open_idx) + 1
footer_idx = base.find(close_marker, inner_start)
end = base.rfind('</div>', inner_start, footer_idx) + len('</div>')

SHELL_HEAD = base[:inner_start]
SHELL_FOOT = base[end:]

CSS_START = "/* ==== NEIGHBORHOODS-V1 CSS START ==== */"
CSS_END = "/* ==== NEIGHBORHOODS-V1 CSS END ==== */"

# Shared design system, IDENTICAL to build_service_areas.py so pages flow.
# Only difference: added .svc-amen amenities grid for master-planned communities.
AREAS_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .svc{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .svc *{{box-sizing:border-box}}
html body #et-main-area .svc img{{display:block;max-width:100%;height:auto}}
html body #et-main-area .svc .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .svc .eyebrow{{font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:#0085c9;font-weight:500;margin:0 0 20px}}

html body #et-main-area .svc-crumb{{background:#fff;padding:14px 0;border-bottom:1px solid #ece8df;font-size:12.5px;color:#6a7078;letter-spacing:.01em}}
html body #et-main-area .svc-crumb a{{color:#6a7078;text-decoration:none;transition:color .2s}}
html body #et-main-area .svc-crumb a:hover{{color:#0085c9}}
html body #et-main-area .svc-crumb .sep{{margin:0 8px;color:#c8c3b3}}
html body #et-main-area .svc-crumb .current{{color:#1a1d21;font-weight:500}}

html body #et-main-area .svc-hero{{position:relative;min-height:clamp(280px,42vh,420px);padding:40px 0;display:flex;align-items:center;overflow:hidden;color:#fff}}
html body #et-main-area .svc-hero .bg{{position:absolute;inset:0;background-position:center center;background-size:cover;background-repeat:no-repeat;image-rendering:-webkit-optimize-contrast}}
html body #et-main-area .svc-hero::after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.48) 0%,rgba(0,0,0,.55) 50%,rgba(0,0,0,.70) 100%)}}
html body #et-main-area .svc-hero .inner{{position:relative;z-index:2;max-width:1360px;margin:0 auto;width:100%;padding:0 clamp(20px,3vw,48px);box-sizing:border-box}}
html body #et-main-area .svc-hero .eyebrow{{color:rgba(255,255,255,.9);margin:0 0 14px}}
html body #et-main-area .svc-hero h1{{font-size:clamp(28px,3.6vw,46px);font-weight:500;letter-spacing:-0.02em;line-height:1.05;margin:0;max-width:22ch;text-transform:none;color:#fff}}
html body #et-main-area .svc-hero p.sub{{font-size:clamp(15px,1.2vw,17px);color:rgba(255,255,255,.92);margin:18px 0 0;max-width:60ch;line-height:1.55}}

html body #et-main-area .svc-facts{{background:#0085c9;color:#fff;padding:24px 0}}
html body #et-main-area .svc-facts .wrap{{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;align-items:start}}
html body #et-main-area .svc-facts .fact{{border-left:1px solid rgba(255,255,255,.28);padding:2px 0 2px 20px}}
html body #et-main-area .svc-facts .fact:first-child{{border-left:0;padding-left:0}}
html body #et-main-area .svc-facts .k{{font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:rgba(255,255,255,.78);margin:0 0 6px;font-weight:500}}
html body #et-main-area .svc-facts .v{{font-size:16px;font-weight:600;line-height:1.35;margin:0;color:#fff}}
html body #et-main-area .svc-facts .v a{{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.4)}}

html body #et-main-area .svc-over{{padding:44px 0 48px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-over .grid{{display:grid;grid-template-columns:.85fr 1.15fr;gap:48px;align-items:center}}
html body #et-main-area .svc-over .col-text .head{{margin:0 0 22px;text-align:left}}
html body #et-main-area .svc-over .col-text .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-over .col-text h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21;max-width:32ch}}
html body #et-main-area .svc-over .col-text .body{{max-width:56ch}}
html body #et-main-area .svc-over .col-text p{{font-size:15.5px;line-height:1.7;color:#3a4048;margin:0 0 16px}}
html body #et-main-area .svc-over .col-text p:last-child{{margin:0}}
html body #et-main-area .svc-over .col-photos{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
html body #et-main-area .svc-over .col-photos .photo{{overflow:hidden;background:#f6f4ef;aspect-ratio:4/3}}
html body #et-main-area .svc-over .col-photos .photo img{{width:100%;height:100%;object-fit:cover;display:block;image-rendering:-webkit-optimize-contrast}}
html body #et-main-area .svc-over .col-photos.single{{grid-template-columns:1fr;max-width:560px;width:100%;justify-self:end;align-self:stretch;position:relative;min-height:100%}}
html body #et-main-area .svc-over .col-photos.single .photo{{position:absolute;inset:0;aspect-ratio:auto;height:auto;width:auto}}

/* Amenities grid. New section for master-planned communities. Reuses .svc-trust visual pattern. */
html body #et-main-area .svc-amen{{padding:36px 0 40px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-amen .head{{max-width:none;margin:0 0 22px}}
html body #et-main-area .svc-amen .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-amen h2{{font-size:clamp(20px,2.2vw,26px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-amen .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:8px}}
html body #et-main-area .svc-amen .item{{padding:24px 24px;border-left:1px solid #ece8df;display:flex;flex-direction:column;gap:6px}}
html body #et-main-area .svc-amen .item:first-child{{border-left:0;padding-left:0}}
html body #et-main-area .svc-amen .item .k{{font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0}}
html body #et-main-area .svc-amen .item .v{{font-size:15.5px;line-height:1.4;color:#1a1d21;font-weight:500;margin:0}}
html body #et-main-area .svc-amen .item .n{{font-size:13.5px;line-height:1.5;color:#5a6069;margin:0;font-weight:400}}

html body #et-main-area .svc-trust{{padding:32px 0 36px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-trust .head{{max-width:none;margin:0 0 20px}}
html body #et-main-area .svc-trust .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-trust h2{{font-size:clamp(20px,2.2vw,26px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-trust .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:8px}}
html body #et-main-area .svc-trust .item{{padding:24px 24px;border-left:1px solid #ece8df;display:flex;flex-direction:column;gap:6px}}
html body #et-main-area .svc-trust .item:first-child{{border-left:0;padding-left:0}}
html body #et-main-area .svc-trust .item .k{{font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0}}
html body #et-main-area .svc-trust .item .v{{font-size:15.5px;line-height:1.4;color:#1a1d21;font-weight:500;margin:0}}
html body #et-main-area .svc-trust .item .n{{font-size:13.5px;line-height:1.5;color:#5a6069;margin:0;font-weight:400}}

html body #et-main-area .svc-hoods{{padding:36px 0 40px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-hoods .head{{max-width:none;margin:0 0 22px}}
html body #et-main-area .svc-hoods .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-hoods h2{{font-size:clamp(20px,2.2vw,26px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-hoods .list{{font-size:clamp(15px,1.3vw,17px);line-height:2;color:#3a4048;letter-spacing:.005em;font-weight:400;margin:0;text-align:justify;text-align-last:center}}
html body #et-main-area .svc-hoods .list .name{{color:#1a1d21;font-weight:500;white-space:nowrap}}
html body #et-main-area .svc-hoods .list .sep{{color:#0085c9;font-weight:400;opacity:.55}}

html body #et-main-area .svc-split{{padding:36px 0 40px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-split .grid{{display:grid;grid-template-columns:1fr 1.1fr;gap:56px;align-items:stretch}}
html body #et-main-area .svc-split .photo{{overflow:hidden;background:#f6f4ef;min-height:100%}}
html body #et-main-area .svc-split .photo img{{width:100%;height:100%;object-fit:cover;display:block;min-height:420px}}
html body #et-main-area .svc-split .photo-col{{display:flex;flex-direction:column}}
html body #et-main-area .svc-split .photo-col .photo-loc{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 10px;text-align:left}}
html body #et-main-area .svc-split .photo-col .photo{{flex:1;min-height:0}}
html body #et-main-area .svc-split .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-split h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 18px;color:#1a1d21}}
html body #et-main-area .svc-split ul{{list-style:none;padding:0;margin:0}}
html body #et-main-area .svc-split li{{padding:16px 0;border-bottom:1px solid #ece8df;display:flex;gap:18px;align-items:flex-start}}
html body #et-main-area .svc-split li:last-child{{border-bottom:0}}
html body #et-main-area .svc-split li .num{{font-size:14px;color:#0085c9;font-weight:600;letter-spacing:.05em;flex:0 0 24px}}
html body #et-main-area .svc-split li .txt{{color:#2a2d33;font-size:15px;line-height:1.6}}
html body #et-main-area .svc-split li .txt strong{{color:#1a1d21;font-weight:600;display:block;margin-bottom:4px}}

html body #et-main-area .svc-feat{{padding:44px 0 48px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-feat .head{{max-width:82ch;margin:0 0 24px}}
html body #et-main-area .svc-feat .head .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0}}
html body #et-main-area .svc-feat h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.2;margin:0 0 18px;color:#1a1d21}}
html body #et-main-area .svc-feat .row{{display:grid;grid-template-columns:.85fr 1fr;gap:56px;align-items:center}}
html body #et-main-area .svc-feat .card{{display:block;text-decoration:none;color:inherit;background:#fff;border:1px solid #e2ddd0;overflow:hidden;transition:border-color .25s ease,box-shadow .25s ease}}
html body #et-main-area .svc-feat .card:hover{{border-color:#0085c9;box-shadow:0 8px 32px rgba(0,0,0,.08)}}
html body #et-main-area .svc-feat .card .photo{{overflow:hidden;background:#ddd;aspect-ratio:3/2;display:block}}
html body #et-main-area .svc-feat .card .photo img{{width:100%;height:100%;object-fit:cover;transition:transform .6s ease;display:block}}
html body #et-main-area .svc-feat .card:hover .photo img{{transform:scale(1.03)}}
html body #et-main-area .svc-feat .card .meta{{padding:16px 20px;display:flex;justify-content:space-between;align-items:center;gap:16px;border-top:1px solid #e2ddd0}}
html body #et-main-area .svc-feat .card .meta .txt{{flex:1;min-width:0}}
html body #et-main-area .svc-feat .card .meta .lab{{font-size:10.5px;letter-spacing:.26em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 5px;display:block}}
html body #et-main-area .svc-feat .card .meta h3{{font-size:16.5px;font-weight:600;letter-spacing:-0.01em;color:#1a1d21;margin:0;line-height:1.3}}
html body #et-main-area .svc-feat .card .meta .arrow{{font-size:20px;color:#0085c9;font-weight:400;flex:0 0 auto;transition:transform .3s ease}}
html body #et-main-area .svc-feat .card:hover .meta .arrow{{transform:translateX(6px)}}
html body #et-main-area .svc-feat .copy{{padding:4px 0}}
html body #et-main-area .svc-feat .copy p{{font-size:17px;line-height:1.7;color:#3a4048;margin:0}}

html body #et-main-area .svc-tiles{{padding:44px 0 44px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-tiles .head{{max-width:none;margin:0 0 24px}}
html body #et-main-area .svc-tiles .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-tiles h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-tiles .cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:0}}
html body #et-main-area .svc-tiles .card{{padding:36px 32px;border:1px solid #e2e0d9;text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:12px;transition:background .2s,border-color .2s}}
html body #et-main-area .svc-tiles .card+.card{{margin-left:-1px}}
html body #et-main-area .svc-tiles .card:hover{{background:#faf9f5;border-color:#0085c9}}
html body #et-main-area .svc-tiles .card h3{{font-size:20px;font-weight:600;letter-spacing:-0.01em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-tiles .card p{{font-size:14.5px;color:#5a6069;line-height:1.6;margin:0}}
html body #et-main-area .svc-tiles .card .go{{margin-top:auto;padding-top:16px;font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:#0085c9;font-weight:600}}

html body #et-main-area .svc-faq{{padding:44px 0 44px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-faq .head{{max-width:820px;margin:0 0 28px;text-align:left}}
html body #et-main-area .svc-faq .head .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-faq .head h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21;line-height:1.15}}
html body #et-main-area .svc-faq .items{{max-width:820px;margin:0}}
html body #et-main-area .svc-faq details{{background:#fff;border:1px solid #ece8df;margin-bottom:12px;padding:0}}
html body #et-main-area .svc-faq summary{{cursor:pointer;padding:20px 24px;font-weight:500;font-size:16px;color:#1a1d21;list-style:none;display:flex;justify-content:space-between;align-items:center}}
html body #et-main-area .svc-faq summary::-webkit-details-marker{{display:none}}
html body #et-main-area .svc-faq summary::after{{content:'+';font-size:22px;color:#0085c9;font-weight:400}}
html body #et-main-area .svc-faq details[open] summary::after{{content:'\\2013'}}
html body #et-main-area .svc-faq details[open] summary{{border-bottom:1px solid #ece8df}}
html body #et-main-area .svc-faq .ans{{padding:18px 24px 22px;color:#4a5058;font-size:15px;line-height:1.7}}

html body #et-main-area .svc-nearby{{padding:36px 0 40px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-nearby .head{{max-width:none;margin:0 0 16px}}
html body #et-main-area .svc-nearby .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-nearby h2{{font-size:clamp(20px,2.2vw,26px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-nearby .list{{font-size:clamp(15px,1.3vw,17px);line-height:1.9;color:#3a4048;letter-spacing:.005em;font-weight:400;margin:0}}
html body #et-main-area .svc-nearby .list a{{color:#0085c9;font-weight:600;text-decoration:underline;text-decoration-color:#0085c9;text-underline-offset:3px;text-decoration-thickness:1px;transition:color .2s,text-decoration-color .2s}}
html body #et-main-area .svc-nearby .list a:hover{{color:#006ba1;text-decoration-color:#006ba1}}
html body #et-main-area .svc-nearby .list .sep{{color:#0085c9;margin:0 12px;font-weight:400;opacity:.55}}
html body #et-main-area .svc-nearby .updated{{font-size:12px;color:#8a8f97;letter-spacing:.02em;margin:22px 0 0}}

html body #et-main-area .svc-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center}}
html body #et-main-area .svc-cta h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 14px;color:#fff !important}}
html body #et-main-area .svc-cta p{{color:rgba(255,255,255,.92) !important;font-size:16px;margin:0 0 26px}}
html body #et-main-area .svc-cta a.btn{{display:inline-block;background:#fff;color:#0085c9;padding:14px 30px;border-radius:999px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;text-decoration:none;transition:background .2s,color .2s}}
html body #et-main-area .svc-cta a.btn:hover{{background:#141821;color:#fff}}

@media (max-width:900px){{
  html body #et-main-area .svc-over .grid{{grid-template-columns:1fr;gap:24px}}
  html body #et-main-area .svc-over .col-photos{{grid-template-columns:1fr 1fr;gap:10px}}
  html body #et-main-area .svc-over .col-photos .photo{{aspect-ratio:4/3}}
  html body #et-main-area .svc-over .col-photos.single{{grid-template-columns:1fr;max-width:none;justify-self:stretch;align-self:auto;position:static;min-height:0;margin-top:8px}}
  html body #et-main-area .svc-over .col-photos.single .photo{{position:static;aspect-ratio:3/2;height:auto;width:100%}}
  html body #et-main-area .svc-amen{{padding:24px 0 28px}}
  html body #et-main-area .svc-amen .grid{{grid-template-columns:1fr 1fr;gap:0}}
  html body #et-main-area .svc-amen .item{{padding:16px 14px;border-left:1px solid #ece8df;border-top:1px solid #ece8df}}
  html body #et-main-area .svc-amen .item:nth-child(-n+2){{border-top:0}}
  html body #et-main-area .svc-amen .item:nth-child(2n+1){{border-left:0;padding-left:0}}
  html body #et-main-area .svc-amen .item .k{{font-size:10px;letter-spacing:.22em}}
  html body #et-main-area .svc-amen .item .v{{font-size:14px}}
  html body #et-main-area .svc-amen .item .n{{font-size:12.5px}}
  html body #et-main-area .svc-trust{{padding:24px 0 28px}}
  html body #et-main-area .svc-trust .grid{{grid-template-columns:1fr 1fr;gap:0}}
  html body #et-main-area .svc-trust .item{{padding:16px 14px;border-left:1px solid #ece8df;border-top:1px solid #ece8df}}
  html body #et-main-area .svc-trust .item:nth-child(-n+2){{border-top:0}}
  html body #et-main-area .svc-trust .item:nth-child(2n+1){{border-left:0;padding-left:0}}
  html body #et-main-area .svc-trust .item .k{{font-size:10px;letter-spacing:.22em}}
  html body #et-main-area .svc-trust .item .v{{font-size:14px}}
  html body #et-main-area .svc-trust .item .n{{font-size:12.5px}}
  html body #et-main-area .svc-hero{{min-height:280px;padding:28px 0}}
  html body #et-main-area .svc-hero .eyebrow{{margin-bottom:8px;font-size:10px;letter-spacing:.24em}}
  html body #et-main-area .svc-hero h1{{font-size:30px;line-height:1.1;max-width:24ch}}
  html body #et-main-area .svc-hero p.sub{{font-size:14px;margin-top:10px;line-height:1.5}}
  html body #et-main-area .svc-facts{{padding:14px 0}}
  html body #et-main-area .svc-facts .wrap{{grid-template-columns:1fr 1fr;gap:8px 12px}}
  html body #et-main-area .svc-facts .fact{{border-left:0;padding-left:0;padding-top:8px;border-top:1px solid rgba(255,255,255,.24)}}
  html body #et-main-area .svc-facts .fact:nth-child(-n+2){{border-top:0;padding-top:0}}
  html body #et-main-area .svc-facts .k{{font-size:10px;margin-bottom:3px;letter-spacing:.2em}}
  html body #et-main-area .svc-facts .v{{font-size:13.5px;line-height:1.3}}
  html body #et-main-area .svc-split .grid{{grid-template-columns:1fr;gap:22px}}
  html body #et-main-area .svc-split .photo{{aspect-ratio:16/10;min-height:0}}
  html body #et-main-area .svc-split .photo img{{min-height:0}}
  html body #et-main-area .svc-feat .row{{grid-template-columns:1fr;gap:22px;max-width:none}}
  html body #et-main-area .svc-feat .card{{border:1px solid #e2ddd0;margin:0 -1px;overflow:hidden}}
  html body #et-main-area .svc-feat .card:hover{{box-shadow:none;border-color:#0085c9}}
  html body #et-main-area .svc-feat .card .photo{{aspect-ratio:16/10;border:0}}
  html body #et-main-area .svc-feat .card .meta{{padding:14px 12px 14px 12px;gap:12px;border-top:1px solid #e2ddd0}}
  html body #et-main-area .svc-feat .card .meta h3{{font-size:15px}}
  html body #et-main-area .svc-feat .card .meta .lab{{font-size:10px;letter-spacing:.22em;margin-bottom:4px}}
  html body #et-main-area .svc-feat .card .meta .arrow{{font-size:20px;font-weight:500}}
  html body #et-main-area .svc-feat .copy p{{font-size:14.5px}}
  html body #et-main-area .svc-tiles .cards{{grid-template-columns:1fr}}
  html body #et-main-area .svc-tiles .card{{padding:20px 22px;gap:8px}}
  html body #et-main-area .svc-tiles .card+.card{{margin-left:0;margin-top:-1px}}
  html body #et-main-area .svc-tiles .card h3{{font-size:17px}}
  html body #et-main-area .svc-over,html body #et-main-area .svc-faq,html body #et-main-area .svc-cta,html body #et-main-area .svc-tiles,html body #et-main-area .svc-feat{{padding:28px 0}}
  html body #et-main-area .svc-split,html body #et-main-area .svc-hoods{{padding:22px 0 28px}}
}}
{CSS_END}
"""

# ---- Business info ----
BIZ_NAME = "Palermo Homes"
BIZ_URL = "https://palermohomes.com"
BIZ_PHONE = "+1-778-760-4113"
BIZ_CITY = "Kelowna"
BIZ_REGION = "BC"
BIZ_COUNTRY = "CA"


def business_schema(lat=None, lon=None):
    geo_block = ""
    if lat is not None and lon is not None:
        geo_block = f',\n    "geo": {{"@type":"GeoCoordinates","latitude":{lat},"longitude":{lon}}}'
    return f'''{{
    "@type": "HomeAndConstructionBusiness",
    "@id": "{BIZ_URL}/#organization",
    "name": "{BIZ_NAME}",
    "url": "{BIZ_URL}",
    "telephone": "{BIZ_PHONE}",
    "priceRange": "$$$$",
    "image": "{BIZ_URL}/wp-content/uploads/2025/12/Cabernet-07.jpg",
    "address": {{"@type":"PostalAddress","addressLocality":"{BIZ_CITY}","addressRegion":"{BIZ_REGION}","addressCountry":"{BIZ_COUNTRY}"}},
    "openingHoursSpecification": [{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"17:00"}}],
    "knowsAbout": ["Custom Home Construction","Home Renovations","General Contracting","Kitchen Renovations","Bathroom Renovations","Whole-Home Renovations","Custom Cabinetry","Finish Carpentry"],
    "sameAs": ["https://www.facebook.com/PalermoHomes","https://www.instagram.com/palermohomesltd/","https://www.houzz.com/professionals/home-builders/palermo-homes-pfvwus-pf~1452287384"]{geo_block}
  }}'''


def service_schema(name, description, page_url, area, region, lat, lon):
    return f'''{{
    "@type": "Service",
    "serviceType": "Custom Home Construction",
    "name": "{name}",
    "description": "{description}",
    "url": "{page_url}",
    "provider": {business_schema(lat, lon)},
    "areaServed": {{"@type":"Place","name":"{area}","address":{{"@type":"PostalAddress","addressLocality":"{area}","addressRegion":"{region}","addressCountry":"CA"}}}}
  }}'''


def place_schema(name, city, region, lat, lon):
    return f'''{{
    "@type": "Place",
    "name": "{name}",
    "address": {{"@type":"PostalAddress","addressLocality":"{city}","addressRegion":"{region}","addressCountry":"CA"}},
    "geo": {{"@type":"GeoCoordinates","latitude":{lat},"longitude":{lon}}},
    "containedInPlace": {{"@type":"AdministrativeArea","name":"{city}, {region}"}}
  }}'''


def faq_schema(faqs):
    items = []
    for q, a in faqs:
        items.append(f'''{{
      "@type":"Question",
      "name":{json.dumps(q)},
      "acceptedAnswer":{{"@type":"Answer","text":{json.dumps(a)}}}
    }}''')
    return f'''{{
    "@type":"FAQPage",
    "mainEntity":[{",".join(items)}]
  }}'''


def breadcrumb_schema(page_url, city_slug, city_name, neighborhood_name):
    return f'''{{
    "@type":"BreadcrumbList",
    "itemListElement":[
      {{"@type":"ListItem","position":1,"name":"Home","item":"{BIZ_URL}/"}},
      {{"@type":"ListItem","position":2,"name":"Service Areas","item":"{BIZ_URL}/service-areas/"}},
      {{"@type":"ListItem","position":3,"name":"{city_name}","item":"{BIZ_URL}/service-areas/{city_slug}/"}},
      {{"@type":"ListItem","position":4,"name":"{neighborhood_name}","item":"{page_url}"}}
    ]
  }}'''


def webpage_schema(page_url, neighborhood, meta_desc):
    return f'''{{
    "@type": "WebPage",
    "@id": "{page_url}#webpage",
    "url": "{page_url}",
    "name": "Custom Home Builder {neighborhood}",
    "description": "{meta_desc}",
    "isPartOf": {{"@id": "{BIZ_URL}/#website"}},
    "about": {{"@id": "{BIZ_URL}/#organization"}},
    "datePublished": "{BUILD_DATE}",
    "dateModified": "{BUILD_DATE}",
    "inLanguage": "en-CA"
  }}'''


def full_schema(*blocks):
    return '<script type="application/ld+json">{"@context":"https://schema.org","@graph":[' + ",".join(blocks) + ']}</script>'


def render_page(title, meta_desc, canonical, schema_block, main_html, out_path: Path):
    html = SHELL_HEAD + main_html + SHELL_FOOT
    if CSS_START in html:
        html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.DOTALL)
    html = re.sub(r"/\* ==== ABOUT-V2 CSS START ==== \*/.*?/\* ==== ABOUT-V2 CSS END ==== \*/", "", html, flags=re.DOTALL)
    html = html.replace("</style></head>", AREAS_CSS + "</style></head>", 1)
    html = html.replace('href="../index.html"', 'href="/"')
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', html, count=1)
    # Strip existing canonical (any attribute order), inject fresh
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{canonical}"/>\n</head>', 1)
    # Strip existing meta description, inject fresh
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{meta_desc}"/>\n</head>', 1)
    # Overwrite stale OG tags inherited from the About shell
    _og_image = f"https://palermohomes.com/wp-content/uploads/2025/12/Cabernet-02.jpg"
    _og_title = title.replace(" | Palermo Homes", "")
    html = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{_og_title}" property="og:title"/>', html, count=1)
    html = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{canonical}" property="og:url"/>', html, count=1)
    html = re.sub(r'<meta[^>]*property="article:modified_time"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:data1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta[^>]*name="twitter:label1"[^>]*/?>\s*', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:description"/>\n?', '', html)
    html = re.sub(r'<meta content="[^"]*" property="og:image"/>\n?', '', html)
    html = re.sub(
        r'(<meta content="[^"]*" property="og:site_name"/>)',
        r'\1' + f'\n<meta content="{meta_desc}" property="og:description"/>\n<meta content="{_og_image}" property="og:image"/>',
        html, count=1,
    )
    html = re.sub(r'<script class="yoast-schema-graph"[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(
        r'<link rel="preload" as="image" href="[^"]*" fetchpriority="high">',
        f'<link rel="preload" as="image" href="{_og_image}" fetchpriority="high">',
        html, count=1,
    )
    html = html.replace("</head>", schema_block + "</head>", 1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"  wrote {out_path.relative_to(SITE)}")


# ---- Data: neighborhoods ----
NEIGHBORHOODS = {
    "lakestone": {
        "name": "Lakestone",
        "parent_city": "Lake Country",
        "parent_slug": "lake-country",
        "region": "BC",
        "lat": "50.0611",
        "lon": "-119.4020",
        "h1": "Custom Home Builder in Lakestone, Lake Country.",
        "sub": "A Macdonald Development master-planned community above Okanagan Lake, minutes from Kelowna Airport, on the Scenic Sip wine trail.",
        "hero": "/wp-content/uploads/2022/04/PAL_220411_Main2.jpg",
        "hero_alt": "Custom home in Lakestone, Lake Country by Palermo Homes",
        "meta_title": "Custom Home Builder Lakestone, Lake Country | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes in Lakestone, a master-planned community above Okanagan Lake in Lake Country, BC.",
        "eyebrow": "Neighbourhood · Lake Country",
        "overview": [
            "Palermo Homes has built two custom homes in Lakestone, Macdonald Development's master-planned community above Okanagan Lake. We know the design guidelines, the ARC submission rhythm, and how the District of Lake Country permit process runs. Every build starts with the view corridor, then the hillside geotech. In-house cabinetry, custom finish carpentry, and envelope details are the finish standard we bring.",
            "We build for Lakestone's mountainside terrain: retaining, drainage, view-first orientation, and the ARC review process. Our two completed builds are in the earlier phases. We're actively taking on new projects across Waterside, Benchlands, Highlands, and The Summit's 57 premium lots opening late 2026.",
            "Lakestone is Macdonald Development Corporation's 1,365-residence master-planned community, finalized 2012 across 12 phases in three areas: Waterside on the shoreline, Benchlands 500 feet above Okanagan Lake, and Highlands up Beacon Hill. Every homeowner gets Lake Club membership (outdoor pool, gym, tennis, pickleball, covered court) plus private beach and marina access. Lakestone sits on the Scenic Sip wine trail; Gray Monk and Ex Nihilo are within walking distance, 50th Parallel a few minutes down Cars Landing Road. YLW is 10 min south, downtown Kelowna 30. Schools are SD23: Peter Greer, HS Grenda, George Elliot.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2026/09/lakestone-lot-view.jpg", "Lakestone lot view over Okanagan Lake, Lake Country, BC"),
        ],
        "amenities": [
            ("Recreation", "The Lake Club", "Residents-only clubhouse with outdoor pool, gym, and lounge"),
            ("Sport Courts", "Tennis + Pickleball", "Multiple outdoor courts plus a covered hockey / basketball court"),
            ("Waterfront", "Lakestone Marina", "Private beach club and marina access on Okanagan Lake"),
            ("Nature", "Community Trails", "Hillside trail network connecting Waterside, Benchlands, and Highlands"),
        ],
        "facts": [
            ("Community Plan", "1,365 Residences · 12 Phases"),
            ("Amenities", "The Lake Club + Marina"),
            ("Kelowna Airport", "10 min · 9.5 km"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why Lakestone clients hire Palermo.",
        "why_items": [
            ("Two Lakestone builds under our belt", "We've delivered two custom homes here and know the Macdonald ARC process, the material palette guidelines, and how each phase sits on the mountainside."),
            ("Hillside and view-corridor experience", "Lakestone lots are cut into the mountainside above Okanagan Lake. Retaining, drainage, and structural engineering carry real weight here. We've been doing hillside custom work for years across Upper Mission and the West Kelowna wine district."),
            ("Fluent in the design guidelines", "Macdonald's Architectural Review Committee checks material palette, roof pitch, massing, and colour on every submission. We design inside the guidelines and handle the ARC package so nothing bounces back."),
            ("District of Lake Country permits", "Lake Country's permit and inspection process runs differently than City of Kelowna. We've been through it, know the timelines, and know the inspectors on the file."),
            ("Same finish standard as our wine-district work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. Lakestone homes hold value because neighbours set a high bar, and we match it."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Lakestone custom home interior by Palermo Homes",
        "split_photo_loc": "Lakestone, Lake Country",
        "feat_h": "Featured Lakestone build.",
        "feat_body": "Our Lakestone custom home. A mountainside build oriented for the Okanagan Lake view corridor, with a custom stone-and-timber exterior that meets the Lakestone design guidelines and a fully custom interior finish package built in-house.",
        "feat_photo": "/wp-content/uploads/2022/04/PAL_220411_Main2.jpg",
        "feat_photo_alt": "Custom Lakestone home by Palermo Homes in Lake Country",
        "feat_link": "/project/lakestone/",
        "feat_link_label": "View this Lakestone home",
        "feat_card_loc": "Lake Country, BC",
        "feat_card_title": "Custom Home in Lakestone",
        "faqs": [
            ("How much does a custom home cost in Lakestone?",
             "Most Lakestone custom builds run $2.5M and up for the home alone, which pencils out around $650 to $900 per square foot depending on finish level. Lot prices start around $700K and go well past $2M for premium Waterside shoreline and Benchlands view lots. Highlands lots up Beacon Hill sit lower on price but usually carry more site work. Total finished cost swings with slope, retaining, geotech, and finish level. A flatter Waterside cut vs. a steep Highlands cut can differ by six figures on site work alone. Add ARC compliance costs (material palette, roof profile, colour approvals) and Lake Club initiation into the budget from the start. We provide line-item pricing up front, break out soft costs (design, permits, geotech, ARC package) from hard costs, and lock in fixed-price contracts where possible so nothing sneaks up on you mid-build."),
            ("Do Lakestone homes have to follow design guidelines?",
             "Yes. Macdonald Development's Architectural Review Committee (ARC) signs off on every custom home before permits go in. They check material palette (natural stone, wood, steel, board-and-batten), roof pitch and profile, massing and height, exterior colour range, glazing ratios, and how the home sits on the lot in relation to neighbours' view corridors. It's stricter than most Okanagan communities and it's what keeps the aesthetic consistent across Waterside, Benchlands, and Highlands. ARC approval typically runs 3 to 5 weeks from a complete submission, and revisions add time. We design inside the guidelines from the first sketch, prepare the full ARC package (site plan, elevations, material board, colour selections, landscaping plan), and manage revisions with the committee. That means fewer bounces, less design cost, and no ARC surprises when it's time to break ground."),
            ("How long does a Lakestone custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and ARC approval, 2 to 3 months for District of Lake Country building permits and geotechnical assessment (longer on steep cuts and complex retaining), and 9 to 12 months of construction. Highlands and steep Benchlands lots often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping compared to flatter Waterside lots. Weather matters too. Excavation, foundations, and framing move fastest through summer, and interior finish work carries through winter without weather risk. We schedule with that seasonality in mind so critical exterior phases hit the right months. A realistic build calendar for Lakestone assumes ARC and permit in the first winter, break ground in spring, lock-up by fall, and interior finish through the following winter for a summer move-in."),
            ("Which Lakestone phases have you built in?",
             "Our two completed Lakestone homes sit in the earlier developed phases. Lot releases continue in stages across the three main areas: Waterside on the Okanagan Lake shoreline (limited inventory, premium pricing), Benchlands 500 feet above the lake (steady release of view lots), and Highlands climbing Beacon Hill (larger inventory, more varied lot types). The newest release is The Summit at Lakestone with 57 premium homesites opening for construction in late 2026 and early 2027. Roughly 250 residences were occupied as of 2020 with the plan totalling 1,365 across 12 phases. We're actively taking on projects across every current release. Whether you already own a lot, are negotiating a purchase, or are picking between Waterside view lots and Highlands hillside cuts, bring us the lot survey. We'll walk the property with you, review the ARC guidelines specific to that phase, and give you a real cost and timeline read before you commit."),
            ("What amenities do Lakestone residents get access to?",
             "Every Lakestone home comes with a Lake Club membership. That covers the outdoor pool, fitness centre, lounge, tennis and pickleball courts, and a covered court that swaps between hockey and basketball. Homeowners also get private beach club and marina access on Okanagan Lake, with boat slip availability tied to phase and inventory. The community trail network runs 28.8 km from the shoreline up to Summit Park, climbing a 300 metre grade with lookouts across the lake. The Okanagan Rail Trail (a 50 km multi-use path along the old CN corridor from Coldstream to Kelowna) is about 5 km away at McCarthy Road. Lakestone also sits on the Scenic Sip wine trail. Gray Monk and Ex Nihilo are within walking distance, 50th Parallel is a few minutes down Cars Landing Road, and Arrowleaf and Ancient Hill round out a five-winery loop within a 10-minute drive. HOA fees fund the Lake Club, common landscaping, and community maintenance."),
            ("What schools are near Lakestone?",
             "Lakestone is in Central Okanagan Public Schools (SD23). Peter Greer Elementary at 10300 Sherman Drive covers K to 6 and offers both English and French Immersion streams. École HS Grenda Middle at 10168 Konschuh Road handles grades 7 to 9. George Elliot Secondary at 10241 Bottom Lake Road is the high school (grades 10 to 12). All three sit inside Lake Country, roughly 5 to 8 minutes from the community. For families looking at independent schools, Aberdeen Hall Preparatory (K to 12) in Kelowna's Glenmore area is about 25 minutes south on Highway 97, and Immaculata Regional High School (Catholic, grades 8 to 12) is a similar drive. Post-secondary is close too. UBC Okanagan and Okanagan College's Kelowna campus are both roughly 25 minutes down the highway."),
            ("How far is Lakestone from Kelowna and the airport?",
             "Kelowna International Airport (YLW) is about 9.5 km south, a 10-minute drive on Highway 97 with direct flights to Vancouver, Calgary, Seattle, and seasonal service to Toronto. Downtown Kelowna is another 20 minutes past the airport. UBC Okanagan, Okanagan College, and Kelowna General Hospital are all roughly 25 minutes south. Vernon is 25 minutes north on the same highway, and Predator Ridge and Sparkling Hill Resort are within 30 minutes. For weekend recreation, Big White Ski Resort is about an hour southeast, Silver Star Mountain Resort is 45 minutes north, and Kalamalka Lake beaches are 20 minutes up the road. The Okanagan Rail Trail at McCarthy Road (5 km away) links cyclists into a 50 km continuous corridor between Coldstream and downtown Kelowna. BX Transit line 23 runs the Highway 97 corridor for those who prefer transit over driving."),
        ],
    },

    "upper-mission": {
        "name": "Upper Mission",
        "parent_city": "Kelowna",
        "parent_slug": "kelowna",
        "region": "BC",
        "lat": "49.8397",
        "lon": "-119.4884",
        "h1": "Custom Home Builder in Upper Mission, Kelowna.",
        "sub": "Kelowna's flagship luxury district on the south hillside above Okanagan Lake. Kettle Valley, Southridge, The Ponds, Crawford Estates.",
        "hero": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "hero_alt": "Modern lakeview custom home by Palermo Homes, portfolio match for Upper Mission",
        "meta_title": "Custom Home Builder Upper Mission, Kelowna | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes across Upper Mission's Kettle Valley, Southridge, The Ponds, and Crawford Estates in Kelowna, BC.",
        "eyebrow": "Neighbourhood · Kelowna",
        "overview": [
            "Palermo Homes builds custom homes across Upper Mission, Kelowna's flagship luxury district on the south hillside above Okanagan Lake. We navigate the sub-community design reviews that Kettle Valley, Southridge, The Ponds, and Crawford Estates each enforce differently, and we cut hillside lots for the lake-view corridor. In-house cabinetry, custom finish carpentry, and envelope details are the standard our Cabernet Way and Lakestone builds set.",
            "We build for Upper Mission's hillside terrain: retaining, drainage, view-first orientation, and the specific design review each sub-community runs. We know City of Kelowna permits and the local geotech. Non-waterfront homes here carry a 20 percent premium over Lower Mission, driven by finish standard as much as location.",
            "Upper Mission is a collection of master-planned sub-communities on Kelowna's south hillside: Kettle Valley (mid-1990s, neo-traditional plan with a dozen parks), Southridge (mid-2000s), The Ponds (newest, still building out), plus Crawford Estates and Westpointe. Mission Recreation Park (44 hectares, 13 sports fields) anchors the north edge, with H2O Adventure Centre (Canada's largest municipal waterpark) next door. Mission Creek Greenway (16 km) and Kettle Valley Rail Trail (42.5 km of 53 km planned) run through the district. Southeast Kelowna's wine trail: CedarCreek, Tantalus, St. Hubertus, Summerhill Pyramid, all within 10 minutes. Downtown 15 min, YLW 25.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2025/12/Cabernet-07.jpg", "Modern hillside custom home facade with stone entry, Palermo Homes portfolio"),
        ],
        "amenities": [
            ("Recreation", "Mission Recreation Park", "Kelowna's largest recreation park at 44 hectares with 13 sports fields"),
            ("Aquatics", "H2O Adventure Centre", "Canada's largest municipal waterpark with FlowRider and 12,000 sq ft gym"),
            ("Nature", "Mission Creek Greenway", "16 km of continuous trail through riparian forest and Scenic Canyon"),
            ("Cycling", "Kettle Valley Rail Trail", "42.5 km rail-corridor path connecting Upper Mission to the wider valley"),
        ],
        "facts": [
            ("Sub-Communities", "Kettle Valley · Southridge · The Ponds"),
            ("Amenities", "Mission Rec Park + H2O"),
            ("Kelowna Airport", "25 min · 20 km"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why Upper Mission clients hire Palermo.",
        "why_items": [
            ("Sub-community fluency", "Kettle Valley, Southridge, The Ponds, and Crawford Estates each have their own design review process and material expectations. We know how each one runs and design inside those guidelines from the start."),
            ("Hillside and view-corridor experience", "Upper Mission lots are cut into the south hillside above Okanagan Lake. Retaining walls, drainage plans, and view-first orientation carry real weight here. We've been doing hillside custom work for years across the West Kelowna wine district and Lakestone."),
            ("City of Kelowna permit fluency", "Upper Mission builds run through City of Kelowna permits and inspection. We know the timelines, the inspectors, and the servicing coordination that hillside lots require."),
            ("Same finish standard as our wine-district work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. Upper Mission homes hold their value because the neighbours set a high bar and we match it."),
            ("Design that respects the view", "The view corridor drives every early decision. Kitchen, primary bedroom, living room placement, glazing ratios, and roofline all get planned around where the lake and mountains sit from each room."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom Upper Mission home interior by Palermo Homes",
        "split_photo_loc": "Upper Mission, Kelowna",
        "feat_h": "Portfolio match for Upper Mission.",
        "feat_body": "Our Modern Lakeview Home on Cabernet Way in West Kelowna is the closest portfolio match for what an Upper Mission custom build should be. Full lake-view orientation, a hillside cut, custom finish carpentry throughout, and the material palette that fits Kelowna's premium hillside districts. Terrain and view considerations map directly to Kettle Valley, Southridge, and Crawford lots.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "feat_photo_alt": "Modern lakeview custom home on Cabernet Way, West Kelowna by Palermo Homes",
        "feat_link": "/project/1252/",
        "feat_link_label": "View the Cabernet Way home",
        "feat_card_loc": "West Kelowna, BC",
        "feat_card_title": "Modern Lakeview Home on Cabernet Way",
        "faqs": [
            ("How much does a custom home cost in Upper Mission?",
             "Most Upper Mission custom builds run $2M and up for the home alone, which pencils out around $600 to $900 per square foot depending on finish level. Lot prices range from around $500K for smaller Southridge or Ponds lots to $2M plus for premium Kettle Valley or Crawford Estates view lots. Total finished cost swings with slope, retaining, geotech, and finish level. A flatter lot vs. a steep hillside cut can differ by six figures on site work alone. Add sub-community design review costs (material palette, roof profile, colour approvals) into the budget from the start. We provide line-item pricing up front, break out soft costs (design, permits, geotech) from hard costs, and lock in fixed-price contracts where possible so nothing sneaks up on you mid-build."),
            ("Do Upper Mission homes have to follow design guidelines?",
             "It depends which sub-community you're building in. Kettle Valley has its own architectural guidelines and colour palette rooted in its neo-traditional village plan. Southridge and The Ponds each have their own submission process. Crawford Estates enforces a material palette and roofline standard. Westpointe has its own review. City of Kelowna sits above all of this with the standard building code and hillside development permits. We design inside the specific sub-community's guidelines from the first sketch and manage the review package on your behalf. That means fewer bounces, less design cost, and no surprises at permit time."),
            ("How long does an Upper Mission custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and sub-community design review, 2 to 3 months for City of Kelowna building permits and geotechnical assessment (longer on steep cuts and complex retaining), and 9 to 12 months of construction. Steep Kettle Valley and Crawford Estates lots often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping compared to flatter Ponds or Southridge lots. Weather matters too. Excavation, foundations, and framing move fastest through Kelowna summers. Interior finish work carries through winter without weather risk, so we schedule critical exterior phases to hit the right months."),
            ("Which Upper Mission sub-community should I build in?",
             "Kettle Valley suits buyers who want a village-scale neighbourhood feel with 12 parks, walking distance to schools, and a mature streetscape. Southridge is a good fit for larger contemporary homes on view lots with more privacy. The Ponds is Upper Mission's newest zone, with modern architecture, a coming middle school, and lots still releasing. Crawford Estates and Westpointe suit buyers who want established prestige with mature landscaping. We build across all of them and can walk any lot with you to compare geotech, servicing, and view corridors before you commit."),
            ("What amenities do Upper Mission residents get access to?",
             "Mission Recreation Park is the big one: 44 hectares, 13 sports fields, off-leash dog area, community garden, and playgrounds. H2O Adventure and Fitness Centre is right next door, with a wave pool, lazy river, waterslides, FlowRider surf simulator, and a 12,000 sq ft fitness floor. Kettle Valley alone has a dozen parks woven into its village plan. Mission Creek Greenway runs 16 km continuously along the creek, and the Kettle Valley Rail Trail carries another 42.5 km of the planned 53 km rail-corridor path for cycling. New for summer 2026, an indoor-outdoor tennis facility is being built at Mission Rec Park, and 2027 brings a new indoor multi-age activity centre."),
            ("What schools are near Upper Mission?",
             "Upper Mission is in Central Okanagan Public Schools (SD23). Chute Lake Elementary at 5240 Lark Street sits inside the district and connects directly to Chute Lake Park. Anne McClymont Elementary at 4489 Lakeshore Road serves the broader Mission area. Canyon Falls Middle School handles grades 6 to 8. Kelowna Secondary is the current high school assignment. The Ponds is slated to receive Kelowna's newest middle school as the sub-community builds out. For independent schools, Aberdeen Hall Preparatory (K to 12) in Glenmore is about 25 minutes north, and Immaculata Regional High School is a similar drive. UBC Okanagan and Okanagan College are 30 minutes north."),
            ("How far is Upper Mission from downtown Kelowna and the airport?",
             "Downtown Kelowna is roughly 15 minutes north on Lakeshore Road, past Rotary Beach and Lower Mission. Kelowna International Airport (YLW) is about 25 minutes north via Highway 97, with direct flights to Vancouver, Calgary, Seattle, and seasonal service to Toronto. UBC Okanagan, Okanagan College, and Kelowna General Hospital are all 25 to 30 minutes away. Big White Ski Resort is about 45 minutes southeast for weekend skiing. The Southeast Kelowna wine trail (CedarCreek, Tantalus, St. Hubertus, Summerhill Pyramid) is 10 minutes east, and West Kelowna's Mission Hill winery is 25 minutes across the bridge."),
        ],
    },

    "kettle-valley": {
        "name": "Kettle Valley",
        "parent_city": "Kelowna",
        "parent_slug": "kelowna",
        "region": "BC",
        "lat": "49.8336",
        "lon": "-119.5019",
        "h1": "Custom Home Builder in Kettle Valley, Kelowna.",
        "sub": "Kelowna's award-winning master-planned neo-traditional village in Upper Mission. Central green, working village centre, and a dozen parks.",
        "hero": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "hero_alt": "Modern lakeview custom home by Palermo Homes, portfolio match for Kettle Valley",
        "meta_title": "Custom Home Builder Kettle Valley, Kelowna | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes in Kettle Valley, Kelowna's master-planned neo-traditional village in Upper Mission.",
        "eyebrow": "Neighbourhood · Kelowna",
        "overview": [
            "Palermo Homes builds custom homes in Kettle Valley, Kelowna's award-winning master-planned neighbourhood on the south Upper Mission hillside. We design inside the neo-traditional architectural review, cut hillside lots for the view corridor, and deliver the finish standard a $1.65M+ Kettle Valley address demands. In-house cabinetry, custom finish carpentry, and envelope details are the standard our Cabernet Way and Lakestone builds set.",
            "We build for Kettle Valley's neo-traditional guidelines: roof pitches, material palettes, front porches, garage siting, and street-relationship all get planned inside architectural review from day one. We know City of Kelowna permits, the hillside geotech Upper Mission demands, and how to design inside the walkable-village aesthetic.",
            "Kettle Valley was established 1996 on the neo-traditional plan by Ekistics, built through the 2000s around a working village square (coffee shop, restaurant, gym, spa, daycare, clinics). The community sits inside 400+ hectares of Johns Family Nature Conservancy trails with the Kettle Valley Railway trail running through it. Quilchena, Curlew, and Bertram Creek parks anchor recreation. Full SD23 pathway inside the community: Chute Lake Elementary, Canyon Falls Middle, Okanagan Mission Secondary. Summerhill Pyramid, St. Hubertus, CedarCreek, and Tantalus wineries within 10 minutes. YLW is 30-35 min north on Highway 97; Highpointe executive lots push past $2M.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2025/12/Cabernet-07.jpg", "Modern hillside custom home facade with stone entry, Palermo Homes portfolio"),
        ],
        "amenities": [
            ("Village Centre", "Coffee, Pizza, Gym, Spa", "Walkable village square with a dozen resident-serving businesses"),
            ("Parks", "Quilchena + Curlew + Bertram Creek", "Waterpark, sport courts, tobogganing hill, plus Okanagan Lake beach"),
            ("Trails", "KVR + Johns Conservancy", "Kettle Valley Railway trail through community, 400+ ha regional park adjacent"),
            ("Schools", "Chute Lake · Canyon Falls · OKM", "Full K-12 SD23 pathway inside the neighbourhood"),
        ],
        "facts": [
            ("Established", "1996 · Neo-Traditional Plan"),
            ("Amenities", "Village Centre + 12 Parks"),
            ("Kelowna Airport", "30 min · Highway 97"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why Kettle Valley clients hire Palermo.",
        "why_items": [
            ("Neo-traditional guideline fluency", "Kettle Valley's architectural review checks roof pitches, front-porch depth, material palette, garage siting, and street-relationship on every home. We design inside those rules from the first sketch and manage the submission so nothing bounces back."),
            ("Hillside and view-corridor experience", "Kettle Valley lots step down the south Upper Mission hillside above Okanagan Lake. Retaining, drainage, and view-first orientation carry real weight. We've been doing hillside custom work for years across the West Kelowna wine district and Lakestone."),
            ("City of Kelowna permit fluency", "Kettle Valley builds run through City of Kelowna permits and inspection. We know the timelines, the inspectors, and the servicing coordination that Upper Mission hillside lots require."),
            ("Walkable-village design instincts", "Kettle Valley is not a subdivision of maximized garages. Front porches, human-scale facades, and how the home reads from the sidewalk all matter. We design homes that fit the village and hold their value because of it."),
            ("Same finish standard as our wine-district work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. Kettle Valley homes hold their value because neighbours set a high bar and we match it."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom Kettle Valley home interior by Palermo Homes",
        "split_photo_loc": "Kettle Valley, Kelowna",
        "feat_h": "Portfolio match for Kettle Valley.",
        "feat_body": "Our Modern Lakeview Home on Cabernet Way in West Kelowna is the closest portfolio match for what a Kettle Valley custom build should be. Hillside cut, full lake-view orientation, custom finish carpentry throughout, and the material palette that fits Kelowna's premium hillside districts. Terrain and view considerations map directly to Kettle Valley lots.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "feat_photo_alt": "Modern lakeview custom home on Cabernet Way, West Kelowna by Palermo Homes",
        "feat_link": "/project/1252/",
        "feat_link_label": "View the Cabernet Way home",
        "feat_card_loc": "West Kelowna, BC",
        "feat_card_title": "Modern Lakeview Home on Cabernet Way",
        "faqs": [
            ("How much does a custom home cost in Kettle Valley?",
             "Most Kettle Valley custom builds run $1.8M and up for the home alone, which pencils out around $600 to $900 per square foot depending on finish level. Lot prices sit well above Kelowna's average, and Highpointe executive lots often push past $2M just for the land. Total finished cost swings with slope, retaining, geotech, and finish level. Add architectural review costs (roof pitch, material palette, porch and garage siting approvals) plus the mandatory community association fee ($300 to $600 annually) into the budget from the start. We provide line-item pricing up front, break out soft costs (design, permits, geotech, ARC package) from hard costs, and lock in fixed-price contracts where possible so nothing sneaks up on you mid-build."),
            ("Do Kettle Valley homes have to follow design guidelines?",
             "Yes. Kettle Valley is a master-planned community with an architectural review process rooted in its 1996 neo-traditional plan. Reviewers look at roof pitches, front-porch depth, material palette, exterior colour range, garage placement, and how the home relates to the street grid. It is stricter than most Kelowna neighbourhoods and it is what keeps the walkable village feel consistent across every block. We design inside the guidelines from the first sketch and manage the review submission for you."),
            ("How long does a Kettle Valley custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and architectural review, 2 to 3 months for City of Kelowna building permits and geotechnical assessment (longer on steep cuts), and 9 to 12 months of construction. Steeper Kettle Valley lots (especially in Highpointe and along the view-corridor edges) often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping. Weather matters too. Excavation, foundations, and framing move fastest through Kelowna summers, and interior finish work carries through winter without weather risk."),
            ("What sub-areas of Kettle Valley are people building in?",
             "Kettle Valley is not divided into named phases the way Lakestone or Wilden are, but there are recognizable pockets. Highpointe is the executive-home enclave at the top of the community with the biggest view lots (often $2M+ for the land alone). The village core is the walkable heart around Quilchena Park with tighter lots and porch-focused streetscapes. The Kettle Valley Railway trail edge lots offer direct trail access with fewer neighbours behind you. Bring us your lot and we will walk it with you, review the specific architectural guidelines that apply, and give you a real cost and timeline read before you commit."),
            ("What amenities do Kettle Valley residents get access to?",
             "Kettle Valley has its own walkable village centre with a coffee shop, pizza takeaway, restaurant, gym, spa, daycare, dentist, and chiropractor. The community includes more than a dozen parks. Quilchena Park is the main hub with a waterpark, playground, and open sports space. Curlew Park adds soccer field, baseball diamond, basketball court, and a tobogganing hill. Bertram Creek Regional Park on Okanagan Lake is minutes down the hill with 17.9 hectares of beach, pier, and a covered amphitheatre. The Kettle Valley Railway trail runs through the community, and the 400+ hectare Johns Family Nature Conservancy Regional Park sits at the edge."),
            ("What schools are near Kettle Valley?",
             "Kettle Valley is in Central Okanagan Public Schools (SD23) and has a full K to 12 pathway inside Upper Mission. Chute Lake Elementary (built 2009, roughly 470 to 500 students) covers K to 6 and connects directly to Chute Lake Park. Canyon Falls Middle School (opened September 2019, roughly 760 students) handles grades 6 to 8 in a purpose-built modern facility with a full sports field. Okanagan Mission Secondary (OKM) is the grade 9 to 12 high school. For independent schools, Aberdeen Hall Preparatory (K to 12) in Kelowna's Glenmore area is about 25 minutes north on Highway 97, and Immaculata Regional High School is a similar drive. UBC Okanagan and Okanagan College are 30 to 35 minutes north."),
            ("How far is Kettle Valley from downtown Kelowna and the airport?",
             "Downtown Kelowna is roughly 20 minutes north down Chute Lake Road and Lakeshore Road, past Lower Mission. Kelowna International Airport (YLW) is 30 to 35 minutes north on Highway 97, with direct flights to Vancouver, Calgary, Seattle, and seasonal service to Toronto. UBC Okanagan, Okanagan College, and Kelowna General Hospital are all 30 to 35 minutes away. Big White Ski Resort is about 45 minutes southeast. The Southeast Kelowna wine trail is at the door: Summerhill Pyramid is under 5 minutes, St. Hubertus 7 minutes, CedarCreek and Tantalus about 9. Mission Hill winery across the bridge in West Kelowna is 30 minutes."),
        ],
    },

    "wilden": {
        "name": "Wilden",
        "parent_city": "Kelowna",
        "parent_slug": "kelowna",
        "region": "BC",
        "lat": "49.9302",
        "lon": "-119.4406",
        "h1": "Custom Home Builder in Wilden, Kelowna.",
        "sub": "BC's largest master-planned community. 1,447 acres, 30 neighbourhoods on the Glenmore Highlands between Okanagan Lake and Glenmore Road.",
        "hero": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "hero_alt": "Modern lakeview custom home by Palermo Homes, portfolio match for Wilden",
        "meta_title": "Custom Home Builder Wilden, Kelowna BC | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes in Wilden, a master-planned community on Kelowna's Glenmore Highlands, BC.",
        "eyebrow": "Neighbourhood · Kelowna",
        "overview": [
            "Palermo Homes builds custom homes in Wilden, BC's largest master-planned community on Kelowna's Glenmore Highlands. We design inside Wilden's architectural guidelines, cut hillside lots for the lake and valley views, and deliver the finish standard our Cabernet Way and Lakestone builds set.",
            "We build for Wilden's hillside terrain: retaining, drainage, view-corridor orientation, and the phase-by-phase design review that each release enforces differently. We know City of Kelowna permits and the Glenmore Highlands geotech.",
            "Wilden Construction Corp launched Wilden in 2003 (assembled by Gerhard Blenk's family in the mid-1990s). It covers 1,447 acres and 30 neighbourhoods with 1,500+ acres of green space, hiking and biking trails, and cluster-neighbourhood design that preserves the wilderness. Phases 1 and 2 total 2,000 homes running through 2035 to 2040. Phase 3 adds 326 single-family homes, 128 duplexes, 444 townhomes, and 148 condominiums. Schools are SD23: North Glenmore, Watson Road, Dr. Knox Middle, and Kelowna Secondary. Downtown Kelowna is 10 minutes down Glenmore Road, YLW airport 15 minutes north on Highway 97, UBC Okanagan 15 minutes northeast.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2025/12/Cabernet-07.jpg", "Modern hillside custom home facade with stone entry, Palermo Homes portfolio"),
        ],
        "amenities": [
            ("Green Space", "1,500+ Acres", "Over half of Wilden's 1,447-acre plan is dedicated parkland, trails, and wildlife"),
            ("Trails", "Extensive Network", "Hiking and biking trails across the Glenmore Highlands connecting all 30 neighbourhoods"),
            ("Schools", "SD23 K-12 Pathway", "North Glenmore, Watson Road, Dr. Knox Middle, Kelowna Secondary"),
            ("Access", "10 min to Downtown", "Fastest downtown Kelowna commute of any master-planned Okanagan community"),
        ],
        "facts": [
            ("Community Size", "1,447 Acres · 30 Neighbourhoods"),
            ("Downtown Kelowna", "10 min · Glenmore Road"),
            ("YLW Airport", "15 min · Highway 97"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why Wilden clients hire Palermo.",
        "why_items": [
            ("Master-planned community fluency", "Wilden's architectural review runs on a phase-by-phase basis. Guidelines shift between neighbourhoods and release types. We know how each phase runs and design inside those rules from the first sketch."),
            ("Glenmore Highlands hillside experience", "Wilden lots are cut into the Glenmore Highlands above Okanagan Lake. Retaining, drainage, and structural engineering carry real weight. We've been doing hillside custom work for years across Upper Mission, Lakestone, and the West Kelowna wine district."),
            ("City of Kelowna permit fluency", "Wilden builds run through City of Kelowna permits and inspection. We know the timelines, the inspectors, and the servicing coordination that hillside lots require."),
            ("View-corridor design", "The view corridor drives every early decision. Kitchen, primary bedroom, living room placement, glazing ratios, and roofline all get planned around where Okanagan Lake and the valley sit from each room."),
            ("Same finish standard as our wine-district work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. Wilden homes hold their value because the neighbours set a high bar and we match it."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom Wilden home interior by Palermo Homes",
        "split_photo_loc": "Wilden, Kelowna",
        "feat_h": "Portfolio match for Wilden.",
        "feat_body": "Our Modern Lakeview Home on Cabernet Way in West Kelowna is the closest portfolio match for what a Wilden custom build should be. Hillside cut, full lake-view orientation, custom finish carpentry throughout, and the material palette that fits Kelowna's premium master-planned districts. Terrain and view considerations map directly to Wilden's Glenmore Highlands lots.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "feat_photo_alt": "Modern lakeview custom home on Cabernet Way, West Kelowna by Palermo Homes",
        "feat_link": "/project/1252/",
        "feat_link_label": "View the Cabernet Way home",
        "feat_card_loc": "West Kelowna, BC",
        "feat_card_title": "Modern Lakeview Home on Cabernet Way",
        "faqs": [
            ("How much does a custom home cost in Wilden?",
             "Most Wilden custom builds run $1.8M and up for the home alone, which pencils out around $600 to $900 per square foot depending on finish level. Lot prices vary widely across Wilden's 30 neighbourhoods. Executive view lots in Phase 3 push past $1.5M, while smaller cluster-neighbourhood lots start closer to $500K. Total finished cost swings with slope, retaining, geotech, and finish level. Add architectural review costs (material palette, roof profile, colour approvals) into the budget from the start. We provide line-item pricing up front, break out soft costs (design, permits, geotech) from hard costs, and lock in fixed-price contracts where possible so nothing sneaks up on you mid-build."),
            ("Do Wilden homes have to follow design guidelines?",
             "Yes. Wilden Construction Corp runs an architectural review process for every custom home before permits go in. Guidelines cover material palette, roof pitch, massing, exterior colour, glazing ratios, and how the home sits on the lot in relation to Wilden's natural landscape philosophy. Guidelines shift between phases and neighbourhood types (single-family, duplex, townhome, cluster). We design inside the guidelines from the first sketch, prepare the full review package, and manage revisions with the committee so nothing bounces back."),
            ("How long does a Wilden custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and architectural review, 2 to 3 months for City of Kelowna building permits and geotechnical assessment (longer on steep cuts), and 9 to 12 months of construction. Steeper Glenmore Highlands lots often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping compared to flatter lots. Weather matters too. Excavation, foundations, and framing move fastest through Kelowna summers, and interior finish work carries through winter without weather risk."),
            ("Which Wilden phase or neighbourhood should I build in?",
             "Phases 1 and 2 are still building out with 2,000 homes total and completion running through 2035 to 2040. Phase 3 opens 326 single-family lots, 128 duplexes, 444 townhomes, and 148 condominiums built in cluster neighbourhoods to preserve the surrounding wilderness. If you're after executive view lots, Phase 3 single-family cluster neighbourhoods on the higher benches offer the best value. Lost Creek Point suits buyers looking at semi-detached townhomes with high-grade finishing. Bring us your lot survey and we'll walk it with you, review the guidelines specific to that phase, and give you a real cost and timeline read before you commit."),
            ("What amenities do Wilden residents get access to?",
             "Wilden is built around 1,500+ acres of dedicated green space, more than half of the 1,447-acre master plan. Residents get direct access to an extensive hiking and biking trail network across the Glenmore Highlands connecting all 30 neighbourhoods. Cluster-neighbourhood design preserves the surrounding wilderness, so most homes sit next to protected forest, lake views, or valley overlooks. The community's proximity to Knox Mountain Park (Kelowna's largest natural park) adds another 235 hectares of trails at the south edge. Downtown Kelowna amenities are 10 minutes down Glenmore Road, and Kelowna General Hospital, UBC Okanagan, and Okanagan College are all inside 20 minutes."),
            ("What schools are near Wilden?",
             "Wilden is in Central Okanagan Public Schools (SD23). North Glenmore Elementary and Watson Road Elementary cover K to 6 catchment. Dr. Knox Middle School handles grades 7 to 9. Kelowna Secondary is the high school for grades 10 to 12. All schools are inside 5 to 10 minutes of the community. For independent schools, Aberdeen Hall Preparatory (K to 12) is a few minutes down Glenmore Road, and Immaculata Regional High School is a similar drive. UBC Okanagan and Okanagan College's Kelowna campus are both 15 to 20 minutes northeast."),
            ("How far is Wilden from downtown Kelowna and the airport?",
             "Downtown Kelowna is 10 minutes south down Glenmore Road, past Knox Mountain. Kelowna International Airport (YLW) is 15 minutes north on Highway 97, with direct flights to Vancouver, Calgary, Seattle, and seasonal service to Toronto. UBC Okanagan and Okanagan College's Kelowna campus are 15 to 20 minutes northeast, Kelowna General Hospital 12 minutes south. Big White Ski Resort is 55 minutes southeast for weekend skiing. West Kelowna's wine district (Mission Hill, Quails' Gate) is 25 minutes across the bridge. The Kelowna Yacht Club, Waterfront Park, and downtown restaurants are the closest urban amenities of any Kelowna master-planned community."),
        ],
    },

    "mckinley-beach": {
        "name": "McKinley Beach",
        "parent_city": "Kelowna",
        "parent_slug": "kelowna",
        "region": "BC",
        "lat": "49.9821",
        "lon": "-119.4155",
        "h1": "Custom Home Builder in McKinley Beach, Kelowna.",
        "sub": "Kelowna's only lakefront master-planned community. 872 acres, 1 km of Okanagan Lake beachfront, private marina, and a working winery underway.",
        "hero": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "hero_alt": "Modern lakeview custom home by Palermo Homes, portfolio match for McKinley Beach",
        "meta_title": "Custom Home Builder McKinley Beach, Kelowna | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes in McKinley Beach, Kelowna's lakefront master-planned community on Okanagan Lake.",
        "eyebrow": "Neighbourhood · Kelowna",
        "overview": [
            "Palermo Homes builds custom homes in McKinley Beach, Kelowna's only lakefront master-planned community. We cut hillside lots for the Okanagan Lake view corridor, design inside McKinley's architectural review, and deliver the finish standard our Cabernet Way and Lakestone builds set. In-house cabinetry, custom finish carpentry, and envelope details are our standard.",
            "We build for McKinley Beach's hillside-to-lakefront terrain: retaining, drainage, view-first orientation, and the design review that each enclave enforces. We know City of Kelowna permits and the geotech across the McKinley hillside above Okanagan Lake.",
            "McKinley Beach is GGroup Development and North American Development Group's 872-acre master-planned community, approved for 1,300 residential units. Over 550 homes are complete across the first three phases (110 acres, six enclaves). Residents get a 110-slip marina, one kilometre of private Okanagan Lake beachfront, tennis and pickleball courts, community gardens, playgrounds, and a future clubhouse. A 42-acre working winery is under construction, and the Hilltown mixed-use village is planned. Custom lots start around $310K, townhomes from mid-$500K, single-family homes from low $600K. YLW airport is 10 minutes north on Highway 97, downtown Kelowna 20 minutes south.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2025/12/Cabernet-07.jpg", "Modern hillside custom home facade with stone entry, Palermo Homes portfolio"),
        ],
        "amenities": [
            ("Waterfront", "1 km Beachfront + Marina", "Kelowna's only lakefront master-planned community with a private 110-slip marina"),
            ("Sport Courts", "Tennis + Pickleball", "Multiple outdoor courts, community gardens, playgrounds"),
            ("Winery", "42-Acre Working Vineyard", "Community-owned working winery under construction"),
            ("Future", "Hilltown Mixed-Use Village", "Planned mixed-use core and residents-only clubhouse"),
        ],
        "facts": [
            ("Community Plan", "1,300 Units · 872 Acres"),
            ("Waterfront", "1 km Beach + 110-Slip Marina"),
            ("YLW Airport", "10 min · Highway 97"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why McKinley Beach clients hire Palermo.",
        "why_items": [
            ("Lakefront and hillside experience", "McKinley Beach lots step down from Highway 97 toward Okanagan Lake. Retaining, drainage, and view-first orientation carry real weight. We've been doing hillside custom work for years across Upper Mission, Lakestone, and the West Kelowna wine district."),
            ("Enclave-specific design review", "McKinley Beach runs six enclaves across the first three phases, each with its own guidelines. We design inside those rules from the first sketch and manage the review package so nothing bounces back."),
            ("City of Kelowna permit fluency", "McKinley Beach builds run through City of Kelowna permits and inspection. We know the timelines, the inspectors, and the servicing coordination that hillside-to-lakefront lots require."),
            ("View-corridor design", "Every early decision starts with the lake. Kitchen, primary bedroom, living room placement, glazing ratios, and roofline all get planned around where Okanagan Lake sits from each room."),
            ("Same finish standard as our wine-district work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. McKinley Beach homes hold their value because the neighbours set a high bar and we match it."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom McKinley Beach home interior by Palermo Homes",
        "split_photo_loc": "McKinley Beach, Kelowna",
        "feat_h": "Portfolio match for McKinley Beach.",
        "feat_body": "Our Modern Lakeview Home on Cabernet Way in West Kelowna is the closest portfolio match for what a McKinley Beach custom build should be. Hillside cut, full lake-view orientation, custom finish carpentry throughout, and the material palette that fits Kelowna's premium master-planned districts. Terrain and view considerations map directly to McKinley Beach lots.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "feat_photo_alt": "Modern lakeview custom home on Cabernet Way, West Kelowna by Palermo Homes",
        "feat_link": "/project/1252/",
        "feat_link_label": "View the Cabernet Way home",
        "feat_card_loc": "West Kelowna, BC",
        "feat_card_title": "Modern Lakeview Home on Cabernet Way",
        "faqs": [
            ("How much does a custom home cost in McKinley Beach?",
             "Most McKinley Beach custom builds run $1.8M and up for the home alone, which pencils out around $600 to $900 per square foot depending on finish level. Custom lot prices start around $310K for hillside lots and rise significantly for premium waterfront and beach-access lots. Total finished cost swings with slope, retaining, geotech, and finish level. Add architectural review costs (material palette, roof profile, colour approvals) into the budget from the start. We provide line-item pricing up front, break out soft costs (design, permits, geotech) from hard costs, and lock in fixed-price contracts where possible so nothing sneaks up on you mid-build."),
            ("Do McKinley Beach homes have to follow design guidelines?",
             "Yes. GGroup Development and NADG run an architectural review process for every custom home before permits go in. Guidelines cover material palette, roof pitch, massing, exterior colour, glazing ratios, and how the home sits on the lot in relation to the lake view corridor. Guidelines vary between the six enclaves. We design inside the guidelines from the first sketch, prepare the full review package, and manage revisions with the committee so nothing bounces back."),
            ("How long does a McKinley Beach custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and architectural review, 2 to 3 months for City of Kelowna building permits and geotechnical assessment (longer on steep cuts), and 9 to 12 months of construction. Steeper hillside lots above the beach corridor often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping compared to flatter lots. Excavation, foundations, and framing move fastest through Kelowna summers, and interior finish work carries through winter without weather risk."),
            ("Which McKinley Beach enclave or phase should I build in?",
             "The first three phases open 110 acres across six enclaves, with over 550 homes already complete and more releasing regularly. The Benches enclave is the top hillside tier with the biggest view corridors. Lower-tier enclaves sit closer to the beach and marina. Custom lots vary widely in slope, servicing, and view. Bring us your lot survey and we'll walk it with you, review the guidelines specific to that enclave, and give you a real cost and timeline read before you commit."),
            ("What amenities do McKinley Beach residents get access to?",
             "McKinley Beach is Kelowna's only lakefront master-planned community. Residents get a 110-slip marina, one kilometre of private Okanagan Lake beachfront, tennis and pickleball courts, community gardens, and playgrounds. A 42-acre working winery is under construction, and the future Hilltown mixed-use village and residents-only clubhouse are planned as later phases build out. The community trail network runs through the surrounding hillside connecting all six enclaves. Ellison Regional Park and its trails are minutes south."),
            ("What schools are near McKinley Beach?",
             "McKinley Beach is in Central Okanagan Public Schools (SD23). Ellison Elementary is the closest K-6 school, a short drive south on Old Vernon Road. Dr. Knox Middle School (grades 7-9) and Kelowna Secondary (grades 10-12) cover the broader area. For independent schools, Aberdeen Hall Preparatory (K to 12) in Glenmore is about 20 minutes south. UBC Okanagan and Okanagan College's Kelowna campus are both roughly 10 to 15 minutes south, making McKinley Beach one of the closest master-planned communities to post-secondary."),
            ("How far is McKinley Beach from downtown Kelowna and the airport?",
             "Kelowna International Airport (YLW) is 10 minutes north on Highway 97, one of the closest master-planned communities to the airport. Downtown Kelowna is 20 minutes south past UBC Okanagan and the Ellison/Glenmore corridor. UBC Okanagan and Okanagan College are 10 to 15 minutes south, Kelowna General Hospital 25 minutes. Vernon is 25 minutes north on Highway 97, and Predator Ridge is 30 minutes. West Kelowna's wine district (Mission Hill, Quails' Gate) is 35 minutes across the bridge."),
        ],
    },

    "predator-ridge": {
        "name": "Predator Ridge",
        "parent_city": "Vernon",
        "parent_slug": "vernon",
        "region": "BC",
        "lat": "50.2027",
        "lon": "-119.4102",
        "h1": "Custom Home Builder in Predator Ridge, Vernon.",
        "sub": "Vernon's #1 luxury destination. 22 neighbourhoods, 36 holes of championship golf, and the first Ritz-Carlton Residences in Western Canada.",
        "hero": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "hero_alt": "Modern lakeview custom home by Palermo Homes, portfolio match for Predator Ridge",
        "meta_title": "Custom Home Builder Predator Ridge, Vernon | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes in Predator Ridge, Vernon's master-planned resort golf community.",
        "eyebrow": "Neighbourhood · Vernon",
        "overview": [
            "Palermo Homes builds custom homes in Predator Ridge, the Okanagan's most amenity-rich master-planned resort community and Vernon's #1 luxury destination. We cut hillside lots for the view corridor, design inside Wesbild's architectural review, and deliver the finish standard our Cabernet Way and Lakestone builds set. In-house cabinetry, custom finish carpentry, and envelope details are our standard.",
            "We build for Predator Ridge's hillside resort-community terrain: retaining, drainage, view-first orientation, and the design review each neighbourhood enforces. We know Regional District of North Okanagan permits, the local geotech, and how to site a home so the golf course and valley views work from every room.",
            "Predator Ridge is Wesbild's master-planned resort community with 22 neighbourhoods, 36 holes of championship golf, and Commonage Market (Starbucks, grocery, local wine and spirits). Custom homes at Ellison Landing start from $1.4 million. The Ritz-Carlton Residences launch in 2026, the first Ritz-Carlton standalone branded residential development in Canada and the first world-class luxury brand in the Okanagan. Amenities include hiking and biking trails, tennis, fitness classes, and seasonal outdoor recreation. Downtown Vernon is 15 minutes north, Sparkling Hill Resort is minutes away, and Kelowna International Airport (YLW) is 40 minutes south on Highway 97.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2025/12/Touriga-109.jpg", "Modern lakeview custom home at dusk, Palermo Homes portfolio"),
        ],
        "amenities": [
            ("Golf", "36 Championship Holes", "Two award-winning courses woven through the resort community"),
            ("Retail", "Commonage Market", "Onsite café, Starbucks, grocery, and local wine and spirits store"),
            ("Recreation", "Trails + Tennis + Fitness", "Extensive hiking and biking network, tennis courts, and seasonal classes"),
            ("Luxury Brand", "Ritz-Carlton Residences 2026", "First Ritz-Carlton standalone branded residential development in Canada"),
        ],
        "facts": [
            ("Community Plan", "22 Neighbourhoods · 36 Golf Holes"),
            ("Ritz-Carlton", "First in Western Canada · 2026"),
            ("Kelowna Airport", "40 min · Highway 97"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why Predator Ridge clients hire Palermo.",
        "why_items": [
            ("Resort-community design fluency", "Predator Ridge runs 22 neighbourhoods each with its own architectural guidelines. We design inside those rules from the first sketch and manage the review package so nothing bounces back."),
            ("Hillside and view-corridor experience", "Predator Ridge lots are cut into the hillside above the Commonage. Retaining, drainage, and view-first orientation carry real weight. We've been doing hillside custom work for years across Upper Mission, Lakestone, and the West Kelowna wine district."),
            ("Regional District of North Okanagan permits", "Predator Ridge builds run through RDNO permits rather than City of Vernon. The process runs differently, and we know the timelines and inspectors on the file."),
            ("Golf-course and lake-view design", "Every early decision starts with what sits outside the window. Kitchen, primary bedroom, living room placement, glazing ratios, and roofline all get planned around where the golf course, hills, and Okanagan Lake sit from each room."),
            ("Same finish standard as our wine-district work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. Predator Ridge homes hold their value because the neighbours (and now the Ritz-Carlton) set a high bar and we match it."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom Predator Ridge home interior by Palermo Homes",
        "split_photo_loc": "Predator Ridge, Vernon",
        "feat_h": "Portfolio match for Predator Ridge.",
        "feat_body": "Our Modern Lakeview Home on Cabernet Way in West Kelowna is the closest portfolio match for what a Predator Ridge custom build should be. Hillside cut, full view orientation, custom finish carpentry throughout, and the material palette that fits the Okanagan's premium master-planned districts. Terrain and view considerations map directly to Predator Ridge lots.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "feat_photo_alt": "Modern lakeview custom home on Cabernet Way, West Kelowna by Palermo Homes",
        "feat_link": "/project/1252/",
        "feat_link_label": "View the Cabernet Way home",
        "feat_card_loc": "West Kelowna, BC",
        "feat_card_title": "Modern Lakeview Home on Cabernet Way",
        "faqs": [
            ("How much does a custom home cost in Predator Ridge?",
             "Custom homes at Ellison Landing start from $1.4 million. Most Predator Ridge custom builds run $2M and up for the home alone, which pencils out around $650 to $950 per square foot depending on finish level. Lot prices vary widely across the 22 neighbourhoods, with Ellison Landing and premium view-corridor lots at the top end. The Ritz-Carlton Residences launching in 2026 will reset the top of the market. Total finished cost swings with slope, retaining, geotech, and finish level. Add architectural review costs (material palette, roof profile, colour approvals) and resort membership fees into the budget from the start. We provide line-item pricing up front so nothing sneaks up on you mid-build."),
            ("Do Predator Ridge homes have to follow design guidelines?",
             "Yes. Wesbild runs an architectural review process for every custom home before permits go in. Guidelines cover material palette, roof pitch, massing, exterior colour, glazing ratios, and how the home sits on the lot in relation to golf course fairways and the view corridor. Guidelines vary between the 22 neighbourhoods (Commonage, Ellison Landing, and others each have their own rules). We design inside the guidelines from the first sketch, prepare the full review package, and manage revisions with the committee."),
            ("How long does a Predator Ridge custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and architectural review, 2 to 3 months for Regional District of North Okanagan building permits and geotechnical assessment (longer on steep cuts), and 9 to 12 months of construction. Steeper hillside lots often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping. Excavation, foundations, and framing move fastest through Okanagan summers, and interior finish work carries through winter without weather risk."),
            ("Which Predator Ridge neighbourhood should I build in?",
             "Predator Ridge covers 22 neighbourhoods. Commonage is the newest expansion, walkable to Commonage Market and the resort core. Ellison Landing offers custom homes from $1.4M with strong view lots. The Ritz-Carlton Residences (launching 2026) sit at the top of the market. Older neighbourhoods offer established landscaping and mature streetscapes. Bring us your lot survey and we'll walk it with you, review the guidelines specific to that neighbourhood, and give you a real cost and timeline read before you commit."),
            ("What amenities do Predator Ridge residents get access to?",
             "Predator Ridge is the Okanagan's most amenity-rich community. 36 holes of championship golf across two award-winning courses. Commonage Market with Starbucks, grocery, local wine and spirits. Extensive hiking and biking trails, tennis courts, fitness classes, and seasonal outdoor recreation. Sparkling Hill Resort's spa and wellness centre is minutes away. The Ritz-Carlton Residences (launching 2026) will bring hotel-branded amenities including luxury spa and dining. Onsite restaurants, resort accommodation, and event venues round out the year-round programming."),
            ("What schools are near Predator Ridge?",
             "Predator Ridge is in Vernon School District 22 (SD22). Coldstream Elementary is the closest K-6 school, roughly 15 minutes north. Kalamalka Secondary in Coldstream covers grades 7 to 12. Vernon's downtown schools (W.L. Seaton Secondary, Ellison Elementary Vernon) are 15 to 20 minutes north. For post-secondary, Okanagan College's Vernon campus is 20 minutes north, and UBC Okanagan is 40 minutes south in Kelowna."),
            ("How far is Predator Ridge from Vernon, Kelowna, and the airport?",
             "Downtown Vernon is 15 minutes north via Highway 97 and Commonage Road. Sparkling Hill Resort is 5 minutes away. Kalamalka Lake beaches are 15 minutes east through Coldstream. Kelowna International Airport (YLW) is 40 minutes south on Highway 97, with direct flights to Vancouver, Calgary, Seattle, and seasonal service to Toronto. Downtown Kelowna is roughly one hour south. Silver Star Mountain Resort is 45 minutes northeast for winter skiing, and Big White is about 90 minutes southeast."),
        ],
    },

    "lakeview-heights": {
        "name": "Lakeview Heights",
        "parent_city": "West Kelowna",
        "parent_slug": "west-kelowna",
        "region": "BC",
        "lat": "49.8556",
        "lon": "-119.5619",
        "h1": "Custom Home Builder in Lakeview Heights, West Kelowna.",
        "sub": "West Kelowna's established wine-country neighbourhood on the west shore of Okanagan Lake, home to Mission Hill Family Estate and 20 minutes from downtown Kelowna.",
        "hero": "/wp-content/uploads/2025/12/Cabernet-07.jpg",
        "hero_alt": "Modern hillside custom home on Cabernet Way in Lakeview Heights, West Kelowna by Palermo Homes",
        "meta_title": "Custom Home Builder Lakeview Heights, West Kelowna | Palermo",
        "meta_desc": "Palermo Homes builds custom homes in Lakeview Heights, West Kelowna's wine-country neighbourhood on the west shore of Okanagan Lake.",
        "eyebrow": "Neighbourhood · West Kelowna",
        "overview": [
            "Palermo Homes is a licensed BC Housing builder based in West Kelowna, and Lakeview Heights is home ground. We know the Boucherie Mountain terrain, the West Kelowna permit process, and how to design custom homes that capture the west-shore view corridors. In-house cabinetry, custom finish carpentry, envelope details, fixed-price contracts.",
            "We build across every phase of Lakeview Heights, from established Boucherie Road estates to newer hillside cuts above Mission Hill. Bring us your lot survey and we walk it with you before you commit.",
            "Lakeview Heights is West Kelowna's historic wine-country neighbourhood on the west shore of Okanagan Lake, just south of the W.R. Bennett Bridge and Shelter Bay Marina. Home to Mission Hill Family Estate (Canada's most awarded winery, designed by Seattle-based Tom Kundig of Olson Kundig with its 12-storey bell tower and 120,000 sqft complex), Quails' Gate Estate, Mt Boucherie Estate Winery, Volcanic Hills, Little Straw, and The Hatch. Homes lean Mediterranean and California-style. Hiking at Kalamoir Regional Park and biking on Mount Boucherie. Beaches include Gellatly Bay and Rotary Beach. Schools are SD23: Mar Jok Elementary, Constable Neil Bruce Middle, Mount Boucherie Secondary. Downtown Kelowna is 20 minutes over the bridge; YLW is 25 minutes.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2022/04/PAL_220411_Row1.jpg", "Lakeview Heights custom home view corridor over Okanagan Lake, West Kelowna, BC"),
        ],
        "amenities": [
            ("Wineries", "Mission Hill Estate", "Canada's most awarded winery, distinctive architecture, minutes from every Lakeview Heights lot"),
            ("Waterfront", "Gellatly Bay", "Public beach, playground, and boat launch on the west shore"),
            ("Recreation", "Mount Boucherie", "Adjacent hiking and biking trails on the extinct volcano behind the community"),
            ("Wine Trail", "West Kelowna Wine Route", "Six wineries within a 10-minute drive along Boucherie Road"),
        ],
        "facts": [
            ("Elevation", "350 to 600 m · Hillside"),
            ("Wine Country", "Mission Hill, Quails Gate, Volcanic Hills"),
            ("Downtown Kelowna", "20 min · W.R. Bennett Bridge"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why Lakeview Heights clients hire Palermo.",
        "why_items": [
            ("Home turf", "Palermo Homes is based in West Kelowna. Lakeview Heights is our neighbourhood. We know every inspector, every geotech firm, every trade that runs Boucherie Road, and how the west-shore soil behaves."),
            ("West-shore view corridor experience", "Almost every Lakeview Heights lot orients around the Okanagan Lake view. We design floor plans around glazing ratios, deck placement, and roof profile that captures the water without overheating the house in July afternoon sun."),
            ("Hillside and slope experience", "Lakeview Heights lots sit on Boucherie's flank. Retaining, drainage, foundation stepping, and structural engineering carry weight here. We've been doing hillside custom work for over 15 years."),
            ("City of West Kelowna permits", "West Kelowna's permit and inspection process is its own animal. Different from City of Kelowna. We've been through hundreds of it and we know how to move a file through without bounces."),
            ("Wine country aesthetic", "Lakeview Heights homes carry a specific West Coast wine-country design language: stone, timber, deep overhangs, patios oriented for lake views and outdoor entertaining. It's the finish standard we build to every time."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom Palermo Homes interior finish, portfolio example for Lakeview Heights",
        "split_photo_loc": "Portfolio · Palermo Homes",
        "feat_h": "Featured Lakeview Heights build.",
        "feat_body": "Our Modern Lakeview Home on Cabernet Way sits on the Lakeview Heights hillside above Okanagan Lake. Full lake-view orientation, hillside cut, in-house custom finish carpentry throughout, and the stone-and-timber material palette that defines Lakeview Heights and West Kelowna's premier wine-country districts. A working example of what a Palermo custom home looks like in this neighbourhood.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "feat_photo_alt": "Modern lakeview custom home on Cabernet Way, Lakeview Heights, West Kelowna by Palermo Homes",
        "feat_link": "/project/cabernet-2/",
        "feat_link_label": "View the Cabernet Way home",
        "feat_card_loc": "West Kelowna, BC",
        "feat_card_title": "Modern Lakeview Home on Cabernet Way",
        "faqs": [
            ("How much does a custom home cost in Lakeview Heights?",
             "Most Lakeview Heights custom builds run $2M and up for the home alone, which pencils out around $600 to $900 per square foot depending on finish level. Lot prices range from around $600K for smaller cuts on side streets to $2.5M plus for premium view lots overlooking Okanagan Lake and the west-shore vineyards. Total finished cost swings with slope, retaining, geotech, and finish level. A flatter cut vs. a steep hillside can differ by six figures on site work alone. Add City of West Kelowna permit costs, geotech (often required on hillside cuts), and any tree management costs into the budget from the start. We provide line-item pricing up front, break out soft costs (design, permits, geotech) from hard costs, and lock in fixed-price contracts where possible so nothing sneaks up on you mid-build."),
            ("Do Lakeview Heights homes have design guidelines?",
             "Lakeview Heights does not have a single master-planned architectural review committee the way Kettle Valley or Lakestone do. However, individual streets and newer subdivisions inside Lakeview Heights (such as some hillside phases above Boucherie Road) may have their own design covenants registered against title. Beyond that, City of West Kelowna zoning bylaws, hillside development permits, and standard building code apply. On steep or hillside lots, geotechnical assessment and hillside development permits are typically required and can affect design (foundation type, retaining, drainage). We check every lot for registered covenants at the design stage and manage all City of West Kelowna submissions on your behalf."),
            ("How long does a Lakeview Heights custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and any required covenant reviews, 2 to 3 months for City of West Kelowna building permits and geotechnical assessment (longer on hillside cuts), and 9 to 12 months of construction. Hillside cuts on Boucherie's flank often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping compared to flatter lots. Weather matters too. Excavation, foundations, and framing move fastest through Okanagan summers. Interior finish work carries through winter without weather risk, so we schedule critical exterior phases to hit the right months."),
            ("Which parts of Lakeview Heights do you build in?",
             "Palermo Homes builds across every part of Lakeview Heights, from the established estate streets along Boucherie Road to the newer hillside cuts above Mission Hill Family Estate. Boucherie Road running from Sunnyside Road down through Anders Road is the historic spine of the community. Streets like Judd Road, Anders Road, and Green Bay Road carry established custom homes on mature lots. Newer cuts extend up the hillside toward Rose Valley, offering elevated view lots. We're actively taking on projects across every current phase. Whether you already own a lot, are negotiating a purchase, or are picking between an established Boucherie Road estate cut and a hillside view lot, bring us the lot survey. We'll walk it with you and give you a real cost and timeline read."),
            ("What amenities do Lakeview Heights residents get access to?",
             "Lakeview Heights sits at the centre of the West Kelowna Wine Route with six wineries within a 10-minute drive: Mission Hill Family Estate, Quails Gate Estate, Volcanic Hills, Little Straw Vineyards, Off the Grid Organic, and Kalala Organic. Mission Hill's Terrace Restaurant is one of the region's top dining destinations. Beaches include Gellatly Bay Regional Park (public beach, playground, boat launch) and Rotary Beach. Mount Boucherie Regional Park offers hiking and biking trails on the extinct volcano behind the community. The West Kelowna Yacht Club and various marinas are minutes away. Gellatly Nut Farm Regional Park is a heritage site with walking trails, and the Westbank rail trail is close by for cyclists. Restaurants, groceries, and services are concentrated along Highway 97 through Westbank Centre, roughly 5 minutes from most Lakeview Heights lots."),
            ("What schools are near Lakeview Heights?",
             "Lakeview Heights is in Central Okanagan Public Schools (SD23). Mar Jok Elementary at 1240 Green Bay Road covers K to 5 and sits inside the neighbourhood. Constable Neil Bruce Middle at 1885 Elk Road handles grades 6 to 8. Mount Boucherie Secondary at 2751 Cameron Road (grades 9 to 12) is the high school and serves all of West Kelowna. All three sit within a 5- to 10-minute drive of most Lakeview Heights homes. For families looking at independent schools, Aberdeen Hall Preparatory (K to 12) in Kelowna's Glenmore area is about 25 to 30 minutes across the bridge, and Immaculata Regional High School (Catholic, grades 8 to 12) is a similar drive. Post-secondary is close: Okanagan College's West Kelowna campus is 5 minutes away, and UBC Okanagan is about 30 minutes across the bridge."),
            ("How far is Lakeview Heights from Kelowna and the airport?",
             "Downtown Kelowna is 20 minutes across the W.R. Bennett Bridge on Highway 97. Kelowna International Airport (YLW) is 25 minutes east with direct flights to Vancouver, Calgary, Seattle, and seasonal service to Toronto. Peachland is 15 minutes south along Highway 97, and Penticton is 45 minutes further. Vernon is 45 minutes north. Kelowna General Hospital is 20 minutes across the bridge, and UBC Okanagan is 30 minutes. For weekend recreation, Big White Ski Resort is about 90 minutes east, Silver Star Mountain Resort is 90 minutes north, and Apex Mountain Resort is 90 minutes south. Crystal Mountain (a small local ski hill) is 30 minutes up Glenrosa Road for a quick day trip."),
        ],
    },

    "naramata-bench": {
        "name": "Naramata Bench",
        "parent_city": "Penticton",
        "parent_slug": "penticton",
        "region": "BC",
        "lat": "49.5928",
        "lon": "-119.5936",
        "h1": "Custom Home Builder on the Naramata Bench, Penticton BC.",
        "sub": "The east-shore wine country appellation above Okanagan Lake, home to over 40 wineries and some of the most desirable custom home lots in BC.",
        "hero": "/wp-content/uploads/2025/12/Cabernet-07.jpg",
        "hero_alt": "Modern custom home portfolio example, Palermo Homes",
        "meta_title": "Custom Home Builder Naramata Bench, Penticton | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes on the Naramata Bench, the east-shore wine country above Okanagan Lake near Penticton, BC.",
        "eyebrow": "Neighbourhood · Penticton",
        "overview": [
            "Palermo Homes is a licensed BC Housing custom home builder (BC1017682, license 42812) that builds across the Okanagan Valley. On the Naramata Bench we bring the same in-house cabinetry, custom finish carpentry, envelope detail, and fixed-price contracts that define every Palermo build.",
            "We serve the Bench as an extension of our Central Okanagan operation. Site visits and design meetings are a scheduled trip and we price that reality transparently. Bring us your lot survey and we walk it with you before you commit.",
            "The Naramata Bench is a wine appellation and unincorporated community (pop. 1,628, 2021 census) in the Regional District of Okanagan-Similkameen, Electoral Area E. Founded 1907 by John Moore Robinson. Runs 14 km along Naramata Road, 15 km north of Penticton. Over 40 wineries in the Naramata Bench Wineries Association including Poplar Grove (an original five), Red Rooster, Four Shadows, Upper Bench Winery & Creamery (BC's only winery-creamery), Lake Breeze, Therapy, Van Westen, Nichol, La Frenz. Kettle Valley Rail Trail runs through. Naramata Village has cafes, the historic Naramata Inn, and a marina. Schools SD67. Penticton 15 min south, Kelowna 1 hour north, YLW 1 hour 15 min.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2025/12/Cabernet-07.jpg", "Custom hillside home portfolio example, Palermo Homes"),
        ],
        "amenities": [
            ("Wineries", "40+ Bench Wineries", "One of Canada's most concentrated wine regions along Naramata Road"),
            ("Recreation", "Kettle Valley Rail Trail", "Historic KVR trail runs through the Bench for cycling and walking"),
            ("Waterfront", "Naramata Beach + Marina", "Public beaches and marina at Naramata Village"),
            ("Village", "Naramata Village", "Cafes, restaurants, historic Naramata Inn, artist studios"),
        ],
        "facts": [
            ("Elevation", "350 to 750 m · Steep Bench"),
            ("Wineries", "40+ within 10 km"),
            ("Penticton", "15 min · Naramata Rd"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why Naramata Bench clients hire Palermo.",
        "why_items": [
            ("Steep-terrain and view-corridor experience", "The Bench rises steeply from the lake. Retaining, drainage, geotech, and view-first orientation are non-negotiable. We've been doing hillside custom work in Upper Mission, Lakeview Heights, and Lakestone for years."),
            ("Wine country aesthetic", "Naramata Bench homes carry a specific West Coast wine-country design language: stone, timber, deep overhangs, patios oriented for view corridors. It's the finish standard we build to."),
            ("Regional District permits", "Naramata is unincorporated. Building permits go through the Regional District of Okanagan-Similkameen (RDOS), which runs differently than City of Penticton or City of Kelowna. We manage the submission and follow-up so you're not chasing paperwork."),
            ("Water and septic on rural lots", "Many Naramata Bench lots are on well water and septic rather than municipal services. That affects design (mechanical room sizing, tank placement, drain field siting) and permits. We coordinate the well driller and septic designer as part of the design phase."),
            ("Same finish standard as our Kelowna work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. Bench homes hold value because the setting is one of the most desirable in BC, and we match the level of build the setting deserves."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom Palermo Homes interior finish, portfolio example",
        "split_photo_loc": "Portfolio · Palermo Homes",
        "feat_h": "Portfolio match for the Naramata Bench.",
        "feat_body": "Our Modern Lakeview Home on Cabernet Way in West Kelowna is the closest portfolio match for what a Naramata Bench custom build should be. Hillside cut, full lake-view orientation, custom finish carpentry throughout, and the stone-and-timber material palette that fits the Okanagan wine-country districts. Terrain and view considerations map directly to Naramata Bench lots.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-07.jpg",
        "feat_photo_alt": "Modern hillside custom home portfolio example, Palermo Homes",
        "feat_link": "/project/cabernet-2/",
        "feat_link_label": "View the Cabernet Way home",
        "feat_card_loc": "West Kelowna, BC · Portfolio",
        "feat_card_title": "Modern Lakeview Home on Cabernet Way",
        "faqs": [
            ("How much does a custom home cost on the Naramata Bench?",
             "Most Naramata Bench custom builds run $2M and up for the home alone, which pencils out around $650 to $950 per square foot depending on finish level and site complexity. Lot prices range from around $500K for smaller off-water Bench lots to $3M plus for premium acreage with vineyard rights or direct lake frontage. Bench lots often carry additional costs: well drilling ($15K to $30K), septic system design and install ($25K to $60K), driveway construction on steep grades ($20K to $80K), and Regional District servicing costs. Total finished cost swings with slope, retaining, geotech, and finish level. We provide line-item pricing up front, break out soft costs (design, permits, geotech, well and septic) from hard costs, and lock in fixed-price contracts where possible."),
            ("Do Naramata Bench homes have design guidelines?",
             "The Naramata Bench does not have a single master-planned architectural review committee. However, individual subdivisions may carry design covenants, and the Regional District of Okanagan-Similkameen (RDOS) zoning bylaws govern setbacks, height, and site coverage. Agricultural Land Reserve (ALR) rules apply to many Bench lots, which restrict subdivision and can affect siting. Hillside development permits and geotechnical assessment are typically required on steep cuts. We check every lot for ALR status, registered covenants, and RDOS zoning at the design stage and manage all submissions on your behalf."),
            ("How long does a Naramata Bench custom home take to build?",
             "Plan on 15 to 22 months from first design meeting to move-in. Roughly 3 to 5 months for design development, 3 to 4 months for RDOS building permits, geotechnical assessment, well and septic design (longer than in-city projects because of ALR and rural servicing coordination), and 9 to 12 months of construction. Steep Bench cuts often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping. Weather matters. Excavation, foundations, and framing move fastest through summer, and rural driveways and site access can become impassable in wet spring conditions. We schedule with that seasonality in mind."),
            ("Which parts of the Naramata Bench do you build in?",
             "Palermo Homes builds across the full length of the Bench, from north of Penticton up through Naramata Village and beyond toward the Chute Lake plateau. The lower Bench between Penticton and Naramata Village carries the highest concentration of wineries and orchards. The upper Bench climbing toward Chute Lake offers larger acreages, elevated views, and more privacy. Naramata Village itself has a small pocket of walkable-to-village lots. We're actively taking on projects across every stretch. Bring us the lot survey and we walk it with you before you commit."),
            ("What amenities do Naramata Bench residents get access to?",
             "The Naramata Bench is home to over 40 wineries, most within a 10-minute drive of any Bench lot. Notable stops include Lake Breeze, Poplar Grove, Red Rooster, Therapy Vineyards, Van Westen, Nichol, Elephant Island, La Frenz, Ruby Blues, and Terravista. Naramata Village has cafes (The Village Grounds), restaurants (Naramata Pub, Legend Distilling), the historic Naramata Inn, artist studios, and a small marina. The Kettle Valley Rail Trail (KVR) runs through the community for cycling and walking, connecting Penticton to Chute Lake and beyond. Public beaches include Naramata Beach, Manitou Park, and Wharf Park. Penticton (15 minutes south) offers full urban services, and downtown has an extensive beach network on Okanagan Lake and Skaha Lake."),
            ("What schools are near the Naramata Bench?",
             "The Naramata Bench is in Okanagan Skaha School District (SD67). Naramata Elementary at 3320 3rd Street in Naramata Village covers K to 7 and sits inside the community. For grades 8 to 12, students attend Penticton Secondary School at 158 Eckhardt Avenue West, roughly 20 minutes south. For families looking at independent schools, Penticton has a limited private school selection, and Kelowna's Aberdeen Hall Preparatory is about 1 hour 15 minutes north. Post-secondary options include Okanagan College's Penticton campus (25 minutes south) and UBC Okanagan (1 hour 15 minutes north in Kelowna)."),
            ("How far is the Naramata Bench from Penticton, Kelowna, and the airports?",
             "Downtown Penticton is 15 minutes south via Naramata Road. Penticton Regional Airport (YYF) is 25 minutes south with limited direct service. Kelowna is 1 hour north via Highway 97 (through Peachland, West Kelowna, and across the W.R. Bennett Bridge). Kelowna International Airport (YLW) is 1 hour 15 minutes with direct flights to Vancouver, Calgary, Seattle, and seasonal service to Toronto. Osoyoos is 45 minutes south. For weekend recreation, Apex Mountain Resort is 45 minutes southwest for winter skiing, Big White is 1 hour 45 minutes northeast, and the US border at Osoyoos is 45 minutes south."),
        ],
    },

    "skaha-hills": {
        "name": "Skaha Hills",
        "parent_city": "Penticton",
        "parent_slug": "penticton",
        "region": "BC",
        "lat": "49.4436",
        "lon": "-119.5928",
        "h1": "Custom Home Builder in Skaha Hills, Penticton.",
        "sub": "Greyback Construction's $250M master-planned community of 600 homes on 550 acres overlooking Skaha Lake on the south side of Penticton.",
        "hero": "/wp-content/uploads/2025/12/1587-Malbec-14.jpg",
        "hero_alt": "Modern lakeview custom home on Malbec Place, portfolio example by Palermo Homes",
        "meta_title": "Custom Home Builder Skaha Hills, Penticton | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes in Skaha Hills, a hillside vineyard community above Skaha Lake in Penticton, BC.",
        "eyebrow": "Neighbourhood · Penticton",
        "overview": [
            "Palermo Homes is a licensed BC Housing custom home builder that brings in-house cabinetry, custom finish carpentry, envelope discipline, and fixed-price contracts to every project. Skaha Hills has design guidelines. We build inside them from the first sketch so nothing bounces at design review.",
            "We serve Skaha Hills from our Central Okanagan operation. Site visits and design meetings are a scheduled trip and we price that reality transparently. Bring us your lot number and we review the phase-specific guidelines before we design.",
            "Skaha Hills is Greyback Construction's $250M master-planned community on 550 acres on the south side of Penticton, overlooking Skaha Lake. 600 homes planned across 7 phases (Phase 1 ranchers, Phase 2 The Ridge, Phase 3 The Vistas terraced villas, Phase 4 opened 2020, full build-out projected at up to 1,000 units). On-site vineyard, restaurant, pool, fitness room, walking trails. Greyback is a 4-generation Penticton family-owned builder with 100+ years of local roots. Downtown Penticton 10 min north via Highway 97, Skaha Beach 5 min, Penticton Regional Airport (YYF) 10 min. SD67 Okanagan Skaha. Kelowna 1 hour north.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2025/12/1587-Malbec-14.jpg", "Modern lakeview custom home on Malbec Place portfolio example, Palermo Homes"),
        ],
        "amenities": [
            ("Recreation", "Community Pool + Clubhouse", "Outdoor pool, fitness centre, and residents-only clubhouse"),
            ("Vineyard", "On-site Vineyard", "Working vineyard integrated with community trails and tasting"),
            ("Waterfront", "Skaha Lake Beaches", "Skaha Lake Park and Skaha Beach 5 minutes north"),
            ("Golf", "Skaha Meadows Golf", "Public 18-hole golf course minutes from the community"),
        ],
        "facts": [
            ("Community Plan", "500+ Residences · Phased"),
            ("Amenities", "Pool + Clubhouse + Vineyard"),
            ("Downtown Penticton", "10 min · Highway 97"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why Skaha Hills clients hire Palermo.",
        "why_items": [
            ("Fluent in Skaha Hills design guidelines", "Greyback's architectural review checks the Mediterranean design vocabulary on every submission: stucco finishes, tile roof profiles, warm colour palette, terraced siting. We design inside the guidelines and handle the design review package."),
            ("Hillside and terraced siting experience", "Skaha Hills lots are cut into the mountainside overlooking Skaha Lake. Retaining, drainage, and structural engineering carry weight. We've been doing hillside custom work across the Okanagan for years."),
            ("City of Penticton permits", "Skaha Hills falls within the City of Penticton municipal boundary. City permits, inspections, and servicing coordination run differently than the Regional District. We've worked through the process."),
            ("Community amenity coordination", "Skaha Hills homeowner fees fund the community pool, clubhouse, fitness centre, and vineyard maintenance. We factor amenity access, initiation, and any phase-specific HOA into your project cost transparently."),
            ("Same finish standard as our wine-district work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. Skaha Hills homes hold value because the community sets a specific design bar, and we build to match."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom Palermo Homes interior finish, portfolio example for Skaha Hills",
        "split_photo_loc": "Portfolio · Palermo Homes",
        "feat_h": "Portfolio match for Skaha Hills.",
        "feat_body": "Our Modern Lakeview Home on Malbec Place in West Kelowna is the closest portfolio match for what a Skaha Hills custom build should be. Hillside cut, full lake-view orientation, custom finish carpentry throughout, and the material palette that fits Okanagan hillside districts. Terrain and view considerations map directly to Skaha Hills lots.",
        "feat_photo": "/wp-content/uploads/2025/12/1587-Malbec-14.jpg",
        "feat_photo_alt": "Modern lakeview custom home on Malbec Place, West Kelowna by Palermo Homes",
        "feat_link": "/project/malbec-place-1/",
        "feat_link_label": "View the Malbec Place home",
        "feat_card_loc": "West Kelowna, BC · Portfolio",
        "feat_card_title": "Modern Lakeview Home on Malbec Place",
        "faqs": [
            ("How much does a custom home cost in Skaha Hills?",
             "Most Skaha Hills custom builds run $1.5M and up for the home alone, which pencils out around $500 to $800 per square foot depending on finish level. Lot prices range from around $400K for smaller cuts in later phases to $1.2M plus for premium view lots with the most direct Skaha Lake orientation. Skaha Hills' Mediterranean design vocabulary (stucco, tile roof, specific colour palette) adds slight cost premium over conventional builds. Community HOA fees fund the pool, clubhouse, and vineyard amenities. We provide line-item pricing up front, break out soft costs (design, permits, design review, HOA) from hard costs, and lock in fixed-price contracts where possible."),
            ("Do Skaha Hills homes have to follow design guidelines?",
             "Yes. Greyback Development's architectural review process signs off on every Skaha Hills custom home before construction begins. Guidelines cover the Mediterranean design vocabulary: stucco exterior finishes, tile roof profiles and colours, warm earth-tone colour palette, terraced hillside siting that respects neighbours' view corridors, and specific glazing and door treatments. It's stricter than most Penticton neighbourhoods and it's what maintains the cohesive Mediterranean aesthetic across the community. We design inside the guidelines from the first sketch, prepare the full design review package (site plan, elevations, material board, colour selections), and manage revisions on your behalf."),
            ("How long does a Skaha Hills custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and Greyback design review, 2 to 3 months for City of Penticton building permits and geotechnical assessment (longer on steep cuts), and 9 to 12 months of construction. Steep Skaha Hills cuts often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping. Weather matters. Excavation, foundations, and framing move fastest through Okanagan summers. Interior finish work carries through winter without weather risk, so we schedule critical exterior phases to hit the right months."),
            ("Which Skaha Hills phases do you build in?",
             "Skaha Hills has developed in phases since launching in 2013. Early phases sit lower on the hillside with more established landscaping. Newer phases climb higher up the mountainside with more elevated view lots. The community continues to release new lots and phases regularly through Greyback Development. We're actively taking on projects across current phases. Whether you already own a lot, are negotiating a purchase, or are picking between elevation options, bring us the lot survey and phase-specific guidelines. We'll walk the lot with you, review the design covenants, and give you a real cost and timeline read before you commit."),
            ("What amenities do Skaha Hills residents get access to?",
             "Skaha Hills homeowners get access to a community pool, clubhouse, fitness centre, and vineyard trails as part of the master-planned community amenities. The on-site vineyard is a working operation integrated with community trails and occasional tasting events. Skaha Meadows Golf Course (public 18-hole) is minutes from the community. Skaha Lake Park with public beach, playground, and boat launch is 5 minutes north. Downtown Penticton with restaurants, wineries, and Okanagan Lake beaches is 10 minutes north. Apex Mountain Resort is 45 minutes southwest for winter skiing. Community HOA fees fund the pool, clubhouse, fitness, and common area maintenance."),
            ("What schools are near Skaha Hills?",
             "Skaha Hills is in Okanagan Skaha School District (SD67). Wiltse Elementary and Uplands Elementary are the closest K to 7 schools, both 5 to 10 minutes from the community. Skaha Lake Middle School handles grades 8 to 9. Penticton Secondary School at 158 Eckhardt Avenue West is the high school (grades 10 to 12), roughly 10 to 15 minutes north. Post-secondary options include Okanagan College's Penticton campus (10 minutes north) and UBC Okanagan (1 hour north in Kelowna)."),
            ("How far is Skaha Hills from Penticton, Kelowna, and the airports?",
             "Downtown Penticton is 10 minutes north via Highway 97. Skaha Beach and Skaha Lake Park are 5 minutes north. Penticton Regional Airport (YYF) is 10 minutes north with limited direct service. Kelowna is 1 hour north via Highway 97 (through Peachland, Summerland, and Kelowna). Kelowna International Airport (YLW) is 1 hour 10 minutes with direct flights to Vancouver, Calgary, Seattle, and seasonal service to Toronto. Osoyoos and the US border are 45 minutes south. For weekend recreation, Apex Mountain Resort is 45 minutes southwest for winter skiing, and Big White is 1 hour 45 minutes northeast."),
        ],
    },

    "adventure-bay": {
        "name": "Adventure Bay",
        "parent_city": "Vernon",
        "parent_slug": "vernon",
        "region": "BC",
        "lat": "50.2481",
        "lon": "-119.3197",
        "h1": "Custom Home Builder in Adventure Bay, Vernon.",
        "sub": "Vernon's hillside community on the northern peninsula of Okanagan Lake, 12 km from downtown Vernon with panoramic mountain and lake views.",
        "hero": "/wp-content/uploads/2025/12/Cabernet-07.jpg",
        "hero_alt": "Modern custom home portfolio example, Palermo Homes",
        "meta_title": "Custom Home Builder Adventure Bay, Vernon | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes in Adventure Bay, Vernon's hillside community above Okanagan Lake with panoramic lake views.",
        "eyebrow": "Neighbourhood · Vernon",
        "overview": [
            "Palermo Homes is a licensed BC Housing custom home builder (BC1017682, license 42812). Adventure Bay is hillside custom home country on Okanagan Lake, where view-corridor design is what the lots demand. In-house cabinetry, custom finish carpentry, envelope discipline, fixed-price contracts.",
            "We serve Adventure Bay from our Central Okanagan operation. Site visits and design meetings are a scheduled trip and we price that reality transparently. Bring us the lot survey and we walk the property with you before you commit.",
            "Adventure Bay sits on the northern peninsula of Okanagan Lake, a 12 km drive from downtown Vernon along Tronson Road. The community rises steeply from the water with panoramic mountain and lake views. Real estate is largely single-family homes plus bare-land strata developments including Canadian Lakeview Estates, The Terraces, and Kestrel Estates. Average listing price runs approximately $886,000, about 5 percent below the Vernon average. Beaches include Paddlewheel Park, Kin Beach, and Ellison Provincial Park's protected shoreline. Schools are Vernon School District 22 (SD22). Downtown Vernon 12 km east, Kelowna 45 min south, Kelowna International Airport 40 min.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2025/12/Cabernet-07.jpg", "Custom hillside home portfolio example, Palermo Homes"),
        ],
        "amenities": [
            ("Waterfront", "Paddlewheel Park", "Public beach, playground, and boat launch minutes from Adventure Bay"),
            ("Nature", "Ellison Provincial Park", "Protected shoreline, hiking trails, and swimming beaches nearby"),
            ("Recreation", "Kin Beach", "Popular Vernon beach park on the west shore"),
            ("Wine + Golf", "Predator Ridge + Sparkling Hill", "Golf, resort spa, and wine country within 20 minutes"),
        ],
        "facts": [
            ("Elevation", "400 to 700 m · Hillside"),
            ("Downtown Vernon", "15 min · Okanagan Landing Rd"),
            ("Kelowna Airport", "40 min · Highway 97"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why Adventure Bay clients hire Palermo.",
        "why_items": [
            ("View-corridor design experience", "Every Adventure Bay lot orients around the Okanagan Lake view. We design floor plans around glazing ratios, deck placement, roof profile, and summer solar gain so the view drives the house without cooking it in July."),
            ("Hillside and slope experience", "Adventure Bay lots are cut into the mountainside. Retaining walls, drainage, foundation stepping, and structural engineering carry weight here. We've been doing hillside custom work across the Okanagan for years."),
            ("City of Vernon permits", "Vernon's permit and inspection process is its own animal. Different from Kelowna, different from Regional District. We know the process, the inspectors, and how to move a file through without bounces."),
            ("Rural water and septic capable", "Some Adventure Bay lots may be on well and septic depending on phase and municipal servicing extent. We coordinate well drillers, septic designers, and permit submissions as part of the design phase where applicable."),
            ("Same finish standard as our wine-district work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. Adventure Bay homes hold value because the setting is one of Vernon's premium lake-view locations, and we match the level of build the setting deserves."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom Palermo Homes interior finish, portfolio example for Adventure Bay",
        "split_photo_loc": "Portfolio · Palermo Homes",
        "feat_h": "Portfolio match for Adventure Bay.",
        "feat_body": "Our Modern Lakeview Home on Cabernet Way in West Kelowna is the closest portfolio match for what an Adventure Bay custom build should be. Hillside cut, full lake-view orientation, custom finish carpentry throughout, and the stone-and-timber material palette that fits Okanagan hillside districts. Terrain and view considerations map directly to Adventure Bay's northern-peninsula sites.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-07.jpg",
        "feat_photo_alt": "Modern hillside custom home portfolio example, Palermo Homes",
        "feat_link": "/project/cabernet-2/",
        "feat_link_label": "View the Cabernet Way home",
        "feat_card_loc": "West Kelowna, BC · Portfolio",
        "feat_card_title": "Modern Lakeview Home on Cabernet Way",
        "faqs": [
            ("How much does a custom home cost in Adventure Bay?",
             "Most Adventure Bay custom builds run $1.5M and up for the home alone, which pencils out around $500 to $800 per square foot depending on finish level. Lot prices range from around $400K for smaller cuts on side streets to $1.5M plus for premium view lots overlooking Okanagan Lake. Total finished cost swings with slope, retaining, geotech, and finish level. A flatter cut vs. a steep hillside can differ by six figures on site work alone. Some lots may require well and septic (add $40K to $90K for both) depending on municipal servicing. We provide line-item pricing up front, break out soft costs (design, permits, geotech) from hard costs, and lock in fixed-price contracts where possible."),
            ("Do Adventure Bay homes have design guidelines?",
             "Adventure Bay does not have a single master-planned architectural review committee. Individual subdivisions inside Adventure Bay may carry design covenants registered against title, particularly newer hillside phases. Beyond that, City of Vernon zoning bylaws, hillside development permits, and standard building code apply. On steep cuts, geotechnical assessment and hillside development permits are typically required. We check every lot for registered covenants at the design stage and manage all City of Vernon submissions on your behalf."),
            ("How long does an Adventure Bay custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and any required covenant reviews, 2 to 3 months for City of Vernon building permits and geotechnical assessment (longer on hillside cuts), and 9 to 12 months of construction. Steep Adventure Bay cuts often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping. Weather matters. Excavation, foundations, and framing move fastest through Okanagan summers, and interior finish work carries through winter without weather risk."),
            ("Which parts of Adventure Bay do you build in?",
             "Palermo Homes builds across the full Adventure Bay hillside, from established streets closer to Okanagan Landing Road up through newer cuts higher on the slope. The neighbourhood has developed in phases with newer hillside subdivisions continuing to open. We're actively taking on projects across every current release. Whether you already own a lot, are negotiating a purchase, or are picking between elevation options, bring us the lot survey and we'll walk it with you before you commit."),
            ("What amenities do Adventure Bay residents get access to?",
             "Adventure Bay sits in Vernon's Okanagan Landing area with strong lake-recreation access. Paddlewheel Park (public beach, playground, boat launch) is minutes away. Kin Beach and Ellison Provincial Park (protected shoreline, hiking trails, swimming beaches) are close by. Predator Ridge Resort (golf, dining, spa) is 20 minutes east. Sparkling Hill Resort (award-winning spa and wellness centre) is 15 minutes east. Silver Star Mountain Resort is 45 minutes northeast for winter skiing. Downtown Vernon with restaurants, shops, and services is 15 minutes on Okanagan Landing Road."),
            ("What schools are near Adventure Bay?",
             "Adventure Bay is in Vernon School District 22 (SD22). Okanagan Landing Elementary at 8300 Tronson Road covers K to 7 and sits inside the community. Vernon Secondary School and W.L. Seaton Secondary handle grades 8 to 12 in downtown Vernon, 15 minutes east. For families looking at independent schools, Vernon Christian School (K to 12) is in Coldstream (25 minutes away). Post-secondary options include Okanagan College's Vernon campus (20 minutes east) and UBC Okanagan (40 minutes south in Kelowna)."),
            ("How far is Adventure Bay from Vernon, Kelowna, and the airport?",
             "Downtown Vernon is 15 minutes east via Okanagan Landing Road. Predator Ridge Resort is 20 minutes east. Sparkling Hill Resort is 15 minutes east. Silver Star Mountain Resort is 45 minutes northeast for winter skiing. Kelowna is 45 minutes south via Highway 97. Kelowna International Airport (YLW) is 40 minutes south with direct flights to Vancouver, Calgary, Seattle, and seasonal service to Toronto. Kalamalka Lake beaches are 20 minutes east through Coldstream. Big White Ski Resort is about 90 minutes southeast, Apex Mountain Resort is 2 hours south."),
        ],
    },

    "eagle-mountain": {
        "name": "Eagle Mountain",
        "parent_city": "Abbotsford",
        "parent_slug": "lower-mainland",
        "region": "BC",
        "lat": "49.0303",
        "lon": "-122.2286",
        "h1": "Custom Home Builder in Eagle Mountain, Abbotsford.",
        "sub": "Abbotsford's premier hillside community and the biggest active custom home development in the Fraser Valley. Home to Vicarro Skyline's 1,400-unit build-out on the historic Vicarro Ranch.",
        "hero": "/wp-content/uploads/2019/06/PAL_Projects_Mahogany2_FEATURE.jpg",
        "hero_alt": "Luxury Mountain View Home on Mahogany Drive, Eagle Mountain Abbotsford by Palermo Homes",
        "meta_title": "Custom Home Builder Eagle Mountain, Abbotsford | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes in Eagle Mountain, Abbotsford, a hillside community in the Fraser Valley.",
        "eyebrow": "Neighbourhood · Abbotsford",
        "overview": [
            "Palermo Homes is a licensed BC Housing custom home builder (BC1017682, license 42812) with more completed custom builds on Eagle Mountain than any other neighbourhood. Mahogany Drive is our featured Eagle Mountain project. Nine plus finished homes across the mountain give us site knowledge, permit fluency, and trade relationships.",
            "We are actively taking on projects across every Eagle Mountain phase including Vicarro Skyline's new release. Bring us your lot number and we walk it with you before you commit.",
            "Eagle Mountain is Abbotsford's premier hillside custom home community and the largest active build-out in the Fraser Valley. The new Vicarro development spans 383 acres and 1,400 units on the historic Vicarro Ranch (Trethewey family for generations). Pacific Peak Homes acquired Vicarro Skyline (55-home first phase) in April 2025 and broke ground August 2026 with Diverse Properties. Homes designed by Abbotsford-based Su Casa Design with a private neighbourhood pool and mountain views. Eagle Mountain proper is releasing its final phase. Schools SD34. Downtown Abbotsford 15 min north, YXX 20 min, Vancouver 1 hour west, Chilliwack 25 min east.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2019/06/PAL_Projects_Mahogany2_FEATURE.jpg", "Luxury Mountain View Home on Mahogany Drive, Eagle Mountain Abbotsford by Palermo Homes"),
        ],
        "amenities": [
            ("Community", "Vicarro Skyline Pool", "Private neighbourhood pool at Vicarro Skyline first phase (Aug 2026)"),
            ("Views", "Mount Baker + Sumas", "Panoramic mountain views south to Mount Baker and Sumas Mountain"),
            ("Golf", "Ledgeview Golf", "Ledgeview Golf Course is 10 min north for championship-level play"),
            ("Access", "15 min to Downtown", "Quick access to downtown Abbotsford and Highway 1"),
        ],
        "facts": [
            ("Scale", "383 Acres · 1,400 Units"),
            ("Palermo Builds", "9+ Completed on Eagle Mountain"),
            ("Downtown Abbotsford", "15 min · Highway 11"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why Eagle Mountain clients hire Palermo.",
        "why_items": [
            ("Proven Eagle Mountain track record", "Nine plus completed Palermo custom builds on Eagle Mountain including our featured Mahogany Drive home. We know the terrain, the covenants, the City of Abbotsford permit process, and the trades on the mountain."),
            ("Hillside and view-corridor experience", "Eagle Mountain lots are cut into the mountainside above Abbotsford. Retaining, drainage, and structural engineering carry real weight. We have done that work here for years."),
            ("Fluent in Vicarro design guidelines", "Vicarro Skyline's Su Casa Design vocabulary sets the aesthetic for the new release. We design inside those guidelines from the first sketch."),
            ("City of Abbotsford permits", "Abbotsford's permit and inspection process runs differently than City of Kelowna. We've been through it on multiple Eagle Mountain projects."),
            ("Same finish standard as our Kelowna work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. Eagle Mountain homes hold value because the mountain sets a specific bar, and we match it."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom Palermo Homes interior finish, portfolio example for Eagle Mountain",
        "split_photo_loc": "Portfolio · Palermo Homes",
        "feat_h": "Featured Eagle Mountain build.",
        "feat_body": "Our Luxury Mountain View Home on Mahogany Drive is a real Palermo custom build on Eagle Mountain, Abbotsford. Full mountain-view orientation, hillside cut, custom finish carpentry throughout, and the modern material palette that defines Fraser Valley premium hillside districts. One of nine plus completed Palermo custom homes on the mountain.",
        "feat_photo": "/wp-content/uploads/2019/06/PAL_Projects_Mahogany2_FEATURE.jpg",
        "feat_photo_alt": "Luxury Mountain View Home on Mahogany Drive, Eagle Mountain Abbotsford by Palermo Homes",
        "feat_link": "/project/eagle-mountain-1/",
        "feat_link_label": "View the Mahogany Drive home",
        "feat_card_loc": "Abbotsford, BC",
        "feat_card_title": "Luxury Mountain View Home on Mahogany Drive",
        "faqs": [
            ("How much does a custom home cost on Eagle Mountain?",
             "Most Eagle Mountain custom builds run $1.5M and up for the home alone, which pencils out around $500 to $850 per square foot depending on finish level. Lot prices in the new Vicarro Skyline release start at premium levels reflecting the community pool, Su Casa Design vocabulary, and 383-acre master plan. Older Eagle Mountain phases offer more established landscaping and varied pricing. Total finished cost swings with slope, retaining, geotech, and finish level. We provide line-item pricing up front, break out soft costs (design, permits, geotech) from hard costs, and lock in fixed-price contracts where possible so nothing sneaks up on you mid-build."),
            ("Do Eagle Mountain homes have design guidelines?",
             "Yes, and they vary by phase. Vicarro Skyline's first phase (55 homes, groundbreaking August 2026) is designed by Abbotsford-based Su Casa Design with a defined material palette, roof profile, and colour palette that Pacific Peak Homes enforces on every submission. Older Eagle Mountain phases have their own registered design covenants. Beyond that, City of Abbotsford zoning bylaws, hillside development permits, and standard building code apply. We check every lot for phase-specific covenants at the design stage and manage all City of Abbotsford submissions on your behalf."),
            ("How long does an Eagle Mountain custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and covenant review, 2 to 3 months for City of Abbotsford building permits and geotechnical assessment (longer on steep cuts), and 9 to 12 months of construction. Steep Eagle Mountain cuts often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping. Weather matters. Excavation and framing move fastest through Fraser Valley summers. Interior finish work carries through winter without weather risk."),
            ("Which parts of Eagle Mountain do you build in?",
             "Palermo Homes has completed nine plus custom builds across Eagle Mountain including our featured Mahogany Drive home. We are actively taking on projects across every current release. Vicarro Skyline's 55-home first phase broke ground August 2026 with the full 1,400-unit build-out running for years. Eagle Mountain proper is now releasing its final phase. Whether you already own a lot, are negotiating a purchase, or are picking between the older Eagle Mountain and new Vicarro releases, bring us your lot survey. We'll walk the property with you, review the phase-specific guidelines, and give you a real cost and timeline read before you commit."),
            ("What amenities do Eagle Mountain residents get access to?",
             "Vicarro Skyline residents get access to a private neighbourhood pool and community amenities designed by Pacific Peak Homes and Diverse Properties. Older Eagle Mountain phases carry their own established landscaping and community feel. Panoramic mountain views south to Mount Baker and Sumas Mountain define the setting. Ledgeview Golf Course is 10 minutes north for championship-level golf. Sumas Mountain Park offers hiking trails, and Cultus Lake Provincial Park is 20 minutes east. Downtown Abbotsford with restaurants, shopping, and services is 15 minutes north via Highway 11."),
            ("What schools are near Eagle Mountain?",
             "Eagle Mountain is in Abbotsford School District 34 (SD34). Auguston Traditional Elementary at 3160 Immel Street is one of the closest K-6 schools. Robert Bateman Secondary at 35045 Exbury Avenue handles grades 8 to 12. For families looking at independent schools, Mennonite Educational Institute (K to 12) is a well-known Abbotsford option. Post-secondary options include University of the Fraser Valley (UFV), roughly 10 minutes north in Abbotsford, and Trinity Western University (TWU) in nearby Langley, 25 minutes west."),
            ("How far is Eagle Mountain from Abbotsford, Vancouver, and the airport?",
             "Downtown Abbotsford is 15 minutes north via Highway 11. Abbotsford International Airport (YXX) is 20 minutes west with direct flights to Calgary, Toronto, Kelowna, and other Canadian destinations. Vancouver International Airport (YVR) is 1 hour west via Highway 1. Downtown Vancouver is 1 hour west. Chilliwack is 25 minutes east. Cultus Lake Provincial Park is 20 minutes east for summer recreation. Sumas Mountain Regional Park is minutes away for hiking. The US border at Sumas is 15 minutes south."),
        ],
    },

    "the-rise": {
        "name": "The Rise",
        "parent_city": "Vernon",
        "parent_slug": "vernon",
        "region": "BC",
        "lat": "50.2903",
        "lon": "-119.2711",
        "h1": "Custom Home Builder at The Rise, Vernon.",
        "sub": "Vernon's hillside golf-course community by Okanagan Hills Development Corp., anchored by an 18-hole Fred Couples signature golf course with panoramic Okanagan Lake and valley views.",
        "hero": "/wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg",
        "hero_alt": "Luxury custom home in Vineyard Estates, West Kelowna portfolio example by Palermo Homes",
        "meta_title": "Custom Home Builder The Rise, Vernon | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes at The Rise, Vernon's hillside golf-course community with panoramic lake and mountain views.",
        "eyebrow": "Neighbourhood · Vernon",
        "overview": [
            "Palermo Homes is a licensed BC Housing custom home builder that brings in-house cabinetry, custom finish carpentry, envelope discipline, and fixed-price contracts to every project. The Rise is a hillside golf-course community and view-corridor design is what these lots demand.",
            "We serve The Rise from our Central Okanagan operation. Site visits and design meetings are a scheduled trip and we price that reality transparently. Bring us your lot survey and we walk the property with you before you commit.",
            "The Rise is a master-planned hillside community by Okanagan Hills Development Corp. on the west side of Vernon, adjacent to Turtle Mountain. Anchored by an 18-hole Fred Couples signature golf course. Community includes townhomes, single-family lots, and estate custom home sites capturing panoramic Okanagan Lake, valley, and mountain views. Amenities include high-end dining and year-round virtual golf. Schools are Vernon School District 22 (SD22). Downtown Vernon 10 min east via Highway 97, Kalamalka Lake 20 min east, Silver Star Mountain Resort 40 min northeast for winter skiing, Kelowna 45 min south, Kelowna International Airport (YLW) 40 min south.",
        ],
        "overview_photos": [
            ("/wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg", "Luxury custom home in Vineyard Estates, West Kelowna portfolio example by Palermo Homes"),
        ],
        "amenities": [
            ("Golf", "Fred Couples Signature Course", "18-hole championship signature golf course by Fred Couples anchors the community"),
            ("Dining", "The Rise Clubhouse", "High-end dining and year-round virtual golf at the community clubhouse"),
            ("Views", "Panoramic Lake + Valley", "Elevated hillside lots capture Okanagan Lake, valley, and mountain views"),
            ("Winter Sports", "Silver Star Mountain", "Silver Star Mountain Resort is 40 min northeast for skiing and mountain biking"),
        ],
        "facts": [
            ("Anchor", "Fred Couples Golf · 18 Holes"),
            ("Downtown Vernon", "10 min · Highway 97"),
            ("YLW Airport", "40 min · Highway 97"),
            ("Direct", '<a href="tel:+17787604113">(778) 760-4113</a>'),
        ],
        "why_h": "Why The Rise clients hire Palermo.",
        "why_items": [
            ("Golf-course lot design experience", "The Rise custom homes orient around the Fred Couples course and Okanagan Lake view corridor. We design floor plans that capture golf-course frontage and view corridors while managing privacy and light."),
            ("Hillside and slope experience", "The Rise lots range from gently sloping to steep hillside cuts. Retaining, drainage, foundation stepping, and structural engineering matter here. We've been doing hillside custom work across the Okanagan for years."),
            ("City of Vernon permits", "The Rise sits inside the City of Vernon. City permits, inspections, and servicing coordination run differently than the Regional District or District of Coldstream. We know the process."),
            ("Community design coordination", "The Rise has phase-specific design covenants that vary by release. We check every lot for registered covenants at the design stage and manage the review package on your behalf."),
            ("Same finish standard as our Kelowna work", "In-house cabinetry, custom finish carpentry, envelope details that hold up. The Rise homes carry high market value because the views and golf-course setting are premium, and we match the level of build the setting deserves."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Custom Palermo Homes interior finish, portfolio example for The Rise",
        "split_photo_loc": "Portfolio · Palermo Homes",
        "feat_h": "Portfolio match for The Rise.",
        "feat_body": "Our Vineyard Estates custom home in West Kelowna is the closest portfolio match for what a Rise custom build should be. Hillside cut, full lake-view orientation, custom finish carpentry throughout, and the stone-and-timber material palette that fits Okanagan hillside districts. Terrain and view considerations map directly to The Rise's golf-course and hillside lots.",
        "feat_photo": "/wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg",
        "feat_photo_alt": "Luxury custom home in Vineyard Estates, West Kelowna by Palermo Homes",
        "feat_link": "/project/vineyard-estates-3/",
        "feat_link_label": "View the Vineyard Estates home",
        "feat_card_loc": "West Kelowna, BC · Portfolio",
        "feat_card_title": "Luxury Custom Home in Vineyard Estates",
        "faqs": [
            ("How much does a custom home cost at The Rise?",
             "Most Rise custom builds run $1.5M and up for the home alone, which pencils out around $500 to $850 per square foot depending on finish level. Lot prices range from around $400K for smaller lots without direct course frontage to $1.5M plus for premium golf-course view lots with panoramic Okanagan Lake orientation. Total finished cost swings with slope, retaining, geotech, and finish level. Golf-course frontage lots often add design considerations around glazing, privacy, and course-side setbacks. We provide line-item pricing up front, break out soft costs (design, permits, geotech) from hard costs, and lock in fixed-price contracts where possible so nothing sneaks up on you mid-build."),
            ("Do Rise homes have to follow design guidelines?",
             "The Rise carries phase-specific design covenants registered against title, plus City of Vernon zoning bylaws, hillside development permits, and standard building code. Design covenants typically cover material palette, roof pitch and profile, massing, exterior colour range, and how homes sit on the lot in relation to neighbours' view corridors and golf-course frontage. On steep cuts, geotechnical assessment and hillside development permits are typically required and can affect design (foundation type, retaining, drainage). We check every lot for registered covenants at the design stage and manage all City of Vernon submissions on your behalf."),
            ("How long does a Rise custom home take to build?",
             "Plan on 14 to 20 months from first design meeting to move-in. Roughly 3 to 5 months for design development and any covenant reviews, 2 to 3 months for City of Vernon building permits and geotechnical assessment (longer on hillside cuts), and 9 to 12 months of construction. Steep Rise cuts often add another 4 to 8 weeks for retaining walls, drainage, and foundation stepping. Weather matters. Excavation, foundations, and framing move fastest through Okanagan summers, and interior finish work carries through winter without weather risk."),
            ("Which parts of The Rise do you build in?",
             "The Rise is a phased master-planned community by Okanagan Hills Development Corp. Early phases developed lower on the hillside with more established landscaping. Newer phases climb higher up the mountainside with more elevated view lots and closer golf-course integration. The community continues to release new lots and phases. We're actively taking on projects across current phases. Whether you already own a lot, are negotiating a purchase, or are picking between golf-course frontage and elevated view options, bring us the lot survey and we'll walk it with you before you commit."),
            ("What amenities do The Rise residents get access to?",
             "The Rise is anchored by an 18-hole Fred Couples signature championship golf course, high-end dining at the community clubhouse, and year-round virtual golf. The adjacent Turtle Mountain area offers hiking and biking trails. Silver Star Mountain Resort is 40 minutes northeast for winter skiing and summer mountain biking. Predator Ridge Resort (36 holes of golf, dining, spa) is 20 minutes east. Sparkling Hill Resort (award-winning wellness centre) is 20 minutes east. Kalamalka Lake beaches are 20 minutes east through Vernon. Downtown Vernon with restaurants, shops, and services is 10 minutes east via Highway 97."),
            ("What schools are near The Rise?",
             "The Rise is in Vernon School District 22 (SD22). Vernon's public elementary and secondary schools serve the community. Ellison Elementary and W.L. Seaton Secondary are among the closest, 10 to 15 minutes east in Vernon. For families looking at independent schools, Vernon Christian School (K to 12) is in Coldstream (20 minutes east). Post-secondary options include Okanagan College's Vernon campus (15 minutes east) and UBC Okanagan (45 minutes south in Kelowna)."),
            ("How far is The Rise from Vernon, Kelowna, and the airport?",
             "Downtown Vernon is 10 minutes east via Highway 97. Kalamalka Lake beaches are 20 minutes east through Vernon. Predator Ridge Resort is 20 minutes east via Commonage Road. Sparkling Hill Resort is 20 minutes east. Silver Star Mountain Resort is 40 minutes northeast for winter skiing. Kelowna is 45 minutes south via Highway 97. Kelowna International Airport (YLW) is 40 minutes south with direct flights to Vancouver, Calgary, Seattle, and seasonal service to Toronto. Big White Ski Resort is about 90 minutes southeast."),
        ],
    },
}


def render_neighborhood(slug, data):
    page_url = f"{BIZ_URL}/neighborhoods/{slug}/"
    canonical = page_url

    # amenity grid html
    amen_items = "\n".join([
        f'        <div class="item"><p class="k">{k}</p><p class="v">{v}</p><p class="n">{n}</p></div>'
        for k, v, n in data["amenities"]
    ])

    # facts strip
    fact_items = "\n".join([
        f'      <div class="fact"><p class="k">{k}</p><p class="v">{v}</p></div>'
        for k, v in data["facts"]
    ])

    # why items (split)
    why_lis = "\n".join([
        f'          <li><span class="num">{str(i+1).zfill(2)}</span><span class="txt"><strong>{t}</strong>{d}</span></li>'
        for i, (t, d) in enumerate(data["why_items"])
    ])

    # overview paragraphs
    over_ps = "\n        ".join([f'<p>{p}</p>' for p in data["overview"]])

    # overview photos (side-by-side, portrait aspect)
    over_photos_html = "\n".join([
        f'          <div class="photo"><img src="{src}" alt="{alt}" loading="lazy"></div>'
        for src, alt in data["overview_photos"]
    ])
    photos_class = "col-photos single" if len(data["overview_photos"]) == 1 else "col-photos"

    # faq html
    faq_html = "\n".join([
        f'<details><summary>{q}</summary><div class="ans">{a}</div></details>'
        for q, a in data["faqs"]
    ])

    # schema
    lat = data.get("lat")
    lon = data.get("lon")
    schema = full_schema(
        business_schema(lat, lon),
        service_schema(
            f"Custom Home Builder {data['name']}",
            f"Palermo Homes provides custom home design and construction in {data['name']}, {data['parent_city']}, {data['region']}.",
            page_url,
            data["name"],
            data["region"],
            lat, lon,
        ),
        place_schema(data["name"], data["parent_city"], data["region"], lat, lon),
        faq_schema(data["faqs"]),
        breadcrumb_schema(page_url, data["parent_slug"], data["parent_city"], data["name"]),
        webpage_schema(page_url, data["name"], data["meta_desc"]),
    )

    main = f"""
<div class="svc">
  <section class="svc-hero">
    <div class="bg" style="background-image:url('{data['hero']}')"></div>
    <div class="inner">
      <p class="eyebrow">{data['eyebrow']}</p>
      <h1>{data['h1']}</h1>
      <p class="sub">{data['sub']}</p>
    </div>
  </section>

  <section class="svc-facts">
    <div class="wrap">
{fact_items}
    </div>
  </section>

  <section class="svc-over">
    <div class="wrap">
      <div class="grid">
        <div class="col-text">
          <div class="head">
            <p class="eyebrow">Overview</p>
            <h2>Custom home builder in {data['name']}, {data['parent_city']}.</h2>
          </div>
          <div class="body">
            {over_ps}
          </div>
        </div>
        <div class="{photos_class}">
{over_photos_html}
        </div>
      </div>
    </div>
  </section>

  <section class="svc-amen">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Community amenities</p>
        <h2>What Lakestone residents get access to.</h2>
      </div>
      <div class="grid">
{amen_items}
      </div>
    </div>
  </section>

  <section class="svc-feat">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Featured build</p>
      </div>
      <div class="row">
        <a class="card" href="{data['feat_link']}" aria-label="View {data['feat_card_title']}">
          <div class="photo"><img src="{data['feat_photo']}" alt="{data['feat_photo_alt']}" loading="lazy"></div>
          <div class="meta">
            <div class="txt">
              <span class="lab">{data['feat_card_loc']}</span>
              <h3>{data['feat_card_title']}</h3>
            </div>
            <span class="arrow">→</span>
          </div>
        </a>
        <div class="copy">
          <h2>{data['feat_h']}</h2>
          <p>{data['feat_body']}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="svc-trust">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Credentials</p>
        <h2>Recognized, licensed, and warrantied.</h2>
      </div>
      <div class="grid">
        <div class="item">
          <p class="k">Award-Winning</p>
          <p class="v">CHBA Fraser Valley</p>
          <p class="n">Awards of Excellence Winner</p>
        </div>
        <div class="item">
          <p class="k">Experience</p>
          <p class="v">15+ Years</p>
          <p class="n">Custom homes across BC</p>
        </div>
        <div class="item">
          <p class="k">Warranty</p>
          <p class="v">2-5-10 Home Warranty</p>
          <p class="n">Full BC-registered coverage</p>
        </div>
        <div class="item">
          <p class="k">Licensed</p>
          <p class="v">Licensed &amp; Insured</p>
          <p class="n">BC Licensed Residential Builder</p>
        </div>
      </div>
    </div>
  </section>

  <section class="svc-split">
    <div class="wrap"><div class="grid">
      <div class="photo-col">
        <p class="photo-loc">{data['split_photo_loc']}</p>
        <div class="photo">
          <img src="{data['split_photo']}" alt="{data['split_photo_alt']}" loading="lazy">
        </div>
      </div>
      <div>
        <p class="eyebrow">Why Palermo</p>
        <h2>{data['why_h']}</h2>
        <ul>
{why_lis}
        </ul>
      </div>
    </div></div>
  </section>

  <section class="svc-tiles">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">What we build in {data['name']}</p>
        <h2>Custom homes, renovations, and general contracting.</h2>
      </div>
      <div class="cards">
        <a class="card" href="/services/custom-homes/">
          <h3>Custom Homes</h3>
          <p>Custom home builds in {data['name']} and across {data['parent_city']}. Every project designed around the lot, the view corridor, and how you actually live.</p>
          <span class="go">Custom Homes →</span>
        </a>
        <a class="card" href="/services/renovations/">
          <h3>Home Renovations</h3>
          <p>Whole-home renovations, kitchens, bathrooms, and additions in {data['name']}. Built to the same finish standard as our custom homes.</p>
          <span class="go">Renovations →</span>
        </a>
        <a class="card" href="/services/general-contracting/">
          <h3>General Contracting</h3>
          <p>Project management with in-house crews on the trades that matter. One team, one contract, one point of contact.</p>
          <span class="go">General Contracting →</span>
        </a>
      </div>
    </div>
  </section>

  <section class="svc-faq">
    <div class="wrap">
      <div class="head"><p class="eyebrow">FAQ</p><h2>Custom homes in {data['name']}, answered.</h2></div>
      <div class="items">{faq_html}</div>
    </div>
  </section>

  <section class="svc-nearby">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Also serving</p>
        <h2>Custom home builder across the Okanagan and Lower Mainland.</h2>
      </div>
      <p class="list">
        <a href="/service-areas/{data['parent_slug']}/">{data['parent_city']}</a>
        <span class="sep">·</span>
        <a href="/service-areas/kelowna/">Kelowna</a>
        <span class="sep">·</span>
        <a href="/service-areas/west-kelowna/">West Kelowna</a>
        <span class="sep">·</span>
        <a href="/service-areas/peachland/">Peachland</a>
        <span class="sep">·</span>
        <a href="/service-areas/vernon/">Vernon</a>
        <span class="sep">·</span>
        <a href="/service-areas/penticton/">Penticton</a>
        <span class="sep">·</span>
        <a href="/service-areas/lower-mainland/">Lower Mainland</a>
      </p>
      <p class="updated">Updated {BUILD_DATE_HUMAN}</p>
    </div>
  </section>

  <section class="svc-cta">
    <div class="wrap">
      <h2>Building in {data['name']}?</h2>
      <p>Tell us about your lot. We'll book a no-pressure consultation.</p>
      <a class="btn" href="/contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""

    render_page(
        title=data["meta_title"],
        meta_desc=data["meta_desc"],
        canonical=canonical,
        schema_block=schema,
        main_html=main,
        out_path=SITE / "neighborhoods" / slug / "index.html",
    )


def main():
    print("Building neighborhood pages...")
    built = 0
    for slug, data in NEIGHBORHOODS.items():
        if slug.startswith("_"):
            continue  # draft entries staged for later review
        render_neighborhood(slug, data)
        built += 1
    print(f"Done. Built {built} neighborhood page(s).")


if __name__ == "__main__":
    main()
