# Content audit (Phase 1)

Written by `scripts/extract-content.mjs`. Rerun the script to refresh it.

## What was built

- 63 content files in `src/content/` (59 published, 4 draft). One per KEEP or NEW URL in docs/URL-PLAN.csv. None for the 11 redirect rows.
- Numbers: 69 current pages. 59 stay (KEEP). 10 are merged into another page. 11 redirect rows (the 10 merged pages plus the Jas Sidhu rename). 4 new legal pages. 63 URLs after launch, 63 content files. `/media/` and `/awards/` stay as two separate pages (client decision).
- Collections: pages, locations (areas and neighbourhoods, with a `parent`), projects, guides. Schema in `src/content.config.ts`.
- Text was extracted as it was. Nothing was rewritten. No Divi markup, scripts or classes were carried. Internal links point to final URLs.
- Old nav, footer and breadcrumbs are not in the text. The header and footer are rebuilt from layouts.

## How word counts were taken

- "Crawl" is the word count in docs/CURRENT-PAGES.csv.
- "Before" is the visible text of the old page without its nav, footer, breadcrumbs and contact form, counted by this script.
- "After" is the H1, the body and the FAQs in the new content file.
- Limit: no page may shrink more than 5 percent without a logged reason.

## Pages that differ by more than 5 percent (After against Before)

| URL | Before | After | Change | Reason |
|-----|--------|-------|--------|--------|
| / | 513 | 1808 | +252.4% | grew: text merged in from /services/custom-homes/, /service-areas/kelowna/ |
| /service-areas/west-kelowna/ | 791 | 901 | +13.9% | grew: text merged in from /projects/cabernet/, /projects/malbec/, /projects/vineyard-estates/ |
| /neighborhoods/upper-mission/ | 1556 | 2898 | +86.2% | grew: text merged in from /neighborhoods/kettle-valley/ |
| /project/touriga-place-1/ | 36 | 72 | +100.0% | grew: text merged in from /projects/touriga/ |
| /project/lakestone/ | 36 | 78 | +116.7% | grew: text merged in from /projects/ledgestone/ |
| /project/west-abbotsford/ | 37 | 65 | +75.7% | grew: text merged in from /projects/west-abbotsford/ |

Pages that shrank by more than 5 percent: none.

Against the crawl count, one page differs by more than 5 percent without a merge: `/contact/` (crawl 109, after 54). The gap is the form text (labels, placeholders, dropdown options, success message). The form is rebuilt as a component in Phase 2, so the words come back there.

## Could not extract cleanly, or needs a decision

