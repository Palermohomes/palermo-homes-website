"""Build /service-areas/ hub + 7 city landing pages using About shell.
Each page: unique title/meta, LocalBusiness+Service+FAQPage schema, editorial layout.
Reuses the .svc design system from build_services.py so everything flows.
Idempotent. Safe to rerun."""
import re
import json
from pathlib import Path

import datetime
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

CSS_START = "/* ==== AREAS-V2 CSS START ==== */"
CSS_END = "/* ==== AREAS-V2 CSS END ==== */"

# Shared design system, matches build_services.py exactly, plus a few
# area-specific additions (fact strip, neighborhood chips, hub grid).
AREAS_CSS = f"""
{CSS_START}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html body #et-main-area .svc{{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1d21;background:#fff}}
html body #et-main-area .svc *{{box-sizing:border-box}}
html body #et-main-area .svc img{{display:block;max-width:100%;height:auto}}
html body #et-main-area .svc .wrap{{max-width:1360px;margin:0 auto;padding:0 clamp(20px,3vw,48px)}}
html body #et-main-area .svc .eyebrow{{font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:#0085c9;font-weight:500;margin:0 0 20px}}

/* Breadcrumb strip. Slim, subtle, above hero. SEO + wayfinding. */
html body #et-main-area .svc-crumb{{background:#fff;padding:14px 0;border-bottom:1px solid #ece8df;font-size:12.5px;color:#6a7078;letter-spacing:.01em}}
html body #et-main-area .svc-crumb a{{color:#6a7078;text-decoration:none;transition:color .2s}}
html body #et-main-area .svc-crumb a:hover{{color:#0085c9}}
html body #et-main-area .svc-crumb .sep{{margin:0 8px;color:#c8c3b3}}
html body #et-main-area .svc-crumb .current{{color:#1a1d21;font-weight:500}}

/* Hero */
html body #et-main-area .svc-hero{{position:relative;min-height:clamp(280px,42vh,420px);padding:40px 0;display:flex;align-items:center;overflow:hidden;color:#fff}}
html body #et-main-area .svc-hero .bg{{position:absolute;inset:0;background-position:center center;background-size:cover;background-repeat:no-repeat;image-rendering:-webkit-optimize-contrast}}
html body #et-main-area .svc-hero::after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.48) 0%,rgba(0,0,0,.55) 50%,rgba(0,0,0,.70) 100%)}}
html body #et-main-area .svc-hero .inner{{position:relative;z-index:2;max-width:1360px;margin:0 auto;width:100%;padding:0 clamp(20px,3vw,48px);box-sizing:border-box}}
html body #et-main-area .svc-hero .eyebrow{{color:rgba(255,255,255,.9);margin:0 0 14px}}
html body #et-main-area .svc-hero h1{{font-size:clamp(28px,3.6vw,46px);font-weight:500;letter-spacing:-0.02em;line-height:1.05;margin:0;max-width:22ch;text-transform:none;color:#fff}}
html body #et-main-area .svc-hero p.sub{{font-size:clamp(15px,1.2vw,17px);color:rgba(255,255,255,.92);margin:18px 0 0;max-width:60ch;line-height:1.55}}
html body #et-main-area .svc-hero.centered{{min-height:clamp(300px,44vh,440px)}}
html body #et-main-area .svc-hero.centered::after{{background:linear-gradient(180deg,rgba(0,0,0,.38) 0%,rgba(0,0,0,.48) 50%,rgba(0,0,0,.58) 100%)}}
html body #et-main-area .svc-hero.centered .inner{{padding:0 clamp(20px,4vw,56px);text-align:center}}
html body #et-main-area .svc-hero.centered .eyebrow{{margin:0 auto 18px}}
html body #et-main-area .svc-hero.centered h1{{font-size:clamp(28px,3.4vw,42px);max-width:26ch;margin:0 auto;line-height:1.1}}
html body #et-main-area .svc-hero.centered p.sub{{margin:20px auto 0;max-width:60ch;text-align:center}}

/* Fact strip under hero */
html body #et-main-area .svc-facts{{background:#0085c9;color:#fff;padding:24px 0}}
html body #et-main-area .svc-facts .wrap{{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;align-items:start}}
html body #et-main-area .svc-facts .fact{{border-left:1px solid rgba(255,255,255,.28);padding:2px 0 2px 20px}}
html body #et-main-area .svc-facts .fact:first-child{{border-left:0;padding-left:0}}
html body #et-main-area .svc-facts .k{{font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:rgba(255,255,255,.78);margin:0 0 6px;font-weight:500}}
html body #et-main-area .svc-facts .v{{font-size:16px;font-weight:600;line-height:1.35;margin:0;color:#fff}}
html body #et-main-area .svc-facts .v a{{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.4)}}

/* Overview */
html body #et-main-area .svc-over{{padding:44px 0 28px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-over .head{{max-width:none;margin:0 0 22px;text-align:left}}
html body #et-main-area .svc-over .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-over h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21;max-width:32ch}}
html body #et-main-area .svc-over .body{{max-width:82ch}}
html body #et-main-area .svc-over p{{font-size:15.5px;line-height:1.7;color:#3a4048;margin:0 0 16px}}
html body #et-main-area .svc-over p:last-child{{margin:0}}

/* Trust signals bar. Credentials + awards in a subtle horizontal row. Authority signal for Google + reassurance for humans. */
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

/* Neighborhoods. Passive labels, NOT clickable */
html body #et-main-area .svc-hoods{{padding:36px 0 40px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-hoods .head{{max-width:none;margin:0 0 22px}}
html body #et-main-area .svc-hoods .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-hoods h2{{font-size:clamp(20px,2.2vw,26px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-hoods .list{{font-size:clamp(15px,1.3vw,17px);line-height:2;color:#3a4048;letter-spacing:.005em;font-weight:400;margin:0;text-align:justify;text-align-last:center}}
html body #et-main-area .svc-hoods .list .name{{color:#1a1d21;font-weight:500;white-space:nowrap}}
html body #et-main-area .svc-hoods .list .sep{{color:#0085c9;font-weight:400;opacity:.55}}

/* Featured neighborhood detail pages. Clickable cards matching the .pv-card style used across project pages. */
html body #et-main-area .svc-npages{{padding:32px 0 48px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-npages .head{{margin:0 0 22px;max-width:820px}}
html body #et-main-area .svc-npages .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-npages h2{{font-size:clamp(20px,2.2vw,28px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0;color:#1a1d21}}
html body #et-main-area .svc-npages .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
html body #et-main-area .svc-npages .card{{display:block;text-decoration:none;color:inherit;background:#fff;overflow:hidden;border:1px solid #c9c3b5;box-shadow:0 2px 10px rgba(0,0,0,.05);transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease}}
html body #et-main-area .svc-npages .card:hover{{transform:translateY(-6px);box-shadow:0 18px 40px rgba(0,0,0,.14);border-color:#0085c9}}
html body #et-main-area .svc-npages .card .photo{{aspect-ratio:4/3;overflow:hidden;background:#e8e5dd;position:relative}}
html body #et-main-area .svc-npages .card .photo img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s ease,filter .3s ease;filter:brightness(.96)}}
html body #et-main-area .svc-npages .card:hover .photo img{{transform:scale(1.04);filter:brightness(1)}}
html body #et-main-area .svc-npages .card .meta{{padding:18px 22px 20px;border-top:2px solid #0085c9;display:flex;justify-content:space-between;align-items:center;gap:14px}}
html body #et-main-area .svc-npages .card .meta .txt{{min-width:0;flex:1}}
html body #et-main-area .svc-npages .card .meta .loc{{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#7a828c;font-weight:500;margin:0 0 6px}}
html body #et-main-area .svc-npages .card .meta h3.name{{font-size:19px;font-weight:600;letter-spacing:-0.01em;line-height:1.2;margin:0;color:#1a1d21}}
html body #et-main-area .svc-npages .card .meta .end{{flex-shrink:0;display:inline-flex;align-items:center;gap:8px}}
html body #et-main-area .svc-npages .card .meta .go{{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#0085c9;font-weight:600}}
html body #et-main-area .svc-npages .card .meta .arr{{color:#0085c9;font-size:20px;line-height:1;font-weight:400;transition:transform .25s ease}}
html body #et-main-area .svc-npages .card:hover .meta .arr{{transform:translateX(4px)}}

/* Split */
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

/* Featured project spotlight. Eyebrow above (left), then 2-col grid (card left, h2+copy right) on desktop, stacked on mobile */
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

/* Service tiles */
html body #et-main-area .svc-tiles{{padding:44px 0 44px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-tiles .head{{max-width:none;margin:0 0 24px}}
html body #et-main-area .svc-tiles .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-tiles h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-tiles .cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:0}}
html body #et-main-area .svc-tiles .card{{padding:36px 32px;border:1px solid #e2e0d9;text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:12px;transition:background .2s,border-color .2s}}
html body #et-main-area .svc-tiles .card+.card{{margin-left:-1px}}
html body #et-main-area .svc-tiles a.card{{cursor:pointer}}
html body #et-main-area .svc-tiles a.card:hover{{background:#faf9f5;border-color:#0085c9}}
html body #et-main-area .svc-tiles .card h3{{font-size:20px;font-weight:600;letter-spacing:-0.01em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-tiles .card p{{font-size:14.5px;color:#5a6069;line-height:1.6;margin:0}}
html body #et-main-area .svc-tiles .card .go{{margin-top:auto;padding-top:16px;font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:#0085c9;font-weight:600}}

/* FAQ */
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

/* Hub grid (7 cities) */
html body #et-main-area .svc-cities{{padding:44px 0 60px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-cities .head{{max-width:820px;margin:0 0 28px}}
html body #et-main-area .svc-cities .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-cities h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-cities .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
@media (max-width:1024px){{html body #et-main-area .svc-cities .grid{{grid-template-columns:repeat(2,1fr);gap:16px}}}}
html body #et-main-area .svc-cities .card{{position:relative;overflow:hidden;text-decoration:none;color:#1a1d21;background:#fff;display:flex;flex-direction:column;cursor:pointer;border:1px solid #e2ddd0;transition:border-color .3s ease,box-shadow .3s ease,transform .3s ease}}
html body #et-main-area .svc-cities .card:hover{{border-color:#0085c9;box-shadow:0 10px 28px rgba(0,133,201,.14);transform:translateY(-3px)}}
html body #et-main-area .svc-cities .card .imgwrap{{position:relative;width:100%;aspect-ratio:4/3;overflow:hidden;background:#eee}}
html body #et-main-area .svc-cities .card img{{width:100%;height:100%;object-fit:cover;transition:transform .7s ease}}
html body #et-main-area .svc-cities .card:hover img{{transform:scale(1.05)}}
html body #et-main-area .svc-cities .card .txt{{padding:18px 22px 20px;border-top:1px solid #e2ddd0;display:flex;flex-direction:column;gap:6px}}
html body #et-main-area .svc-cities .card .lab{{display:block;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:#8a8f97;font-weight:600;margin:0;line-height:1.5;min-height:2.6em}}
html body #et-main-area .svc-cities .card h3{{font-size:19px;font-weight:600;letter-spacing:-0.01em;margin:0;color:#1a1d21;line-height:1.3;display:flex;justify-content:space-between;align-items:center;gap:12px}}
html body #et-main-area .svc-cities .card h3 span{{color:#1a1d21}}
html body #et-main-area .svc-cities .card h3 .pre{{color:#1a1d21;font-weight:600}}
html body #et-main-area .svc-cities .card h3 span:first-child{{flex:1;color:#1a1d21}}
html body #et-main-area .svc-cities .card h3 .arr{{color:#0085c9 !important;font-size:20px;font-weight:400;transition:transform .3s ease;flex-shrink:0}}
html body #et-main-area .svc-cities .card:hover h3 .arr{{transform:translateX(6px)}}

/* Related cities. Editorial inline block, internal linking boost + local SEO context */
html body #et-main-area .svc-nearby{{padding:36px 0 40px;background:#fff;border-bottom:1px solid #e2ddd0}}
html body #et-main-area .svc-nearby .head{{max-width:none;margin:0 0 16px}}
html body #et-main-area .svc-nearby .eyebrow{{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:#0085c9;font-weight:600;margin:0 0 12px}}
html body #et-main-area .svc-nearby h2{{font-size:clamp(20px,2.2vw,26px);font-weight:500;letter-spacing:-0.02em;margin:0;color:#1a1d21}}
html body #et-main-area .svc-nearby .list{{font-size:clamp(15px,1.3vw,17px);line-height:1.9;color:#3a4048;letter-spacing:.005em;font-weight:400;margin:0}}
html body #et-main-area .svc-nearby .list a{{color:#0085c9;font-weight:600;text-decoration:underline;text-decoration-color:#0085c9;text-underline-offset:3px;text-decoration-thickness:1px;transition:color .2s,text-decoration-color .2s}}
html body #et-main-area .svc-nearby .list a:hover{{color:#006ba1;text-decoration-color:#006ba1}}
html body #et-main-area .svc-nearby .list .sep{{color:#0085c9;margin:0 12px;font-weight:400;opacity:.55}}
html body #et-main-area .svc-nearby .updated{{font-size:12px;color:#8a8f97;letter-spacing:.02em;margin:22px 0 0}}

/* CTA */
html body #et-main-area .svc-cta{{background:#0085c9;color:#fff;padding:56px 0;text-align:center}}
html body #et-main-area .svc-cta h2{{font-size:clamp(22px,2.4vw,30px);font-weight:500;letter-spacing:-0.02em;line-height:1.15;margin:0 0 14px;color:#fff !important}}
html body #et-main-area .svc-cta p{{color:rgba(255,255,255,.92) !important;font-size:16px;margin:0 0 26px}}
html body #et-main-area .svc-cta a.btn{{display:inline-block;background:#fff;color:#0085c9;padding:14px 30px;border-radius:999px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;text-decoration:none;transition:background .2s,color .2s}}
html body #et-main-area .svc-cta a.btn:hover{{background:#141821;color:#fff}}

@media (max-width:900px){{
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
  html body #et-main-area .svc-cities .grid{{grid-template-columns:1fr 1fr;gap:10px}}
  html body #et-main-area .svc-cities .card .imgwrap{{aspect-ratio:4/3}}
  html body #et-main-area .svc-cities .card .txt{{padding:12px 14px 14px;gap:4px}}
  html body #et-main-area .svc-cities .card h3{{font-size:14px}}
  html body #et-main-area .svc-cities .card h3 .pre{{display:none}}
  html body #et-main-area .svc-cities .card h3 .arr{{font-size:16px}}
  html body #et-main-area .svc-cities .card .lab{{font-size:9px;letter-spacing:.18em;margin-bottom:2px;line-height:1.5;min-height:2.6em}}
  html body #et-main-area .svc-over,html body #et-main-area .svc-faq,html body #et-main-area .svc-cta,html body #et-main-area .svc-tiles,html body #et-main-area .svc-feat,html body #et-main-area .svc-cities{{padding:28px 0}}
  html body #et-main-area .svc-split,html body #et-main-area .svc-hoods{{padding:22px 0 28px}}
  html body #et-main-area .svc-npages{{padding:22px 0 32px}}
  html body #et-main-area .svc-npages .grid{{grid-template-columns:repeat(2,1fr);gap:10px}}
  html body #et-main-area .svc-npages .card .photo{{aspect-ratio:4/3}}
  html body #et-main-area .svc-npages .card .meta{{padding:12px 14px 14px;gap:8px}}
  html body #et-main-area .svc-npages .card .meta .loc{{font-size:10px;letter-spacing:.2em;margin:0 0 4px}}
  html body #et-main-area .svc-npages .card .meta h3.name{{font-size:14.5px;line-height:1.25}}
  html body #et-main-area .svc-npages .card .meta .go{{font-size:0;letter-spacing:0}}
  html body #et-main-area .svc-npages .card .meta .arr{{font-size:18px}}
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


def business_schema(city_lat=None, city_lon=None):
    """LocalBusiness with full E-A-T fields. Geo passed per-city so each page
    signals that specific service area, not just HQ (Kelowna)."""
    geo_block = ""
    if city_lat is not None and city_lon is not None:
        geo_block = f',\n    "geo": {{"@type":"GeoCoordinates","latitude":{city_lat},"longitude":{city_lon}}}'
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


def service_schema(service_type, name, description, page_url, city, region="BC", city_lat=None, city_lon=None):
    return f'''{{
    "@type": "Service",
    "serviceType": "{service_type}",
    "name": "{name}",
    "description": "{description}",
    "url": "{page_url}",
    "provider": {business_schema(city_lat, city_lon)},
    "areaServed": {{"@type":"City","name":"{city}","containedInPlace":{{"@type":"AdministrativeArea","name":"{region}"}}}}
  }}'''


def place_schema(city, region="BC"):
    return f'''{{
    "@type": "Place",
    "name": "{city}, {region}",
    "address": {{"@type":"PostalAddress","addressLocality":"{city}","addressRegion":"{region}","addressCountry":"CA"}}
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


def breadcrumb_schema(page_url, city):
    return f'''{{
    "@type":"BreadcrumbList",
    "itemListElement":[
      {{"@type":"ListItem","position":1,"name":"Home","item":"{BIZ_URL}/"}},
      {{"@type":"ListItem","position":2,"name":"Custom Home Builder {city}","item":"{page_url}"}}
    ]
  }}'''


def webpage_schema(page_url, city, meta_desc):
    return f'''{{
    "@type": "WebPage",
    "@id": "{page_url}#webpage",
    "url": "{page_url}",
    "name": "Custom Home Builder {city}",
    "description": "{meta_desc}",
    "isPartOf": {{"@id": "{BIZ_URL}/#website"}},
    "about": {{"@id": "{BIZ_URL}/#organization"}},
    "datePublished": "2026-09-01",
    "dateModified": "{BUILD_DATE}",
    "inLanguage": "en-CA"
  }}'''


def full_schema(*blocks):
    return '<script type="application/ld+json">{"@context":"https://schema.org","@graph":[' + ",".join(blocks) + ']}</script>'


# ---- Page renderer ----
def render_page(title, meta_desc, canonical, schema_block, main_html, out_path: Path):
    html = SHELL_HEAD + main_html + SHELL_FOOT
    if CSS_START in html:
        html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.DOTALL)
    html = re.sub(r"/\* ==== ABOUT-V2 CSS START ==== \*/.*?/\* ==== ABOUT-V2 CSS END ==== \*/", "", html, flags=re.DOTALL)
    html = html.replace("</style></head>", AREAS_CSS + "</style></head>", 1)
    # About-page shell has `href="../index.html"` in Divi's hidden mobile menu, which
    # from a 2-deep city page resolves to a non-existent `/service-areas/index.html`. Root it.
    html = html.replace('href="../index.html"', 'href="/"')
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', html, count=1)
    # Strip existing canonical (any attribute order), inject fresh
    html = re.sub(r'<link[^>]*rel="canonical"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<link rel="canonical" href="{canonical}"/>\n</head>', 1)
    # Strip existing meta description, inject fresh
    html = re.sub(r'<meta[^>]*name="description"[^>]*/?>', '', html)
    html = html.replace("</head>", f'<meta name="description" content="{meta_desc}"/>\n</head>', 1)
    # Overwrite stale OG tags from the About shell
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


# ---- Data: 7 service area cities ----
# Each entry drives content, hero, projects referenced, neighborhoods, and schema.
CITIES = {
    "kelowna": {
        "name": "Kelowna",
        "region": "BC",
        "lat": "49.8880",
        "lon": "-119.4960",
        "h1": "Custom Home Builder in Kelowna, BC.",
        "sub": "Serving Kelowna clients from our West Kelowna base. Upper Mission, Kettle Valley, Wilden, Glenmore, Lower Mission. 10 minutes across the bridge, same in-house team.",
        "hero": "/wp-content/uploads/2025/12/Cabernet-07.jpg",
        "hero_alt": "Modern lakeview custom home representative of Palermo Homes Central Okanagan builds",
        "meta_title": "Custom Home Builder Kelowna, BC | Palermo Homes",
        "meta_desc": "Palermo Homes serves Kelowna clients from our West Kelowna base. Custom homes for Upper Mission, Kettle Valley, Wilden, Glenmore. 15+ years in the Central Okanagan.",
        "eyebrow": "Service Area · Central Okanagan",
        "neighborhoods": [
            "Upper Mission", "Wilden", "Kettle Valley", "The Ponds",
            "McKinley Beach", "Lower Mission", "Glenmore", "University Heights",
            "Black Mountain", "Dilworth Mountain", "Sheerwater", "South East Kelowna",
        ],
        "neighborhood_pages": [
            ("upper-mission", "Upper Mission",
             "Kelowna's flagship luxury district on the south hillside. Kettle Valley, Southridge, The Ponds, Crawford Estates. Transferable hillside engineering from our West Kelowna wine-district portfolio.",
             "/wp-content/uploads/2026/01/1583-Malbec-13.jpg",
             "Lakeview custom home interior representative of Palermo Homes hillside builds, closest match for Upper Mission"),
            ("kettle-valley", "Kettle Valley",
             "Award-winning master-planned neo-traditional village in Upper Mission. Central green, walkable village centre, and a dozen parks. Hillside builds transferable from our West Kelowna portfolio.",
             "/wp-content/uploads/2025/12/Cabernet-07.jpg",
             "Modern hillside custom home facade representative of Palermo Homes Central Okanagan builds"),
            ("wilden", "Wilden",
             "BC's largest master-planned community. 1,447 acres, 30 neighbourhoods, 1,500+ acres of green space on the Glenmore Highlands. Hillside work transferable from West Kelowna's wine district.",
             "/wp-content/uploads/2025/12/1587-Malbec-14.jpg",
             "Modern lakeview custom home representative of Palermo Homes builds, closest match for Wilden hillside lots"),
            ("mckinley-beach", "McKinley Beach",
             "Kelowna's only lakefront master-planned community. 872 acres, 1 km of Okanagan Lake beachfront, 110-slip marina, working winery. Lakefront experience transferable from West Kelowna.",
             "/wp-content/uploads/2025/12/Touriga-109.jpg",
             "Modern lakeview custom home representative of Palermo Homes lakefront portfolio, closest match for McKinley Beach"),
        ],
        "overview": [
            "Palermo Homes serves Kelowna clients from our West Kelowna base, 10 minutes across the W.R. Bennett Bridge. Our completed custom homes are concentrated in West Kelowna's wine district (Cabernet Way, Malbec Place, Touriga Place, Vineyard Estates), with additional builds in Lake Country. Most of our Kelowna-side clients choose a West Kelowna or Lake Country lot for the view, the price per acre, and the lot sizes.",
            "Kelowna's hillside neighbourhoods (Upper Mission, Kettle Valley, Wilden, McKinley Beach) and valley-floor areas (Glenmore, Lower Mission) each build differently. We know the City of Kelowna permit process, the geotech reports for the south hillside, the view-corridor rules in Upper Mission, and the drainage work hillside lots demand. If you have a Kelowna-proper lot, we'd walk it with you to talk feasibility before design starts.",
        ],
        "why_h": "Why Kelowna clients hire Palermo.",
        "why_items": [
            ("Central Okanagan portfolio depth", "Fifteen-plus years building custom homes in the Central Okanagan with concentrated portfolio in West Kelowna's wine district and Lake Country. Transferable experience for any Kelowna lot."),
            ("City of Kelowna permit familiarity", "We know the City of Kelowna permit process, geotech requirements for Upper Mission and Wilden hillside lots, and the view-corridor rules that affect design on the south hillside."),
            ("Lakeview and hillside expertise", "Steep lots, view corridors, retaining walls, drainage, and slope stability. The hillside work in Upper Mission and Kettle Valley is the same engineering we do daily in West Kelowna."),
            ("In-house project management", "One contract, one point of contact. Weekly photo updates and honest schedule check-ins. Nothing for you to coordinate."),
            ("Central Okanagan trades on speed dial", "The same electricians, plumbers, framers, and finishers on every project. Consistent quality across both sides of the bridge."),
            ("Lot walk before you buy", "We walk any Kelowna lot with you to flag geotech, slope, servicing, or view-corridor issues before purchase. No cost, no obligation."),
        ],
        "split_photo": "/wp-content/uploads/2025/12/Cabernet-25.jpg",
        "split_photo_alt": "Lakeview custom home interior representative of Palermo Homes builds across the Central Okanagan",
        "split_photo_loc": "Central Okanagan",
        "feat_h": "What a Palermo home for a Kelowna client looks like.",
        "feat_body": "Our closest completed portfolio project to Kelowna is this modern lakeview custom home on Cabernet Way in West Kelowna, 10 minutes across the W.R. Bennett Bridge from downtown Kelowna. The lakeview siting, custom cabinetry, in-house finish carpentry, and detail execution are directly transferable to an Upper Mission, Kettle Valley, or Wilden lot. If you have a Kelowna-proper lot, you'd get first-build pricing, extra on-site attention, and the same in-house team on every stage.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "feat_photo_alt": "Lakeview custom home on Cabernet Way, West Kelowna by Palermo Homes, representative of Kelowna-area builds",
        "feat_link": "/contact/",
        "feat_link_label": "Book a Kelowna lot walk",
        "feat_card_loc": "Kelowna, BC",
        "feat_card_title": "Free Kelowna Lot Walk + Feasibility Snapshot",
        "faqs": [
            ("Have you built in Kelowna proper?",
             "Our completed custom homes are concentrated in West Kelowna (Cabernet Way, Malbec Place, Touriga Place, Vineyard Estates) and Lake Country. Most of our Kelowna-side clients choose a West Kelowna lot for the view and the price per acre. If you have a Kelowna-proper lot (Upper Mission, Kettle Valley, Glenmore, Wilden), you would get first-build pricing and extra on-site attention from the full in-house team."),
            ("How much does a custom home cost in Kelowna?",
             "Most Palermo custom builds in the Central Okanagan fall between $600 and $1,500+ per square foot depending on lot, size, finish level, and complexity. Lakeview and hillside lots in Upper Mission or Kettle Valley typically sit at the upper end because of the site work involved. We provide transparent line-item pricing from day one."),
            ("How long does a Kelowna custom build take?",
             "A typical Kelowna custom home takes 12 to 18 months from the first design meeting to final walk-through. That is 2 to 4 months for design, 2 to 3 months for City of Kelowna permits and geotech (longer for hillside), and 8 to 12 months for construction. You get weekly photo updates and we flag schedule issues early."),
            ("What's the City of Kelowna permit process like?",
             "City of Kelowna permits typically run 8 to 12 weeks for a straightforward lot, longer for hillside geotech review in Upper Mission, Kettle Valley, Wilden, or McKinley Beach. We prep complete packages up front so applications move cleanly through plan check and inspection."),
            ("Can you help me find a lot in Kelowna?",
             "We work with several Central Okanagan Realtors and can walk Kelowna lots with you before purchase. Understanding buildability up front (geotech, slope, servicing, view corridors, setbacks) saves you from paying for a lot that costs twice as much to build on as the one across the street."),
            ("Do you build on hillside lots in Upper Mission or Kettle Valley?",
             "Yes. Hillside engineering is our daily work in West Kelowna's wine district. Retaining walls, foundation design, drainage, and view optimization on steep lots is the same regardless of which side of the bridge the lot is on."),
            ("Can I get a free Kelowna lot walk?",
             "Yes. We'll walk the lot with you, flag geotech, slope, servicing, view-corridor, or City of Kelowna permit issues, and give you a feasibility snapshot before you commit. No cost."),
            ("Do you handle renovations in Kelowna?",
             "Yes. Whole-home renovations, additions, kitchens, and bathrooms across Kelowna and the Central Okanagan. Same finish standards as our custom builds and the same in-house trades."),
        ],
    },

    "west-kelowna": {
        "name": "West Kelowna",
        "region": "BC",
        "lat": "49.8628",
        "lon": "-119.5836",
        "h1": "Custom Home Builder in West Kelowna, BC.",
        "sub": "Lakeview homes in the wine district. Cabernet Way, Malbec Place, Touriga Place, Vineyard Estates. And across West Kelowna's most desirable hillside neighbourhoods.",
        "hero": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "hero_alt": "Modern custom home on Cabernet Way in West Kelowna by Palermo Homes",
        "meta_title": "Custom Home Builder West Kelowna, BC | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom lakeview homes across West Kelowna's wine district: Cabernet Way, Malbec Place, Touriga Place, Vineyard Estates.",
        "eyebrow": "Service Area · Wine District",
        "neighborhoods": [
            "Cabernet Way", "Malbec Place", "Touriga Place", "Vineyard Estates",
            "Lakeview Heights", "Rose Valley", "West Kelowna Estates",
            "Smith Creek", "Shannon Lake", "West Harbour", "Tallus Ridge", "Casa Loma",
        ],
        "neighborhood_pages": [
            ("lakeview-heights", "Lakeview Heights",
             "West Kelowna's historic wine-country neighbourhood on the west shore of Okanagan Lake. Home to Mission Hill Family Estate, Quails Gate, and Volcanic Hills.",
             "/wp-content/uploads/2025/12/Cabernet-07.jpg",
             "Modern hillside custom home on Cabernet Way in Lakeview Heights, West Kelowna"),
        ],
        "overview": [
            "West Kelowna is our most active build market. We have completed custom lakeview homes on Cabernet Way, Malbec Place, Touriga Place, and Vineyard Estates. The wine district streets that define custom home building in the Okanagan.",
            "The wine district is not a subdivision you drop a spec home into. Custom-only streets, unforgiving lots, and neighbouring homes that set the finish-quality bar. Steel moment frames, custom cabinetry, in-house finish carpentry, geotechnical retaining, and high-performance envelopes on every build.",
        ],
        "why_h": "Why West Kelowna clients hire Palermo.",
        "why_items": [
            ("The wine district specialist", "Multiple completed custom builds on Cabernet Way, Malbec Place, Touriga Place, and Vineyard Estates. We know every lot line on those streets."),
            ("Hillside and lakeview engineering", "Structural, drainage, retaining, and geotech expertise for the steep West Kelowna lots that other builders shy away from."),
            ("District of West Kelowna permit fluency", "We know the DWK permit rhythm, the geotech reports the district wants to see, and the inspectors."),
            ("View-first orientation", "Every home we design in the wine district is oriented for the view corridor first, then optimized for light, privacy, and prevailing wind."),
            ("15+ years of custom homes", "Portfolio depth means proven trade relationships and predictable pricing on the finish details that make a West Kelowna custom home."),
        ],
        "split_photo": "/wp-content/uploads/2025/12/Touriga-109.jpg",
        "split_photo_alt": "Modern lakeview custom home on Touriga Place, West Kelowna by Palermo Homes",
        "split_photo_loc": "Touriga Place · West Kelowna",
        "feat_h": "Featured West Kelowna build.",
        "feat_body": "A modern lakeview custom home on Malbec Place. One of West Kelowna's most sought-after cul-de-sacs in the wine district. Full lakeview siting on Okanagan Lake, custom stone-and-timber exterior, in-house finish carpentry throughout, and the kind of details that make a Malbec Place home hold its value long after the market moves.",
        "feat_photo": "/wp-content/uploads/2025/12/1587-Malbec-14.jpg",
        "feat_photo_alt": "Featured modern lakeview custom home on Malbec Place, West Kelowna by Palermo Homes",
        "feat_link": "/project/malbec-place-1/",
        "feat_link_label": "View this Malbec Place home",
        "feat_card_loc": "West Kelowna, BC",
        "feat_card_title": "Modern Lakeview Home on Malbec Place",
        "faqs": [
            ("Do you build in the West Kelowna wine district?",
             "Yes. It's our most active market. We've completed multiple custom homes on Cabernet Way, Malbec Place, Touriga Place, and Vineyard Estates. If you're buying a lot on one of those streets, we've almost certainly built a house next to it."),
            ("How much does a lakeview custom home cost in West Kelowna?",
             "West Kelowna lakeview builds in the wine district typically start around $2M and scale up substantially based on square footage, site work, and specification level. Cabernet Way and Touriga Place lots often carry meaningful geotech and retaining costs that a flatter lot wouldn't."),
            ("Can you help me evaluate a West Kelowna lot before I buy?",
             "Yes. We regularly walk lots with buyers before purchase. Especially in the wine district and Rose Valley. We'll give you an honest read on buildability, geotech, view corridors, and setback constraints. Best hour you can spend before you write an offer."),
            ("How long does a West Kelowna custom home take?",
             "Typically 12 to 18 months from design kickoff to hand-over. Wine district hillside lots often add 1 or 2 months on the front end for geotech and District of West Kelowna permitting because of the slope."),
            ("Do you handle the retaining and site work in-house?",
             "We manage all of it. Structural engineering, geotech coordination, retaining, drainage, and servicing are all handled by our project management team with the same trades we've used for years. One contract, one point of accountability."),
        ],
    },

    "lake-country": {
        "name": "Lake Country",
        "region": "BC",
        "lat": "50.0603",
        "lon": "-119.4130",
        "h1": "Custom Home Builder in Lake Country, BC.",
        "sub": "Custom homes across Lake Country's lakefront and orchard-view neighbourhoods. From Lakestone and Ledgestone Road to Oyama and Carr's Landing.",
        "hero": "/wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg",
        "hero_alt": "Modern custom home on Cabernet Way by Palermo Homes, representative of Lake Country lakeview builds",
        "meta_title": "Custom Home Builder Lake Country, BC | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes across Lake Country, BC, including Lakestone, Ledgestone Road, Oyama, and Carr's Landing.",
        "eyebrow": "Service Area · North Okanagan",
        "neighborhoods": [
            "Lakestone", "Ledgestone Road", "The Highlands", "Carr's Landing",
            "Coral Beach", "Pixton Road", "Oyama", "Okanagan Centre",
            "The Lakes", "Copper Hill", "Winfield",
        ],
        "neighborhood_pages": [
            ("lakestone", "Lakestone",
             "Macdonald Development's master-planned community above Okanagan Lake. Lake Club, marina, Scenic Sip wineries.",
             "/wp-content/uploads/2026/09/lakestone-lot-view.jpg",
             "Lakestone community view over Okanagan Lake, Lake Country BC"),
        ],
        "overview": [
            "Lake Country sits at the top of the Central Okanagan. Palermo Homes builds custom lakefront and lakeview homes across Lake Country, from Lakestone and The Lakes to Ledgestone Road, Carr's Landing, and the orchard-view lots in Oyama and Winfield.",
            "Servicing on rural and orchard-adjacent lots takes more coordination, and the District of Lake Country permit process has its own rhythm. Lakefront lots on Okanagan Lake, Wood Lake, and Kalamalka Lake each carry their own foreshore, riparian, and setback rules. Fifteen-plus years across the Central and North Okanagan means we know what to plan for.",
        ],
        "why_h": "Why Lake Country clients hire Palermo.",
        "why_items": [
            ("Lakestone and Ledgestone Road experience", "Completed custom builds inside Lakestone and on Ledgestone Road. We know the community design guidelines and the local geotech."),
            ("Lakefront and foreshore expertise", "Riparian setbacks, foreshore leases, dock coordination. We've worked through them all on Okanagan, Wood, and Kalamalka Lakes."),
            ("District of Lake Country permitting", "Fluent in the DLC permit process and the servicing coordination that Lake Country's rural lots often require."),
            ("Orchard and view-lot design", "Homes oriented for the specific view and light conditions of Lake Country's orchard, hillside, and lakefront lots."),
            ("One-team accountability", "In-house project management, in-house finish carpentry, and consistent trade relationships across every Lake Country build."),
        ],
        "split_photo": "/wp-content/uploads/2022/04/PAL_220411_Row1.jpg",
        "split_photo_alt": "Lake Country custom home interior by Palermo Homes",
        "split_photo_loc": "Ledgestone Road · Lake Country",
        "feat_h": "Featured Lake Country build.",
        "feat_body": "Our Ledgestone Road custom home in Lake Country. A modern hillside build oriented for Okanagan Lake views and Lake Country's evening light. Custom stone-and-cedar exterior, in-house finish carpentry, and the kind of siting decisions you can only make when you understand how the lot actually behaves through all four seasons.",
        "feat_photo": "/wp-content/uploads/2022/04/PAL_220411_Main2.jpg",
        "feat_photo_alt": "Featured Ledgestone Road custom home in Lake Country by Palermo Homes",
        "feat_link": "/project/lakestone/",
        "feat_link_label": "View this Ledgestone Road home",
        "feat_card_loc": "Lake Country, BC",
        "feat_card_title": "Modern Home on Ledgestone Road",
        "faqs": [
            ("Do you build in Lakestone?",
             "Yes. Palermo Homes has completed custom builds inside Lakestone and on Ledgestone Road. We're familiar with the community design guidelines, the local geotech, and the way Lakestone lots want to be sited."),
            ("How much does a custom home cost in Lake Country?",
             "Most Lake Country custom builds fall in the same $600 to $1,500+ per square foot range as Central Okanagan projects, with lakefront and hillside lots at the upper end. Rural and orchard-adjacent lots sometimes need extra servicing coordination that we budget for on day one."),
            ("Can you build on a lakefront lot in Lake Country?",
             "Yes. Palermo has completed lakefront and lakeview custom homes across Lake Country. Foreshore, riparian setbacks, dock coordination, and geotech on lakefront lots all have their own rhythm, and we've navigated them before."),
            ("How long does it take to build in Lake Country?",
             "A typical Lake Country custom build runs 12 to 18 months from the first design meeting to hand-over. Some rural and lakefront lots add a month or two on the front end for servicing coordination and District of Lake Country permitting."),
            ("Do you handle orchard-lot custom builds?",
             "Yes. Oyama, Carr's Landing, and Winfield orchard-view lots each have their own siting and servicing considerations. We plan for them up front so nothing becomes a surprise at ground-break."),
        ],
    },

    "peachland": {
        "name": "Peachland",
        "region": "BC",
        "lat": "49.7770",
        "lon": "-119.7371",
        "h1": "Custom Home Builder in Peachland, BC.",
        "sub": "Lakefront and hillside custom homes across Peachland. From Ponderosa and Somerset Reach to Beach Avenue and the upper Peachland benches.",
        "hero": "/wp-content/uploads/2025/12/1587-Malbec-14.jpg",
        "hero_alt": "Lakeview custom home representative of Palermo Homes builds in Peachland and the Central Okanagan",
        "meta_title": "Custom Home Builder Peachland, BC | Palermo Homes",
        "meta_desc": "Palermo Homes is a custom home builder serving Peachland, BC. Lakefront, hillside, and bench-lot custom homes with 15+ years of Central Okanagan experience.",
        "eyebrow": "Service Area · Central Okanagan",
        "neighborhoods": [
            "Ponderosa", "Beach Avenue", "Somerset Reach", "Trepanier",
            "Upper Princeton", "Renfrew Road", "Lipsett Avenue", "Buchanan Road",
            "Pincushion", "Hardy Falls", "MacKinnon Road",
        ],
        "overview": [
            "Peachland is a small lakefront town on the west shore of Okanagan Lake, 20 minutes south of West Kelowna. Palermo Homes builds custom homes across Peachland, from Ponderosa and Hardy Falls to the Trepanier and Upper Princeton benches, plus lakefront on Beach Avenue and Somerset Reach.",
            "The upper benches climb quickly from the lake, so drainage, retaining, and foundation engineering carry real weight on most lots. Several upper-bench areas sit near the Agricultural Land Reserve boundary. Beach Avenue lakefront carries foreshore setbacks and view-corridor rules. The District of Peachland OCP governs lot coverage, height, and tree retention. We work through all of it up front so there are no surprises at permit stage.",
        ],
        "why_h": "Why Peachland clients hire Palermo.",
        "why_items": [
            ("Steep-lot and hillside expertise", "Peachland's upper benches are unforgiving. Our structural, drainage, and retaining experience across the Central Okanagan translates directly to Ponderosa, Trepanier, and the Upper Princeton benches."),
            ("Lakefront and foreshore knowledge", "Beach Avenue and Somerset Reach lakefront lots demand foreshore setback, riparian zone, and view-corridor fluency. We've done the engineering coordination on comparable Okanagan Lake projects."),
            ("District of Peachland permit familiarity", "Small-town permit offices have their own rhythm. We know the DoP OCP rules on lot coverage, height, and tree retention, and we know the local inspectors."),
            ("ALR and zoning awareness", "Several upper-bench areas sit near the Agricultural Land Reserve boundary. We flag that up front so you know what's buildable before you buy."),
            ("View-first design orientation", "Every Peachland custom home is oriented around the specific lake view, sunset angle over Squally Point, and lot-specific setback constraints."),
            ("One team, one contract", "In-house project management, in-house finish carpentry, and consistent trade relationships across every Peachland build. No subcontract chain to navigate."),
        ],
        "split_photo": "/wp-content/uploads/2025/12/Cabernet-21.jpg",
        "split_photo_alt": "Lakeview custom home interior representative of Palermo Homes builds in the Central Okanagan",
        "split_photo_loc": "Central Okanagan",
        "feat_h": "What a Palermo home in Peachland looks like.",
        "feat_body": "We're honest about this. Our completed-portfolio projects closest to Peachland are our lakeview and hillside custom homes across West Kelowna's wine district (Cabernet Way, Malbec Place, Touriga Place, Vineyard Estates) and Lake Country's Ledgestone Road, 20 to 40 minutes north. The hillside engineering, view-first orientation, retaining and drainage work, and finish quality are all directly transferable to Ponderosa, Trepanier, or Beach Avenue. If you're planning the first Palermo build in Peachland, you get first-build pricing, extra on-site attention, and the full in-house team on every stage.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "feat_photo_alt": "Lakeview custom home by Palermo Homes, representative of Peachland builds",
        "feat_link": "/contact/",
        "feat_link_label": "Book a Peachland lot walk",
        "feat_card_loc": "Peachland, BC",
        "feat_card_title": "Free Peachland Lot Walk + Feasibility Snapshot",
        "faqs": [
            ("Do you build in Peachland?",
             "Yes. Palermo Homes serves Peachland as part of our Central Okanagan service area. We've built extensively on comparable West Kelowna and Lake Country hillside and lakeview lots and bring the same construction standards and in-house trades to every Peachland project."),
            ("How much does a Peachland custom home cost?",
             "Peachland custom homes typically run $600 to $1,500+ per square foot depending on lot, size, finish, and complexity. Hillside benches and Beach Avenue lakefront lots tend to carry additional geotech, retaining, and site-work costs that we budget for up front rather than letting them show up as change orders."),
            ("Can you build on a Peachland lakefront lot?",
             "Yes. Beach Avenue and Somerset Reach lakefront lots have foreshore setback, riparian zone, and dock considerations that we've navigated on comparable Okanagan Lake projects. We handle the permit and engineering coordination in-house."),
            ("How long does a Peachland custom build take?",
             "A typical Peachland custom home runs 12 to 18 months from the first design meeting to hand-over. Steep hillside lots on the upper benches and lakefront lots sometimes add a month or two of front-end engineering."),
            ("What are the ALR rules on Peachland upper-bench lots?",
             "Several upper-bench areas sit at or near the Agricultural Land Reserve boundary. ALR-designated lots have strict limits on dwelling size, outbuildings, and subdivision. We check ALR status as part of a lot walk before you commit to a purchase."),
            ("Does the District of Peachland OCP affect what I can build?",
             "Yes. Peachland's OCP sets lot coverage, maximum height, tree retention, and setback rules by zoning area. Most hillside residential lots cap building height to protect downslope views. We confirm what's allowed on your specific lot before design starts."),
            ("How does the Highway 97 corridor affect upper-bench lots?",
             "Upper-bench lots facing east toward Highway 97 can carry road noise. We mitigate with window specification, exterior wall assemblies, and site orientation. On exposed lots we often design primary bedrooms and quiet-living spaces away from the corridor side."),
            ("Can I get a free lot walk before I buy a Peachland lot?",
             "Yes. We'll walk the lot with you, flag ALR, slope, foreshore, servicing, or view-corridor issues, and give you a feasibility snapshot before you commit. No cost and no obligation."),
            ("Do you also renovate in Peachland?",
             "Yes. Whole-home renovations, additions, kitchens, and bathrooms across Peachland and the Central Okanagan. Same finish standards as our custom builds and the same in-house trades."),
        ],
    },

    "vernon": {
        "name": "Vernon",
        "region": "BC",
        "lat": "50.2670",
        "lon": "-119.2721",
        "h1": "Custom Home Builder in Vernon, BC.",
        "sub": "Custom homes across Vernon and the North Okanagan. From The Rise and Predator Ridge to Middleton Mountain, East Hill, and Okanagan Landing.",
        "hero": "/wp-content/uploads/2025/12/homepage3.jpg",
        "hero_alt": "Modern custom home representative of Palermo Homes builds in Vernon and the North Okanagan",
        "meta_title": "Custom Home Builder Vernon, BC | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes across Vernon, BC and the North Okanagan. The Rise, Predator Ridge, Middleton Mountain, Okanagan Landing, Coldstream.",
        "eyebrow": "Service Area · North Okanagan",
        "neighborhoods": [
            "Predator Ridge", "The Rise", "Adventure Bay", "Okanagan Landing",
            "Middleton Mountain", "Coldstream", "Foothills", "Turtle Mountain",
            "Silver Star Foothills", "East Hill", "Bella Vista", "BX",
        ],
        "neighborhood_pages": [
            ("predator-ridge", "Predator Ridge",
             "Vernon's #1 luxury destination. 22 neighbourhoods, 36 holes of championship golf, and the first Ritz-Carlton Residences in Western Canada.",
             "/wp-content/uploads/2025/12/Touriga-109.jpg",
             "Modern lakeview custom home at dusk, Palermo Homes portfolio"),
            ("adventure-bay", "Adventure Bay",
             "Vernon's hillside community on the northern peninsula of Okanagan Lake. Panoramic mountain and lake views, 12 km from downtown Vernon.",
             "/wp-content/uploads/2025/12/Cabernet-07.jpg",
             "Custom home portfolio example for Adventure Bay, Vernon BC by Palermo Homes"),
            ("the-rise", "The Rise",
             "Vernon's hillside golf-course community by Okanagan Hills Development Corp. Anchored by an 18-hole Fred Couples signature course.",
             "/wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg",
             "Custom home at The Rise, Vernon BC portfolio example by Palermo Homes"),
        ],
        "overview": [
            "Vernon sits at the top of the Okanagan Valley, 45 minutes north of Kelowna, defined by three lakes (Okanagan, Kalamalka, Swan), Silver Star ski terrain, and the province's most sought-after golf communities. Palermo Homes builds custom homes across Vernon, from The Rise and Middleton Mountain to Predator Ridge, Adventure Bay, East Hill, and lakefront on Okanagan Landing and Kalamalka Lake.",
            "The North Okanagan builds differently than Kelowna. The 2.4 kPa ground snow load zone (vs 1.6 kPa in Central Okanagan) drives roof framing and truss design. Triple-pane glazing and tighter envelope detailing stop being optional on east-facing BX, Silver Star Foothills, or Turtle Mountain lots. Predator Ridge and The Rise both run formal Design Review Committees. Kalamalka Lake carries provincial protected-area setbacks. The City of Vernon and District of Coldstream split also catches builders who've only worked in Kelowna. We've worked through all of it.",
        ],
        "why_h": "Why Vernon clients hire Palermo.",
        "why_items": [
            ("North Okanagan climate design", "Vernon's 2.4 kPa snow-load zone and winter exposure demand real envelope performance. Triple-pane windows, upgraded roof framing, and thermal detailing designed for the North Okanagan, not transplanted from Kelowna specs."),
            ("Predator Ridge and The Rise DRC fluency", "Both communities run formal Design Review Committees with specific exterior, material, and site rules. We've prepared packages that get through DRC without the rework cycles that eat months."),
            ("Jurisdiction split awareness", "City of Vernon, District of Coldstream, and Regional District of North Okanagan each handle permits differently. We know which rules apply on your lot before design starts."),
            ("Hillside and lakefront expertise", "Middleton Mountain, Turtle Mountain, Silver Star Foothills hillside lots. Okanagan Landing and Kalamalka Lake foreshore builds. The geotech, retaining, and setback coordination is handled in-house."),
            ("Protected-area Kalamalka Lake setbacks", "Kalamalka Lake Protected Area regulations limit shoreline construction more than Okanagan Lake. We handle the provincial coordination so you don't get stuck mid-permit."),
            ("One-team accountability", "In-house project management, weekly progress reporting, in-house finish carpentry, and consistent trade relationships on every Vernon build."),
        ],
        "split_photo": "/wp-content/uploads/2025/12/Cabernet-25.jpg",
        "split_photo_alt": "Custom home interior representative of Palermo Homes builds in Vernon and the North Okanagan",
        "split_photo_loc": "North Okanagan",
        "feat_h": "What a Palermo home in Vernon looks like.",
        "feat_body": "We're honest about this. Our closest completed portfolio project to Vernon is our modern lakeview custom home on Cabernet Way in West Kelowna, about 45 minutes south. The lakeview siting, in-house finish carpentry, custom cabinetry, and detail execution are directly transferable to an Okanagan Landing lakefront, a Predator Ridge DRC build, or a Middleton Mountain hillside. For your Vernon build we'd add the climate-specific detailing (triple-pane, upgraded snow-load framing, thermal envelope) that the North Okanagan actually needs. First Palermo build in Vernon? You get first-build pricing and extra on-site attention.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "feat_photo_alt": "Lakeview custom home by Palermo Homes, closest portfolio match for Vernon builds",
        "feat_link": "/contact/",
        "feat_link_label": "Book a Vernon lot walk",
        "feat_card_loc": "Vernon, BC",
        "feat_card_title": "Free Vernon Lot Walk + Feasibility Snapshot",
        "faqs": [
            ("Do you build in Vernon?",
             "Yes. Palermo Homes serves Vernon and the North Okanagan as part of our Okanagan Valley service area, drawing on 15+ years of experience across comparable hillside, golf-course, and lakefront lots in the Central Okanagan."),
            ("Do you build at Predator Ridge or The Rise?",
             "Yes. Both communities have formal Design Review Committees with specific guidelines on exterior materials, roof pitch, massing, and site integration. We prepare DRC packages up front so approvals move cleanly."),
            ("What is the Vernon snow load, and does it affect my build?",
             "Vernon sits in a roughly 2.4 kPa ground snow load zone, compared to about 1.6 kPa in the Central Okanagan. That means heavier roof framing, upgraded truss design, and site drainage planning for snow melt. We spec for it so your roof and envelope hold up."),
            ("Are triple-pane windows worth it in Vernon?",
             "On most Vernon lots, yes. Winter exposure on East Hill, Silver Star Foothills, Turtle Mountain, and BX makes triple-pane a meaningful comfort and heating-cost upgrade. On sheltered south-facing lots it's less critical. We make the call lot by lot."),
            ("How much does a Vernon custom home cost?",
             "Vernon custom homes typically run $600 to $1,500+ per square foot depending on lot, size, finish, and complexity. Hillside lots at The Rise, Middleton Mountain, or Turtle Mountain carry additional geotech and retaining costs. Predator Ridge builds often sit higher per square foot due to community design standards."),
            ("How long does a Vernon custom build take?",
             "A typical Vernon custom home runs 12 to 18 months from the first design meeting to hand-over. Predator Ridge and The Rise can add one to three months for community DRC review. We plan for it on the schedule up front."),
            ("What are the Kalamalka Lake setback rules?",
             "Kalamalka Lake is a Provincial Protected Area with tighter foreshore and setback regulations than Okanagan Lake. New lakefront builds need provincial coordination on shoreline work. We handle it as part of permit preparation."),
            ("What's the difference between City of Vernon and Coldstream permits?",
             "City of Vernon and District of Coldstream each run their own permit offices with different fees, inspection schedules, and OCP rules. Lots split between the two jurisdictions have additional coordination. We know which office handles your lot before design starts."),
            ("Can I get a free lot walk before I buy in Vernon?",
             "Yes. We'll walk the lot with you, flag snow-load, slope, protected-area, DRC, or jurisdiction issues, and give you a feasibility snapshot before you commit. No cost."),
            ("Do you also renovate in Vernon?",
             "Yes. Whole-home renovations, additions, kitchens, and bathrooms across Vernon and the North Okanagan. Same finish standards as our custom builds."),
        ],
    },

    "penticton": {
        "name": "Penticton",
        "region": "BC",
        "lat": "49.4991",
        "lon": "-119.5937",
        "h1": "Custom Home Builder in Penticton, BC.",
        "sub": "Custom homes across Penticton and the South Okanagan. From the Naramata Bench to Skaha Lake, Uplands, and Wiltse.",
        "hero": "/wp-content/uploads/2025/12/Touriga-109.jpg",
        "hero_alt": "Custom lakeview home on Touriga Place by Palermo Homes, representative of Penticton South Okanagan builds",
        "meta_title": "Custom Home Builder Penticton, BC | Palermo Homes",
        "meta_desc": "Palermo Homes builds custom homes across Penticton and the South Okanagan. Naramata Bench, Skaha Lake, Uplands, Wiltse. 15+ years of Okanagan experience.",
        "eyebrow": "Service Area · South Okanagan",
        "neighborhoods": [
            "Naramata Bench", "Skaha Hills", "Sendero Canyon", "Wiltse",
            "Uplands", "West Bench", "Skaha Lake", "Columbia",
            "Middle Bench Road", "Naramata Village", "Kaleden", "Okanagan Falls",
        ],
        "neighborhood_pages": [
            ("naramata-bench", "Naramata Bench",
             "The east-shore wine country appellation above Okanagan Lake. Over 40 wineries, Kettle Valley Rail Trail, 15 minutes from Penticton.",
             "/wp-content/uploads/2025/12/Cabernet-07.jpg",
             "Custom home on the Naramata Bench, Penticton BC by Palermo Homes"),
            ("skaha-hills", "Skaha Hills",
             "Greyback Construction's $250M master-planned community. 600 homes on 550 acres above Skaha Lake with vineyard, pool, and clubhouse.",
             "/wp-content/uploads/2025/12/1587-Malbec-14.jpg",
             "Modern lakeview custom home portfolio example for Skaha Hills, Palermo Homes"),
        ],
        "overview": [
            "Penticton sits between Okanagan Lake and Skaha Lake, 50 minutes south of Kelowna, with the Naramata Bench climbing east into Canada's most celebrated wine country. Palermo Homes builds custom homes across Penticton and the South Okanagan, from Naramata Bench and Skaha Hills to Skaha Lake waterfront, Uplands, Wiltse, Kaleden, and Okanagan Falls.",
            "The South Okanagan builds differently than Kelowna. Summer sun on south and west elevations drives overhang design, exterior shading, and low-U-value glass selection. Most of Naramata Bench sits inside the Agricultural Land Reserve with vineyard-overlay zoning that limits dwelling size and outbuildings. The Regional District of Okanagan-Similkameen handles permits for Naramata, Kaleden, and Okanagan Falls; the City of Penticton handles everything inside the municipal boundary. Skaha Hills is a planned community with its own HOA guidelines. We work through all of it up front.",
        ],
        "why_h": "Why Penticton clients hire Palermo.",
        "why_items": [
            ("Naramata Bench ALR and zoning fluency", "Most of the Bench sits inside the Agricultural Land Reserve with vineyard-overlay zoning that constrains dwelling size, outbuildings, and subdivision. We check lot status before you commit."),
            ("South Okanagan passive cooling", "South Okanagan sun demands real overhang design, exterior shading, and glazing selection on west and south elevations. We plan the envelope around comfort, not just code minimum."),
            ("RDOS and City of Penticton permit split", "Naramata, Kaleden, and Okanagan Falls fall under the Regional District of Okanagan-Similkameen. Inside Penticton it's municipal. We know which office handles your lot."),
            ("Skaha Hills HOA guidelines", "Skaha Hills is a planned community with specific HOA rules on exteriors, massing, and site integration. We prep packages that get through HOA review cleanly."),
            ("Skaha and Okanagan Lake foreshore", "Waterfront lots on both lakes have foreshore, setback, and dock rules. We've navigated them on comparable Central Okanagan projects."),
            ("Trade commute planning", "Most of our South Okanagan finish trades commute from the Central Okanagan. We build it into the schedule so site days are productive, not travel buffer."),
            ("One-team accountability", "In-house project management, weekly progress reporting, in-house finish carpentry, and consistent trade relationships on every Penticton build."),
        ],
        "split_photo": "/wp-content/uploads/2025/12/Touriga-12.jpg",
        "split_photo_alt": "Lakeview custom home interior representative of Palermo Homes builds in the South Okanagan",
        "split_photo_loc": "South Okanagan",
        "feat_h": "What a Palermo home in Penticton looks like.",
        "feat_body": "We're honest about this. Our closest completed portfolio project to Penticton is our modern lakeview custom home on Cabernet Way in West Kelowna's wine district, 50 minutes north. The vineyard-view siting, in-house finish carpentry, and detail execution are directly transferable to a Naramata Bench vineyard build, a Skaha Lake waterfront, or a Skaha Hills HOA lot. For your Penticton build we'd add the passive-cooling envelope work (overhangs, shading, west-elevation glazing) that the South Okanagan climate rewards. First Palermo build in Penticton? You get first-build pricing, extra on-site attention, and planned trade logistics from the start.",
        "feat_photo": "/wp-content/uploads/2025/12/Cabernet-02.jpg",
        "feat_photo_alt": "Lakeview custom home by Palermo Homes, closest portfolio match for Penticton builds",
        "feat_link": "/contact/",
        "feat_link_label": "Book a Penticton lot walk",
        "feat_card_loc": "Penticton, BC",
        "feat_card_title": "Free Penticton Lot Walk + Feasibility Snapshot",
        "faqs": [
            ("Do you build in Penticton?",
             "Yes. Palermo Homes serves Penticton and the South Okanagan as part of our Okanagan Valley service area, drawing on 15+ years of experience across comparable Central Okanagan hillside, lakefront, and vineyard-view builds."),
            ("Do you build on the Naramata Bench?",
             "Yes. Naramata Bench lots are steep, vineyard-adjacent, and view-driven. Most sit inside the Agricultural Land Reserve with vineyard-overlay zoning that affects dwelling size and outbuildings. We walk the lot with you before purchase to talk buildability."),
            ("What are the Naramata Bench ALR rules?",
             "Most Naramata Bench lots are inside the Agricultural Land Reserve. ALR rules cap primary dwelling floor area, limit outbuilding footprint, and restrict subdivision. Some lots also have vineyard-overlay zoning on top. We confirm what's buildable before design starts."),
            ("How does South Okanagan sun affect my build?",
             "Summer sun on south and west elevations in Penticton can drive serious heat gain on uncovered glass. We design overhangs, exterior shading, and specify low-U-value glass to control it. Passive cooling detail reduces air-conditioning load and improves comfort."),
            ("Who handles permits for Naramata, Kaleden, or Okanagan Falls?",
             "Those areas sit inside the Regional District of Okanagan-Similkameen (RDOS). Permit processes differ from City of Penticton. We know which office your lot falls under and prep accordingly."),
            ("What are the Skaha Hills HOA rules?",
             "Skaha Hills is a planned community with HOA guidelines on exterior finishes, roof pitch, massing, and site integration. We prep architectural packages that meet HOA review in the first round."),
            ("How much does a Penticton custom home cost?",
             "Penticton custom homes typically run $600 to $1,500+ per square foot depending on lot, size, and finish. Naramata Bench vineyard-view and Skaha Lake lakefront lots often carry additional geotech and site-work costs. Trade commute from the Central Okanagan can also factor in."),
            ("How long does a Penticton custom build take?",
             "A typical Penticton custom home runs 12 to 18 months from the first design meeting to hand-over. Naramata Bench and West Bench hillside lots can add one to two months of front-end engineering. ALR-affected lots sometimes add agricultural coordination time."),
            ("Can I get a free Penticton lot walk?",
             "Yes. We'll walk the lot with you, flag ALR, slope, south-sun exposure, HOA, foreshore, or permit-jurisdiction issues, and give you a feasibility snapshot before you commit. No cost."),
            ("Do you handle renovations in Penticton?",
             "Yes. Whole-home renovations, additions, kitchens, and bathrooms across Penticton and the South Okanagan. Same custom-home finish standards on every project."),
        ],
    },

    "lower-mainland": {
        "name": "Lower Mainland",
        "region": "BC",
        "lat": "49.0504",
        "lon": "-122.3045",
        "h1": "Custom Home Builder in the Lower Mainland.",
        "sub": "Select custom homes and renovations across Abbotsford, Chilliwack, and Langley. Including our Eagle Mountain, West Abbotsford, and Verado Court projects.",
        "hero": "/wp-content/uploads/2019/06/PAL_Projects_Mahogany2_FEATURE.jpg",
        "hero_alt": "Custom home in Eagle Mountain, Abbotsford by Palermo Homes",
        "meta_title": "Custom Home Builder Lower Mainland, BC | Palermo Homes",
        "meta_desc": "Palermo Homes takes on select custom home and renovation projects across the Lower Mainland, including Eagle Mountain and West Abbotsford.",
        "eyebrow": "Service Area · Fraser Valley",
        "neighborhoods": [
            "Eagle Mountain", "Auguston", "Ledgeview", "McKee Peak",
            "West Abbotsford", "Promontory", "Sardis", "Ryder Lake",
            "Fort Langley", "Salmon River Uplands", "Brookswood",
        ],
        "neighborhood_pages": [
            ("eagle-mountain", "Eagle Mountain",
             "Abbotsford's premier hillside community and Fraser Valley's biggest active build-out. Home to Vicarro Skyline's 1,400-unit development. 9+ Palermo builds completed.",
             "/wp-content/uploads/2019/06/PAL_Projects_Mahogany2_FEATURE.jpg",
             "Luxury Mountain View Home on Mahogany Drive, Eagle Mountain Abbotsford by Palermo Homes"),
        ],
        "overview": [
            "Palermo Homes was originally built on Lower Mainland custom homes. Our Eagle Mountain, West Abbotsford, and Verado Court projects in Abbotsford defined the company's early portfolio. Our primary market has shifted to Kelowna and the Okanagan, but we continue to take on select Lower Mainland projects for returning clients and referrals across Abbotsford, Chilliwack, and Langley.",
            "The Lower Mainland is a different construction environment than the Okanagan. Higher rainfall, denser lots, more restrictive setbacks, and different geotech. Fifteen-plus years in Abbotsford means we know the Aquila Drive terrain, the Eagle Mountain community design guidelines, and the Fraser Valley Regional District permit rhythm.",
        ],
        "why_h": "Why Lower Mainland clients hire Palermo.",
        "why_items": [
            ("Abbotsford portfolio depth", "Multiple completed Eagle Mountain and West Abbotsford custom homes. We know the neighbourhoods, the permit rhythm, and the trades."),
            ("Eagle Mountain community expertise", "Repeated Eagle Mountain builds mean familiarity with the community design guidelines, the terrain, and the Aquila Drive lot geometry."),
            ("Fraser Valley permit fluency", "City of Abbotsford, City of Chilliwack, and Township of Langley. We know the permit and inspection rhythm."),
            ("Selective engagement", "Because our primary market is now Kelowna and the Okanagan, we choose Lower Mainland projects carefully. That means real focus on every build we take on."),
            ("Same finish quality as our Okanagan builds", "One-team accountability, in-house finish carpentry, and consistent trade relationships on every Lower Mainland project."),
        ],
        "split_photo": "/wp-content/uploads/2025/12/Cabernet-25.jpg",
        "split_photo_alt": "Custom home interior by Palermo Homes",
        "split_photo_loc": "Fraser Valley",
        "feat_h": "Featured Lower Mainland build.",
        "feat_body": "Our Verado Court custom home in Eagle Mountain, Abbotsford. A signature Fraser Valley build. Custom stone-and-timber exterior, in-house finish carpentry, and the community design guideline compliance that Eagle Mountain requires from every build.",
        "feat_photo": "/wp-content/uploads/2019/06/PAL_Projects_Mahogany2_FEATURE.jpg",
        "feat_photo_alt": "Eagle Mountain Verado Court custom home by Palermo Homes in Abbotsford",
        "feat_link": "/project/verado-court/",
        "feat_link_label": "View this Verado Court home",
        "feat_card_loc": "Abbotsford, BC",
        "feat_card_title": "Custom Home on Verado Court, Eagle Mountain",
        "faqs": [
            ("Do you still build in the Lower Mainland?",
             "Yes. Selectively. Our primary market is now Kelowna and the Okanagan, but we continue to take on Lower Mainland custom homes and renovations for returning clients, referrals, and the right fit. Abbotsford, Chilliwack, and Langley are all in scope."),
            ("Which Lower Mainland neighborhoods have you built in?",
             "Eagle Mountain and West Abbotsford make up most of our Lower Mainland portfolio. The Eagle Mountain community especially, where we've completed multiple builds including our Verado Court project. Chilliwack and Langley are also in scope."),
            ("How much does a custom home cost in the Lower Mainland?",
             "Lower Mainland custom builds typically run $600 to $1,500+ per square foot depending on lot, size, and finish. Fraser Valley lot geometry and permit costs sometimes differ from Kelowna, which we account for in day-one budgeting."),
            ("How long does a Lower Mainland custom home take?",
             "Similar to our Okanagan builds. 12 to 18 months from the first design meeting to hand-over. Fraser Valley permit and geotech rhythms sometimes vary from Kelowna, which we plan for."),
            ("Do you take on Lower Mainland renovations?",
             "Yes. Whole-home renovations, additions, kitchens, and bathrooms across Abbotsford, Chilliwack, and Langley for returning and referred clients."),
        ],
    },
}


def render_city(slug, data):
    page_url = f"{BIZ_URL}/service-areas/{slug}/"
    canonical = page_url

    # neighborhoods as middot-separated inline list. Spaces around the separator give the browser break points so the line wraps naturally.
    hoods_list = ' <span class="sep">·</span> '.join([f'<span class="name">{h}</span>' for h in data["neighborhoods"]])

    # Featured neighborhood detail pages. Rendered only if data has entries.
    npages_section = ""
    if data.get("neighborhood_pages"):
        cards = "\n".join([
            f'''        <a class="card" href="/neighborhoods/{slug}/">
          <div class="photo"><img src="{photo}" alt="{alt}" loading="lazy"></div>
          <div class="meta">
            <div class="txt">
              <p class="loc">{data["name"]}, BC</p>
              <h3 class="name">{hname}</h3>
            </div>
            <div class="end">
              <span class="go">View</span>
              <span class="arr">→</span>
            </div>
          </div>
        </a>'''
            for slug, hname, teaser, photo, alt in data["neighborhood_pages"]
        ])
        npages_section = f'''
  <section class="svc-npages">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Featured community</p>
        <h2>Neighbourhoods in {data["name"]}.</h2>
      </div>
      <div class="grid">
{cards}
      </div>
    </div>
  </section>
'''

    # nearby cities. Every OTHER city, linked with anchor text. Editorial middot join.
    other_cities = [(s, CITIES[s]["name"]) for s in CITIES if s != slug]
    nearby_list = ' <span class="sep">·</span> '.join([f'<a href="/service-areas/{s}/">{n}</a>' for s, n in other_cities])

    # why items (split)
    why_lis = "\n".join([
        f'          <li><span class="num">{str(i+1).zfill(2)}</span><span class="txt"><strong>{t}</strong>{d}</span></li>'
        for i, (t, d) in enumerate(data["why_items"])
    ])

    # overview paragraphs
    over_ps = "\n        ".join([f'<p>{p}</p>' for p in data["overview"]])

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
            "Custom Home Construction",
            f"Custom Home Builder {data['name']}",
            f"Palermo Homes provides custom home design and construction across {data['name']}, {data['region']}.",
            page_url,
            data["name"],
            data["region"],
            lat, lon,
        ),
        place_schema(data["name"], data["region"]),
        faq_schema(data["faqs"]),
        breadcrumb_schema(page_url, data["name"]),
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
      <div class="fact"><p class="k">Service Area</p><p class="v">{data['name']}, BC</p></div>
      <div class="fact"><p class="k">Experience</p><p class="v">15+ Years Custom Homes</p></div>
      <div class="fact"><p class="k">Phone</p><p class="v"><a href="tel:+17787604113">(778) 760-4113</a></p></div>
      <div class="fact"><p class="k">Quote</p><p class="v"><a href="/contact/">Start a Conversation →</a></p></div>
    </div>
  </section>

  <section class="svc-over">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Overview</p>
        <h2>Custom home builder serving {data['name']} and the surrounding area.</h2>
      </div>
      <div class="body">
        {over_ps}
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

  <section class="svc-hoods">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Where we build in {data['name']}</p>
        <h2>Neighbourhoods and communities.</h2>
      </div>
      <p class="list">{hoods_list}</p>
    </div>
  </section>
{npages_section}
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
          <p>Custom home builds in {data['name']} and the surrounding area. Every project designed around how you actually live.</p>
          <span class="go">Custom Homes →</span>
        </a>
        <a class="card" href="/services/renovations/">
          <h3>Home Renovations</h3>
          <p>Whole-home renovations, kitchens, bathrooms, and additions across {data['name']}. Built to the same finish standard as our custom homes.</p>
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
      <p class="list">{nearby_list}</p>
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
        out_path=SITE / "service-areas" / slug / "index.html",
    )


def hub_page():
    page_url = f"{BIZ_URL}/service-areas/"
    canonical = page_url

    cards_html = ""
    for slug, data in CITIES.items():
        cards_html += (
            f'<a class="card" href="/service-areas/{slug}/">'
            f'<div class="imgwrap">'
            f'<img src="{data["hero"]}" alt="{data["hero_alt"]}" loading="lazy">'
            f'</div>'
            f'<div class="txt">'
            f'<span class="lab">{data["eyebrow"]}</span>'
            f'<h3><span><span class="pre">Custom Home Builder in </span>{data["name"]}, BC</span><span class="arr">&rarr;</span></h3>'
            f'</div>'
            f'</a>\n'
        )

    schema = full_schema(
        business_schema(),
        f'''{{
    "@type":"CollectionPage",
    "name":"Service Areas | Palermo Homes",
    "url":"{page_url}",
    "description":"Palermo Homes serves Kelowna, West Kelowna, Lake Country, Peachland, Vernon, Penticton, and the Lower Mainland."
  }}''',
        f'''{{
    "@type":"BreadcrumbList",
    "itemListElement":[
      {{"@type":"ListItem","position":1,"name":"Home","item":"{BIZ_URL}/"}},
      {{"@type":"ListItem","position":2,"name":"Service Areas","item":"{page_url}"}}
    ]
  }}''',
        f'''{{
    "@type":"FAQPage",
    "mainEntity":[
      {{"@type":"Question","name":"Which Okanagan city does Palermo Homes build in most often?","acceptedAnswer":{{"@type":"Answer","text":"Palermo Homes builds the majority of our custom homes in Kelowna and West Kelowna, with regular projects in Lake Country and Peachland. Kelowna, West Kelowna, Lake Country, and Peachland together form our primary Central Okanagan service area, where we complete most of our annual builds."}}}},
      {{"@type":"Question","name":"Does Palermo Homes build outside the Central Okanagan?","acceptedAnswer":{{"@type":"Answer","text":"Yes. Palermo Homes extends into the North Okanagan (Vernon), the South Okanagan (Penticton), and select Lower Mainland communities (Abbotsford, Chilliwack, Langley, Vancouver, West Vancouver). Projects outside the Central Okanagan are typically for returning clients, referred clients, or complex builds that fit our capability set."}}}},
      {{"@type":"Question","name":"Is Palermo Homes a BC Housing licensed custom home builder?","acceptedAnswer":{{"@type":"Answer","text":"Yes. Palermo Homes Ltd. is BC Housing Licensed Residential Builder number 42812, registered under BC Corporate Registration BC1017682. Every custom home we build is covered by the mandatory British Columbia 2-5-10 New Home Warranty program."}}}},
      {{"@type":"Question","name":"Can Palermo Homes build on hillside or lakefront lots?","acceptedAnswer":{{"@type":"Answer","text":"Yes. We have delivered custom homes on hillside benches in Upper Mission and Lakeview Heights, lakefront on Okanagan Lake, vineyard-view parcels on the Naramata Bench, and hillside lots on Eagle Mountain in Abbotsford. Hillside and lakefront builds carry their own geotechnical, drainage, and setback requirements, which we scope at the estimating stage."}}}},
      {{"@type":"Question","name":"What is the farthest Palermo Homes will travel for a custom build?","acceptedAnswer":{{"@type":"Answer","text":"Our primary custom home service area is the Okanagan Valley from Vernon in the north to Penticton in the south, with a secondary Lower Mainland service area covering Abbotsford through Vancouver. Beyond that geographic range, we take on projects selectively based on scope, timeline, and client fit."}}}}
    ]
  }}'''
    )

    main = f"""
