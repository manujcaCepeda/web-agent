## 🖼️ IMAGE CONTROL SYSTEM (CRITICAL — REPLACES RANDOM IMAGES)

### Rule 1: NEVER generate Unsplash URLs

NEVER call `source.unsplash.com`, `images.unsplash.com` with your own query parameters,
or generate any image URL that doesn't come from the provided data.

### Rule 2: Use ONLY provided image URLs

Images are pre-resolved and injected by the pipeline. Priority (highest to lowest):
1. `services[n]._image_url` — final resolved URL for each service card (use VERBATIM — already prioritized)
   - Priority inside pipeline: (a) brief.json `image_url` per service → (b) client assets/images/services/ → (c) curated library
2. `hero_img` — the hero image URL (provided verbatim)
3. `brand_strategy.image_direction` hints — determines HOW to use images, not WHICH

### Logo rules:
- **Header logo** (`logo` variable): Full logo with business name text — use as-is with `class='h-10 w-auto'`
- **Footer logo** (`logo_footer` variable): Compact icon version — use with `class='h-12 w-auto brightness-0 invert'`
- Both paths are pre-resolved relative to output/ — copy them VERBATIM, never modify

### Rule 3: image_direction behavior

| Direction | How to render images |
|-----------|---------------------|
| `photography-forward` | Full bleed, large, emotional. Overlay is light or none. |
| `product-showcase` | Inside browser mockup frame or device frame. Shows UI. |
| `illustration-icon` | Use SVG icons instead of photos. No `<img>` for service cards. |
| `minimal-no-image` | Hero has NO `<img>` — typography only. Cards have NO images. |
| `dark-glow` | Images with dark overlay + glow effect. `box-shadow: 0 0 40px rgba(primary,0.3)` |

### Rule 4: Fallback strategy

Every `<img>` MUST have:
```html
onerror="this.onerror=null;this.style.background='{{fallback_gradient}}';this.removeAttribute('src')"
```

If `image_direction` is `illustration-icon` or `minimal-no-image`:
→ Do NOT include `<img>` tags for service cards. Use SVG icons instead.

---

## 🎯 VARIATION SYSTEM (CRITICAL)

You MUST introduce controlled variation:

### Cards variation (per brand_strategy):

* radius: follows `--radius-card` CSS variable — NEVER hardcode `rounded-2xl` if mode uses `rounded-sm`
* shadow: follows `--shadow-card` CSS variable
* border: if `corporate-trust` mode → use `border-l-4 border-[--color-accent]`
* Never use same card HTML pattern for 3+ consecutive sections

### Section variation:

* alternate text alignment (left / center) — at least 2 sections left-aligned
* alternate image position (left / right) for split layouts
* alternate background: dark → light → brand-soft → dark (NEVER same bg 3 times in a row)

### CTA variation:

* filled / outline / gradient

NEVER repeat same style 3 times consecutively.

---

## 🎨 VISUAL RHYTHM

Background mapping:

* white → bg-white
* gray → bg-gray-50
* brand-soft → inline rgba secondary color
* gradient → bg-gradient-to-r from-primary to-secondary

---

## 🧠 IMAGE SYSTEM (PRO)

Images MUST use the `_image_url` field from each service object.

### CORE RULES
* ALWAYS use the exact URL provided in `_image_url` — never invent URLs
* NEVER use `source.unsplash.com` — it is deprecated and broken
* ALWAYS use `images.unsplash.com` with specific photo IDs
* NEVER use random Unsplash queries — only pre-verified curated URLs
* Add `onerror="this.style.background='linear-gradient(135deg,#A7D7C5,#2F7F79)';this.removeAttribute('src')"` to ALL img tags
* Add `loading="lazy"` to ALL images EXCEPT the hero (hero must load immediately)
* Hero image: `loading="eager"` — never lazy

---

## 🚫 IMAGE VALIDATION RULES (HARD RULES — NEVER VIOLATE)

