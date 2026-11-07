import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Dates in the old crawl are missing for some pages. They stay null (never invented)
// and are listed in docs/OPEN-QUESTIONS.md. test:urls fails at launch if a published page still has null.
const isoDate = z.string().regex(/^\d{4}-\d{2}-\d{2}$/);

const image = z.object({
  src: z.string().startsWith('/'),
  alt: z.string().min(1, 'every image needs alt text'),
  width: z.number().int().positive(),
  height: z.number().int().positive(),
  webp: z.string().optional(),
  role: z.enum(['hero', 'content']),
  dimsFrom: z.string().optional(),
});

const faq = z.object({ q: z.string().min(1), a: z.string().min(1) });

const base = {
  url: z.string().regex(/^\/([a-z0-9-]+\/)*$/, 'lowercase, trailing slash'),
  title: z.string().min(10).max(80), // SEO target is 50 to 60; old indexed titles longer than that are kept and logged
  description: z.string().min(20).max(200),
  h1: z.string().min(1),
  datePublished: isoDate.nullable(),
  updated: isoDate.nullable(),
  status: z.enum(['published', 'draft']),
  template: z.string(),
  images: z.array(image),
  backgroundImages: z.array(z.string()).default([]),
  faqs: z.array(faq),
  embeds: z.array(z.object({ src: z.string().url(), title: z.string() })).optional(),
  related: z.array(z.string()).default([]),
  mergedFrom: z.array(z.string()),
  crawlWords: z.number().nullable().optional(),
  wordCount: z.number().optional(),
};

const dir = (name: string) => glob({ pattern: '*.md', base: `./src/content/${name}` });

export const collections = {
  pages: defineCollection({ loader: dir('pages'), schema: z.object(base) }),
  locations: defineCollection({
    loader: dir('locations'),
    schema: z.object({
      ...base,
      kind: z.enum(['city', 'neighbourhood']),
      city: z.string().nullable().optional(),
      parent: z.string().nullable(),
    }),
  }),
  projects: defineCollection({
    loader: dir('projects'),
    schema: z.object({
      ...base,
      locations: z.array(z.string()),
      street: z.string().nullable(),
      town: z.string().nullable(),
    }),
  }),
  guides: defineCollection({
    loader: dir('guides'),
    schema: z.object({ ...base, author: z.string() }),
  }),
};
