# Deploy notes

Status: Phase 0 done locally. No Netlify access yet, so every Netlify fact below is marked as inferred or unconfirmed.

## Current Netlify configuration

What the repo shows (confirmed from files):

- The old `site/netlify.toml` had `publish = "."` and `functions = "netlify/functions"`, with no build command.
- Functions lived in `site/netlify/functions/submission-created.js`.
- There was no `netlify.toml` at the repo root.

What this implies (inferred, NOT confirmed):

- Base directory is probably `site`, because the config files sat there and `publish = "."` is relative to the base.
- Build command is probably empty (plain static files).
- Publish directory is probably `.` (the base itself).
- Functions directory is probably `netlify/functions` (relative to the base).

TODO(Asim), when Netlify access exists, check these in Site configuration > Build and deploy:

1. Base directory (expected `site`).
2. Build command and publish directory set in the dashboard. Dashboard values can override netlify.toml, so note them even if they look empty.
3. Functions directory.
4. Production branch is `main` (Continuous deployment). Branch deploys must not be enabled for `redesign` on the live site.
5. Env var `SLACK_WEBHOOK_URL` exists on the live site.
6. Node version Netlify uses (local is Node 26; see below).

## How the repo is laid out now (branch `redesign`)

- `legacy/` is the whole old static export, moved with `git mv`. Reference only. It is not built or published.
- `site/` is the new Astro project. This keeps the same base directory (`site`) as today, so if the guess above is right, the merge needs no dashboard change.
- `site/netlify.toml` has `command = "npm run build"`, `publish = "dist"`, `functions = "netlify/functions"`, and the immutable cache headers for `/wp-content/*` and `/_astro/*`.
- `_build/` is untouched.

Risk to check at launch: if the dashboard has a publish directory set (for example `site`), it would override `dist` in netlify.toml. Confirm before merging to `main`.

## Phase 0 results

- Astro 7.4.7, static output, `trailingSlash: 'always'`, `build.format: 'directory'`.
- `site/public/wp-content/uploads/` is an unchanged copy of the old uploads folder (159 MB). The IndexNow key file is in `site/public/`.
- `site/netlify/functions/submission-created.js` is copied as is. It still has the unescaped input problem. Hardening is Phase 4.
- Old `_redirects` and `robots.txt` were NOT copied. Phase 4 builds them from docs/REDIRECTS.proposed.
- Indexing is opt-in (`src/lib/indexing.mjs`). Indexable only when `CONTEXT=production` and the host of `URL` is palermohomes.com. Verified locally:
  - no env vars: noindex meta, `Disallow: /`, `X-Robots-Tag: noindex`
  - `CONTEXT=production URL=https://example.netlify.app`: noindex (the required test)
  - `CONTEXT=production URL=https://palermohomes.com`: index, robots.txt allows all, no noindex header
  - Run `npm run test:indexing` for the unit tests.
- `npm run check` and `npm audit` are clean. The test scripts for urls, redirects, images, parity and security are stubs until Phase 4.
- TypeScript is pinned to 6.x because `@astrojs/check` does not support 7 yet.

## Staging (Asim chooses, not done)

Not set up. No Netlify access. Preferred: a new Netlify site linked to Palermohomes/palermo-homes-website with `redesign` as its production branch, base directory `site`. Because of the indexing rule, it stays noindex even then. Use a different `SLACK_WEBHOOK_URL` (or none) on staging.

Phase 0 items still open because they need Netlify or a push:

- Confirm production branch is `main`.
- Push `redesign` (Asim, from GitHub Desktop).
- Staging URL loads and sends `X-Robots-Tag: noindex`.
- Staging form test.
