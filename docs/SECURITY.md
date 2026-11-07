# Security

Goal: a static site with nothing to hack, safe browser headers, and a contact form that cannot be abused. The old site was a hacked WordPress install (20,000+ spam URLs), so this matters.

## 1. What static already gives us

No database, no admin login, no plugins, no PHP. Do not add any of those. If Jas wants a CMS later it is a git-based editor, never a server with a login on palermohomes.com.

## 2. Secrets

- No keys, tokens, passwords or webhook URLs in the repo, in docs, in commit messages or in chat. The Slack webhook (`SLACK_WEBHOOK_URL`) lives only in Netlify environment variables.
- `.gitignore` must include `.env*`, `node_modules`, `dist`, `.DS_Store`, `*.log`.
- The current repo was checked: no webhook URLs, no `.env`, no SQL dumps, no backups. Keep it that way.

## 3. Headers (`public/_headers`, applies to all pages)

Always on:

```
/*
  Strict-Transport-Security: max-age=31536000
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
  Cross-Origin-Opener-Policy: same-origin
```

- Do not add `includeSubDomains` or `preload` to HSTS until Asim confirms every subdomain of palermohomes.com runs on HTTPS.
- Content-Security-Policy: start in report-only on staging with `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'`. Fix every violation, then switch to the enforcing header before launch. Add a source only with a written reason in docs/THIRD-PARTY.md.
- On non-production builds the same file also carries `X-Robots-Tag: noindex` (see CLAUDE.md).
- Cache headers for `/wp-content/*` and `/_astro/*` stay immutable. HTML is revalidated.

## 4. The contact form and the Slack function

The current `netlify/functions/submission-created.js` puts raw visitor input into a Slack message, including a `tel:` link built from the phone field. That allows link injection and mass mentions (`<!channel>`). Fix when you recreate it:

- Escape `&`, `<` and `>` in every field, and strip `<!channel>`, `<!here>` and `<!everyone>`.
- Build the `tel:` link only from digits, plus signs and spaces after cleaning. If the phone field is not a plausible phone number, show it as plain text.
- Cap lengths (name 100, phone 30, email 200, message 2,000) and trim.
- Keep the Netlify honeypot (`bot-field`). Netlify's built-in spam filtering stays on.
- Return 200 with no secrets in any log line. Never log the webhook URL.
- Test with hostile input on staging (a message containing `<!channel>`, a link, and 10,000 characters) and show Asim the Slack result.

## 5. Dependencies

- Keep dependencies few. Commit the lockfile. Use exact or tightly pinned versions.
- Run `npm audit` before every staging review and before launch. Fix high and critical findings or explain them.
- No packages with install scripts you cannot explain. No browser extensions or analytics SDKs.

## 6. Third-party code

- No third-party scripts, iframes, fonts or embeds by default. Fonts are self-hosted.
- Anything added later goes in docs/THIRD-PARTY.md: what, why, what data it sends, whether it sets cookies. If it sets cookies it waits for consent.
- Any CDN script needs Subresource Integrity. Better: no CDN scripts.

## 7. What must never be published

Only the Astro `dist` folder is published. `docs/`, `CLAUDE.md`, `legacy/`, `_build/`, `scripts/`, source maps, `.git`, `.env*` and backups must not appear on the site. `scripts/check-security.mjs` requests these paths on staging and fails if any returns 200: `/CLAUDE.md`, `/docs/`, `/legacy/`, `/_build/`, `/.git/config`, `/.env`, `/netlify.toml`, `*.map`.

## 8. Transport

- HTTPS only. No mixed content. Canonical host is `https://palermohomes.com`.
- `http://` and `www.` versions must reach `https://palermohomes.com/` in one hop. Test on launch day.

## 9. Accounts (Asim)

- Turn on two-factor authentication on GitHub and Netlify.
- Use the minimum role you need. Never share the Slack webhook in chat.

## 10. Tests

- `npm run test:security BASE_URL` checks every header above and the unpublished-paths list.
- Run Mozilla Observatory and securityheaders.com on staging. Target grade A or better. Put the results in docs/QA-REPORT.md.
