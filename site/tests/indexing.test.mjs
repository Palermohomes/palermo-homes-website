import { test } from 'node:test';
import assert from 'node:assert/strict';
import { isIndexable } from '../src/lib/indexing.mjs';

test('production on palermohomes.com is indexable', () => {
  assert.equal(isIndexable({ CONTEXT: 'production', URL: 'https://palermohomes.com' }), true);
});
test('production on another host is noindex', () => {
  assert.equal(isIndexable({ CONTEXT: 'production', URL: 'https://example.netlify.app' }), false);
});
test('branch deploy and previews are noindex', () => {
  assert.equal(isIndexable({ CONTEXT: 'branch-deploy', URL: 'https://palermohomes.com' }), false);
  assert.equal(isIndexable({ CONTEXT: 'deploy-preview', URL: 'https://palermohomes.com' }), false);
});
test('local build (no env) is noindex', () => {
  assert.equal(isIndexable({}), false);
});
test('bad URL is noindex', () => {
  assert.equal(isIndexable({ CONTEXT: 'production', URL: 'not a url' }), false);
});
