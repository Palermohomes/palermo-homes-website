# SEO spec

Applies to every page. Where a page already has a title or H1 that Google has indexed (see docs/CURRENT-PAGES.csv), keep it unless this spec says otherwise, and log any change in docs/TITLE-CHANGES.md.

## Titles, descriptions, headings

- Title: 50 to 60 characters, primary keyword first, brand last: `Custom Home Builder in Kelowna | Palermo Homes`.
- Meta description: 140 to 160 characters, plain sentence, a reason to click, no keyword stuffing. No phone number.
- One H1 per page, matching the page's main search. H2s are real sections, not styling.
- Patterns:
  - Homepage: `Custom Home Builder in Kelowna | Palermo Homes`
  - Service: `General Contractor in Kelowna, BC | Palermo Homes`, `Home Renovations in Kelowna | Palermo Homes`
  - Place: `Custom Home Builder in West Kelowna, BC | Palermo Homes`
  - Neighbourhood: `Custom Home Builder in Wilden, Kelowna | Palermo Homes`
  - Project: `[Style] Home on [Street], [Town] | Palermo Homes`
  - Guide: keep current until the guides phase.
- Every title and description is unique across the site. `scripts/check-urls.mjs` fails on duplicates.

## Page blueprints

Blocks in order. A block with no real content is left out, not filled with filler.

**Homepage (custom home builder Kelowna)**: hero with H1 and consultation button, trust bar (licence, warranty, rating only if confirmed), three service cards (custom homes explained on this page, general contracting, renovations), build process in 5 steps, pricing guidance with link to the cost guide, three featured projects, reviews (real only), areas served, guides, FAQ, call to action.

**Service page (one service, Kelowna)**: hero, trust bar, what we do (6 to 8 items), how it works (5 steps with timing), cost and contract (links to the cost guide), two featured projects, reviews, FAQ (5 to 6 questions visible on the page), areas served and guide links, call to action. 800 words or more.

**Place page (one city, all three services)**: hero, local intro (why local, 100 to 150 unique words), the three services as short cards (two link to service pages, custom homes links to the homepage), projects in this place (real ones only), neighbourhoods Palermo has built in (links), local know-how (the city permit process with a link to the city site, lot types, timing), reviews from this city, local FAQs (3 to 4), nearby areas, call to action. 700 to 1,000 words. The unique blocks are local intro, projects and local know-how. If those are empty, the page is a copy.

**Neighbourhood page**: hero, who builds here and what lots look like, amenities and local rules (HOA, design review, permits), projects in this neighbourhood (real only), link up to the city page, FAQ, call to action. Remove the current "Portfolio match" and "Featured build" blocks wherever the project is not in that place.

**Project page**: H1 with style, street and town (street name only, never a house number), a spec list (size, bedrooms, year, build time, features: details come from Jas, never invented), gallery (hero image first, then in order), what was special about the site or brief, links to the place and neighbourhood pages and to the matching service, call to action. Target 250 to 400 words of real content.

**Hub pages** (/services/, /service-areas/, /projects/): short intro, cards linking to each child, one line of text per card.

**Projects hub**: filter by location (West Kelowna, Lake Country, Lower Mainland, Eagle Mountain, Lakeview Heights, Lakestone). Filtering must work without JavaScript as links to anchors or static views, so every project is in the HTML.

## Internal linking

- Homepage links to both service pages, the West Kelowna page, the projects hub, three featured projects and the cost guide.
- Each service page links to the homepage, the other service, the area hub and the best two guides.
- Each place page links to the homepage, both service pages, its neighbourhoods, its projects, and the nearby places.
- Each neighbourhood links up to its city (Kelowna neighbourhoods link to the homepage), to the two service pages, and to its projects.
- Each project links to the place and neighbourhood where it sits and to one matching service page.
- Footer: services, areas, legal pages, phone, email. Header menu as in BUILD-PLAN.
- Breadcrumbs: Home, Service areas, City, Neighbourhood. For Kelowna neighbourhoods: Home, Neighbourhood. Breadcrumb text must match the page H1 root name.
- Link anchors are descriptive (`custom homes in Lake Country`), never "click here".

## Schema (JSON-LD)

- Sitewide: Organization and HomeAndConstructionBusiness (keep the current `@id`s, telephone, email, areaServed, sameAs, logo, foundingDate only once Jas confirms), WebSite.
- Every page except the homepage: BreadcrumbList and WebPage.
- Service pages: Service with provider pointing to the business `@id` and areaServed.
- Place pages: Service with areaServed set to that City.
- Neighbourhood pages: WebPage with `about` a Place.
- Project pages: WebPage with an ImageObject for the hero. No Review or AggregateRating.
- Guides: Article with real datePublished and dateModified, author Person (Jas Sidhu, `@id` on his page).
- /about/jas-sidhu/: Person.
- FAQPage only where the questions and answers are visible on the page.
- No Review or AggregateRating markup for Palermo itself (self-serving, Google ignores it). Show real reviews as plain content.
- Validate every type in the Rich Results Test and the Schema.org validator.

## Images

- Width and height attributes on every image, descriptive alt text (what is in the photo, location where it helps), no keyword lists.
- Hero image: eager and `fetchpriority="high"`. All others `loading="lazy"`.
- New images: AVIF or WebP, sized for their slot, `srcset` for responsive. Existing WebP files stay at their current URLs.
- Every page has an Open Graph image (1200 by 630): project hero for projects, a set image for other pages.

## Local SEO details

- NAP in the footer exactly: Palermo Homes, West Kelowna, BC, 778-760-4113, info@palermohomes.com. No street address.
- `<html lang="en-CA">`, Canadian spelling in copy.
- No embedded Google Map until a consent banner exists. A static image linking to the Google Business Profile is fine.
- Link to the Google Business Profile and the review page from the contact page and footer once Jas supplies the URLs.

## Performance and accessibility

- LCP under 2.5 s, CLS under 0.1, INP under 200 ms on mobile.
- Content pages ship under 50 KB of JavaScript (gzip) and no render-blocking third-party scripts.
- Fonts: self-hosted, `font-display: swap`, at most two families and four weights, preloaded for the above-the-fold text.
- Pinch zoom allowed. Visible focus states. Contrast AA or better. Menu works from the keyboard.

## Technical SEO checklist

- Valid, semantic HTML with landmarks (`header`, `nav`, `main`, `footer`). One H1. Heading order does not skip levels.
- Compression and caching: Netlify serves Brotli or gzip automatically. Hashed assets cache for a year. HTML revalidates.
- A real 404 page that returns status 404 and links to the main pages. Removed spam URLs return 410.
- No orphan pages. No duplicate URLs through parameters, uppercase, or a missing slash.
- Canonical, robots, sitemap and `hreflang` handled as above (`hreflang` not needed, one language).
- Open Graph and Twitter tags on every page, with an image.
- Structured data valid on every page type. No markup for content that is not visible.
- Mobile first: viewport allows zoom, tap targets at least 44 px, text at least 16 px.
- Security headers on every response (see docs/SECURITY.md).
- Resource hints only where measured: preload the hero image and the main font, nothing else.
- Third-party requests: zero on first load.

## Do not

- Do not create doorway pages: a place or neighbourhood page needs unique local content and, where possible, a real project.
- Do not show the same text on two pages with the place name swapped.
- Do not add noindex to a page in the plan on production.
- Do not put personal data in URLs or query strings.
