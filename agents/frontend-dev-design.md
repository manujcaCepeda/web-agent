## DESIGN LANGUAGE SYSTEM (CRITICAL — READ FIRST)

Before writing ANY code, read `style_mode` from **style-engine output** (NOT business-analyzer).
Then inject the matching CSS variables block into `<style>` in `<head>`.
Every color, radius, shadow, and spacing decision MUST follow the active mode.

---

### MODE: premium-care
*Warm, generous, human. Healthcare, senior care, wellness, family services.*
```css
:root {
  --color-primary: #2F7F79;
  --color-primary-dark: #236059;
  --color-primary-light: #3a9e97;
  --color-secondary: #A7D7C5;
  --color-secondary-light: #ceeae0;
  --color-accent: #F59E0B;
  --color-bg: #FAFFFE;
  --radius-card: 1rem;        /* rounded-2xl */
  --radius-button: 0.75rem;   /* rounded-xl */
  --radius-image: 1.5rem;     /* rounded-3xl */
  --shadow-card: 0 2px 12px rgba(47,127,121,0.08);
  --shadow-button: 0 8px 30px rgba(47,127,121,0.30);
}
body { background: var(--color-bg); font-family: 'Inter', sans-serif; }
```
Card style: `bg-white rounded-2xl border border-[rgba(167,215,197,0.25)] shadow-md hover:shadow-xl`
Section bg alternation: white → `#F0FAF7` → white → brand gradient
Hero bg: `linear-gradient(135deg, #f0faf7 0%, #e6f7f0 100%)`

---

### MODE: modern-clinic
*Clean, precise, data-driven. Medical clinics, dental, diagnostics, physio.*
```css
:root {
  --color-primary: #1E40AF;
  --color-primary-dark: #1e3a8a;
  --color-primary-light: #3B82F6;
  --color-secondary: #BFDBFE;
  --color-secondary-light: #EFF6FF;
  --color-accent: #10B981;
  --color-bg: #FFFFFF;
  --radius-card: 0.5rem;      /* rounded-lg */
  --radius-button: 0.5rem;    /* rounded-lg */
  --radius-image: 0.75rem;    /* rounded-xl */
  --shadow-card: 0 1px 4px rgba(0,0,0,0.06);
  --shadow-button: 0 4px 14px rgba(30,64,175,0.25);
}
body { background: var(--color-bg); font-family: 'Inter', sans-serif; }
```
Card style: `bg-white rounded-lg border border-slate-200 shadow-sm hover:shadow-md`
Section bg alternation: white → `#F8FAFC` → white → blue-50
Hero bg: `linear-gradient(135deg, #ffffff 0%, #eff6ff 100%)`
Data blocks: show numbers prominently — large font, blue accent

---

### MODE: luxury-service
*Exclusive, refined, authoritative. Law firms, finance, high-end consulting.*
```css
:root {
  --color-primary: #B8860B;
  --color-primary-dark: #8B6914;
  --color-primary-light: #D4A017;
  --color-secondary: #F5F0E8;
  --color-secondary-light: #FAF7F0;
  --color-accent: #C9A84C;
  --color-bg: #0A0A0A;
  --radius-card: 0.125rem;    /* rounded-sm */
  --radius-button: 0.125rem;  /* rounded-sm */
  --radius-image: 0.25rem;    /* rounded-md */
  --shadow-card: none;
  --shadow-button: 0 0 30px rgba(184,134,11,0.35);
}
body { background: var(--color-bg); font-family: 'Inter', sans-serif; color: #A8A8A8; }
h1, h2, h3 { font-family: 'Georgia', serif; color: #FFFFFF; }
```
Card style: `bg-[#111] rounded-sm border border-[rgba(184,134,11,0.2)] p-8`
Section bg: all dark — alternate `#0A0A0A` → `#111111` → `#0A0A0A`
Hero: always `minimal-luxury` variant — NO background image
Headings: serif font, white, very large (text-6xl to text-8xl on hero)
CTA: gold background with gold glow — `box-shadow: 0 0 30px rgba(184,134,11,0.35)`

---

### MODE: luxury-dark
*Tech premium, agency, SaaS, digital studio. Dark backgrounds, electric accents, glassmorphism.*
```css
:root {
  --color-primary: #06B6D4;         /* electric cyan — change per art_direction */
  --color-primary-dark: #0891B2;
  --color-primary-light: #22D3EE;
  --color-secondary: #1E293B;
  --color-secondary-light: #334155;
  --color-accent: #F97316;
  --color-bg: #0F172A;              /* deep navy dark */
  --color-bg-card: #1E293B;
  --color-text: #F8FAFC;
  --color-text-muted: #94A3B8;
  --radius-card: 0.75rem;
  --radius-button: 0.625rem;
  --radius-image: 1rem;
  --shadow-card: 0 0 0 1px rgba(6,182,212,0.12), 0 4px 24px rgba(0,0,0,0.4);
  --shadow-button: 0 0 30px rgba(6,182,212,0.4);
}
body { background: var(--color-bg); font-family: 'Inter', sans-serif; color: var(--color-text); }
```
Card style: `bg-[#1E293B] rounded-xl border border-[rgba(6,182,212,0.15)] hover:border-[rgba(6,182,212,0.4)] hover:shadow-[0_0_30px_rgba(6,182,212,0.15)] transition-all duration-300`
Section bg alternation: `#0F172A` → `#111827` → `#0F172A` → accent-gradient-band
Headlines: Use gradient text on hero H1: `bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent`
CTA primary: electric accent color with glow shadow
Glassmorphism: `bg-white/5 backdrop-blur-md border border-white/10`
NEVER use white body background in this mode — ALL sections dark or very dark.