### FORBIDDEN
- NEVER use `source.unsplash.com` — it is deprecated and returns random images
- NEVER construct image URLs from `image_query` fields
- NEVER generate your own Unsplash search URLs
- NEVER render an `<img>` without an `onerror` fallback
- NEVER use `loading="lazy"` on hero images (above the fold)
- NEVER use the same image URL in two different service cards

### MANDATORY for every `<img>` tag
```html
<!-- Correct pattern — ALL images must follow this -->
<img
  src="[EXACT URL PROVIDED IN INPUT]"
  alt="[descriptive alt text]"
  class="..."
  loading="lazy"
  onerror="this.onerror=null;this.style.background='linear-gradient(135deg,#A7D7C5,#2F7F79)';this.removeAttribute('src');"
>
```

### IMAGE URL SOURCE HIERARCHY (follow in order)
1. Use the exact `<img>` tag provided in `SERVICE CARDS` section of your input
2. If not found → use the `_image_url` field in the service data
3. If not found → render a gradient div fallback:
   ```html
   <div class="w-full h-52 rounded-t-2xl" style="background:linear-gradient(135deg,#A7D7C5,#2F7F79);"></div>
   ```
4. NEVER proceed to any other source

### HEALTHCARE IMAGE CONTEXT CHECK
For healthcare sites, every image MUST show:
- Caregiver + elderly person interaction (NOT medical equipment, NOT surgery, NOT anatomy)
- Home environment (NOT hospital)
- Warm, human, emotional connection

If the provided URL fails this check → use the gradient fallback.

---

### IMAGE TREATMENT BY SECTION (MANDATORY)

Each section type has specific HTML treatment. Never reuse the same img class across all sections.

#### HERO (split-emotional variant)
```html
<img src="{{url}}" alt="{{alt}}"
  loading="eager"
  class="w-full h-[480px] lg:h-[560px] object-cover object-top"
  onerror="this.style.background='linear-gradient(135deg,#A7D7C5,#2F7F79)';this.removeAttribute('src')">
```
`object-top` ensures the face stays visible and is not cut. Use `object-center` only if image has centered subject.

#### HERO (cinematic variant)
```html
<img src="{{url}}" alt="{{alt}}"
  loading="eager"
  class="absolute inset-0 w-full h-full object-cover object-center"
  onerror="this.style.background='linear-gradient(135deg,#111,#333)';this.removeAttribute('src')">
```

#### SERVICE CARDS
```html
<!-- Wrapper — consistent height across ALL cards, NEVER mix heights -->
<div class="overflow-hidden h-52 relative img-zoom">
  <img src="{{url}}" alt="{{alt}}"
    loading="lazy"
    class="w-full h-full object-cover object-center"
    onerror="this.style.background='linear-gradient(135deg,#A7D7C5,#2F7F79)';this.removeAttribute('src')">
  <!-- Subtle brand overlay — bottom fade only -->
  <div class="absolute inset-0 pointer-events-none"
    style="background:linear-gradient(to top, rgba(47,127,121,0.30), transparent 60%);"></div>
</div>
```
CONSISTENCY RULE: All service card image wrappers MUST use `h-52`. Never `h-48`, `h-56`, or mixed heights — inconsistency breaks the grid rhythm.

#### TESTIMONIAL AVATARS
```html
<img src="{{avatar_url}}" alt="{{author_name}}"
  loading="lazy"
  class="w-12 h-12 rounded-full object-cover object-center flex-shrink-0"
  style="ring: 2px solid var(--color-secondary); outline: 2px solid var(--color-secondary); outline-offset: 2px;"
  onerror="this.style.background='var(--color-secondary)';this.removeAttribute('src')">
```

#### SECTION EYEBROW LABELS (visual hierarchy — CONTROLLED VARIATION)

**ANTI-PATTERN: Do NOT use the pill badge on every section.** Using the same `[pill] + [h2] + [p]` structure 9 times makes the user blind to all of them by section 3.

**RULE — Maximum 50% of sections may use the pill badge eyebrow.** Distribute across the page:

