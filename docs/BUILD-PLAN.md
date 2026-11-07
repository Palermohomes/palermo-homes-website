# Build plan

Work in order. Each phase ends with a commit, a staging deploy, and a short plain-language report to Asim: what was built, the staging URL, and what is next. Do not start a phase before the previous one passes its checks.

## Phase 0. Setup and staging

- [ ] Clone the repo, create branch `redesign`.
- [ ] Find the current Netlify configuration (base directory, build command, publish directory, functions directory). Write it in docs/DEPLOY.md. Do not change dashboard settings.
- [ ] Move the old static export to `legacy/` (git mv) so it stays as reference. Keep `_build/` as is.
- [ ] Scaffold Astro (static output, TypeScript) where the Netlify base directory points. Set `trailingSlash: 'always'` and `build.format: 'directory'`.
- [ ] Write the netlify.toml for the redesign branch: build command, publish directory (`dist`), functions directory. Keep the immutable cache headers for `/wp-content/*` and `/_astro/*`.
- [ ] Copy `wp-content/uploads/` into `public/wp-content/uploads/` unchanged. Copy the IndexNow key file to `public/`. Recreate `netlify/functions/submission-created.js`.
- [ ] Add the staging noindex logic (see CLAUDE.md: indexable only when CONTEXT is production and URL host is palermohomes.com). Add a test for it.
- [ ] Add `.gitignore` (`.env*`, `node_modules`, `dist`, `.DS_Store`, `*.log`).
- [ ] Add scripts: `npm run check` (astro check), `npm run test:urls`, `npm run test:redirects`, `npm run test:images`, `npm run test:parity`, `npm run test:security`. Build them in Phase 4, create empty stubs now.
- [ ] Confirm in Netlify that the live site's production branch is `main` (Site configuration, Build and deploy, Continuous deployment). Pushing `redesign` must never publish to palermohomes.com.
- [ ] Push `redesign`. Asim sets up staging in Netlify: preferably a new site linked to this repo with `redesign` as its production branch, or alternatively a branch deploy on the live site. Confirm the staging URL loads a blank Astro page and sends `X-Robots-Tag: noindex`.

Done when: staging URL loads, is noindex, and the live site (`main`) is untouched.

## Phase 1. Content extraction