---

### MODE: ultra-minimal
*Apple-like. Design studios, consultants, architects, photographers, premium coaches.*
```css
:root {
  --color-primary: #111111;
  --color-primary-dark: #000000;
  --color-primary-light: #333333;
  --color-secondary: #F5F5F5;
  --color-secondary-light: #FAFAFA;
  --color-accent: #2563EB;          /* only used sparingly */
  --color-bg: #FFFFFF;
  --color-text: #111111;
  --color-text-muted: #6B7280;
  --radius-card: 0rem;              /* sharp edges for ultra-minimal */
  --radius-button: 0.25rem;
  --radius-image: 0.5rem;
  --shadow-card: none;
  --shadow-button: none;
}
body { background: var(--color-bg); font-family: 'Inter', sans-serif; color: var(--color-text); }
```
Card style: `border-b border-gray-200 py-8` (list style, not box cards)
Section bg: pure white → near-white `#F9FAFB` → pure white. ONE black section for contrast.
Headlines: Oversized (text-6xl md:text-8xl), ultra-heavy or ultra-light weight contrast
Hero: Massive headline, minimal elements, tons of whitespace. No background image.
CTA: Black button with no shadow — clean and confident. Or outlined black border.
NEVER use rounded-2xl or heavy shadows — they break the minimal aesthetic.

---

### MODE: warm-local
*Restaurants, food, local services, artisans, family businesses, wellness.*
```css
:root {
  --color-primary: #C1440E;         /* terracotta — or use brief primary_color */
  --color-primary-dark: #A33A0C;
  --color-primary-light: #D4541A;
  --color-secondary: #FEF3E2;
  --color-secondary-light: #FFF8F3;
  --color-accent: #D97706;          /* amber */
  --color-bg: #FAFAF8;
  --color-text: #1C1917;
  --color-text-muted: #78716C;
  --radius-card: 1rem;
  --radius-button: 0.5rem;
  --radius-image: 1.5rem;
  --shadow-card: 0 2px 16px rgba(193,68,14,0.08);
  --shadow-button: 0 8px 30px rgba(193,68,14,0.30);
}
body { background: var(--color-bg); font-family: 'Inter', sans-serif; color: var(--color-text); }
```
Card style: `bg-white rounded-2xl shadow-sm border border-[#F5E6D0] hover:shadow-md`
Section bg: `#FAFAF8` → `#FFF8F3` → white → warm-dark-band (`#1C0F07`)
Hero: Photography-forward. Large warm-tinted image. Overlay with warm gradient.
Headlines: Rich, warm tones — use `--color-primary` for key words
Texture: Subtle grain or warm gradient overlays acceptable.

---

### MODE: corporate-trust
*Law, finance, insurance, clinics, accounting, established professional services.*
```css
:root {
  --color-primary: #0F2D52;         /* deep navy */
  --color-primary-dark: #091F3A;
  --color-primary-light: #1A4070;
  --color-secondary: #F0F4F9;
  --color-secondary-light: #F8FAFC;
  --color-accent: #B8960C;          /* gold */
  --color-bg: #FFFFFF;
  --color-text: #0F2D52;
  --color-text-muted: #64748B;
  --radius-card: 0.5rem;
  --radius-button: 0.375rem;
  --radius-image: 0.5rem;
  --shadow-card: 0 1px 8px rgba(15,45,82,0.08);
  --shadow-button: 0 4px 20px rgba(15,45,82,0.25);
}
body { background: var(--color-bg); font-family: 'Inter', sans-serif; color: var(--color-text); }
```
Card style: `bg-white rounded-lg border-l-4 border-[--color-accent] shadow-sm`
Section bg: white → `#F0F4F9` → dark navy band (`#0F2D52` with white text) → white
Authority signals: credentials bar, team section, years of experience as featured stat
Gold accent: use on borders, underlines, numbered list markers — not as fill color
NEVER use casual or playful design elements.

---

### MODE: creative-bold
*Creative agencies, fashion, events, youth brands, beauty, entertainment.*
```css
:root {
  --color-primary: #EC4899;         /* hot pink — override per brief */
  --color-primary-dark: #BE185D;
  --color-primary-light: #F472B6;
  --color-secondary: #FDF4FF;
  --color-secondary-light: #FEFCE8;
  --color-accent: #FACC15;          /* electric yellow */
  --color-bg: #FFFBF0;             /* warm cream — not plain white */
  --color-text: #0F0F0F;
  --color-text-muted: #6B7280;
  --radius-card: 1.5rem;
  --radius-button: 9999px;         /* pill buttons */
  --radius-image: 2rem;
  --shadow-card: 4px 4px 0px 0px #0F0F0F;  /* bold offset shadow */
  --shadow-button: 4px 4px 0px 0px #0F0F0F;
}
body { background: var(--color-bg); font-family: 'Inter', sans-serif; color: var(--color-text); }
```
Card style: `bg-white rounded-3xl border-2 border-black shadow-[4px_4px_0_#000]`
Section bg: cream → full-bleed color block → cream → black section
Bold moves: oversized typography, diagonal dividers, overlapping elements
CTA: Pill-shaped with bold offset shadow — NOT standard rounded-lg button

---

---

## TYPOGRAPHY SYSTEM BY MODE (CRITICAL — INJECT IN `<head>` BEFORE TAILWIND)