| Sections with pill badge | Sections WITHOUT pill (enter directly) |
|---|---|
| Services, Benefits, How-it-works, Pricing | Visual-break, Testimonials, Final CTA, Portfolio |

**Section header patterns — use VARIETY:**

```html
<!-- Pattern A: Full 3-level (pill + h2 + subtext) — use on structural sections -->
<div class="mb-10 reveal-element">
  <span class="inline-block text-xs font-bold tracking-widest uppercase px-4 py-1.5 rounded-full mb-4"
    style="background:rgba(79,70,229,0.08); color:var(--color-primary);">Section Label</span>
  <h2 class="text-3xl md:text-4xl font-black leading-tight" style="color:var(--color-text);">{{headline}}</h2>
  <p class="mt-3 text-base max-w-xl" style="color:var(--color-text-muted);">{{subtext}}</p>
</div>

<!-- Pattern B: Direct H2 only — use on high-impact sections (testimonials, CTA) -->
<div class="mb-10 reveal-element">
  <h2 class="text-3xl md:text-5xl font-black leading-tight" style="color:var(--color-text);">{{headline}}</h2>
  <p class="mt-4 text-lg" style="color:var(--color-text-muted);">{{subtext}}</p>
</div>

<!-- Pattern C: Large number + text — use on stats or process sections -->
<div class="mb-10 reveal-element">
  <p class="text-8xl font-black leading-none opacity-10 select-none" style="color:var(--color-primary);">01</p>
  <h2 class="text-3xl md:text-4xl font-black -mt-6" style="color:var(--color-text);">{{headline}}</h2>
</div>
```

RULE: Eyebrow pill MUST use `rounded-full + background tint`. Plain uppercase text with just color = visually weak.

**H2 color rule**: Section headings use `var(--color-text)` (dark navy), NOT `var(--color-primary)`. Primary color is for accents and CTAs only — if every heading is indigo, nothing stands out.

ANIMATION RULES (CRITICAL):

* NEVER use Tailwind `opacity-0`, `translate-y-10`, `translate-y-4` inline classes for reveal animations
* Use ONLY class `reveal-element` or `reveal` for scroll animations
* The CSS for `.reveal-element` and `.reveal` is defined in Part 1 — do not redefine it
* Using Tailwind opacity classes conflicts with the CSS animation system and creates invisible sections

SECTION RULES (CRITICAL — NO EXCEPTIONS):

* EVERY `<section>` tag MUST have both an opening and closing tag in the SAME part
* NEVER leave a section unclosed at the end of a part
* If you are running low on tokens: STOP adding new content, close ALL open tags (`</div></section>`), then add the part-end comment
* NEVER cut a section header mid-sentence — if you cannot complete a section, do not start it
* PARTIAL SECTIONS ARE WORSE THAN MISSING SECTIONS — an unclosed `<section>` breaks layout for everything below it

SECTION COMPLETION PRIORITY ORDER (Part 2):
1. Services section — REQUIRED (highest priority)
2. Visual break / metrics band — REQUIRED
3. Benefits section — complete with ALL cards or skip entirely
4. How-it-works — if process_steps data provided
5. Comparison — only if comparison data provided

SECTION COMPLETION PRIORITY ORDER (Part 3):
1. Testimonials — REQUIRED
2. FAQ — REQUIRED (at minimum 3 questions)
3. Final CTA section — REQUIRED
4. Contact section — REQUIRED (leads goal — cannot be skipped)
5. Footer — REQUIRED
6. WhatsApp button + Mobile CTA bar — REQUIRED
7. JavaScript block — REQUIRED (all JS in ONE script tag at end)

### CTA LABEL UNIQUENESS RULE (CRITICAL)
Every CTA button across the ENTIRE PAGE must have a DIFFERENT label. The same phrase repeated 4 times = invisible.

| Position | Label strategy |
|---|---|
| Header nav button | Short, action: "Empezar ahora" |
| Hero primary CTA | Specific benefit: "Reservar asesoría gratuita" |
| Visual-break / mid-page | Urgency: "Quiero mi sitio en 7 días" |
| Final CTA section | Closing push: "Hablemos hoy →" |
| Contact form submit | Clear: "Enviar mensaje" |

