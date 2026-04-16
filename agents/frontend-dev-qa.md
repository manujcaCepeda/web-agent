# ✅ QA CHECKLIST (MANDATORY — run before output)

Run through EVERY item. If any fail → fix before returning HTML.

## STRUCTURE
- [ ] All sections from layout JSON are present
- [ ] Section order matches UX flow: Hero → Services → How It Works → CTA → Stats → Benefits → Badge Grid → Wow Section → Testimonials → FAQ → CTA → Contact
- [ ] No section repeated consecutively
- [ ] Backgrounds alternate: white → gray → brand-soft → gradient (never same twice in a row)

## HERO
- [ ] Correct variant rendered (cinematic | split-emotional | minimal-luxury)
- [ ] Hero image: `loading="eager"` (NOT lazy)
- [ ] Hero image: correct aspect ratio per variant
- [ ] Trust pill badge above headline (split-emotional only)
- [ ] Star rating + review count below CTAs (split-emotional only)
- [ ] Floating stat badge on image (split-emotional only)

## TYPOGRAPHY & EYEBROWS
- [ ] Every section has 3-level hierarchy: eyebrow pill → H2 → subtext
- [ ] Eyebrow uses `rounded-full + background tint` — NEVER plain colored text
- [ ] H2 minimum: `text-3xl md:text-4xl`
- [ ] No `font-600` — use `font-semibold` or `font-bold`
- [ ] Section header margin: `mb-10` NOT `mb-16`

## TRUST BLOCKS
- [ ] Stats bar: numbers `text-5xl md:text-6xl font-black` minimum
- [ ] Stats bar: 4 items with stagger delays (0/100/200/300ms)
- [ ] Badge grid: 4 badges present (Background Checked, Licensed & Insured, Free Consultation, 24/7 Support)
- [ ] Testimonials: real avatar photos (Unsplash), NOT initials
- [ ] Testimonials: each has name + role (e.g. "Daughter of client")
- [ ] Testimonials: ★★★★★ stars above every quote
- [ ] How It Works section: 3-step process with numbered circles present
- [ ] Wow Section: full-bleed background image with dark overlay + emotional quote

## MICRO UX
- [ ] `.btn-primary::after` shimmer CSS present
- [ ] `.icon-circle` + `.group:hover .icon-circle` CSS present
- [ ] All feature cards have `group` class
- [ ] Stagger delays on Benefits cards (0/100/200/300/400/500ms)
- [ ] IntersectionObserver removes: `opacity-0`, `translate-y-10`, `translate-y-6`
- [ ] Service cards: `group-hover:scale-105` or `img-zoom` on image

## IMAGES
- [ ] All images (except hero) have `loading="lazy"`
- [ ] All images have `onerror` fallback (brand gradient or initials)
- [ ] Service card images: `h-52` consistent height
- [ ] Testimonial avatars: `w-12 h-12 rounded-full object-cover`
- [ ] No broken image creates blank space

## FORMS & INTERACTION
- [ ] Select element: `appearance-none` + custom SVG chevron wrapper
- [ ] Contact form: EmailJS + WhatsApp dual channel
- [ ] WhatsApp float button present with pulse animation
- [ ] Mobile sticky CTA bar present (z-40, pb-safe)
- [ ] Mobile sticky CTA: single bar only (no duplicates)
- [ ] FAQ accordion: JS toggle with `max-height` + smooth transition

## SEO & META
- [ ] Favicon: SVG data URL (`data:image/svg+xml,...`)
- [ ] Schema.org: `url`, `foundingDate`, `telephone`, `email` all populated (no empty strings)
- [ ] Schema.org: `sameAs` is `[]` if no social links (not `["#","#","#"]`)
- [ ] Open Graph: title, description, image all set
- [ ] Twitter Card: present
- [ ] `<title>` includes location keyword

## RESPONSIVE
- [ ] Hero image: `order-first lg:order-last` on mobile (image appears above text on mobile)
- [ ] Footer: `pb-24 md:pb-6` for mobile sticky CTA clearance
- [ ] Body: `padding-bottom: 68px` on mobile, `0` on desktop (via media query)
- [ ] Nav hamburger menu functional on mobile
- [ ] All grids: `grid-cols-1` base, then md/lg breakpoints

---

## FINAL RULE

If it looks generic → REBUILD
If it feels repetitive → REBUILD
If it doesn’t feel premium → REBUILD