- [ ] Write `scripts/extract-content.mjs`. It reads the pages in `legacy/` and writes Markdown or JSON into `src/content/` with headings, body text, FAQs, image paths and alt text. Use docs/CURRENT-PAGES.csv as the checklist.
- [ ] Apply the URL plan. Create content files only for URLs whose action in docs/URL-PLAN.csv is KEEP or NEW. Never create a page or content file for a 301 URL.
- [ ] For each of the 12 redirected URLs, move the useful text, headings, FAQs and images into the target page's content file before dropping it. The target must cover the same topic or place. List what moved in `docs/MERGE-REPORT.md`.
- [ ] Write `public/_redirects` now from docs/REDIRECTS.proposed: the 301s plus the 410 spam rules. Keep both slash and no-slash forms, one hop only. Phase 4 only tests and refines it.
- [ ] If Asim adds the Ahrefs or Search Console Links export, propose 301s for old URLs that have backlinks, pointing to the closest same-intent page, in docs/PROPOSED-CHANGES.md. Ask before adding any redirect that is not in docs/URL-PLAN.csv.
- [ ] Every content file gets `datePublished` (the real date from docs/CURRENT-PAGES.csv, never changed), `updated` (changes only when the content really changes) and `status`. Pages live today are `status: published`. New pages (the four legal pages) are `status: draft`. Draft pages stay out of the sitemap, the menus and all internal links, and are noindex if built. `test:urls` must fail at launch if any URL in the plan is still draft.
- [ ] Collections: `pages`, `locations` (areas and neighbourhoods, with a `parent` field), `projects` (19), `guides` (10).
- [ ] Projects need these fields: slug, title, h1, street, town, location tags (for example `west-kelowna` and `lakeview-heights`), published date, images (in order), description. Use the location tags in docs/URL-PLAN.csv notes (each project's "Shows on" text).
- [ ] Do not rewrite copy in this phase. Extract exactly. Strip Divi markup and `et_pb` classes. Do not copy themes, et-cache, wp-includes, plugins or any WordPress or jQuery scripts (see CLAUDE.md, cleanup section).
- [ ] Keep each page's `date_published` from docs/CURRENT-PAGES.csv in its content file. Add an `updated` field that starts as the old modified date and changes only on real edits.
- [ ] Write `docs/CONTENT-AUDIT.md`: for each page, word count before and a list of blocks you could not extract cleanly.

Done when: every KEEP and NEW URL in docs/URL-PLAN.csv has a content file, no 301 URL has one, docs/MERGE-REPORT.md lists what moved, `public/_redirects` exists, and word counts match the crawl within 5 percent (merged targets may grow).

## Phase 1b. Design reference

- [ ] Asim puts a PDF of website design ideas in `docs/design/`. Read the whole PDF.
- [ ] Write `docs/DESIGN-NOTES.md` with: the overall look (layout, colours, fonts, spacing, components); section ideas for each page; anything that conflicts with docs/SEO-SPEC.md or the URL plan (for example sliders, pop-ups, text inside images, heavy animation); and questions for Asim.
- [ ] Where the PDF and docs/DESIGN-BRIEF.md differ on look and layout, the PDF wins. Where they differ on SEO, security or URLs, the docs win, and Asim is told.
- [ ] Stop and wait for Asim's confirmation before starting Phase 2.

Done when: Asim confirms DESIGN-NOTES.md.

## Phase 2. Design system and layout

Start only after Asim confirms Phase 1b.

- [ ] Read docs/DESIGN-NOTES.md (the PDF wins on look and layout) and docs/DESIGN-BRIEF.md. Propose design tokens (colour from the logo, type scale, spacing) and one homepage layout as a static preview. Stop and wait for Asim's approval.
- [ ] Build: base layout, SEO head component (title, description, canonical, robots, Open Graph, Twitter, one JSON-LD slot), header and mobile menu, footer (NAP, services, areas, legal links), breadcrumbs, button, CTA band, contact form, project card, project gallery, FAQ accordion, location list.
- [ ] Menu: Home, Services (GC, Renovations), Service Areas, Projects, Guides, About, Contact. Phone number click-to-call in the header on mobile.
- [ ] Contact form works with Netlify Forms and the Slack function.

Done when: Asim approves the look on staging and the form delivers a test lead to Slack.

## Phase 3. Templates and pages (in this order)

1. Homepage (blueprint in SEO-SPEC)
2. Services: hub, general contracting, renovations
3. Service areas: hub and six place pages
4. Neighborhoods: 11 pages
5. Projects: hub with location filter, then 19 project pages
6. Guides: port the hub and 10 guides as they are (no rewrite now)
7. Company: about, Jas Sidhu, awards, contact, faq
8. Legal: four pages with placeholder text clearly marked `TODO(legal)`, linked from the footer

Rules for every page: use the blueprint for its type, use the current text until a content brief replaces it, show only real projects for that place, add breadcrumbs and JSON-LD. Keep current titles and H1s on indexed pages unless SEO-SPEC changes them. Log every title or H1 change in `docs/TITLE-CHANGES.md` (old, new, reason).

Done when: every URL in docs/URL-PLAN.csv with action KEEP or NEW returns 200 on staging.

## Phase 4. Redirects, sitemap, robots, tests

- [ ] Test and refine `public/_redirects` (written in Phase 1). Check that no page exists at a 301 source URL.
- [ ] Sitemap: final indexable URLs only, real `lastmod` from content dates (store a `updated` date per content file). No priority or changefreq needed.
- [ ] robots.txt per CLAUDE.md. Production: allow all, link the sitemap, no spam path disallows. Staging: disallow all.
- [ ] Custom 404 page.
- [ ] `scripts/check-urls.mjs BASE_URL`: reads docs/URL-PLAN.csv. For KEEP and NEW: expects 200, one H1, unique title and description, self canonical, JSON-LD parses, no noindex when BASE is production. For 301: expects one hop to `final_url` and a 200 there.
- [ ] `scripts/check-links.mjs`: crawls the built site, fails on any internal link that returns 3xx or 4xx.
- [ ] `scripts/check-images.mjs`: every file under `public/wp-content/uploads/` that the old site referenced returns 200 at the same path.
- [ ] Test the query-string 410 rules with `curl -I` on staging. Report which ones work.
- [ ] `public/_headers` with the security headers in docs/SECURITY.md. Content-Security-Policy in report-only first, fix violations, then enforce.
- [ ] Rewrite `netlify/functions/submission-created.js` with the input hardening in docs/SECURITY.md. Test with hostile input.
- [ ] `scripts/check-parity.mjs`: compares the legacy build and the new build for every KEEP URL per docs/MIGRATION-CHECKS.md and writes docs/PARITY-REPORT.md.
- [ ] `scripts/check-security.mjs BASE_URL`: checks every header and requests the must-not-be-published paths.
- [ ] Add an orphan check to `check-links.mjs`: every indexable page has at least 3 internal links pointing to it from relevant pages.

Done when: all the test scripts pass against the staging URL.

## Phase 5. Staging QA (report to Asim, do not self-approve)

- [ ] Lighthouse on mobile for homepage, one service page, one place page, one project page. Targets: performance 90 or more, accessibility 95 or more, best practices 95 or more, SEO 100.
- [ ] Core Web Vitals targets on mobile: LCP under 2.5 s, CLS under 0.1, INP under 200 ms.
- [ ] Schema validates (Rich Results Test and Schema.org validator) on each page type.
- [ ] Pinch zoom works. Keyboard navigation works. Colour contrast passes.
- [ ] Mobile layouts checked at 360, 390 and 768 px wide. Desktop at 1280 and 1536.
- [ ] Form test: submit, check the Slack message, check the spam honeypot.
- [ ] Security: Mozilla Observatory and securityheaders.com grade A or better on staging, `npm audit` clean of high and critical findings, the hostile-input form test shown to Asim.
- [ ] Write `docs/QA-REPORT.md` with results and anything failing.

## Phase 6. Launch (Asim decides the date)

- [ ] Final run of all test scripts against staging. Fresh sitemap.
- [ ] Merge `redesign` into `main`. Netlify builds production.
- [ ] Run `npm run test:urls` and `test:redirects` against https://palermohomes.com. Confirm no noindex anywhere.
- [ ] Asim in Search Console: resubmit the sitemap, request indexing for the homepage and the two service pages, and request indexing for the old URL `/about/jaspal-sidhu/` so Google sees its 301.
- [ ] Test that `http://` and `www.` reach `https://palermohomes.com/` in one hop.
- [ ] Submit one real test lead with Jas watching Slack.
- [ ] Ping IndexNow once with the URL list.
- [ ] Keep every 301 for at least one year.

## Phase 7. After launch

- Weekly for 8 weeks: Search Console Page indexing report, redirects, crawl errors.
- Add Google Analytics and the consent banner only after Asim approves the cookie policy text.
- Update Houzz, Facebook, Instagram, LinkedIn and Google Business Profile links so they point at the homepage.
- Next content phases (done in Cowork, then built here): money page briefs, guides rewrite, project page content, keyword validation in Ahrefs.