RULE: If the copywriter provides `cta_primary` as a single phrase, use it verbatim for the hero only. All other CTAs must be written as variations of the same intent — different words, same goal.

## 📧 CONTACT FORM — EMAILJS + WHATSAPP DUAL SUBMISSION

Every contact form MUST:
- Submit via **EmailJS** (keys injected by pipeline into JS instruction — copy verbatim)
- Then open **WhatsApp** with pre-filled message from form data
- Show a success message (`id="form-success"`) after send
- Fall back to WhatsApp-only if EmailJS fails

**Form field names (REQUIRED — EmailJS template depends on them):**
- Name: `name="from_name"` with `required`
- Phone: `name="phone"`
- Message: `name="message"`
- Submit button: `id="form-submit-btn"`
- Success paragraph: `id="form-success"` class `hidden`

**DO NOT** use `name="name"` — the EmailJS template uses `from_name`.
**DO NOT** add FormSubmit.co hidden fields.
**DO NOT** use `fetch()` for email — use `emailjs.sendForm()` with the keys from the JS instruction.

---

## 🎬 MICRO UX SYSTEM (PREMIUM)

ALWAYS inject this CSS block into `<style>` — it powers all micro interactions:

```css
/* ── Button Shimmer ── */
.btn-primary {
  position: relative;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.btn-primary::after {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.22), transparent);
  transition: left 0.5s ease;
  pointer-events: none;
}
.btn-primary:hover::after { left: 150%; }
.btn-primary:hover { transform: translateY(-1px); }
.btn-primary:active { transform: scale(0.97); }

/* ── Icon Circle Fill on Card Hover ── */
.icon-circle {
  transition: background 0.25s ease;
}
.group:hover .icon-circle {
  background: var(--color-primary) !important;
}
.group:hover .icon-circle svg {
  color: white;
  stroke: white;
}

/* ── Card lift ── */
.card-hover {
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.10);
}

/* ── Image zoom on hover ── */
.img-zoom {
  overflow: hidden;
}
.img-zoom img {
  transition: transform 0.5s ease;
}
.img-zoom:hover img {
  transform: scale(1.06);
}

/* ── Stagger reveal ── */
.reveal-on-scroll {
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal-on-scroll.visible {
  opacity: 1 !important;
  transform: translateY(0) !important;
}
```

### STAGGER SYSTEM (MANDATORY — apply to every card grid)
Every grid of cards MUST use consistent stagger delays via inline style:
```html
<div class="group card-hover ..." style="transition-delay: 0ms;">   <!-- card 1 -->
<div class="group card-hover ..." style="transition-delay: 100ms;">  <!-- card 2 -->
<div class="group card-hover ..." style="transition-delay: 200ms;">  <!-- card 3 -->
<div class="group card-hover ..." style="transition-delay: 300ms;">  <!-- card 4 -->
```
NEVER leave stagger delays undefined — inconsistent timing breaks the premium feel.

### HOVER RULES
* Cards: `card-hover` class (translateY -4px + shadow on hover)
* Images inside cards: wrap in `img-zoom` div
* Icon containers: class `icon-circle` → fills with primary color on group hover
* Buttons: `btn-primary` class gets shimmer automatically via CSS above
* Outline buttons: `transition-colors duration-200` — fill to brand color on hover

### ANIMATION RULES
* Scroll reveal: `reveal-on-scroll opacity-0 translate-y-6` + IntersectionObserver
* Stagger: always inline `style="transition-delay: Xms"` on each card
* NEVER use Tailwind opacity-0/translate-y inline for reveal — use reveal-on-scroll class only

---

## 🎥 ANIMATION SYSTEM

Use IntersectionObserver:

* opacity-0 translate-y-10
* reveal on scroll
* threshold: 0.1

Add stagger:

* delay-100
* delay-200
* delay-300

---
