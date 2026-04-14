# Inspiration Library

This folder stores structural layout references that influence (but are NOT copied into) generated sites.

## Purpose

The inspiration system gives the brand-strategist and frontend-dev concrete reference patterns
to draw from — section structures, composition ideas, visual rhythm patterns.

**RULE: Influence structure, never copy content.**

---

## Folder Structure

```
templates/inspiration/
  layouts/          → Section composition patterns (JSON or markdown description)
  visual-breaks/    → WOW section reference patterns
  hero-patterns/    → Hero variant reference layouts
```

---

## How to Use

When brand-strategist selects `layout_variation: editorial-list`, the frontend-dev can reference
`layouts/editorial-list.md` to understand the expected HTML pattern.

These are NOT templates — they are structural reference descriptions.

---

## Available Layout References

### editorial-list
```
Pattern: 1 featured item (full-width, horizontal) + N numbered items (list, no images)
Best for: SaaS, agencies, web studios, tech services
Key elements:
  - Featured: 60% text / 40% image, horizontal flex, gradient badge ("Más destacado")
  - Numbered items: large faded number (02, 03...) + title + chips, NO images
  - Visual effect: contrast between "hero service" and supporting services
```

### cards-horizontal
```
Pattern: Each service = full-width row, image alternates left/right
Best for: Healthcare, consulting, local services
Key elements:
  - Image: 40% width, full height, rounded on inside edge only
  - Content: 60% width, centered vertically, generous padding
  - Alternation: odd rows = image left, even rows = image right (flex-row-reverse)
  - Visual effect: natural reading rhythm, like a brochure
```

### stacked-list
```
Pattern: Numbered vertical list, dividers, NO images
Best for: Law, finance, ultra-minimal brands, coaching
Key elements:
  - Number: text-4xl font-black in primary color, fixed width (w-12)
  - Dividers: border-t between each item, generous vertical padding
  - Typography: title is the star — no images, no icons
  - Visual effect: editorial, confident, non-decorative
```

### masonry-mixed
```
Pattern: Asymmetric grid — wide + narrow cells alternate
Best for: Creative, fashion, portfolio, photography
Key elements:
  - Row 1: 1 wide card (col-span-2) + 1 narrow card
  - Row 2: 1 narrow + 1 wide (alternates)
  - Images: dominant, full-height within each cell
  - Visual effect: dynamic, gallery-like, non-uniform
```

---

## WOW Section References

### dark-metrics-band
```
Full-bleed dark section (matches --color-bg-dark)
4 counters: large animated number + label + subtle icon below
Horizontal layout at all breakpoints
Counter animation: JS increments from 0 to target over 1.5s when in viewport
```

### editorial-manifesto
```
Dark section, oversized brand statement (text-5xl+ font-black)
Left-aligned on desktop (not centered)
Decorative element: thin horizontal rule in brand color below text
Optional: subtle texture or noise overlay (opacity 0.03)
No CTA — this is a moment, not a conversion point
```

### browser-mockup-showcase
```
Dark section background
Browser chrome: top bar with 3 colored dots + fake URL bar
Content: screenshot or placeholder showing the product/result
Shadow: large blurred drop shadow for depth
Effect: makes the product/work tangible
```

### split-proof
```
50/50 grid — no padding between halves
Left half: dark background, headline + emotional claim
Right half: light background (brand-soft), stats or testimonial excerpt
Border between halves: 2px brand color
Visual effect: strong contrast, credibility proof adjacent to claim
```