<div class="svc">
  <section class="svc-hero">
    <div class="bg" style="background-image:url('/wp-content/uploads/2025/12/Cabernet-71.jpg')"></div>
    <div class="inner">
      <p class="eyebrow">Service Areas · Kelowna, BC</p>
      <h1>Custom home builder serving Kelowna, the Okanagan Valley, and the Lower Mainland.</h1>
      <p class="sub">Seven service areas. One team, one contract, one point of accountability from permits to hand-over.</p>
    </div>
  </section>

  <section class="svc-over">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Where we build</p>
        <h2>Rooted in Kelowna. Building across the Okanagan and beyond.</h2>
      </div>
      <div class="body">
        <p>Palermo Homes is a custom home builder headquartered in Kelowna, BC (BC Housing License 42812, BC Corporate Registration BC1017682). We build across the Central Okanagan including Kelowna, West Kelowna, Lake Country, and Peachland, plus Vernon, Penticton, and select Lower Mainland communities for returning clients.</p>
        <p>Fifteen-plus years in the Okanagan and Fraser Valley means we have navigated the permit rhythms, geotechnical conditions, and architectural design review boards in every city on this page, from Upper Mission hillsides and Wilden hilltop lots to Naramata Bench vineyard-view parcels and Eagle Mountain in Abbotsford.</p>
      </div>
    </div>
  </section>

  <section class="svc-cities">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Service Areas</p>
        <h2>Choose your city.</h2>
      </div>
      <div class="grid">
        {cards_html}
      </div>
    </div>
  </section>

  <section class="svc-tiles">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">Why clients across the Okanagan hire Palermo</p>
        <h2>One team. Seven cities. Fifteen years of local build knowledge.</h2>
      </div>
      <div class="cards">
        <div class="card">
          <h3>Hyperlocal permit fluency</h3>
          <p>Every municipality in our service area has its own permit process, review timelines, and inspectors. We know the City of Kelowna, City of West Kelowna, District of Lake Country, District of Peachland, Regional District of Central Okanagan, City of Vernon, City of Penticton, and the City of Abbotsford processes directly, so permits move without surprises.</p>
        </div>
        <div class="card">
          <h3>Hillside and lakefront experience</h3>
          <p>Most Central Okanagan custom builds involve hillside geotech, foreshore setbacks, or both. We have delivered custom homes on Upper Mission benches, Lakeview Heights slopes above Okanagan Lake, Naramata Bench vineyard terraces, and Lakestone lakefront lots. The structural, drainage, and siting playbooks are already built.</p>
        </div>
        <div class="card">
          <h3>One team from design to hand-over</h3>
          <p>Our owner, Jas Sidhu, is directly involved on every active build in every city we work in. Clients get one point of contact, one fixed-price contract, and one project team, whether the lot is in Kelowna, Vernon, or Abbotsford.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="svc-faq">
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">FAQ</p>
        <h2>Service area questions, answered.</h2>
      </div>
      <div class="items">
        <details><summary>Which Okanagan city does Palermo Homes build in most often?</summary><div class="ans">Palermo Homes builds the majority of our custom homes in Kelowna and West Kelowna, with regular projects in Lake Country and Peachland. Kelowna, West Kelowna, Lake Country, and Peachland together form our primary Central Okanagan service area, where we complete most of our annual builds.</div></details>
        <details><summary>Does Palermo Homes build outside the Central Okanagan?</summary><div class="ans">Yes. Palermo Homes extends into the North Okanagan (Vernon), the South Okanagan (Penticton), and select Lower Mainland communities (Abbotsford, Chilliwack, Langley, Vancouver, West Vancouver). Projects outside the Central Okanagan are typically for returning clients, referred clients, or complex builds that fit our capability set.</div></details>
        <details><summary>Is Palermo Homes a BC Housing licensed custom home builder?</summary><div class="ans">Yes. Palermo Homes Ltd. is BC Housing Licensed Residential Builder number 42812, registered under BC Corporate Registration BC1017682. Every custom home we build is covered by the mandatory British Columbia 2-5-10 New Home Warranty program.</div></details>
        <details><summary>Can Palermo Homes build on hillside or lakefront lots?</summary><div class="ans">Yes. We have delivered custom homes on hillside benches in Upper Mission and Lakeview Heights, lakefront on Okanagan Lake, vineyard-view parcels on the Naramata Bench, and hillside lots on Eagle Mountain in Abbotsford. Hillside and lakefront builds carry their own geotechnical, drainage, and setback requirements, which we scope at the estimating stage.</div></details>
        <details><summary>What is the farthest Palermo Homes will travel for a custom build?</summary><div class="ans">Our primary custom home service area is the Okanagan Valley from Vernon in the north to Penticton in the south, with a secondary Lower Mainland service area covering Abbotsford through Vancouver. Beyond that geographic range, we take on projects selectively based on scope, timeline, and client fit.</div></details>
      </div>
    </div>
  </section>

  <section class="svc-cta">
    <div class="wrap">
      <h2>Building somewhere else in BC?</h2>
      <p>Ask us. We take on projects outside our service areas for the right fit.</p>
      <a class="btn" href="/contact/">Start a conversation</a>
    </div>
  </section>