1. **Contact form.** The form markup is not extracted. It is rebuilt as a Netlify Forms component (fields and names in CLAUDE.md). The dropdown options in the old form were: Custom home, Renovation, General contracting, Not sure yet.
2. **Hero images set in CSS.** These pages used a CSS background for the hero, so there is no `img` tag, no alt text and no dimensions: `/`, `/services/general-contracting/`, `/services/renovations/`, `/service-areas/`, `/service-areas/west-kelowna/`, `/service-areas/lake-country/`, `/service-areas/lower-mainland/`, `/service-areas/vernon/`, `/service-areas/penticton/`, `/service-areas/peachland/`, `/neighborhoods/upper-mission/`, `/neighborhoods/mckinley-beach/`, `/neighborhoods/wilden/`, `/neighborhoods/lakeview-heights/`, `/neighborhoods/lakestone/`, `/neighborhoods/eagle-mountain/`, `/neighborhoods/adventure-bay/`, `/neighborhoods/predator-ridge/`, `/neighborhoods/the-rise/`, `/neighborhoods/naramata-bench/`, `/neighborhoods/skaha-hills/`, `/projects/`, `/about/`, `/awards/`, `/media/`. The file paths are saved in `backgroundImages`. Each needs a proper image with alt text when the page is built from Asim's spec.
3. **Missing dates.** The crawl has no `date_published` for 8 published pages: `/services/`, `/services/general-contracting/`, `/services/renovations/`, `/service-areas/`, `/projects/`, `/guides/`, `/about/jas-sidhu/`, `/faq/`. Their `datePublished` is `null`. 7 of them also have no `date_modified` (`/services/`, `/services/general-contracting/`, `/services/renovations/`, `/service-areas/`, `/projects/`, `/guides/`, `/faq/`), so `updated` is `null` there too. Nothing was invented. The sitemap date of 2026-10-19 was not used because it is stamped on every page. See docs/OPEN-QUESTIONS.md. `test:urls` must fail at launch while a published page has a null date.
4. **Draft pages.** The four legal pages are `status: draft` with a `TODO(legal)` placeholder. Their titles and descriptions are placeholders too.
5. **Borrowed project blocks.** These pages still contain the old "Portfolio match" or "Featured build" text, which SEO-SPEC says to remove when the page is built (it shows projects from other places): `/`, `/service-areas/west-kelowna/`, `/service-areas/lake-country/`, `/service-areas/lower-mainland/`, `/service-areas/vernon/`, `/service-areas/penticton/`, `/service-areas/peachland/`, `/neighborhoods/upper-mission/`, `/neighborhoods/mckinley-beach/`, `/neighborhoods/wilden/`, `/neighborhoods/lakeview-heights/`, `/neighborhoods/lakestone/`, `/neighborhoods/eagle-mountain/`, `/neighborhoods/adventure-bay/`, `/neighborhoods/predator-ridge/`, `/neighborhoods/the-rise/`, `/neighborhoods/naramata-bench/`, `/neighborhoods/skaha-hills/`. Left in place for now so no word is lost without a decision.
6. **Merged FAQ headings.** The heading above a merged FAQ block stays in the body text while the questions sit in the `faqs` field.
7. **Project pages.** Each has only the H1 and a gallery in the old build (about 36 words). The "Previous / Next" lines and the "Service area" text at the bottom are carried as text. Previous and next links are navigation and will be rebuilt automatically. Street, town and location tags come from docs/URL-PLAN.csv notes. Specs (size, bedrooms, year) are not on the old pages, so none exist. They are open question 10.
8. **Image sizes.** 38 images in the old HTML had no width or height. The size was read from the file in `public/wp-content/uploads/` and saved. These are marked `dimsFrom: "file"`.
9. **Titles over 60 characters (kept as they are, not changed in Phase 1):** /neighborhoods/eagle-mountain/ (62), /neighborhoods/naramata-bench/ (61), /project/vineyard-estates-3/ (61), /project/vineyard-estates-4/ (61), /project/eagle-mountain-1/ (62), /project/eagle-mountain-2/ (62), /project/eagle-mountain-3/ (62), /project/eagle-mountain-4/ (61), /project/verado-court/ (62), /guides/custom-home-building-process-kelowna/ (67), /guides/custom-home-permits-okanagan/ (72), /guides/financing-custom-home-bc/ (79), /guides/hillside-custom-home-kelowna/ (68), /guides/whole-home-renovation-cost-okanagan/ (66).
10. **Descriptions under 120 characters (kept as they are):** /neighborhoods/mckinley-beach/ (115), /neighborhoods/wilden/ (108), /neighborhoods/lakestone/ (115), /neighborhoods/eagle-mountain/ (107), /neighborhoods/predator-ridge/ (99), /neighborhoods/skaha-hills/ (114), /projects/ (116), /project/vineyard-estates-3/ (111), /project/vineyard-estates-4/ (104), /project/west-abbotsford/ (115), /guides/fixed-price-vs-cost-plus-custom-home-kelowna/ (114).
11. **Title, H1 and description** come from docs/CURRENT-PAGES.csv. Differences between the old HTML and the CSV found by the script: none.
13. **YouTube embeds on `/media/`.** The old page has 4 YouTube iframes. They are saved in the `embeds` field (source and title) and are not rendered. Third-party embeds need a written reason in docs/THIRD-PARTY.md, and a plain YouTube embed sets cookies, which the launch rules forbid until a consent banner exists. Options for Phase 3: a click-to-load placeholder, a privacy-friendly embed, or plain links.
12. **Markup choices.** "Eyebrow" labels (short labels above headings) are kept as italic lines. Fact tiles are kept as bold label lines. Card links are kept as linked headings.

