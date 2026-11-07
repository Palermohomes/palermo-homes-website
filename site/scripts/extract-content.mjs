// Phase 1 content extraction.
// Reads the old static export in ../legacy and writes content files into src/content/.
// Rules: extract exactly (no rewriting), no Divi markup, no files for 301 URLs
// (their useful text is moved into the target page), links point to final URLs only.
// Run from the site folder: node scripts/extract-content.mjs

import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import * as cheerio from 'cheerio';
import { imageSize } from 'image-size';

const SITE_DIR = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const ROOT = resolve(SITE_DIR, '..');
const LEGACY = join(ROOT, 'legacy');
const OUT = join(SITE_DIR, 'src', 'content');

// ---------- small helpers ----------

function parseCsv(text) {
  const rows = [];
  let row = [], cell = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; }
      else if (c === '"') q = false;
      else cell += c;
    } else if (c === '"') q = true;
    else if (c === ',') { row.push(cell); cell = ''; }
    else if (c === '\n') { row.push(cell); rows.push(row); row = []; cell = ''; }
    else if (c !== '\r') cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const [head, ...rest] = rows;
  return rest.filter((r) => r.length > 1).map((r) => Object.fromEntries(head.map((h, i) => [h, r[i] ?? ''])));
}

const plan = parseCsv(readFileSync(join(ROOT, 'docs', 'URL-PLAN.csv'), 'utf8'));
const current = Object.fromEntries(
  parseCsv(readFileSync(join(ROOT, 'docs', 'CURRENT-PAGES.csv'), 'utf8')).map((r) => [r.url, r]),
);
const planByUrl = Object.fromEntries(plan.map((r) => [r.url, r]));
const redirects = plan.filter((r) => r.action === '301');
const redirectMap = Object.fromEntries(redirects.map((r) => [r.url, r.final_url]));

