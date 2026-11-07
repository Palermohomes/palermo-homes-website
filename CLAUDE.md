# Palermo Homes website rebuild

Read this file first, then docs/BUILD-PLAN.md. Detail lives in docs/. If something here conflicts with your own judgment, follow this file and tell Asim.

## The project

Rebuild palermohomes.com as a fast static Astro site. Palermo Homes is a custom home builder based in West Kelowna, BC, serving Kelowna and the Okanagan. The domain is about 13 years old and Google has 46 of the 69 current pages indexed, so the rule is: protect what Google already knows, improve everything else.

Goals, in this order: (1) an SEO-safe migration: Google must see the same URLs, the same real dates and the same useful content, only better; (2) a technically excellent site: fast, clean HTML, valid schema, no old WordPress weight; (3) a secure site: nothing to hack, safe headers, a safe contact form. No file can promise rankings. These rules make the technical foundation as strong as it can be.

People: Jas Sidhu is the owner (client). Asim is the SEO lead and your user. The client gave a free hand on design and structure. This is a premium build, so no shortcuts and no guessing. Asim is not a full-time developer: explain what you did in plain words, show the staging URL after each phase, and ask before anything destructive.

## Business facts (use only these, mark gaps as TODO(Jas))

- Name: Palermo Homes Ltd. (display name: Palermo Homes)
- Phone: 778-760-4113 (tel:+17787604113). Use this number everywhere.
- Email: info@palermohomes.com
- Base: West Kelowna, BC. Service-area business: do not add a street address.
- Services: custom homes (carried by the homepage), general contracting, home renovations.
- Social and identity links: copy the sameAs list from the current homepage schema unchanged.
- Conflicts to leave out until Jas confirms: the About page says "15+ years", the schema says founded 2014. Licence numbers appear in the current Eagle Mountain page text: copy only after Jas confirms.
- Never invent reviews, awards, statistics, prices, timelines, project facts or licence details. If the current site does not say it, leave a visible TODO(Jas) in the draft and list it in docs/OPEN-QUESTIONS.md.

## Stack and hosting