## Per page

| URL | Status | File | Crawl | Before | After | Change | FAQs | Merged in |
|-----|--------|------|-------|--------|-------|--------|------|-----------|
| / | published | `pages/home.md` | 526 | 513 | 1808 | +252.4% | 13 | 2 |
| /services/ | published | `pages/services.md` | 664 | 664 | 664 | +0.0% | 7 | - |
| /services/general-contracting/ | published | `pages/services-general-contracting.md` | 392 | 392 | 395 | +0.8% | 5 | - |
| /services/renovations/ | published | `pages/services-renovations.md` | 476 | 476 | 476 | +0.0% | 6 | - |
| /service-areas/ | published | `pages/service-areas.md` | 678 | 678 | 685 | +1.0% | 5 | - |
| /service-areas/west-kelowna/ | published | `locations/west-kelowna.md` | 791 | 791 | 901 | +13.9% | 5 | 3 |
| /service-areas/lake-country/ | published | `locations/lake-country.md` | 755 | 755 | 755 | +0.0% | 5 | - |
| /service-areas/lower-mainland/ | published | `locations/lower-mainland.md` | 736 | 736 | 736 | +0.0% | 5 | - |
| /service-areas/vernon/ | published | `locations/vernon.md` | 1145 | 1145 | 1145 | +0.0% | 10 | - |
| /service-areas/penticton/ | published | `locations/penticton.md` | 1117 | 1117 | 1117 | +0.0% | 10 | - |
| /service-areas/peachland/ | published | `locations/peachland.md` | 1034 | 1034 | 1034 | +0.0% | 9 | - |
| /neighborhoods/upper-mission/ | published | `locations/upper-mission.md` | 1556 | 1556 | 2898 | +86.2% | 14 | 1 |
| /neighborhoods/mckinley-beach/ | published | `locations/mckinley-beach.md` | 1358 | 1358 | 1358 | +0.0% | 7 | - |
| /neighborhoods/wilden/ | published | `locations/wilden.md` | 1428 | 1428 | 1428 | +0.0% | 7 | - |
| /neighborhoods/lakeview-heights/ | published | `locations/lakeview-heights.md` | 1673 | 1673 | 1673 | +0.0% | 7 | - |
| /neighborhoods/lakestone/ | published | `locations/lakestone.md` | 1739 | 1739 | 1739 | +0.0% | 7 | - |
| /neighborhoods/eagle-mountain/ | published | `locations/eagle-mountain.md` | 1381 | 1381 | 1425 | +3.2% | 7 | 1 |
| /neighborhoods/adventure-bay/ | published | `locations/adventure-bay.md` | 1406 | 1406 | 1406 | +0.0% | 7 | - |
| /neighborhoods/predator-ridge/ | published | `locations/predator-ridge.md` | 1383 | 1383 | 1383 | +0.0% | 7 | - |
| /neighborhoods/the-rise/ | published | `locations/the-rise.md` | 1422 | 1422 | 1422 | +0.0% | 7 | - |
| /neighborhoods/naramata-bench/ | published | `locations/naramata-bench.md` | 1519 | 1519 | 1519 | +0.0% | 7 | - |
| /neighborhoods/skaha-hills/ | published | `locations/skaha-hills.md` | 1439 | 1439 | 1439 | +0.0% | 7 | - |
| /projects/ | published | `pages/projects.md` | 123 | 123 | 123 | +0.0% | 0 | - |
| /project/1252/ | published | `projects/1252.md` | 36 | 36 | 36 | +0.0% | 0 | - |
| /project/cabernet-2/ | published | `projects/cabernet-2.md` | 36 | 36 | 36 | +0.0% | 0 | - |
| /project/cabernet-3/ | published | `projects/cabernet-3.md` | 36 | 36 | 36 | +0.0% | 0 | - |
| /project/malbec-place-1/ | published | `projects/malbec-place-1.md` | 36 | 36 | 36 | +0.0% | 0 | - |
| /project/malbec-2/ | published | `projects/malbec-2.md` | 36 | 36 | 36 | +0.0% | 0 | - |
| /project/touriga-place-1/ | published | `projects/touriga-place-1.md` | 36 | 36 | 72 | +100.0% | 0 | 1 |
| /project/vineyard-estates-3/ | published | `projects/vineyard-estates-3.md` | 35 | 35 | 35 | +0.0% | 0 | - |
| /project/vineyard-estates-4/ | published | `projects/vineyard-estates-4.md` | 36 | 36 | 36 | +0.0% | 0 | - |
| /project/lakestone/ | published | `projects/lakestone.md` | 36 | 36 | 78 | +116.7% | 0 | 1 |
| /project/eagle-mountain-1/ | published | `projects/eagle-mountain-1.md` | 46 | 46 | 46 | +0.0% | 0 | - |
| /project/eagle-mountain-2/ | published | `projects/eagle-mountain-2.md` | 48 | 48 | 48 | +0.0% | 0 | - |
| /project/eagle-mountain-3/ | published | `projects/eagle-mountain-3.md` | 45 | 45 | 45 | +0.0% | 0 | - |
| /project/eagle-mountain-4/ | published | `projects/eagle-mountain-4.md` | 47 | 47 | 47 | +0.0% | 0 | - |
| /project/eagle-mountain-5/ | published | `projects/eagle-mountain-5.md` | 48 | 48 | 48 | +0.0% | 0 | - |
| /project/eagle-mountain-6/ | published | `projects/eagle-mountain-6.md` | 46 | 46 | 46 | +0.0% | 0 | - |
| /project/eagle-mountain-9/ | published | `projects/eagle-mountain-9.md` | 48 | 48 | 48 | +0.0% | 0 | - |
| /project/verado-court/ | published | `projects/verado-court.md` | 45 | 45 | 45 | +0.0% | 0 | - |
| /project/713/ | published | `projects/713.md` | 40 | 40 | 40 | +0.0% | 0 | - |
| /project/west-abbotsford/ | published | `projects/west-abbotsford.md` | 37 | 37 | 65 | +75.7% | 0 | 1 |
| /guides/bc-2-5-10-new-home-warranty-explained/ | published | `guides/bc-2-5-10-new-home-warranty-explained.md` | 2043 | 2035 | 2049 | +0.7% | 0 | - |
| /guides/custom-home-building-process-kelowna/ | published | `guides/custom-home-building-process-kelowna.md` | 2443 | 2434 | 2439 | +0.2% | 0 | - |
| /guides/custom-home-cost-kelowna/ | published | `guides/custom-home-cost-kelowna.md` | 1405 | 1395 | 1395 | +0.0% | 0 | - |
| /guides/custom-home-permits-okanagan/ | published | `guides/custom-home-permits-okanagan.md` | 2368 | 2360 | 2371 | +0.5% | 0 | - |
| /guides/financing-custom-home-bc/ | published | `guides/financing-custom-home-bc.md` | 2440 | 2432 | 2444 | +0.5% | 0 | - |
| /guides/fixed-price-vs-cost-plus-custom-home-kelowna/ | published | `guides/fixed-price-vs-cost-plus-custom-home-kelowna.md` | 1534 | 1528 | 1528 | +0.0% | 0 | - |
| /guides/hillside-custom-home-kelowna/ | published | `guides/hillside-custom-home-kelowna.md` | 2241 | 2233 | 2241 | +0.4% | 0 | - |
| /guides/how-long-to-build-custom-home-kelowna/ | published | `guides/how-long-to-build-custom-home-kelowna.md` | 1964 | 1953 | 1957 | +0.2% | 0 | - |
| /guides/how-to-choose-custom-home-builder-kelowna/ | published | `guides/how-to-choose-custom-home-builder-kelowna.md` | 1769 | 1758 | 1765 | +0.4% | 0 | - |
| /guides/ | published | `pages/guides.md` | 502 | 500 | 500 | +0.0% | 0 | - |
| /guides/whole-home-renovation-cost-okanagan/ | published | `guides/whole-home-renovation-cost-okanagan.md` | 2047 | 2039 | 2050 | +0.5% | 0 | - |
| /about/ | published | `pages/about.md` | 584 | 584 | 584 | +0.0% | 5 | - |
| /about/jas-sidhu/ | published | `pages/about-jas-sidhu.md` | 654 | 650 | 650 | +0.0% | 0 | - |
| /awards/ | published | `pages/awards.md` | 155 | 155 | 155 | +0.0% | 0 | - |
| /media/ | published | `pages/media.md` | 210 | 210 | 210 | +0.0% | 0 | - |
| /contact/ | published | `pages/contact.md` | 109 | 54 | 54 | +0.0% | 0 | - |
| /faq/ | published | `pages/faq.md` | 3064 | 3062 | 3062 | +0.0% | 32 | - |
| /privacy-policy/ | draft | `pages/privacy-policy.md` | - | - | 22 | - | 0 | - |
| /terms-and-conditions/ | draft | `pages/terms-and-conditions.md` | - | - | 24 | - | 0 | - |
| /disclaimer/ | draft | `pages/disclaimer.md` | - | - | 20 | - | 0 | - |
| /cookie-policy/ | draft | `pages/cookie-policy.md` | - | - | 22 | - | 0 | - |