const norm = (s) => s.replace(/\s+/g, ' ').trim();
const wordsOfText = (s) => (s.match(/[\p{L}\p{N}][\p{L}\p{N}'’$%.,\-]*/gu) || []).length;

function mdToPlain(md) {
  return md
    .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/<!--.*?-->/gs, ' ')
    .replace(/[*_#>|]/g, ' ')
    .replace(/^\s*-\s+/gm, ' ');
}
const wordsOfMd = (md) => wordsOfText(mdToPlain(md));

function urlToFile(url) {
  if (url === '/') return join(LEGACY, 'index.html');
  return join(LEGACY, url.replace(/^\/|\/$/g, ''), 'index.html');
}

let currentPageUrl = '/';
function fixHref(href) {
  if (!href) return href;
  let h = href.trim().replace(/^https?:\/\/(www\.)?palermohomes\.com/, '');
  if (h && !/^([a-z][a-z0-9+.-]*:|\/|#)/i.test(h)) {
    const u = new URL(h, 'https://palermohomes.com' + currentPageUrl);
    h = u.pathname + u.search + u.hash;
  }
  if (h === '') h = '/';
  h = h.replace(/(^|\/)index\.html(?=$|[?#])/, '$1');
  const m = h.match(/^([^#?]*)([?#].*)?$/);
  if (m && m[1].startsWith('/')) {
    let path = m[1];
    const withSlash = path.endsWith('/') || path.includes('.') ? path : path + '/';
    if (redirectMap[withSlash]) path = redirectMap[withSlash];
    else path = withSlash;
    return path + (m[2] || '');
  }
  return h;
}

// ---------- HTML to Markdown ----------

const SKIP_TAGS = new Set(['script', 'style', 'noscript', 'svg', 'iframe', 'video', 'audio', 'canvas', 'input', 'select', 'textarea', 'option', 'form', 'button', 'template']);
const SKIP_CLASS = /(^|\s)(crumb|crumbs|sep|hp)(\s|$)/;
const isHidden = ($, n) => $(n).attr('aria-hidden') === 'true';

function makeConverter($, state) {
  function inline(node) {
    let out = '';
    $(node).contents().each((_, n) => {
      if (n.type === 'text') { out += n.data.replace(/\s+/g, ' '); return; }
      if (n.type !== 'tag') return;
      const tag = n.name;
      if (SKIP_TAGS.has(tag)) return;
      const cls = $(n).attr('class') || '';
      if (SKIP_CLASS.test(cls)) return;
      if (tag === 'br') { out += '  \n'; return; }
      if (tag === 'img' || tag === 'picture') { const im = image(n); if (im) out += im; return; }
      const inner = inline(n);
      if (tag === 'strong' || tag === 'b') out += inner.trim() ? `**${inner.trim()}**` : '';
      else if (tag === 'em' || tag === 'i') out += inner.trim() ? `*${inner.trim()}*` : '';
      else if (tag === 'a') {
        const href = fixHref($(n).attr('href'));
        const t = inner.trim();
        out += href && t ? `[${t}](${href})` : inner;
      } else if (tag === 'span') out += ` ${inner} `;
      else out += inner;
    });
    return out;
  }

  function image(n) {
    const img = n.name === 'img' ? $(n) : $(n).find('img').first();
    if (!img.length) return '';
    const src = img.attr('src');
    if (!src) return '';
    const webp = n.name === 'picture' ? $(n).find('source[type="image/webp"]').first().attr('srcset') : $(n).parent().find('source[type="image/webp"]').first().attr('srcset');
    const rec = {
      src: fixHref(src),
      alt: (img.attr('alt') ?? '').trim(),
      width: Number(img.attr('width')) || null,
      height: Number(img.attr('height')) || null,
    };
    if (!rec.width || !rec.height) {
      try {
        const f = join(SITE_DIR, 'public', rec.src.split('?')[0]);
        const dim = imageSize(readFileSync(f));
        rec.width = dim.width; rec.height = dim.height;
        rec.dimsFrom = 'file';
      } catch { /* left null and reported */ }
    }
    if (webp) rec.webp = fixHref(webp.split(/\s+/)[0]);
    if (img.attr('fetchpriority') === 'high') rec.hero = true;
    state.images.push(rec);
    return `![${rec.alt}](${rec.src})`;
  }

  // Returns an array of markdown blocks for a node's children.
  function capture(node) {
    const saved = state.cur;
    const sub = { cls: 'sub', md: [] };
    state.cur = sub;
    blocks(node);
    state.cur = saved;
    return sub;
  }

  function blocks(node) {
    const out = { push: (...a) => state.cur.md.push(...a) };
    $(node).contents().each((_, n) => {
      if (n.type === 'text') {
        const t = norm(n.data);
        if (t) out.push(t);
        return;
      }
      if (n.type !== 'tag') return;
      const tag = n.name;
      const cls = $(n).attr('class') || '';
      if (SKIP_TAGS.has(tag)) {
        if (tag === 'form') state.notes.add('form markup not extracted (rebuilt as a component later)');
        else if (tag === 'iframe') {
          state.embeds.push({ src: $(n).attr('src') || '', title: ($(n).attr('title') || '').trim() });
          state.notes.add('iframe embeds (YouTube) saved in the embeds field, not rendered: third-party embeds need a written reason in docs/THIRD-PARTY.md');
        } else if (['svg', 'video', 'audio', 'canvas'].includes(tag)) state.notes.add(`${tag} element not extracted`);
        return;
      }
      if (SKIP_CLASS.test(cls) || isHidden($, n)) return;
      if (/^h[1-6]$/.test(tag)) {
        const text = norm(inline(n));
        if (!text) return;
        if (tag === 'h1') { state.h1s.push(text); return; }
        out.push('#'.repeat(Number(tag[1])) + ' ' + text);
        return;
      }
      if (tag === 'p') {
        const t = norm(inline(n)).replace(/ ?\n ?/g, '\n');
        if (t) out.push(cls.includes('eyebrow') ? `*${t}*` : t);
        return;
      }
      if (tag === 'ul' || tag === 'ol') {
        const items = [];
        $(n).children('li').each((i, li) => {
          const t = norm(inline(li));
          if (t) items.push((tag === 'ol' ? `${i + 1}. ` : '- ') + t);
        });
        if (items.length) out.push(items.join('\n'));
        return;
      }
      if (tag === 'table') {
        const rows = [];
        $(n).find('tr').each((_, tr) => {
          const cells = $(tr).children('th,td').map((_, c) => norm(inline(c)).replace(/\|/g, '/')).get();
          if (cells.length) rows.push('| ' + cells.join(' | ') + ' |');
        });
        if (rows.length) {
          const cols = rows[0].split('|').length - 2;
          rows.splice(1, 0, '|' + ' --- |'.repeat(cols));
          out.push(rows.join('\n'));
        }
        return;
      }
      if (tag === 'blockquote') {
        const sub = capture(n);
        if (sub.md.length) out.push(sub.md.join('\n\n').split('\n').map((l) => '> ' + l).join('\n'));
        return;
      }
      if (tag === 'details') {
        const q = norm(inline($(n).children('summary').first()));
        const ansEl = $(n).children().not('summary');
        const sub = { md: [] };
        ansEl.each((_, a) => {
          if (a.type === 'tag' && ['div', 'section'].includes(a.name)) sub.md.push(...capture(a).md);
          else if (a.type === 'tag' && a.name === 'p') sub.md.push(norm(inline(a)));
          else sub.md.push(norm(inline(a)));
        });
        const a = sub.md.filter(Boolean).join('\n\n');
        if (q) state.faqs.push({ q, a });
        return;
      }
      if (tag === 'img' || tag === 'picture') { const im = image(n); if (im) out.push(im); return; }
      if (tag === 'figure') {
        const im = image($(n).find('img').first()[0] || n);
        if (im) out.push(im);
        const cap = norm(inline($(n).find('figcaption').first()));
        if (cap) out.push(cap);
        return;
      }
      if (tag === 'a') {
        const href = fixHref($(n).attr('href'));
        const hasBlock = $(n).find('h1,h2,h3,h4,h5,h6,p,div,img,picture').length > 0;
        if (!hasBlock) {
          const t = norm(inline(n));
          if (t && href) out.push(`[${t}](${href})`);
          else if (t) out.push(t);
          return;
        }
        // Card style link: a heading, an image and some text inside one link.
        const sub = capture(n);
        const head = $(n).find('h2,h3,h4').first();
        const headText = norm(head.text());
        const label = $(n).attr('aria-label');
        sub.md = sub.md.map((b) => (headText && b.replace(/^#+ /, '') === headText && href ? b.replace(/^(#+ )(.*)$/, `$1[$2](${href})`) : b));
        out.push(...sub.md);
        if (href && !sub.md.some((b) => b.includes(`](${href})`))) out.push(`[${norm(label || n.attribs['title'] || 'More')}](${href})`);
        return;
      }
      if (tag === 'section') {
        const next = { cls: cls || 'section', md: [] };
        state.chunks.push(next);
        state.cur = next;
        blocks(n);
        state.cur = { cls: 'root', md: [] };
        state.chunks.push(state.cur);
        return;
      }
      if (/(^|\s)fact(\s|$)/.test(cls)) {
        const k = norm($(n).find('.k').text());
        const v = norm(inline($(n).find('.v').first()));
        if (k || v) out.push(`**${k}:** ${v}`);
        return;
      }
      if (tag === 'hr' || /et_pb_divider/.test(cls)) return;
      // generic container (div, article, main, span, etc.)
      blocks(n);
    });
  }

  return { blocks, inline };
}

function cleanDom($) {
  $('script, style, noscript, link, meta').remove();
  $('#site-nav, #site-footer, header#site-nav, footer#site-footer, .et-l--footer, [class*="_tb_footer"]').remove();
  $('.crumb, .crumbs, [aria-hidden="true"]').remove();
  return $('body');
}

// ---------- extract one legacy page ----------

function extractPage(url) {
  const file = urlToFile(url);
  if (!existsSync(file)) return null;
  currentPageUrl = url;
  const html = readFileSync(file, 'utf8');
  const $ = cheerio.load(html);
  const head = {
    title: norm($('title').first().text()),
    description: $('meta[name="description"]').attr('content') || '',
    canonical: $('link[rel="canonical"]').attr('href') || '',
  };
  const bgs = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)]
    .flatMap((m) => [...m[1].matchAll(/url\(['"]?([^)'"]*wp-content\/uploads[^)'"]*)['"]?\)/g)].map((x) => '/' + x[1].replace(/^\//, '').replace(/\?.*$/, '')))
    .filter((v, i, a) => a.indexOf(v) === i);
  const body = cleanDom($);
  $('[style*="url("]', body).each((_, el) => {
    const m = ($(el).attr('style') || '').match(/url\(['"]?([^)'"]*wp-content\/uploads[^)'"]*)['"]?\)/);
    if (m) { const v = '/' + m[1].replace(/^(\.\.?\/)+/, '').replace(/^\//, '').replace(/\?.*$/, ''); if (!bgs.includes(v)) bgs.push(v); }
  });
  // words "before": visible text of the cleaned page (no nav, footer, crumbs, form)
  const $c = cheerio.load($.html(body));
  $c('form').remove();
  const wordsBefore = wordsOfText(norm(cheerio.load($c('body').html().replace(/<[^>]+>/g, ' ')).text()));

  const state = { images: [], faqs: [], embeds: [], h1s: [], chunks: [], notes: new Set() };
  const conv = makeConverter($, state);
  state.cur = { cls: 'root', md: [] };
  state.chunks.push(state.cur);
  conv.blocks(body);
  // blocks() pushes new chunks for sections; text outside sections went to `first`
  return { url, head, bgs, state, wordsBefore, rawBytes: html.length };
}

// ---------- front matter ----------

function yamlValue(v) { return JSON.stringify(v); }
function frontMatter(obj) {
  let s = '---\n';
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined) continue;
    if (Array.isArray(v)) {
      if (!v.length) s += `${k}: []\n`;
      else s += `${k}:\n` + v.map((x) => `  - ${yamlValue(x)}`).join('\n') + '\n';
    } else s += `${k}: ${yamlValue(v)}\n`;
  }
  return s + '---\n';
}

// ---------- what each page becomes ----------

const CITY_OF = {
  'Kelowna': { name: 'Kelowna', parent: '/' },
  'West Kelowna': { name: 'West Kelowna', parent: '/service-areas/west-kelowna/' },
  'Lake Country': { name: 'Lake Country', parent: '/service-areas/lake-country/' },
  'Abbotsford': { name: 'Abbotsford', parent: '/service-areas/lower-mainland/' },
  'Vernon': { name: 'Vernon', parent: '/service-areas/vernon/' },
  'Penticton': { name: 'Penticton', parent: '/service-areas/penticton/' },
};
const slugify = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

function classify(url) {
  if (url === '/') return { coll: 'pages', file: 'home' };
  if (/^\/project\/[^/]+\/$/.test(url)) return { coll: 'projects', file: url.split('/')[2] };
  if (/^\/guides\/[^/]+\/$/.test(url)) return { coll: 'guides', file: url.split('/')[2] };
  if (/^\/neighborhoods\/[^/]+\/$/.test(url)) return { coll: 'locations', file: url.split('/')[2], kind: 'neighbourhood' };
  if (/^\/service-areas\/[^/]+\/$/.test(url)) return { coll: 'locations', file: url.split('/')[2], kind: 'city' };
  return { coll: 'pages', file: url.replace(/^\/|\/$/g, '').replace(/\//g, '-') };
}

// Merge map: redirected page -> where its useful text goes.
// heading: the H2 added on the target. skip: section classes that are navigation,
// calls to action or lists of links to other pages (not useful text).
const SKIP_IN_MERGE = ['svc-cta', 'svc-nearby', 'svc-tiles', 'svc-npages', 'svc-hoods', 'pv-cta', 'aw-cta', 'pv-hero'];
const MERGES = {
  '/services/custom-homes/': { to: '/', heading: 'Custom homes' },
  '/service-areas/kelowna/': { to: '/', heading: 'Kelowna' },
  '/neighborhoods/kettle-valley/': { to: '/neighborhoods/upper-mission/', heading: 'Kettle Valley' },
  '/projects/cabernet/': { to: '/service-areas/west-kelowna/', heading: 'Cabernet Way' },
  '/projects/malbec/': { to: '/service-areas/west-kelowna/', heading: 'Malbec Place' },
  '/projects/vineyard-estates/': { to: '/service-areas/west-kelowna/', heading: 'Vineyard Estates' },
  '/projects/touriga/': { to: '/project/touriga-place-1/', heading: null },
  '/projects/ledgestone/': { to: '/project/lakestone/', heading: null },
  '/projects/west-abbotsford/': { to: '/project/west-abbotsford/', heading: null },
  '/projects/eagle-mountain/': { to: '/neighborhoods/eagle-mountain/', heading: 'Eagle Mountain homes' },
  '/about/jaspal-sidhu/': { to: '/about/jas-sidhu/', heading: null },
};

function chunksToMd(chunks, { skip = [], demote = 0 } = {}) {
  const parts = [];
  for (const c of chunks) {
    if (skip.some((k) => c.cls.split(/\s+/).includes(k))) continue;
    for (const b of c.md) parts.push(demote ? b.replace(/^(#{1,6}) /gm, (_, h) => '#'.repeat(Math.min(6, h.length + demote)) + ' ') : b);
  }
  return parts.join('\n\n');
}

// ---------- main ----------

const report = { files: [], audit: [], merges: [], wordDiffs: [] };

// wipe and rebuild generated content so reruns are clean
rmSync(OUT, { recursive: true, force: true });
for (const d of ['pages', 'locations', 'projects', 'guides']) mkdirSync(join(OUT, d), { recursive: true });

const staying = plan.filter((r) => r.action === 'KEEP' || r.action === 'NEW');
const extracted = {};
for (const r of plan) {
  if (r.action === 'NEW') continue;
  const ex = extractPage(r.url);
  if (!ex) { report.audit.push({ url: r.url, issue: 'no legacy file found' }); continue; }
  extracted[r.url] = ex;
}

// Build content objects for staying pages
const content = {};
for (const r of staying) {
  const url = r.url;
  const cls = classify(url);
  const cur = current[url];
  if (r.action === 'NEW') {
    const name = {
      '/privacy-policy/': 'Privacy Policy',
      '/terms-and-conditions/': 'Terms and Conditions',
      '/disclaimer/': 'Disclaimer',
      '/cookie-policy/': 'Cookie Policy',
    }[url];
    content[url] = {
      cls,
      fm: {
        url, title: `${name} | Palermo Homes`, description: `TODO(legal): ${name} for palermohomes.com. Replace after the legal text is reviewed.`, h1: name,
        datePublished: null, updated: null, status: 'draft', template: 'legal',
        images: [], faqs: [], mergedFrom: [],
      },
      body: `TODO(legal): placeholder. Real ${name.toLowerCase()} text must be reviewed by a lawyer or a BC-compliant generator (docs/OPEN-QUESTIONS.md #14).`,
      wordsBefore: 0, crawlWords: 0,
    };
    continue;
  }
  const ex = extracted[url];
  const st = ex.state;
  const h1Html = st.h1s[0] || '';
  const h1 = cur.h1 || h1Html;
  if (cur.h1 && h1Html && norm(cur.h1) !== norm(h1Html)) report.audit.push({ url, issue: `H1 in HTML differs from CURRENT-PAGES.csv: html="${h1Html}" csv="${cur.h1}". CSV kept.` });
  if (st.h1s.length !== 1) report.audit.push({ url, issue: `found ${st.h1s.length} H1 elements in the old page` });
  if (cur.title && norm(cur.title) !== ex.head.title) report.audit.push({ url, issue: `title in HTML differs from CSV: html="${ex.head.title}"` });

  const body = chunksToMd(st.chunks);
  const imgs = [];
  for (const im of st.images) if (!imgs.find((x) => x.src === im.src)) imgs.push(im);
  imgs.forEach((im, i) => { im.role = i === 0 && (im.hero || cls.coll === 'projects') ? 'hero' : im.hero ? 'hero' : 'content'; delete im.hero; });
  for (const im of imgs) {
    if (!im.alt) report.audit.push({ url, issue: `image without alt text: ${im.src}` });
    if (!im.width || !im.height) report.audit.push({ url, issue: `image without width or height: ${im.src}` });
  }
  const fm = {
    url,
    title: cur.title,
    description: cur.meta_description,
    h1,
    datePublished: cur.date_published || null,
    updated: cur.date_modified || null,
    status: 'published',
  };
  if (cls.coll === 'locations') {
    fm.kind = cls.kind;
    const note = r.note;
    if (cls.kind === 'neighbourhood') {
      const cityName = Object.keys(CITY_OF).find((c) => new RegExp(`^${c}\\.|\\. ?${c}\\.`).test(note)) ||
        Object.keys(CITY_OF).find((c) => note.startsWith(c));
      fm.city = cityName || null;
      fm.parent = cityName ? CITY_OF[cityName].parent : null;
    } else {
      fm.parent = '/service-areas/';
    }
  }
  if (cls.coll === 'projects') {
    const shows = (r.note.match(/Shows on ([^.]*)\./) || [])[1];
    fm.locations = shows ? shows.split(/ and |, /).map(slugify) : [];
    const mStreet = h1.match(/ (?:on|in) ([^,]+)(?:,|$)/);
    fm.street = mStreet ? mStreet[1] : null;
    const town = fm.locations.includes('west-kelowna') ? 'West Kelowna' : fm.locations.includes('lake-country') ? 'Lake Country' : fm.locations.includes('lower-mainland') ? 'Abbotsford' : null;
    fm.town = town;
  }
  if (cls.coll === 'guides') fm.author = 'Jas Sidhu';
  fm.template = cls.coll === 'pages' ? (url === '/' ? 'home' : 'page') : cls.coll.replace(/s$/, '');
  fm.images = imgs;
  fm.backgroundImages = ex.bgs;
  fm.faqs = st.faqs;
  if (st.embeds.length) fm.embeds = st.embeds;
  fm.mergedFrom = [];
  fm.crawlWords = Number(cur.words) || null;
  content[url] = { cls, fm, body, wordsBefore: ex.wordsBefore, extra: [...st.notes] };
  for (const n of st.notes) report.audit.push({ url, issue: n });
  if (ex.bgs.length) report.audit.push({ url, issue: `CSS background images not placed in the body (decorative, no alt): ${ex.bgs.join(', ')}` });
}

// Apply merges
for (const [from, m] of Object.entries(MERGES)) {
  const ex = extracted[from];
  const target = content[m.to];
  const entry = { from, to: m.to, heading: m.heading, moved: [], dropped: [] };
  if (!ex) {
    entry.dropped.push('No legacy page file exists for this URL (nothing to move).');
    report.merges.push(entry);
    continue;
  }
  if (!target) { entry.dropped.push(`TARGET MISSING: ${m.to}`); report.merges.push(entry); continue; }
  const st = ex.state;
  const h1 = current[from]?.h1 || st.h1s[0] || '';
  const targetPlain = norm(mdToPlain(target.body));
  const seen = (b) => targetPlain.includes(norm(mdToPlain(b)));
  const kept = [];
  const droppedSections = [];
  let cardsDropped = 0;
  let dupes = 0;
  for (const c of st.chunks) {
    if (SKIP_IN_MERGE.some((k) => c.cls.split(/\s+/).includes(k))) { droppedSections.push(c.cls); continue; }
    const blocksKept = c.md.filter((b) => {
      if (b.startsWith('![')) return false; // images handled below
      if (!norm(b)) return false;
      if (!/[\p{L}\p{N}]/u.test(b)) return false;
      if (from.startsWith('/projects/') && (/^#{1,6} \[[^\]]*\]\(\/project\//.test(b) || /^\*\d+ homes?\*$/.test(b) || /^[A-Z][A-Za-z ]+(, BC| · [A-Za-z ]+)$/.test(b))) { cardsDropped++; return false; }
      if (seen(b)) { dupes++; if (norm(mdToPlain(b)).split(' ').length > 3) entry.dropped.push(`already on target: "${norm(mdToPlain(b)).slice(0, 70)}"`); return false; }
      return true;
    });
    kept.push(...blocksKept);
  }
  // sections kept in the merged text
  const demoted = kept.map((b) => b.replace(/^(#{1,6}) /gm, (_, h) => '#'.repeat(Math.min(6, h.length + 1)) + ' '));
  let text = demoted.join('\n\n');
  if (m.heading && text) text = `## ${m.heading}\n\n<!-- moved from ${from} -->\n\n${text}`;
  else if (text) text = `<!-- moved from ${from} -->\n\n${text}`;
  if (text) {
    target.body += '\n\n' + text;
    entry.moved.push(`${wordsOfMd(text)} words of text and headings`);
  }
  // FAQs
  const faqMoved = [];
  for (const f of st.faqs) {
    if (!target.fm.faqs.find((x) => norm(x.q) === norm(f.q))) { target.fm.faqs.push(f); faqMoved.push(f.q); }
  }
  if (faqMoved.length) entry.moved.push(`${faqMoved.length} FAQ(s): ${faqMoved.join(' | ')}`);
  // images (skip card images of homes: they already live on the project pages)
  const isStreetCard = from.startsWith('/projects/') && ['/service-areas/west-kelowna/', '/neighborhoods/eagle-mountain/'].includes(m.to);
  const imgsMoved = [];
  const allKnown = new Set();
  for (const c of Object.values(content)) for (const im of c.fm.images) allKnown.add(im.src);
  for (const im of st.images) {
    if (target.fm.images.find((x) => x.src === im.src)) continue;
    if (isStreetCard && allKnown.has(im.src)) { entry.dropped.push(`image already on its project page: ${im.src}`); continue; }
    if (!im.alt) report.audit.push({ url: from, issue: `merged image without alt: ${im.src}` });
    const rec = { ...im, role: 'content' }; delete rec.hero;
    target.fm.images.push(rec);
    imgsMoved.push(im.src);
  }
  if (imgsMoved.length) entry.moved.push(`${imgsMoved.length} image(s): ${imgsMoved.join(', ')}`);
  if (cardsDropped) entry.dropped.push(`${cardsDropped} project card line(s) (home title links, home counts, location labels): rebuilt automatically as projects in this place`);
  if (droppedSections.length) entry.dropped.push(`sections dropped as navigation or calls to action: ${droppedSections.join(', ')}`);
  entry.dropped.push(`old H1 "${h1}" (title and H1 are replaced by the target's)`);
  entry.wordsSource = ex.wordsBefore;
  entry.crawlWords = Number(current[from]?.words) || null;
  target.fm.mergedFrom.push(from);
  report.merges.push(entry);
}

// Write files
for (const [url, c] of Object.entries(content)) {
  const fm = c.fm;
  const wordsAfter = wordsOfText(fm.h1) + wordsOfMd(c.body) + fm.faqs.reduce((n, f) => n + wordsOfText(f.q) + wordsOfMd(f.a), 0);
  fm.wordCount = wordsAfter;
  const dir = c.cls.coll;
  const faqsInFm = fm.faqs;
  const fmCopy = { ...fm };
  const file = join(OUT, dir, c.cls.file + '.md');
  writeFileSync(file, frontMatter(fmCopy) + '\n' + c.body.trim() + '\n');
  const before = c.wordsBefore;
  const diff = before ? ((wordsAfter - before) / before) * 100 : 0;
  report.files.push({ url, file: `src/content/${dir}/${c.cls.file}.md`, status: fm.status, before, after: wordsAfter, crawl: fm.crawlWords, diff, merged: fm.mergedFrom.length, faqs: faqsInFm.length });
  if (before && Math.abs(diff) > 5) report.wordDiffs.push({ url, before, after: wordsAfter, diff });
}

mkdirSync(join(SITE_DIR, '_tmp'), { recursive: true });
writeFileSync(join(SITE_DIR, '_tmp', 'extract-report.json'), JSON.stringify(report, null, 2));
console.log(`wrote ${report.files.length} content files, ${report.merges.length} merges, ${report.audit.length} audit items, ${report.wordDiffs.length} word diffs over 5 percent`);

// ---------- reports ----------

const pct = (n) => (n >= 0 ? '+' : '') + n.toFixed(1) + '%';
let mr = `# Merge report

Written by \`scripts/extract-content.mjs\`. Rerun the script to refresh it.

${redirects.length} rows in docs/URL-PLAN.csv are 301s: ${report.merges.length - 1} old pages whose text was merged, plus the Jas Sidhu rename (\`/about/jaspal-sidhu/\`, which has no old page). None of them gets a page or a content file. Before dropping each page, its useful text, headings, FAQs and images were moved into the target page's content file. \`/media/\` is not in this list: the client wants Media and Awards kept as two separate pages.

How it was done:

- Moved text sits at the end of the target body under its own H2 (where the old page had a topic of its own) with an HTML comment \`<!-- moved from /old-url/ -->\`. Headings from the old page are pushed down one level. Asim's page specs decide the final order and wording later.
- Text already present on the target was not copied again.
- Dropped on purpose: breadcrumbs, calls to action, lists of links to other pages (tiles, "nearby", neighbourhood lists) and project card lines. These are rebuilt automatically from the URL plan, so carrying them would only add links to redirected URLs.
- Moved FAQs are added to the target's \`faqs\` list. The FAQ heading text that sat above them in the old page is still in the body text.
- Every internal link in every content file is rewritten to the final URL, so no content file links to a redirected URL.
- The old title, meta description and H1 of a merged page are not carried. The target keeps its own.

| # | Old URL (301) | Target | Moved | Not moved |
|---|---------------|--------|-------|-----------|
`;
report.merges.forEach((m, i) => {
  mr += `| ${i + 1} | \`${m.from}\` | \`${m.to}\` | ${m.moved.length ? m.moved.join('<br>') : 'nothing'} | ${m.dropped.length ? m.dropped.join('<br>').replace(/\|/g, '/') : '-'} |\n`;
});
mr += `
## Notes

- \`/about/jaspal-sidhu/\` has no file in the old export and no row in docs/CURRENT-PAGES.csv. Search Console knows the URL, but there is no text to move. The 301 to \`/about/jas-sidhu/\` is in \`public/_redirects\`.
- The homepage now carries the text of \`/services/custom-homes/\` and \`/service-areas/kelowna/\` (the plan says the homepage owns custom homes and Kelowna). It grows from about 513 words to about ${content['/'].fm.wordCount}. This is expected. Asim's homepage spec decides what stays.
- \`/neighborhoods/upper-mission/\` carries the Kettle Valley text under its own H2 and its FAQs, since Kettle Valley sits inside Upper Mission.
- The three street pages (Cabernet Way, Malbec Place, Vineyard Estates) had one intro paragraph each. These went under their own H2 on \`/service-areas/west-kelowna/\`. The home cards on those pages were not moved because the same homes and photos already live on their project pages.
`;
writeFileSync(join(ROOT, 'docs', 'MERGE-REPORT.md'), mr);

const bgPages = Object.values(content).filter((c) => c.fm.backgroundImages?.length).map((c) => c.fm.url);
const borrowed = Object.values(content).filter((c) => /Portfolio match|Featured build/.test(c.body)).map((c) => c.fm.url);
const nullPub = Object.values(content).filter((c) => c.fm.status === 'published' && !c.fm.datePublished).map((c) => c.fm.url);
const nullUpd = Object.values(content).filter((c) => c.fm.status === 'published' && !c.fm.updated).map((c) => c.fm.url);
const longTitles = Object.values(content).filter((c) => c.fm.title.length > 60).map((c) => `${c.fm.url} (${c.fm.title.length})`);
const shortDesc = Object.values(content).filter((c) => c.fm.status === 'published' && c.fm.description.length < 120).map((c) => `${c.fm.url} (${c.fm.description.length})`);
const dimsFromFile = Object.values(content).reduce((n, c) => n + c.fm.images.filter((i) => i.dimsFrom).length, 0);

let ca = `# Content audit (Phase 1)

Written by \`scripts/extract-content.mjs\`. Rerun the script to refresh it.

## What was built

- ${report.files.length} content files in \`src/content/\` (${report.files.filter((f) => f.status === 'published').length} published, ${report.files.filter((f) => f.status === 'draft').length} draft). One per KEEP or NEW URL in docs/URL-PLAN.csv. None for the ${redirects.length} redirect rows.
- Numbers: 69 current pages. 59 stay (KEEP). 10 are merged into another page. 11 redirect rows (the 10 merged pages plus the Jas Sidhu rename). 4 new legal pages. 63 URLs after launch, 63 content files. \`/media/\` and \`/awards/\` stay as two separate pages (client decision).
- Collections: pages, locations (areas and neighbourhoods, with a \`parent\`), projects, guides. Schema in \`src/content.config.ts\`.
- Text was extracted as it was. Nothing was rewritten. No Divi markup, scripts or classes were carried. Internal links point to final URLs.
- Old nav, footer and breadcrumbs are not in the text. The header and footer are rebuilt from layouts.

## How word counts were taken

- "Crawl" is the word count in docs/CURRENT-PAGES.csv.
- "Before" is the visible text of the old page without its nav, footer, breadcrumbs and contact form, counted by this script.
- "After" is the H1, the body and the FAQs in the new content file.
- Limit: no page may shrink more than 5 percent without a logged reason.

## Pages that differ by more than 5 percent (After against Before)

`;
if (!report.wordDiffs.length) ca += 'None.\n';
else {
  ca += '| URL | Before | After | Change | Reason |\n|-----|--------|-------|--------|--------|\n';
  for (const d of report.wordDiffs) {
    const merged = content[d.url].fm.mergedFrom;
    ca += `| ${d.url} | ${d.before} | ${d.after} | ${pct(d.diff)} | grew: text merged in from ${merged.join(', ')} |\n`;
  }
}
const shrunk = report.files.filter((f) => f.before && f.diff < -5);
ca += `\nPages that shrank by more than 5 percent: ${shrunk.length ? shrunk.map((f) => f.url).join(', ') : 'none'}.\n`;
const contact = report.files.find((f) => f.url === '/contact/');
ca += `\nAgainst the crawl count, one page differs by more than 5 percent without a merge: \`/contact/\` (crawl ${contact.crawl}, after ${contact.after}). The gap is the form text (labels, placeholders, dropdown options, success message). The form is rebuilt as a component in Phase 2, so the words come back there.\n`;

ca += `
## Could not extract cleanly, or needs a decision

1. **Contact form.** The form markup is not extracted. It is rebuilt as a Netlify Forms component (fields and names in CLAUDE.md). The dropdown options in the old form were: Custom home, Renovation, General contracting, Not sure yet.
2. **Hero images set in CSS.** These pages used a CSS background for the hero, so there is no \`img\` tag, no alt text and no dimensions: ${bgPages.map((u) => `\`${u}\``).join(', ') || 'none'}. The file paths are saved in \`backgroundImages\`. Each needs a proper image with alt text when the page is built from Asim's spec.
3. **Missing dates.** The crawl has no \`date_published\` for ${nullPub.length} published pages: ${nullPub.map((u) => `\`${u}\``).join(', ')}. Their \`datePublished\` is \`null\`. ${nullUpd.length} of them also have no \`date_modified\` (${nullUpd.map((u) => `\`${u}\``).join(', ')}), so \`updated\` is \`null\` there too. Nothing was invented. The sitemap date of 2026-10-19 was not used because it is stamped on every page. See docs/OPEN-QUESTIONS.md. \`test:urls\` must fail at launch while a published page has a null date.
4. **Draft pages.** The four legal pages are \`status: draft\` with a \`TODO(legal)\` placeholder. Their titles and descriptions are placeholders too.
5. **Borrowed project blocks.** These pages still contain the old "Portfolio match" or "Featured build" text, which SEO-SPEC says to remove when the page is built (it shows projects from other places): ${borrowed.map((u) => `\`${u}\``).join(', ') || 'none'}. Left in place for now so no word is lost without a decision.
6. **Merged FAQ headings.** The heading above a merged FAQ block stays in the body text while the questions sit in the \`faqs\` field.
7. **Project pages.** Each has only the H1 and a gallery in the old build (about 36 words). The "Previous / Next" lines and the "Service area" text at the bottom are carried as text. Previous and next links are navigation and will be rebuilt automatically. Street, town and location tags come from docs/URL-PLAN.csv notes. Specs (size, bedrooms, year) are not on the old pages, so none exist. They are open question 10.
8. **Image sizes.** ${dimsFromFile} images in the old HTML had no width or height. The size was read from the file in \`public/wp-content/uploads/\` and saved. These are marked \`dimsFrom: "file"\`.
9. **Titles over 60 characters (kept as they are, not changed in Phase 1):** ${longTitles.join(', ') || 'none'}.
10. **Descriptions under 120 characters (kept as they are):** ${shortDesc.join(', ') || 'none'}.
11. **Title, H1 and description** come from docs/CURRENT-PAGES.csv. Differences between the old HTML and the CSV found by the script: ${report.audit.filter((a) => /differs/.test(a.issue)).length || 'none'}.
13. **YouTube embeds on \`/media/\`.** The old page has 4 YouTube iframes. They are saved in the \`embeds\` field (source and title) and are not rendered. Third-party embeds need a written reason in docs/THIRD-PARTY.md, and a plain YouTube embed sets cookies, which the launch rules forbid until a consent banner exists. Options for Phase 3: a click-to-load placeholder, a privacy-friendly embed, or plain links.
12. **Markup choices.** "Eyebrow" labels (short labels above headings) are kept as italic lines. Fact tiles are kept as bold label lines. Card links are kept as linked headings.

## Per page

| URL | Status | File | Crawl | Before | After | Change | FAQs | Merged in |
|-----|--------|------|-------|--------|-------|--------|------|-----------|
`;
for (const f of report.files) {
  ca += `| ${f.url} | ${f.status} | \`${f.file.replace('src/content/', '')}\` | ${f.crawl ?? '-'} | ${f.before || '-'} | ${f.after} | ${f.before ? pct(f.diff) : '-'} | ${f.faqs} | ${f.merged || '-'} |\n`;
}
const audit2 = report.audit.filter((a) => !/differs/.test(a.issue));
if (audit2.length) {
  ca += '\n## Script notes\n\n' + audit2.map((a) => `- \`${a.url}\`: ${a.issue}`).join('\n') + '\n';
}
writeFileSync(join(ROOT, 'docs', 'CONTENT-AUDIT.md'), ca);
console.log('wrote docs/MERGE-REPORT.md and docs/CONTENT-AUDIT.md');