Typography is 40% of visual differentiation. Every mode MUST load its own font pair.
Inject the Google Fonts `<link>` tag as the FIRST item inside `<head>`, before Tailwind CDN.

DO NOT use generic `font-family: 'Inter'` for all modes — that is the #1 cause of all sites looking identical.

### Font pair matrix

| `style_mode` | Heading font | Body font | Character |
|---|---|---|---|
| `premium-care` | Nunito | Inter | Warm, round, accessible — friendly authority |
| `modern-clinic` | Inter (800 tight) | Inter | Clinical precision — size and weight are the style |
| `luxury-service` | DM Serif Display | Inter Light | Authoritative, refined, old-money serif |
| `luxury-dark` | Space Grotesk | Inter | Technical, modern, electric — geometric punch |
| `ultra-minimal` | Inter (extreme contrast) | Inter Light | 900 vs 200 weight contrast IS the identity |
| `warm-local` | Playfair Display | Lato | Editorial, artisanal, warm — feels handcrafted |
| `corporate-trust` | Inter (900, tight) | Inter | Data-driven authority — weight contrast IS the identity. No serif. |
| `creative-bold` | Syne | Inter | Expressive, asymmetric — creativity as identity |

### Google Fonts imports (copy exactly for active mode)

**premium-care:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```
```css
body { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4 { font-family: 'Nunito', sans-serif; font-weight: 800; }
```

**luxury-dark:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
```
```css
body { font-family: 'Inter', sans-serif; font-weight: 300; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; font-weight: 700; letter-spacing: -0.02em; }
```

**luxury-service:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
```
```css
body { font-family: 'Inter', sans-serif; font-weight: 300; color: #A8A8A8; }
h1, h2, h3 { font-family: 'DM Serif Display', serif; font-weight: 400; color: #FFFFFF; letter-spacing: -0.01em; }
```

**ultra-minimal:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;700;900&display=swap" rel="stylesheet">
```
```css
body { font-family: 'Inter', sans-serif; font-weight: 400; }
/* Ultra-minimal: EXTREME weight contrast is the identity */
h1 { font-family: 'Inter', sans-serif; font-weight: 900; letter-spacing: -0.04em; }
h2 { font-family: 'Inter', sans-serif; font-weight: 200; letter-spacing: 0.06em; text-transform: uppercase; }
/* Alternate: some H2s use 900 weight — use contrast intentionally */
```

**warm-local:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Lato:wght@400;700&display=swap" rel="stylesheet">
```
```css
body { font-family: 'Lato', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif; font-weight: 700; }
h1 { font-weight: 900; }
```

**corporate-trust:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
```
```css
body { font-family: 'Inter', sans-serif; font-weight: 400; }
h1 { font-family: 'Inter', sans-serif; font-weight: 900; letter-spacing: -0.04em; line-height: 1.05; }
h2 { font-family: 'Inter', sans-serif; font-weight: 800; letter-spacing: -0.03em; line-height: 1.1; }
h3 { font-family: 'Inter', sans-serif; font-weight: 700; letter-spacing: -0.02em; }
/* NO Merriweather — weight contrast is the identity, not serif */
```

**creative-bold:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@400;500&display=swap" rel="stylesheet">
```
```css
body { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; letter-spacing: -0.02em; }
```

**modern-clinic:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```
```css
body { font-family: 'Inter', sans-serif; }
h1, h2 { font-family: 'Inter', sans-serif; font-weight: 800; letter-spacing: -0.02em; }
```

### TYPOGRAPHY INJECTION RULE
1. Identify `style_mode` from brand_strategy
2. Copy the exact `<link>` tags above for that mode
3. Inject them as the FIRST content inside `<head>` (before Tailwind CDN)
4. Add the mode-specific `body` and `h1/h2/h3` CSS rules inside the `<style>` block, AFTER the `:root {}` variables block
5. NEVER load multiple font families — only load the pair for the active mode

---

### ART DIRECTION INTEGRATION (CRITICAL)

You will receive `art_direction` from the business-analyzer.
READ IT BEFORE WRITING ANY CSS.

Rules:
1. `art_direction.color_palette.primary` OVERRIDES the mode default primary color
2. `art_direction.wow_sections` defines 2 sections you MUST implement with high visual impact
3. `art_direction.forbidden` lists patterns you MUST avoid for this specific site
4. `art_direction.layout_signature` describes the unique visual character — implement it

If `art_direction` is provided, the color_palette values take precedence over mode defaults.

---

### SECTION HEADER SPACING RULE
Section headers inside `py-12` sections MUST use `mb-10`, never `mb-16`.
`mb-16` (64px) + `py-12` padding = 112px of dead space before content reaches the user.
Formula: section padding ÷ 2 = max mb allowed. For py-12 → mb-10. For py-16 → mb-12.

### BENEFITS / FEATURE CARDS — HOVER RULE (CRITICAL)
Every feature/benefit card MUST have the `group` class for icon-circle hover to work.
Without `group`, the `.group:hover .icon-circle` CSS selector fires on NOTHING.
```html
<!-- CORRECT -->
<div class="group bg-gray-50 hover:bg-white rounded-2xl p-8 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 border border-transparent hover:border-[rgba(167,215,197,0.4)]">
  <div class="icon-circle w-14 h-14 rounded-2xl ...">{{icon}}</div>
```
```html
<!-- WRONG — icon-circle hover will never trigger -->
<div class="bg-gray-50 rounded-2xl p-8">
  <div class="w-14 h-14 rounded-2xl ...">{{icon}}</div>
```

### BENEFITS SECTION — LAYOUT VARIETY RULE
NEVER render all benefits as identical equal-size cards in a uniform grid. This creates a "list" feel, not a designed section.

**REQUIRED PATTERN: Featured first + mixed grid**

```html
<!-- Benefit 1: FEATURED — full width, dark bg, big number anchor -->
<div class="rounded-2xl overflow-hidden mb-6 reveal-element" style="background:#0F172A;">
  <div class="flex flex-col md:flex-row items-center">
    <!-- Left: big number or large icon as visual anchor -->
    <div class="flex-shrink-0 w-full md:w-48 flex items-center justify-center py-10 md:h-44"
      style="background:rgba(var(--color-primary-rgb),0.15);">
      <span class="font-black" style="font-size:5rem; color:var(--color-primary);">{{key_number}}</span>
    </div>
    <!-- Right: content -->
    <div class="flex-1 p-8">
      <span class="...badge...">Nuestra promesa #1</span>
      <h3 class="text-xl font-black text-white mb-2">{{benefit_1_title}}</h3>
      <p class="text-sm" style="color:rgba(255,255,255,0.55);">{{benefit_1_description}}</p>
    </div>
  </div>
</div>

<!-- Benefits 2-4: 3-col grid with standard cards -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-5">
  <!-- standard benefit cards -->
</div>

<!-- Benefits 5-6: 2-col horizontal cards (icon left + text right) -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
  <div class="flex items-start gap-5 p-6 rounded-xl ...">
    <div class="icon-circle ...">{{icon}}</div>
    <div><h3 ...>{{title}}</h3><p ...>{{description}}</p></div>
  </div>
</div>
```

**The key_number for the featured card** = the most impactful metric from the brief (e.g. "7" for 7 days, "5" for 5 years, etc.)

### TRUST BAND — VISUAL WEIGHT RULE
The trust band (id="trust") MUST have visual weight proportional to its position in the page flow. After a large dark section, a `py-8 border-y` strip is invisible.

**REQUIRED:** Use `py-12 md:py-16` with a soft indigo gradient background:
```html
<section id="trust" class="py-12 md:py-16" style="background:linear-gradient(135deg,#F5F7FF 0%,#EEF0FF 100%); border-top:1px solid rgba(79,70,229,0.08); border-bottom:1px solid rgba(79,70,229,0.08);">
  <div class="max-w-7xl mx-auto px-6">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
      <!-- Each trust item: icon square + large stat text + label -->
      <div class="flex flex-col items-center text-center gap-2 reveal-element">
        <div class="w-12 h-12 rounded-2xl flex items-center justify-center mb-1"
          style="background:rgba(79,70,229,0.1);">
          {{icon}}
        </div>
        <p class="text-2xl font-black" style="color:#0F172A;">{{stat_value}}</p>
        <p class="text-xs font-semibold uppercase tracking-wider" style="color:var(--color-text-muted);">{{stat_label}}</p>
      </div>
    </div>
  </div>
</section>
```
RULE: Each trust item shows a number/value at `text-2xl font-black` — NOT a small text label with an inline icon. Size = credibility.

### REVEAL ANIMATION CONSISTENCY RULE
Use ONLY `translate-y-10` for scroll-reveal elements — NEVER `translate-y-6` or other values.
The IntersectionObserver JS removes `opacity-0` and `translate-y-10` specifically.
Using a different translate class means the element will appear but stay offset visually.
EXCEPTION: Stats bar uses `translate-y-6` — ensure JS also removes it (add to classList.remove list).

### SELECT DROPDOWN RULE
NEVER use `appearance-none` on a `<select>` without adding a custom arrow SVG:
```html
<div class="relative">
  <select class="... appearance-none pr-10">...</select>
  <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4">
    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
    </svg>
  </div>
</div>
```

### DESIGN LANGUAGE RULES (ALL MODES)
* NEVER mix variables from different modes in the same site
* NEVER hardcode a color that belongs to a different mode
* If `style_mode` is missing from analysis → default to `premium-care`
* The mode controls: colors, radii, shadows, hero variant, section backgrounds
* Section headers: always use `--color-primary` for the eyebrow label (small caps above H2)

---

## GLOBAL DESIGN SYSTEM

* max-w-7xl mx-auto px-6
* responsive grid
* whitespace priority per mode (luxury-service uses more)

---

## SPACING

ALL sections default:

* py-12 md:py-16

Density modifier:

* compact → py-10 md:py-12
* normal → py-12 md:py-16 (default)
* spacious → py-16 md:py-20

NEVER use py-20 md:py-28 or larger as default — sections become too tall on desktop screens and cause bad UX on standard monitor sizes.

---

## 🎯 BRAND STRATEGY RENDERING (CRITICAL — NEW)

Before writing ANY HTML, read `brand_strategy` and apply:

### 1. Services section — dynamic layout based on `layout_variation`

**`editorial-list`**:
```html
<!-- Featured card: full-width, horizontal layout -->
<div class="flex flex-col lg:flex-row gap-0 rounded-2xl overflow-hidden shadow-xl mb-8">
  <div class="lg:w-3/5 p-10 flex flex-col justify-center bg-[--color-bg-card]">
    <span class="badge">Más solicitado</span>
    <h3 class="text-2xl font-bold mt-3 mb-4">{{services[0].name}}</h3>
    <p class="text-muted mb-6">{{services[0].description}}</p>
    <div class="flex flex-wrap gap-2"><!-- chip tags --></div>
  </div>
  <div class="lg:w-2/5 min-h-[280px] bg-cover bg-center"><!-- image --></div>
</div>
<!-- Remaining services: numbered list items -->
<div class="grid md:grid-cols-2 gap-6">
  <!-- For each remaining service: number badge (02, 03...) + title + description + chips -->
  <div class="flex gap-5 p-6 bg-[--color-bg-alt] rounded-xl">
    <span class="text-5xl font-black text-[--color-primary]/20 leading-none">02</span>
    <div>...</div>
  </div>
</div>
```

**`cards-horizontal`**:
```html
<!-- Each service: full-width row, image alternates L/R -->
<div class="flex flex-col md:flex-row gap-0 rounded-2xl overflow-hidden shadow-md mb-6 [even:flex-row-reverse]">
  <div class="md:w-2/5"><img ...></div>
  <div class="md:w-3/5 p-8 flex flex-col justify-center">...</div>
</div>
```

**`stacked-list`**:
```html
<!-- Numbered list with dividers — no images, typography-forward -->
<div class="divide-y divide-[--color-secondary]">
  <div class="py-8 flex gap-6 items-start">
    <span class="text-4xl font-black text-[--color-primary] w-12 shrink-0">01</span>
    <div>
      <h3 class="text-xl font-bold mb-2">{{service.name}}</h3>
      <p class="text-muted">{{service.description}}</p>
    </div>
  </div>
</div>
```

**`icon-columns`**:
```html
<!-- 4+ columns, icon + title + 1-line description — feature-list style, NOT cards -->
<div class="grid grid-cols-2 md:grid-cols-4 gap-6">
  <div class="text-center p-4">
    <div class="w-12 h-12 mx-auto mb-3 rounded-xl bg-[--color-primary]/10 flex items-center justify-center">
      <!-- icon svg -->
    </div>
    <h4 class="font-semibold text-sm mb-1">{{service.name}}</h4>
    <p class="text-xs text-muted">{{short description}}</p>
  </div>
</div>
```

**`masonry-mixed`** — Asymmetric grid: 1 large featured card + 2-3 smaller cards in first row, then swapped in second row. Visual weight varies intentionally:
```html
<!-- Masonry-mixed services — creative, portfolio, agency -->
<div class="space-y-6">
  <!-- Row 1: 1 large (2/3) + 1 small (1/3) -->
  <div class="grid md:grid-cols-3 gap-6">
    <!-- Large card — featured service -->
    <div class="md:col-span-2 group relative rounded-2xl overflow-hidden shadow-lg card-hover"
      style="min-height:360px;">
      <div class="img-zoom absolute inset-0">
        <img src="{{services[0]._image_url}}" alt="{{services[0].name}}"
          class="w-full h-full object-cover object-center"
          loading="lazy"
          onerror="this.onerror=null;this.style.background='linear-gradient(135deg,var(--color-secondary),var(--color-primary))';this.removeAttribute('src')">
      </div>
      <!-- Overlay gradient -->
      <div class="absolute inset-0" style="background:linear-gradient(to top, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.1) 60%);"></div>
      <!-- Content anchored to bottom -->
      <div class="absolute bottom-0 left-0 right-0 p-8">
        <span class="inline-block text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full mb-3"
          style="background:var(--color-primary); color:#fff;">{{eyebrow_badge}}</span>
        <h3 class="text-2xl md:text-3xl font-bold text-white mb-2">{{services[0].name}}</h3>
        <p class="text-white/70 text-sm leading-relaxed">{{services[0].description}}</p>
      </div>
    </div>
    <!-- Small card -->
    <div class="group relative rounded-2xl overflow-hidden shadow-md card-hover"
      style="min-height:360px;">
      <div class="img-zoom absolute inset-0">
        <img src="{{services[1]._image_url}}" alt="{{services[1].name}}"
          class="w-full h-full object-cover object-center"
          loading="lazy"
          onerror="this.onerror=null;this.style.background='linear-gradient(135deg,var(--color-secondary),var(--color-primary))';this.removeAttribute('src')">
      </div>
      <div class="absolute inset-0" style="background:linear-gradient(to top, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.1) 60%);"></div>
      <div class="absolute bottom-0 left-0 right-0 p-6">
        <h3 class="text-xl font-bold text-white mb-1">{{services[1].name}}</h3>
        <p class="text-white/65 text-sm">{{services[1].description}}</p>
      </div>
    </div>
  </div>
  <!-- Row 2: 1 small (1/3) + 1 large (2/3) — swapped weights -->
  <div class="grid md:grid-cols-3 gap-6">
    <!-- Small card -->
    <div class="group relative rounded-2xl overflow-hidden shadow-md card-hover"
      style="min-height:300px;">
      <div class="img-zoom absolute inset-0">
        <img src="{{services[2]._image_url}}" alt="{{services[2].name}}"
          class="w-full h-full object-cover object-center"
          loading="lazy"
          onerror="this.onerror=null;this.style.background='linear-gradient(135deg,var(--color-secondary),var(--color-primary))';this.removeAttribute('src')">
      </div>
      <div class="absolute inset-0" style="background:linear-gradient(to top, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.1) 60%);"></div>
      <div class="absolute bottom-0 left-0 right-0 p-6">
        <h3 class="text-xl font-bold text-white mb-1">{{services[2].name}}</h3>
        <p class="text-white/65 text-sm">{{services[2].description}}</p>
      </div>
    </div>
    <!-- Large card — second feature -->
    <div class="md:col-span-2 group relative rounded-2xl overflow-hidden shadow-lg card-hover"
      style="min-height:300px;">
      <div class="img-zoom absolute inset-0">
        <img src="{{services[3]._image_url}}" alt="{{services[3].name}}"
          class="w-full h-full object-cover object-center"
          loading="lazy"
          onerror="this.onerror=null;this.style.background='linear-gradient(135deg,var(--color-secondary),var(--color-primary))';this.removeAttribute('src')">
      </div>
      <div class="absolute inset-0" style="background:linear-gradient(to top, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.1) 60%);"></div>
      <div class="absolute bottom-0 left-0 right-0 p-8">
        <h3 class="text-2xl font-bold text-white mb-2">{{services[3].name}}</h3>
        <p class="text-white/70 text-sm leading-relaxed">{{services[3].description}}</p>
      </div>
    </div>
  </div>
  <!-- Row 3: remaining services in equal columns (if 5+) -->
  <!-- If fewer than 4 services total: skip row 2 and render only row 1 -->
</div>
```

**`cards-3`** (ONLY if brand_strategy explicitly specifies this):
Standard 3-column card grid with image top + content below.

---

### 2. Visual Break section — render based on `visual_break.type`

**`dark-metrics-band`** — Full-bleed dark section, 4 animated counters, headline + sub:
```html
<section class="py-20 md:py-28 relative overflow-hidden" style="background:#0A0A0A;">
  <!-- Ambient top glow line -->
  <div class="absolute top-0 left-0 right-0 h-px" style="background:linear-gradient(90deg, transparent, var(--color-primary), transparent); opacity:0.6;"></div>
  <div class="max-w-7xl mx-auto px-6">
    <!-- Optional section headline -->
    <div class="text-center mb-16">
      <h2 class="text-3xl md:text-4xl font-bold text-white mb-3">{{visual_break_headline}}</h2>
      <p class="text-white/50 max-w-xl mx-auto">{{visual_break_sub}}</p>
    </div>
    <!-- 4 metrics grid -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
      <div class="reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:0ms;">
        <p class="text-6xl md:text-8xl font-black leading-none mb-3" style="color:var(--color-primary);">{{stat_1_value}}</p>
        <p class="text-sm text-white/50 uppercase tracking-[0.15em] font-semibold">{{stat_1_label}}</p>
      </div>
      <div class="reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:100ms;">
        <p class="text-6xl md:text-8xl font-black leading-none mb-3" style="color:var(--color-primary);">{{stat_2_value}}</p>
        <p class="text-sm text-white/50 uppercase tracking-[0.15em] font-semibold">{{stat_2_label}}</p>
      </div>
      <div class="reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:200ms;">
        <p class="text-6xl md:text-8xl font-black leading-none mb-3" style="color:var(--color-primary);">{{stat_3_value}}</p>
        <p class="text-sm text-white/50 uppercase tracking-[0.15em] font-semibold">{{stat_3_label}}</p>
      </div>
      <div class="reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:300ms;">
        <p class="text-6xl md:text-8xl font-black leading-none mb-3" style="color:var(--color-primary);">{{stat_4_value}}</p>
        <p class="text-sm text-white/50 uppercase tracking-[0.15em] font-semibold">{{stat_4_label}}</p>
      </div>
    </div>
    <!-- Optional CTA inside dark band -->
    <div class="text-center mt-16">
      <a href="#contact" class="btn-primary inline-block px-10 py-4 text-base font-semibold">{{cta_primary}}</a>
    </div>
  </div>
  <!-- Ambient bottom glow line -->
  <div class="absolute bottom-0 left-0 right-0 h-px" style="background:linear-gradient(90deg, transparent, var(--color-primary), transparent); opacity:0.6;"></div>
</section>
```

**`editorial-manifesto`** — Oversized quote/statement, left-aligned, dark background. No grid:
```html
<section class="py-24 md:py-32 overflow-hidden relative" style="background:#0A0A0A;">
  <div class="max-w-6xl mx-auto px-6">
    <!-- Decorative quotation mark -->
    <div class="text-[180px] leading-none font-black select-none pointer-events-none mb-[-60px] ml-[-10px]"
      style="color:var(--color-primary); opacity:0.15; font-family:Georgia,serif;">"</div>
    <!-- The manifesto statement — left-aligned, massive -->
    <p class="text-4xl md:text-6xl xl:text-7xl font-black text-white leading-[1.1] tracking-tight max-w-5xl mb-12">
      {{brand_strategy_design_concept_or_brand_statement}}
    </p>
    <!-- Accent rule + attribution -->
    <div class="flex items-center gap-6">
      <div class="h-0.5 w-16" style="background:var(--color-primary);"></div>
      <p class="text-sm font-semibold uppercase tracking-widest" style="color:var(--color-primary);">{{business_name}}</p>
    </div>
  </div>
</section>
```

**`browser-mockup-showcase`** — Portfolio/product inside browser chrome, centered, with floating stats:
```html
<section class="py-20 md:py-28 relative overflow-hidden" style="background:var(--color-bg);">
  <div class="max-w-5xl mx-auto px-6">
    <!-- Section header -->
    <div class="text-center mb-12">
      <span class="inline-block text-sm font-semibold tracking-widest uppercase px-4 py-1.5 rounded-full mb-4"
        style="background:rgba(var(--badge-rgb,6,182,212),0.12); color:var(--color-primary);">{{eyebrow}}</span>
      <h2 class="text-3xl md:text-4xl font-bold mb-4" style="color:var(--color-text,#F8FAFC);">{{headline}}</h2>
    </div>
    <!-- Browser frame -->
    <div class="relative">
      <div class="rounded-xl overflow-hidden shadow-2xl" style="border:1px solid rgba(var(--badge-rgb,6,182,212),0.25);">
        <!-- Chrome bar -->
        <div class="flex items-center gap-2 px-4 py-3" style="background:#1E293B;">
          <span class="w-3 h-3 rounded-full bg-red-500 opacity-80"></span>
          <span class="w-3 h-3 rounded-full bg-yellow-400 opacity-80"></span>
          <span class="w-3 h-3 rounded-full bg-green-500 opacity-80"></span>
          <div class="flex-1 rounded-md mx-3 py-1 px-3 text-xs" style="background:#0F172A; color:rgba(255,255,255,0.4);">
            {{business_url_or_domain}}
          </div>
        </div>
        <!-- Image inside browser -->
        <img src="{{hero_image_url}}" alt="{{business_name}} — {{eyebrow}}"
          class="w-full object-cover object-top" style="max-height:480px;"
          loading="lazy"
          onerror="this.onerror=null;this.style.background='var(--color-secondary)';this.removeAttribute('src')">
      </div>
      <!-- Floating stat card — top left -->
      <div class="absolute -top-5 -left-5 bg-white rounded-xl shadow-xl px-5 py-4 z-10"
        style="min-width:150px; border:1px solid #F1F5F9;">
        <p class="text-xs font-bold uppercase tracking-widest mb-1" style="color:var(--color-text-muted,#94A3B8);">{{float_1_label}}</p>
        <p class="text-2xl font-extrabold" style="color:var(--color-primary);">{{float_1_value}}</p>
      </div>
      <!-- Floating stat card — bottom right -->
      <div class="absolute -bottom-5 -right-5 bg-white rounded-xl shadow-xl px-5 py-4 z-10"
        style="min-width:150px; border:1px solid #F1F5F9;">
        <p class="text-xs font-bold uppercase tracking-widest mb-1" style="color:var(--color-text-muted,#94A3B8);">{{float_2_label}}</p>
        <p class="text-2xl font-extrabold" style="color:var(--color-primary);">{{float_2_value}}</p>
      </div>
    </div>
  </div>
</section>
```

**`split-proof`** — 50/50: left dark panel with headline, right light panel with proof/results:
```html
<section class="overflow-hidden">
  <div class="grid md:grid-cols-2 min-h-[500px]">
    <!-- Left: dark panel — bold claim -->
    <div class="flex items-center px-12 py-16 md:py-20" style="background:#0A0A0A;">
      <div>
        <!-- Eyebrow -->
        <p class="text-xs font-bold uppercase tracking-[0.2em] mb-6" style="color:var(--color-primary);">{{eyebrow}}</p>
        <!-- Big bold claim -->
        <h2 class="text-4xl md:text-5xl font-black text-white leading-tight mb-6">{{concept_headline}}</h2>
        <p class="text-white/60 leading-relaxed mb-8">{{concept_description}}</p>
        <div class="h-0.5 w-16" style="background:var(--color-primary);"></div>
      </div>
    </div>
    <!-- Right: light panel — evidence/proof -->
    <div class="flex items-center px-12 py-16 md:py-20" style="background:var(--color-secondary-light,#F8FAFC);">
      <div class="w-full">
        <!-- Proof items: stats or testimonial excerpt -->
        <div class="space-y-8">
          <div class="flex items-start gap-5">
            <div class="w-12 h-12 rounded-xl flex-shrink-0 flex items-center justify-center"
              style="background:var(--color-secondary);">
              {{proof_icon_1}}
            </div>
            <div>
              <p class="text-3xl font-black mb-1" style="color:var(--color-primary);">{{proof_value_1}}</p>
              <p class="text-sm font-semibold" style="color:var(--color-text-muted,#64748B);">{{proof_label_1}}</p>
            </div>
          </div>
          <div class="flex items-start gap-5">
            <div class="w-12 h-12 rounded-xl flex-shrink-0 flex items-center justify-center"
              style="background:var(--color-secondary);">
              {{proof_icon_2}}
            </div>
            <div>
              <p class="text-3xl font-black mb-1" style="color:var(--color-primary);">{{proof_value_2}}</p>
              <p class="text-sm font-semibold" style="color:var(--color-text-muted,#64748B);">{{proof_label_2}}</p>
            </div>
          </div>
          <div class="flex items-start gap-5">
            <div class="w-12 h-12 rounded-xl flex-shrink-0 flex items-center justify-center"
              style="background:var(--color-secondary);">
              {{proof_icon_3}}
            </div>
            <div>
              <p class="text-3xl font-black mb-1" style="color:var(--color-primary);">{{proof_value_3}}</p>
              <p class="text-sm font-semibold" style="color:var(--color-text-muted,#64748B);">{{proof_label_3}}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

**`full-bleed-image`** — Edge-to-edge photo, minimal text overlay, emotional impact through image:
```html
<section class="relative min-h-[520px] md:min-h-[640px] flex items-end overflow-hidden">
  <!-- Full-bleed background image -->
  <img src="{{hero_image_url}}" alt="{{visual_break_concept}}"
    class="absolute inset-0 w-full h-full object-cover object-center"
    loading="lazy"
    onerror="this.onerror=null;this.style.background='linear-gradient(135deg,var(--color-secondary),var(--color-primary))';this.removeAttribute('src')">
  <!-- Gradient overlay — bottom-weighted for text legibility -->
  <div class="absolute inset-0" style="background:linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 50%, rgba(0,0,0,0.05) 100%);"></div>
  <!-- Minimal text overlay — bottom left anchored -->
  <div class="relative z-10 w-full max-w-7xl mx-auto px-6 pb-14 md:pb-20">
    <div class="max-w-2xl">
      <!-- Thin accent line above -->
      <div class="h-0.5 w-12 mb-6" style="background:var(--color-primary);"></div>
      <h2 class="text-4xl md:text-5xl font-black text-white leading-tight mb-4">{{concept_headline}}</h2>
      <p class="text-white/70 text-lg mb-8 max-w-lg">{{concept_description}}</p>
      <a href="#contact" class="btn-primary inline-block px-8 py-3 text-base font-semibold">{{cta_primary}}</a>
    </div>
  </div>
</section>
```

**`timeline-horizontal`** — Process steps in a horizontal scrollable strip, numbered, distinct rhythm:
```html
<section class="py-20 md:py-28 overflow-hidden" style="background:var(--color-bg);">
  <div class="max-w-7xl mx-auto px-6">
    <!-- Section header -->
    <div class="mb-14">
      <span class="inline-block text-sm font-semibold tracking-widest uppercase px-4 py-1.5 rounded-full mb-4"
        style="background:var(--color-secondary); color:var(--color-primary);">{{eyebrow}}</span>
      <h2 class="text-3xl md:text-4xl font-bold mb-3" style="color:var(--color-text,#111111);">{{headline}}</h2>
      <p class="text-base max-w-2xl" style="color:var(--color-text-muted,#6B7280);">{{subheadline}}</p>
    </div>
    <!-- Timeline strip — horizontal scroll on mobile, flex-row on desktop -->
    <div class="relative">
      <!-- Horizontal connector line (desktop only) -->
      <div class="hidden md:block absolute top-10 left-0 right-0 h-0.5" style="background:var(--color-secondary);"></div>
      <!-- Steps -->
      <div class="flex flex-col md:flex-row gap-10 md:gap-0 overflow-x-auto pb-4">
        <!-- Step 1 -->
        <div class="flex-1 min-w-[200px] md:px-8 reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:0ms;">
          <!-- Number circle — sits on the connector line -->
          <div class="w-20 h-20 rounded-full flex items-center justify-center text-2xl font-black mb-6 relative z-10 shadow-lg"
            style="background:var(--color-primary); color:#FFFFFF;">01</div>
          <h3 class="text-lg font-bold mb-2" style="color:var(--color-text,#111111);">{{step_1_title}}</h3>
          <p class="text-sm leading-relaxed" style="color:var(--color-text-muted,#6B7280);">{{step_1_description}}</p>
        </div>
        <!-- Step 2 -->
        <div class="flex-1 min-w-[200px] md:px-8 reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:150ms;">
          <div class="w-20 h-20 rounded-full flex items-center justify-center text-2xl font-black mb-6 relative z-10 shadow-lg"
            style="background:var(--color-primary); color:#FFFFFF;">02</div>
          <h3 class="text-lg font-bold mb-2" style="color:var(--color-text,#111111);">{{step_2_title}}</h3>
          <p class="text-sm leading-relaxed" style="color:var(--color-text-muted,#6B7280);">{{step_2_description}}</p>
        </div>
        <!-- Step 3 -->
        <div class="flex-1 min-w-[200px] md:px-8 reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:300ms;">
          <div class="w-20 h-20 rounded-full flex items-center justify-center text-2xl font-black mb-6 relative z-10 shadow-lg"
            style="background:var(--color-primary); color:#FFFFFF;">03</div>
          <h3 class="text-lg font-bold mb-2" style="color:var(--color-text,#111111);">{{step_3_title}}</h3>
          <p class="text-sm leading-relaxed" style="color:var(--color-text-muted,#6B7280);">{{step_3_description}}</p>
        </div>
        <!-- Step 4 (if exists) -->
        <div class="flex-1 min-w-[200px] md:px-8 reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:450ms;">
          <div class="w-20 h-20 rounded-full flex items-center justify-center text-2xl font-black mb-6 relative z-10 shadow-lg"
            style="background:var(--color-secondary); color:var(--color-primary);">04</div>
          <h3 class="text-lg font-bold mb-2" style="color:var(--color-text,#111111);">{{step_4_title}}</h3>
          <p class="text-sm leading-relaxed" style="color:var(--color-text-muted,#6B7280);">{{step_4_description}}</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

---

### 3. Spacing Scale — apply to ALL sections

| `spacing_scale` | Section padding |
|-----------------|-----------------|
| `compact` | `py-10 md:py-14` |
| `balanced` | `py-14 md:py-20` |
| `generous` | `py-20 md:py-28` |
| `editorial` | Hero `py-28+`, others vary — some `py-10`, some `py-24` |

---

### 4. Forbidden Patterns — active checks before writing HTML

For EACH item in `brand_strategy.forbidden_patterns`:

* If pattern = "3 identical rounded cards" → MUST NOT generate 3 visually identical card divs in a row
* If pattern = "centered h2+grid for every section" → alternate left-aligned headers
* If pattern = "all sections bg-gray-50/bg-white" → at least 2 sections must use brand color or dark bg
* If pattern = "primary color #2563EB" → NEVER use this hex anywhere in the HTML/CSS
* If pattern references a layout type → use a different layout type for that section

---