- Astro (current stable), static output, TypeScript, Content Collections. Plain CSS with design tokens. No UI framework and minimal JavaScript.
- Hosted on Netlify from the GitHub repo Palermohomes/palermo-homes-website. Production is branch `main` and it is live now.
- Work only on branch `redesign`. Never push to `main`. Launch is one merge of `redesign` into `main`.
- Day to day, build and preview on localhost (`npm run dev`). Nothing is public and the live site is not touched.
- Staging is a Netlify deploy of `redesign` on its own address, either a branch deploy of the live Netlify site or, preferably, a separate Netlify site linked to the same repo with `redesign` as its production branch (so the live site's settings are never touched). Asim chooses. Write the choice in docs/DEPLOY.md.
- Staging must be noindex. The live site must not be. Make indexing opt-in, not opt-out: emit indexable output only when `process.env.CONTEXT === 'production'` AND the hostname of `process.env.URL` equals the hostname of `site` in astro.config (palermohomes.com). In every other case emit `<meta name="robots" content="noindex, nofollow">`, a robots.txt with `Disallow: /`, and a `_headers` file with `X-Robots-Tag: noindex`. This holds even when a separate staging site treats `redesign` as its production branch. Test it: a build with CONTEXT=production and URL=https://example.netlify.app must come out noindex.
- Staging leads: set a different Slack webhook (or none) on the staging site so test form submissions never look like real leads.
- Phase 0 first task: find out how Netlify is configured today (base directory, build command, publish directory, functions directory). The repo has `site/netlify.toml` and `site/netlify/functions/`, which suggests base directory `site`. Put the Astro project where the base directory points and keep build settings in the netlify.toml that Netlify actually reads, so the merge needs no dashboard change. Record the findings in docs/DEPLOY.md. Do not change dashboard settings.
- The contact form is Netlify Forms: `name="contact"`, `data-netlify="true"`, honeypot `bot-field`, fields `name`, `phone`, `email`, `project-type`, `message`, action `/contact/?submitted=1#form`. The function `netlify/functions/submission-created.js` posts each lead to Slack and needs env var SLACK_WEBHOOK_URL. Keep both working. Test a submission on staging.

## URL rules (not negotiable)

1. The approved structure is docs/URL-PLAN.csv. Every URL in it must behave exactly as written: 200 for KEEP and NEW, a single-hop 301 for 301 rows. Do not add, rename or remove URLs without Asim's approval. Put suggestions in docs/PROPOSED-CHANGES.md.
2. Lowercase, trailing slash always (`trailingSlash: 'always'`, `build.format: 'directory'`). Keep the American spelling in `/neighborhoods/`.
3. Do not generate a page at any 301 source URL. A real file beats a Netlify redirect.
4. Redirects live in `public/_redirects`. Written in Phase 1 from docs/REDIRECTS.proposed (slash and no-slash forms, one hop). The wildcard 410 rules for the old hack spam stay. Create no page or content file for a 301 URL. Move its useful content into the target first and log it in docs/MERGE-REPORT.md. Ask Asim before adding any redirect that is not in docs/URL-PLAN.csv.
5. robots.txt on production must not disallow the spam paths that return 410, or Google cannot see the 410. The current robots.txt does this wrongly and also blocks `/?`. Fix it.
6. Reserved paths, never create real pages here: /collect, /casino, /category, /tag, /author, /attachment, /page, /feed, any .shtml.
7. Old image URLs under `/wp-content/uploads/` must keep working at the same path. Copy that folder into `public/wp-content/uploads/`. New images may use Astro image handling.
8. Internal links point to final URLs only. No link to a URL that redirects. No redirect chains.
9. Canonical is self-referencing and absolute: `https://palermohomes.com/path/`.
10. The sitemap lists final, indexable URLs only, with real `lastmod` (the date the content changed). Never stamp today's date on every page. Keep real published dates in schema and on pages.
11. Keep the IndexNow key file in the site root (`a7f3c9e2d8b641578a4e9c3b2f6d8e1a.txt`).

## Migration rules (SEO safe)

Details and the checklist are in docs/MIGRATION-CHECKS.md. Run `npm run test:parity` before every staging review and before launch.

- Every content file has `datePublished` (real, never changed), `updated` (only on real edits) and `status` (`published` for pages live today, `draft` for the four legal pages). Draft pages stay out of the sitemap, menus and internal links and are noindex. `test:urls` fails at launch if any planned URL is still draft.
- Keep each page's real published date from docs/CURRENT-PAGES.csv, on the page and in schema. `dateModified` and sitemap `lastmod` change only when the content really changes.
- Useful text on a KEEP page may not shrink by more than 5 percent without a logged reason. Titles, H1s and meta descriptions on indexed pages change only as logged in docs/TITLE-CHANGES.md.
- When a page is merged, move the useful text from it to the target page first.
- Nothing is indexable on staging. Nothing is noindex on production.

## Cleanup of the old WordPress build

There is no database in this repo. It is already a static export of the old WordPress and Divi site, so there is nothing to remove on the database side. What must not be carried over:

- `site/wp-content/themes/` (Divi), `site/wp-content/et-cache/`, `site/wp-includes/`, any plugin folders, jQuery, jQuery Migrate, jQuery UI, the Divi scripts and CSS, `et_pb_*` classes, and the inline Divi CSS (the homepage HTML is about 277 KB today).
- Only `wp-content/uploads/` is copied, because image URLs must keep working.
- Fonts are already self-hosted under `site/fonts/`. Reuse the files if the design keeps those fonts. No requests to Google Fonts or other third parties at runtime.
- No generator tag, no WordPress REST, feed or emoji links. None exist now, so do not add any.
- Targets (report the actual numbers): homepage HTML under 60 KB, total CSS under 40 KB, JavaScript under 50 KB (gzip) on content pages.

## Security

Details in docs/SECURITY.md. The short version:

- No secrets anywhere in the repo. `SLACK_WEBHOOK_URL` lives only in Netlify settings. `.gitignore` covers `.env*`, `node_modules`, `dist`.
- Security headers in `public/_headers` on every page (HSTS, nosniff, frame denial, referrer policy, permissions policy, then an enforcing Content-Security-Policy after a report-only trial on staging).
- The Slack function currently inserts raw visitor input into the message. Escape it, strip mass mentions, build the phone link only from a cleaned number, cap field lengths, and test with hostile input.
- No third-party scripts, iframes or embeds without a written reason in docs/THIRD-PARTY.md. No database, no admin login, no custom CMS.
- Only the built `dist` folder is published. `docs/`, `CLAUDE.md`, `legacy/`, `_build/`, `scripts/` and source maps never are. `npm run test:security` checks this.
- Run `npm audit` before every staging review and before launch.

## Site structure (summary, the CSV is the source of truth)

- `/` homepage: custom home builder Kelowna. Carries custom homes. There is no separate custom homes page and no Kelowna area page.
- `/services/` hub, `/services/general-contracting/`, `/services/renovations/`: one service per page, named for Kelowna.
- `/service-areas/` hub and one page per place (West Kelowna, Lake Country, Lower Mainland, Vernon, Penticton, Peachland). Each place page covers all three services in short form and shows its projects.
- `/neighborhoods/<name>/`: 11 pages. Each links up to its city page (Kelowna ones link to the homepage).
- `/projects/` is the one list page, filterable by location. `/project/<slug>/` is one finished home (19 pages). There are no street collection pages any more.
- `/guides/` and 10 guides: carry over as they are for now. Guides get redone in a later phase.
- Company: /about/, /about/jas-sidhu/, /awards/, /contact/, /faq/.
- Legal (new): /privacy-policy/, /terms-and-conditions/, /disclaimer/, /cookie-policy/. Linked from the footer on every page.

## Page and SEO rules

Follow docs/SEO-SPEC.md for titles, headings, schema, internal links and page blueprints. The short version:

- One H1 per page, unique title and meta description, `<html lang="en-CA">`.
- Kelowna first. West Kelowna is the home base page, not the homepage.
- Each location page shows only projects that are really in that place. Never show a West Kelowna project as a "portfolio match" on a Vernon or Penticton page. Remove those borrowed blocks.
- No self-serving review or rating markup. Show real reviews only when Jas supplies them.
- The viewport must allow pinch zoom. The current site blocks it (`maximum-scale=1, user-scalable=0`). Do not carry that over.
- No analytics, ad pixels or map embeds that set cookies until a consent banner exists. The current site has none, so launch clean.
- Every image has width, height and alt text. Hero image eager with fetchpriority high, the rest lazy.
- Every page gets an Open Graph image. The current pages have none.

## How content is managed (no custom CMS)

- The rules live in code, not in per-page typing. Head tags, canonical, robots, Open Graph, JSON-LD, breadcrumbs, the sitemap, image dimensions and the related-link blocks are generated by layouts and components from content fields.
- Each page's content is a file in `src/content/` with required fields, enforced by a Zod schema in `src/content.config.ts`: title, description, h1, updated date, images (each with alt text), location tags, related links, FAQs where they exist.
- The build fails on: a missing, duplicate or over-length title or description; a missing or second H1; an image without alt, width or height; an internal link to a URL that redirects or does not exist; a page in the build that is not in docs/URL-PLAN.csv; a KEEP or NEW URL missing from the build; noindex on a production build.
- Automatic links: breadcrumbs, projects in this place, neighbourhoods in this city, nearby areas, header and footer. Links inside body text are written by hand, following docs/INTERNAL-LINKS.md when Asim provides it.
- No admin login, no database, no custom CMS. After launch a git-based editor (Keystatic or similar) can sit on top of the same files if Jas wants to add projects himself. Do not build one now.

## Page specs from Asim

Asim designs every page. The page blueprints in docs/SEO-SPEC.md are only defaults, and Asim's page specs override them. He gives a spec for each page, in the design PDF or in chat: the sections in order, the text, images, links and call to action. A blank spec form is docs/pages/_TEMPLATE.md.

1. Build one page at a time and wait for Asim's spec before building it. Never invent sections, text or design.
2. The automatic parts stay automatic: head tags, canonical, schema, breadcrumbs, image attributes and the URL plan.
3. If a spec conflicts with the SEO rules or the URL plan, tell Asim before building and explain why.
4. After each page, show the localhost address and list what was built.

## Design

Free hand, with two fixed points: keep the Palermo logo as is (`/wp-content/uploads/brand/palermo-logo-blue.png`) and make mobile the first design target. See docs/DESIGN-BRIEF.md. Asim supplies a design ideas PDF in docs/design/. In Phase 1b read all of it and write docs/DESIGN-NOTES.md, then wait for Asim's confirmation before Phase 2. Where the PDF and docs/DESIGN-BRIEF.md differ on look and layout, the PDF wins. Where they differ on SEO, security or URLs, the docs win and you tell Asim. Propose the design tokens and a homepage layout to Asim and wait for approval before building every template.

## Copy style

Plain, human, specific, short sentences. Canadian spelling in copy (colour, neighbourhood). No em dashes or en dashes anywhere, including code comments and commit messages. No filler like "welcome to" or "we pride ourselves".

## How to work

- Follow docs/BUILD-PLAN.md phase by phase. Commit at the end of each phase with a plain message.
- After each phase run `npm run build`, `npm run check` and `npm run test:urls`, and fix failures before moving on.
- Add a dependency only with a one-line reason.
- Do not delete `_build/` or the old static files until after launch. Move them to `legacy/` on the redesign branch so they stay as reference.
- Keep docs/OPEN-QUESTIONS.md current. Do not guess an answer that belongs to Jas.

## Waiting on answers (do not block on these, build around them)

- Jas: does he take work in Vernon, Penticton and Peachland? Which Kelowna neighbourhoods has he built in? Is the 2023 Verado Court home (`/project/eagle-mountain-9/`) a different house from the 2020 one (`/project/verado-court/`)? Which renovation types does he take? How does he describe a general contracting client versus a custom home client?
- Asim: Ahrefs "Best by links" export and Search Console Links export. These may add redirects for old URLs that have backlinks.
- Legal page text, to be reviewed by a lawyer or a BC-compliant generator.