</div>
"""

    render_page(
        title="Our Service Areas | Kelowna & the Okanagan | Palermo Homes",
        meta_desc="Palermo Homes serves Kelowna, West Kelowna, Lake Country, Peachland, Vernon, Penticton, and the Lower Mainland. Custom homes and renovations.",
        canonical=canonical,
        schema_block=schema,
        main_html=main,
        out_path=SITE / "service-areas" / "index.html",
    )


if __name__ == "__main__":
    print("Building service area pages...")
    for slug, data in CITIES.items():
        render_city(slug, data)
    # Build the /service-areas/ hub page so Google has a central link source
    # pointing at every city page. Also helps rank for broader "custom home
    # builder okanagan / BC" queries.
    hub_page()
    print("Done.")


_POSTBUILD_DIR = Path(__file__).parent


def run_post_build():
    import subprocess, sys
    for script in ("replace_nav.py", "replace_footer.py", "kill_dashes.py", "generate_sitemap.py", "validate_links.py"):
        print("\n>>> " + script)
        r = subprocess.run([sys.executable, str(_POSTBUILD_DIR / script)])
        if r.returncode != 0 and script == "validate_links.py":
            raise SystemExit("validate_links.py failed exit " + str(r.returncode))


import atexit
atexit.register(run_post_build)
