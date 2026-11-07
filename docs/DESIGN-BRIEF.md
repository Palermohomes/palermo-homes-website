# Design brief

## Goal

A calm, premium, photo-led site that makes a home buyer feel this builder is careful and established, and makes the next step (call or book a consultation) obvious on every screen. The client gave a free hand. Two fixed points: keep the Palermo logo as is, and design for mobile first.

## Audience

Homeowners in Kelowna and the Okanagan planning a custom home, a major renovation, or hiring a general contractor. They compare two or three builders, look at photos first, check proof (licence, warranty, finished homes, reviews), then call. Many arrive on a phone.

## Feel

- Quiet confidence. Generous white space, large photography, restrained colour.
- Colour comes from the logo blue plus neutral warm greys. One accent for buttons. Propose exact values after looking at the logo and the current site.
- Type: one clean sans-serif for body, optionally one serif for headings. Self-hosted. Large body text (17 to 18 px on mobile).
- Motion: almost none. A soft fade on images is the limit. Respect `prefers-reduced-motion`.

## Must-have elements

- Header: logo, short menu, click-to-call phone on mobile, "Book a consultation" button.
- Sticky mobile bar with Call and Book buttons (hides while the form is on screen).
- Trust bar near the top of money pages (only confirmed facts).
- Project cards with a large photo, street and town, and style. Galleries that load fast and open full-screen.
- A consistent call to action band before the footer on every page.
- Footer with phone, email, service areas, legal links.

## Avoid

- Stock photography, sliders and carousels as the main hero, auto-playing video, pop-ups, chat widgets, and heavy animation libraries.
- Anything that sets cookies before consent.
- Walls of text. Break copy with headings, short paragraphs and photos.

## Process

1. Read the logo, the current homepage and two project pages.
2. Propose design tokens (colours, type scale, spacing, radius) and a homepage layout as a static preview on staging.
3. Wait for Asim's approval. Then build the shared components and templates.