## Script notes

- `/about/jaspal-sidhu/`: no legacy file found
- `/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-07-mobile.avif, /wp-content/uploads/2025/12/Cabernet-07-mobile.webp, /wp-content/uploads/2025/12/Cabernet-07-desktop.avif, /wp-content/uploads/2025/12/Cabernet-07-desktop.webp, /wp-content/uploads/2025/12/Cabernet-07.jpg, /wp-content/uploads/2025/12/homepage2.jpg, /wp-content/uploads/2025/12/homepage3.jpg
- `/services/general-contracting/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/gc-hero-exterior.jpg
- `/services/renovations/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2023/08/Vineyard-Estates-3-Re-Sized-Photo_2.jpg
- `/service-areas/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-71.jpg
- `/service-areas/west-kelowna/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-02.jpg
- `/service-areas/lake-country/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg
- `/service-areas/lower-mainland/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2019/06/PAL_Projects_Mahogany2_FEATURE.jpg
- `/service-areas/vernon/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/homepage3.jpg
- `/service-areas/penticton/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Touriga-109.jpg
- `/service-areas/peachland/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/1587-Malbec-14.jpg
- `/neighborhoods/upper-mission/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-02.jpg
- `/neighborhoods/mckinley-beach/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-02.jpg
- `/neighborhoods/wilden/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-02.jpg
- `/neighborhoods/lakeview-heights/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-07.jpg
- `/neighborhoods/lakestone/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2022/04/PAL_220411_Main2.jpg
- `/neighborhoods/eagle-mountain/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2019/06/PAL_Projects_Mahogany2_FEATURE.jpg
- `/neighborhoods/adventure-bay/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-07.jpg
- `/neighborhoods/predator-ridge/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-02.jpg
- `/neighborhoods/the-rise/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2023/08/095-1524-Cabernet-Wy-95_2.jpg
- `/neighborhoods/naramata-bench/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-07.jpg
- `/neighborhoods/skaha-hills/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/1587-Malbec-14.jpg
- `/projects/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Cabernet-71.jpg
- `/about/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/Touriga-109.jpg
- `/awards/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2020/03/TCP_1084.jpg, /wp-content/uploads/2020/03/TCP_6696.jpg
- `/media/`: iframe embeds (YouTube) saved in the embeds field, not rendered: third-party embeds need a written reason in docs/THIRD-PARTY.md
- `/media/`: CSS background images not placed in the body (decorative, no alt): /wp-content/uploads/2025/12/media-hero.jpg
- `/contact/`: form markup not extracted (rebuilt as a component later)
