import { defineConfig } from 'astro/config';
import { writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { SITE, isIndexable } from './src/lib/indexing.mjs';

// Writes robots.txt and the noindex header into dist after the build.
// Public files cannot do this because the content depends on the build environment.
function indexingFiles() {
  return {
    name: 'indexing-files',
    hooks: {
      'astro:build:done': ({ dir }) => {
        const out = fileURLToPath(dir);
        mkdirSync(out, { recursive: true });
        const indexable = isIndexable();
        const robots = indexable
          ? `User-agent: *\nAllow: /\n\nSitemap: ${SITE}/sitemap.xml\n`
          : `User-agent: *\nDisallow: /\n`;
        writeFileSync(out + 'robots.txt', robots);
        // Phase 4 adds the security headers to this file.
        const headers = indexable ? '' : `/*\n  X-Robots-Tag: noindex\n`;
        writeFileSync(out + '_headers', headers);
        console.log(`[indexing] ${indexable ? 'INDEXABLE (production)' : 'NOINDEX (not production)'}`);
      },
    },
  };
}

export default defineConfig({
  site: SITE,
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [indexingFiles()],
});
