# Migration checks

The point of a migration is that Google sees the same site, only better. These checks prove it. `npm run test:parity` runs them and writes docs/PARITY-REPORT.md. Every difference needs a one-line reason or a fix.

## What must carry over for every KEEP page

| Item | Rule |
|------|------|
| URL | Identical, trailing slash included. |
| Title and H1 | Same as docs/CURRENT-PAGES.csv unless SEO-SPEC changes them. Each change is logged in docs/TITLE-CHANGES.md. |
| Meta description | Kept unless improved. Logged. |
| Canonical | Self, absolute. |
| Body text | Useful text is kept. Word count may not drop more than 5 percent without a logged reason. Growth is welcome. |
| Headings | Existing H2 topics are kept or merged on purpose. |
| Internal links | Every sensible link on the old page still exists, pointing to a final URL (a link to a merged page points to its new target). |
| Images | Same URLs, same or better alt text. Nothing referenced by the old page goes missing. |
| Schema | At least the same types. Nothing invalid. |
| Published date | The real `date_published` from docs/CURRENT-PAGES.csv is kept in the page and in schema. |
| Modified date | Changes only when the content really changes. Never set to the build date. |

## Merged and redirected pages

- Before a page is merged, the text worth keeping from it is moved to the target page (for example anything useful on `/neighborhoods/kettle-valley/` that is not on Upper Mission). List what moved in docs/PARITY-REPORT.md.
- Each 301 is one hop, to a final 200 page, with the target topic matching the source topic.

## Old site facts to protect

- 46 of 69 URLs are indexed. The indexed ones in docs/CURRENT-PAGES.csv get the most care: never leave one returning an error, a redirect chain, or noindex.
- The hacked-site spam URLs keep returning 410 and stay crawlable (no robots.txt disallow).
- `/about/jaspal-sidhu/` is the only URL Search Console knows for Jas's page: its 301 must work on day one.

## Before launch

1. Crawl the legacy build and the new staging build. Compare URL lists against docs/URL-PLAN.csv.
2. Run test:urls, test:redirects, test:images, test:parity, test:security.
3. Confirm production-mode build has no noindex and staging build has it everywhere.
4. Confirm the sitemap has only final, indexable URLs and real `lastmod` dates.

## After launch (Asim, with Search Console)

- Resubmit the sitemap. Request indexing for the homepage, both service pages and the West Kelowna page.
- Check Page indexing weekly for 8 weeks. Watch for new "Not found (404)", "Page with redirect" and "Duplicate" entries.
- Keep a before and after of clicks and impressions for the 46 indexed URLs.
- Ping IndexNow with the URL list once (the key file is in the site root).
- Keep every 301 for at least a year.
