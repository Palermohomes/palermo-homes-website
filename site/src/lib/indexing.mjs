// Indexing is opt-in. A build is indexable only on the real production site.
export const SITE = 'https://palermohomes.com';

export function isIndexable(env = process.env, site = SITE) {
  if (env.CONTEXT !== 'production') return false;
  if (!env.URL) return false;
  try {
    return new URL(env.URL).hostname === new URL(site).hostname;
  } catch {
    return false;
  }
}
