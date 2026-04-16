## SECTION RENDERING

---

### HERO

⚠️ CRITICAL: You MUST use `hero_variant` from **hero-system output**.
DO NOT default to split-emotional or any other variant without reading hero-system.
DO NOT use `hero_variant` from ui-designer — hero-system is authoritative.

Render the matching variant below based on hero-system's `hero_variant` value.

---

#### VARIANT: CINEMATIC
Full-bleed image, dark overlay, centered white text. For restaurants, events, hospitality.
```html
<section class="relative min-h-[90vh] flex items-center overflow-hidden">
  <!-- Background image -->
  <img src="{{hero_image_url}}" alt="{{hero_alt}}" loading="eager"
    class="absolute inset-0 w-full h-full object-cover object-center">
  <!-- Dark gradient overlay — NEVER flat black -->
  <div class="absolute inset-0" style="background:linear-gradient(to bottom, rgba(0,0,0,0.25) 0%, rgba(0,0,0,0.65) 60%, rgba(0,0,0,0.80) 100%);"></div>
  <!-- Content centered -->
  <div class="relative z-10 max-w-4xl mx-auto px-6 text-center text-white">
    <!-- Trust pill -->
    <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold mb-8 border border-white/30 bg-white/10 backdrop-blur-sm">
      {{trust_badge_text}}
    </div>
    <h1 class="text-5xl md:text-7xl font-extrabold leading-tight tracking-tight mb-6">{{headline}}</h1>
    <p class="text-xl md:text-2xl text-white/80 leading-relaxed mb-10 max-w-2xl mx-auto">{{subheadline}}</p>
    <div class="flex flex-col sm:flex-row gap-4 justify-center">
      <a href="#contact" class="px-10 py-4 rounded-xl font-bold text-white text-lg" style="background:var(--color-primary);">{{cta_primary}}</a>
      <a href="#menu" class="px-10 py-4 rounded-xl font-semibold text-white text-lg border-2 border-white/50 hover:bg-white/10 transition-colors">{{cta_secondary}}</a>
    </div>
  </div>
  <!-- Bottom fade -->
  <div class="absolute bottom-0 left-0 right-0 h-32" style="background:linear-gradient(to bottom, transparent, rgba(0,0,0,0.4));"></div>
</section>
```

---

#### VARIANT: SPLIT EMOTIONAL (default — healthcare, services, wellness)
60% text / 40% image. Human face required. Floating stat badge on image.
Uses CSS variables — adapts to any style_mode automatically. DO NOT hardcode colors.
```html
<section class="py-14 md:py-20 overflow-hidden" style="background:linear-gradient(135deg, var(--color-bg) 0%, var(--color-secondary-light) 100%);">
  <div class="max-w-7xl mx-auto px-6">
    <div class="grid grid-cols-1 lg:grid-cols-[3fr_2fr] gap-12 xl:gap-16 items-center">

      <!-- Text column -->
      <div>
        <!-- Trust pill badge — uses mode secondary as background tint -->
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold mb-8"
          style="background:var(--color-secondary); color:var(--color-primary-dark); border:1px solid var(--color-secondary);">
          {{trust_badge_text}}
        </div>
        <!-- H1 — emotionally punchy, uses heading font from TYPOGRAPHY SYSTEM -->
        <h1 class="text-4xl md:text-5xl xl:text-6xl font-extrabold leading-tight tracking-tight mb-6"
          style="color:var(--color-text, #111111);">
          {{headline_line_1}}
          <span class="block mt-1" style="color:var(--color-primary);">{{headline_accent}}</span>
        </h1>
        <p class="text-lg md:text-xl leading-relaxed mb-8 max-w-2xl"
          style="color:var(--color-text-muted, #6B7280);">{{subheadline}}</p>
        <!-- CTAs -->
        <div class="flex flex-col sm:flex-row gap-4 mb-8">
          <a href="#contact" class="btn-primary px-8 py-4 text-base text-center">{{cta_primary}}</a>
          <a href="tel:{{phone}}" class="btn-outline px-8 py-4 text-base text-center">{{cta_secondary}}</a>
        </div>
        <!-- Star rating social proof — MANDATORY in split-emotional -->
        <div class="flex items-center gap-3">
          <div class="flex text-amber-400">★★★★★</div>
          <span class="text-sm font-semibold" style="color:var(--color-text-muted,#6B7280);">{{rating}} · {{reviews_count}}+ clients</span>
        </div>
      </div>

      <!-- Image column -->
      <div class="relative">
        <div class="overflow-hidden shadow-2xl" style="border-radius:var(--radius-image); border:3px solid var(--color-secondary);">
          <img src="{{hero_image_url}}" alt="{{hero_alt}}" loading="eager"
            class="w-full h-[480px] lg:h-[560px] object-cover object-top"
            onerror="this.onerror=null;this.style.background='linear-gradient(135deg,var(--color-secondary),var(--color-primary))';this.removeAttribute('src')">
          <div class="absolute inset-0" style="background:linear-gradient(180deg, transparent 55%, color-mix(in srgb, var(--color-primary) 15%, transparent) 100%); border-radius:var(--radius-image);"></div>
        </div>
        <!-- Floating stat badge — anchored bottom-left of image -->
        <div class="absolute -bottom-6 -left-6 bg-white rounded-2xl shadow-xl px-5 py-4 flex items-center gap-3 border border-gray-100 z-10">
          <div class="w-12 h-12 rounded-xl flex items-center justify-center"
            style="background:var(--color-secondary);">
            {{badge_icon_svg}}
          </div>
          <div>
            <p class="text-2xl font-extrabold leading-none" style="color:var(--color-primary);">{{badge_number}}</p>
            <p class="text-xs font-medium mt-0.5 leading-tight" style="color:var(--color-text-muted,#6B7280);">{{badge_label}}</p>
          </div>
        </div>
        <!-- Top-right decorative accent -->
        <div class="absolute -top-4 -right-4 w-24 h-24 rounded-full opacity-40 z-0"
          style="background:radial-gradient(circle, var(--color-secondary) 0%, transparent 70%);"></div>
      </div>

    </div>
  </div>
</section>
```

---

#### VARIANT: MINIMAL LUXURY
Solid background, no image, oversized typography. For law, finance, premium consulting.
```html
<section class="py-20 md:py-28 overflow-hidden bg-gray-950">
  <div class="max-w-6xl mx-auto px-6">
    <!-- Thin rule accent -->
    <div class="flex items-center gap-4 mb-12">
      <div class="h-px flex-1" style="background:var(--color-primary);opacity:0.4;"></div>
      <span class="text-xs font-bold tracking-[0.3em] uppercase" style="color:var(--color-primary);">{{trust_badge_text}}</span>
      <div class="h-px flex-1" style="background:var(--color-primary);opacity:0.4;"></div>
    </div>
    <!-- Oversized headline -->
    <h1 class="text-6xl md:text-8xl font-black text-white leading-none tracking-tight mb-8 max-w-4xl">
      {{headline_line_1}}<br>
      <span style="color:var(--color-primary);">{{headline_accent}}</span>
    </h1>
    <div class="flex flex-col md:flex-row gap-12 items-start md:items-end">
      <p class="text-lg md:text-xl text-white/60 leading-relaxed max-w-xl">{{subheadline}}</p>
      <div class="flex flex-col sm:flex-row gap-4 flex-shrink-0">
        <a href="#contact" class="px-10 py-4 rounded-xl font-bold text-white text-base"
          style="background:var(--color-primary);">{{cta_primary}}</a>
      </div>
    </div>
  </div>
</section>
```

---

#### VARIANT: BROWSER MOCKUP (luxury-dark, SaaS, digital agencies, tech startups)
Product inside browser frame. Left column text (40%) + right column browser mockup (60%).
Floating metric cards anchored to mockup corners. Dark background mandatory.
```html
<section class="py-16 md:py-24 overflow-hidden" style="background:var(--color-bg);">
  <div class="max-w-7xl mx-auto px-6">
    <div class="grid grid-cols-1 lg:grid-cols-[2fr_3fr] gap-16 items-center">

      <!-- Left: Text column -->
      <div>
        <!-- Category badge -->
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-bold tracking-widest uppercase mb-8"
          style="background:rgba(var(--badge-rgb,6,182,212),0.12); color:var(--color-primary); border:1px solid rgba(var(--badge-rgb,6,182,212),0.25);">
          {{trust_badge_text}}
        </div>
        <!-- Headline: large, tight, gradient on key word -->
        <h1 class="text-4xl md:text-5xl xl:text-6xl font-bold leading-[1.05] tracking-tight mb-6"
          style="color:var(--color-text,#F8FAFC);">
          {{headline_line_1}}<br>
          <span style="background:linear-gradient(90deg, var(--color-primary), var(--color-primary-light)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
            {{headline_accent}}
          </span>
        </h1>
        <p class="text-base md:text-lg leading-relaxed mb-10"
          style="color:var(--color-text-muted,#94A3B8);">{{subheadline}}</p>
        <!-- CTAs -->
        <div class="flex flex-col sm:flex-row gap-4 mb-10">
          <a href="#contact" class="btn-primary px-8 py-4 text-base font-semibold text-center">{{cta_primary}}</a>
          <a href="#services" class="px-8 py-4 text-base font-semibold text-center rounded-lg transition-colors"
            style="color:var(--color-primary); border:1px solid rgba(var(--badge-rgb,6,182,212),0.3);">{{cta_secondary}}</a>
        </div>
        <!-- 3 quick trust metrics: inline row -->
        <div class="flex gap-6">
          <div>
            <p class="text-2xl font-bold" style="color:var(--color-primary);">{{metric_1_value}}</p>
            <p class="text-xs" style="color:var(--color-text-muted,#94A3B8);">{{metric_1_label}}</p>
          </div>
          <div class="w-px" style="background:rgba(var(--badge-rgb,6,182,212),0.2);"></div>
          <div>
            <p class="text-2xl font-bold" style="color:var(--color-primary);">{{metric_2_value}}</p>
            <p class="text-xs" style="color:var(--color-text-muted,#94A3B8);">{{metric_2_label}}</p>
          </div>
          <div class="w-px" style="background:rgba(var(--badge-rgb,6,182,212),0.2);"></div>
          <div>
            <p class="text-2xl font-bold" style="color:var(--color-primary);">{{metric_3_value}}</p>
            <p class="text-xs" style="color:var(--color-text-muted,#94A3B8);">{{metric_3_label}}</p>
          </div>
        </div>
      </div>

      <!-- Right: Browser mockup -->
      <div class="relative">
        <!-- Browser frame -->
        <div class="rounded-xl overflow-hidden shadow-2xl" style="border:1px solid rgba(var(--badge-rgb,6,182,212),0.2);">
          <!-- Browser bar -->
          <div class="flex items-center gap-2 px-4 py-3" style="background:#1E293B;">
            <span class="w-3 h-3 rounded-full bg-red-500 opacity-80"></span>
            <span class="w-3 h-3 rounded-full bg-yellow-400 opacity-80"></span>
            <span class="w-3 h-3 rounded-full bg-green-500 opacity-80"></span>
            <div class="flex-1 rounded-md mx-3 py-1 px-3 text-xs" style="background:#0F172A; color:rgba(255,255,255,0.4);">
              {{business_url_or_domain}}
            </div>
          </div>
          <!-- Screenshot / hero image -->
          <img src="{{hero_image_url}}" alt="{{business_name}} platform"
            class="w-full object-cover object-top" style="max-height:420px;"
            loading="eager"
            onerror="this.onerror=null;this.style.background='var(--color-secondary)';this.removeAttribute('src')">
        </div>
        <!-- Floating stat card — top left -->
        <div class="absolute -top-4 -left-4 bg-white rounded-xl shadow-xl px-4 py-3 border border-gray-100 z-10"
          style="min-width:140px;">
          <p class="text-xs font-bold uppercase tracking-wide" style="color:var(--color-text-muted,#94A3B8);">{{float_card_1_label}}</p>
          <p class="text-xl font-extrabold mt-0.5" style="color:var(--color-primary);">{{float_card_1_value}}</p>
        </div>
        <!-- Floating stat card — bottom right -->
        <div class="absolute -bottom-4 -right-4 bg-white rounded-xl shadow-xl px-4 py-3 border border-gray-100 z-10"
          style="min-width:140px;">
          <p class="text-xs font-bold uppercase tracking-wide" style="color:var(--color-text-muted,#94A3B8);">{{float_card_2_label}}</p>
          <p class="text-xl font-extrabold mt-0.5" style="color:var(--color-primary);">{{float_card_2_value}}</p>
        </div>
        <!-- Ambient glow behind mockup -->
        <div class="absolute inset-0 -z-10 blur-3xl opacity-20 rounded-full"
          style="background:var(--color-primary); transform:scale(0.8);"></div>
      </div>

    </div>
  </div>
</section>
```

---

#### VARIANT: STATS HERO (corporate-trust, premium B2B, authority-driven services)
No full-width image. Headline + 4 large metric boxes as the primary visual element.
Numbers ARE the hero. Trust through data. Clean, commanding, data-dense.
```html
<section class="py-20 md:py-28" style="background:var(--color-bg);">
  <div class="max-w-6xl mx-auto px-6">

    <!-- Top: eyebrow + headline + sub -->
    <div class="max-w-3xl mb-16">
      <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-sm text-xs font-bold tracking-[0.2em] uppercase mb-8"
        style="color:var(--color-accent,#B8960C); border-bottom:2px solid var(--color-accent,#B8960C);">
        {{trust_badge_text}}
      </div>
      <h1 class="text-5xl md:text-7xl font-bold leading-[1.0] tracking-tight mb-8"
        style="color:var(--color-text,#0F2D52);">
        {{headline_line_1}}<br>
        <em style="color:var(--color-primary); font-style:italic;">{{headline_accent}}</em>
      </h1>
      <p class="text-lg leading-relaxed mb-10 max-w-xl" style="color:var(--color-text-muted,#64748B);">{{subheadline}}</p>
      <div class="flex gap-4">
        <a href="#contact" class="btn-primary px-10 py-4 text-base font-semibold">{{cta_primary}}</a>
        <a href="#services" class="px-10 py-4 text-base font-semibold rounded transition-colors"
          style="color:var(--color-primary); text-decoration:underline; text-underline-offset:4px;">{{cta_secondary}}</a>
      </div>
    </div>

    <!-- Bottom: 4 large metrics grid — THE HERO VISUAL -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-0 border-t border-b"
      style="border-color:var(--color-secondary,#F0F4F9);">
      <!-- Metric 1 -->
      <div class="py-10 px-8 border-r" style="border-color:var(--color-secondary,#F0F4F9);">
        <p class="text-6xl md:text-7xl font-black leading-none mb-3" style="color:var(--color-primary);">{{stat_1_value}}</p>
        <p class="text-sm font-semibold uppercase tracking-widest" style="color:var(--color-text-muted,#64748B);">{{stat_1_label}}</p>
      </div>
      <!-- Metric 2 -->
      <div class="py-10 px-8 border-r" style="border-color:var(--color-secondary,#F0F4F9);">
        <p class="text-6xl md:text-7xl font-black leading-none mb-3" style="color:var(--color-primary);">{{stat_2_value}}</p>
        <p class="text-sm font-semibold uppercase tracking-widest" style="color:var(--color-text-muted,#64748B);">{{stat_2_label}}</p>
      </div>
      <!-- Metric 3 -->
      <div class="py-10 px-8 border-r" style="border-color:var(--color-secondary,#F0F4F9);">
        <p class="text-6xl md:text-7xl font-black leading-none mb-3" style="color:var(--color-primary);">{{stat_3_value}}</p>
        <p class="text-sm font-semibold uppercase tracking-widest" style="color:var(--color-text-muted,#64748B);">{{stat_3_label}}</p>
      </div>
      <!-- Metric 4 -->
      <div class="py-10 px-8">
        <p class="text-6xl md:text-7xl font-black leading-none mb-3" style="color:var(--color-primary);">{{stat_4_value}}</p>
        <p class="text-sm font-semibold uppercase tracking-widest" style="color:var(--color-text-muted,#64748B);">{{stat_4_label}}</p>
      </div>
    </div>

  </div>
</section>
```

---

#### VARIANT: EDITORIAL STATEMENT (ultra-minimal, creative-bold, luxury-service)
Pure typography. Zero images. Asymmetric 2-column text layout.
Left: oversized headline (one or two words per line, massive scale).
Right: subheadline + CTA + decorative accent element.
The white space and font contrast IS the design.
```html
<section class="min-h-[85vh] flex items-center py-20" style="background:var(--color-bg);">
  <div class="max-w-7xl mx-auto px-6 w-full">
    <div class="grid grid-cols-1 lg:grid-cols-[3fr_2fr] gap-16 xl:gap-24 items-end">

      <!-- Left: Oversized headline — typographic statement -->
      <div>
        <!-- Decorative line above — thin brand accent -->
        <div class="w-16 h-0.5 mb-10" style="background:var(--color-primary);"></div>
        <h1 class="leading-[0.9] tracking-tight mb-0" style="color:var(--color-text,#111111);">
          <!-- Each key word on its own line, massive scale -->
          <span class="block text-6xl md:text-8xl xl:text-9xl font-black">{{headline_word_1}}</span>
          <span class="block text-6xl md:text-8xl xl:text-9xl font-black" style="color:var(--color-primary);">{{headline_word_2}}</span>
          <span class="block text-6xl md:text-8xl xl:text-9xl font-black">{{headline_word_3}}</span>
        </h1>
      </div>

      <!-- Right: Context + CTA — balanced, not competing -->
      <div class="lg:pb-4">
        <!-- Eyebrow / category -->
        <p class="text-xs font-bold tracking-[0.3em] uppercase mb-8" style="color:var(--color-primary);">
          {{trust_badge_text}}
        </p>
        <!-- Subheadline: readable, not oversized -->
        <p class="text-lg md:text-xl leading-relaxed mb-10"
          style="color:var(--color-text-muted,#6B7280);">{{subheadline}}</p>
        <!-- Primary CTA -->
        <a href="#contact" class="btn-primary inline-block px-10 py-4 text-base font-semibold mb-8">
          {{cta_primary}}
        </a>
        <!-- Secondary: text link only, minimal -->
        <div>
          <a href="#services" class="text-sm font-semibold"
            style="color:var(--color-primary); text-decoration:underline; text-underline-offset:4px;">
            {{cta_secondary}} →
          </a>
        </div>
        <!-- Decorative large number or year — optional flavor element -->
        <div class="mt-16 text-8xl font-black leading-none select-none pointer-events-none opacity-[0.06]"
          style="color:var(--color-text,#111111);">
          {{decorative_year_or_number}}
        </div>
      </div>

    </div>
  </div>
</section>
```

---

### HERO VARIANT → STYLE MODE MATRIX

Use this table to confirm `hero_variant` matches `style_mode`. Mismatch = wrong visual identity.

| `style_mode` | Primary hero_variant | Alternative |
|---|---|---|
| `premium-care` | `split-emotional` | — |
| `modern-clinic` | `split-emotional` | `stats-hero` |
| `luxury-service` | `minimal-luxury` | `editorial-statement` |
| `luxury-dark` | `browser-mockup` | `stats-hero` |
| `ultra-minimal` | `editorial-statement` | `minimal-luxury` |
| `warm-local` | `cinematic` | `split-emotional` |
| `corporate-trust` | `stats-hero` | `minimal-luxury` |
| `creative-bold` | `editorial-statement` | `cinematic` |

If `brand_strategy.hero_variant` is set → USE IT. This matrix is a fallback only.

---

HERO RULES (ALL VARIANTS):
* NEVER use a flat color overlay — always use a gradient
* NEVER center text on split-emotional — text is always left-aligned
* Star rating is MANDATORY on split-emotional hero
* Floating badge is MANDATORY on split-emotional hero image
* Hero image: loading="eager" — NEVER lazy on hero
* H1 copy must be emotionally punchy — if it reads like a tagline, REWRITE it
* Browser-mockup hero: ALWAYS dark background (--color-bg must be dark)
* Stats-hero: metrics must use real data from brief.json trust[] array — NEVER invented numbers
* Editorial-statement: H1 MUST have at least 3 lines — one key word per line, never all on one line

---

### SERVICES

* grid dynamic (3 or 4)
* cards with hover lift
* image zoom on hover

---

### BENEFITS

* icon + text alignment
* spacing clarity
* readable blocks

---

### PORTFOLIO

**TRIGGER:** Render when `section_order` includes `"portfolio"`. Required for `digital-agency` / `creative-studio` business types.

**CONCEPT:** Proof of work. A design agency that doesn't show its designs doesn't exist. This section is the single strongest trust signal — it makes every copywriting claim concrete and visual. Place it immediately after services.

**SECTION HEADER:** Pattern B (NO pill badge — enter directly with large H2):
```html
<div class="mb-12 reveal-element">
  <h2 class="text-4xl md:text-5xl font-black leading-tight mb-4" style="color:#0F172A;">
    Nuestro trabajo,<br>por sí solo.
  </h2>
  <p class="text-lg" style="color:var(--color-text-muted);">Proyectos reales. Resultados reales.</p>
</div>
```

**PORTFOLIO CARD BLUEPRINT (repeat for each `brief.portfolio[]` item):**
```html
<!-- ═══════════════════════════════════════ PORTFOLIO -->
<section id="portfolio" class="py-14 md:py-20 bg-gray-50">
  <div class="max-w-7xl mx-auto px-6">

    <!-- Header: Pattern B — no pill -->
    <div class="mb-12 reveal-element">
      <h2 class="text-4xl md:text-5xl font-black leading-tight mb-4" style="color:#0F172A;">
        Nuestro trabajo,<br>por sí solo.
      </h2>
      <p class="text-lg" style="color:var(--color-text-muted);">Proyectos reales. Resultados reales.</p>
    </div>

    <!-- 3-col project grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

      {{#each brief.portfolio}}
      <!-- Portfolio card -->
      <div class="group bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300 reveal-element"
        style="transition-delay:{{@index}}00ms; border:1px solid rgba(0,0,0,0.06);">

        <!-- Browser mockup frame -->
        <div class="relative">
          <!-- Chrome bar -->
          <div class="flex items-center gap-2 px-4 py-2.5" style="background:#1E2330;">
            <div class="flex gap-1.5">
              <div class="w-2.5 h-2.5 rounded-full" style="background:#FF5F57;"></div>
              <div class="w-2.5 h-2.5 rounded-full" style="background:#FEBC2E;"></div>
              <div class="w-2.5 h-2.5 rounded-full" style="background:#28C840;"></div>
            </div>
            <div class="flex-1 mx-2 px-3 py-1 rounded text-xs truncate"
              style="background:#2D3347; color:rgba(255,255,255,0.35); font-size:10px;">
              {{url}}
            </div>
          </div>
          <!-- Screenshot area -->
          <div class="overflow-hidden" style="height:200px;">
            <img src="{{image}}"
              alt="{{title}} — SitioPro"
              class="w-full h-full object-cover object-top transition-transform duration-500 group-hover:scale-105"
              loading="lazy"
              onerror="this.onerror=null;this.style.background='linear-gradient(135deg, #4F46E5 0%, #3730A3 100%)';this.removeAttribute('src')">
          </div>
        </div>

        <!-- Card info -->
        <div class="p-5">
          <div class="flex items-start justify-between gap-3 mb-3">
            <span class="inline-block text-xs font-bold px-3 py-1 rounded-full"
              style="background:rgba(79,70,229,0.08); color:var(--color-primary);">{{category}}</span>
            {{#if outcome}}
            <span class="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full"
              style="background:rgba(16,185,129,0.08); color:#059669;">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
              </svg>
              {{outcome}}
            </span>
            {{/if}}
          </div>
          <h3 class="font-bold text-gray-900 text-base leading-tight">{{title}}</h3>
        </div>
      </div>
      {{/each}}

    </div>

    <!-- Bottom link -->
    <div class="text-center mt-10 reveal-element">
      <p class="text-sm text-gray-500 mb-4">¿Querés ver más proyectos?</p>
      <a href="#contact" class="btn-outline px-8 py-3 text-sm font-semibold inline-flex items-center gap-2">
        Hablemos de tu proyecto
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
        </svg>
      </a>
    </div>

  </div>
</section>
```

**DATA MAPPING:**
- `{{title}}` → `brief.portfolio[].title`
- `{{category}}` → `brief.portfolio[].category`
- `{{outcome}}` → `brief.portfolio[].outcome`
- `{{image}}` → `brief.portfolio[].image`
- `{{url}}` → `brief.portfolio[].url` (show in browser bar — shorten to domain only, e.g. "mariscosdonpepe.ec")

**STYLE NOTES:**
- Never skip this section for digital-agency clients even if `portfolio[]` is empty — render 3 cards with gradient fallback backgrounds
- onerror fallback: indigo gradient `linear-gradient(135deg, #4F46E5 0%, #3730A3 100%)` — looks like a branded placeholder, not a broken image
- Card hover: combined translateY + shadow — the group-hover:scale-105 on the image creates a zoom effect

---

### HOW-IT-WORKS

**TRIGGER:** Render when `section_order` includes `"how-it-works"` AND `brief.process_steps[]` is not empty.

**CONCEPT:** 3-step numbered horizontal process. Removes fear of complexity — shows the client exactly what happens, in order, with no surprises. Each step has a large number as visual anchor.

```html
<!-- ═══════════════════════════════════════ HOW IT WORKS -->
<section id="how-it-works" class="py-20 md:py-28 bg-white">
  <div class="max-w-7xl mx-auto px-6">

    <!-- Section header -->
    <div class="text-center mb-16 reveal-element">
      <span class="inline-block text-xs font-bold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4"
        style="background:rgba(var(--color-primary-rgb,79,70,229),0.08); color:var(--color-primary);">
        Cómo funciona
      </span>
      <h2 class="text-3xl md:text-4xl font-black text-gray-900">Simple. Rápido. Sin sorpresas.</h2>
      <p class="mt-4 text-gray-500 max-w-xl mx-auto">Tres pasos y tu negocio está en línea.</p>
    </div>

    <!-- Steps grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12 relative">

      <!-- Connector line (desktop only) -->
      <div class="hidden md:block absolute top-10 left-1/6 right-1/6 h-px" style="background:linear-gradient(90deg, transparent, var(--color-primary), transparent); opacity:0.25;"></div>

      <!-- Step — repeat for each process_step -->
      {{#each brief.process_steps}}
      <div class="flex flex-col items-center text-center gap-4 reveal-element" style="transition-delay:{{@index}}00ms;">
        <!-- Step number circle -->
        <div class="w-20 h-20 rounded-full flex items-center justify-center flex-shrink-0 font-black text-3xl relative z-10"
          style="background:var(--color-primary); color:#fff; box-shadow:0 0 0 8px rgba(var(--color-primary-rgb,79,70,229),0.1);">
          {{step}}
        </div>
        <h3 class="text-xl font-bold text-gray-900 mt-2">{{title}}</h3>
        <p class="text-gray-500 leading-relaxed text-sm max-w-xs">{{description}}</p>
      </div>
      {{/each}}
    </div>

    <!-- Bottom CTA nudge -->
    <div class="text-center mt-14 reveal-element">
      <a href="#contact" class="btn-primary px-8 py-4 text-sm font-bold inline-flex items-center gap-2">
        Empezar ahora
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
        </svg>
      </a>
    </div>

  </div>
</section>
```

**DATA MAPPING:** Each `process_steps[].step` (e.g. "01"), `.title`, `.description` directly rendered. If only 3 steps exist → use all 3. Never truncate.

**STEP COLOR RULE (CRITICAL — NO EXCEPTIONS):**
ALL step number circles MUST use the SAME color — `var(--color-primary)`. NEVER change the last step to amber, gold, or any accent color. Color variation across steps = broken design, not intentional design.
```html
<!-- ALL steps use this — never change color per step -->
style="background:var(--color-primary); color:#fff; box-shadow:0 0 0 8px rgba(79,70,229,0.1);"
```

**STYLE NOTES:**
- `corporate-trust` / `authority` personality: keep step numbers navy, remove connector line glow
- `warm-local`: use rounded-3xl cards instead of circles, warmer bg tint per step
- `luxury-dark`: dark section bg (`var(--color-bg)`), white text, cyan step circles

---

### CTA-BANNER

**TRIGGER:** Render when `section_order` includes `"cta-banner"` (mid-page inline CTA strip, NOT the final CTA section).

**CONCEPT:** A full-width contrasting strip that interrupts the scroll rhythm and re-focuses attention on conversion. Shorter than the final CTA — no subheadline needed. Just a punchy line and a button.

```html
<!-- ═══════════════════════════════════════ CTA BANNER (mid-page) -->
<div id="cta-banner" class="py-12 relative overflow-hidden"
  style="background:linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark, #3730A3) 100%);">

  <!-- Decorative background circle -->
  <div class="absolute -right-24 -top-24 w-96 h-96 rounded-full opacity-10"
    style="background:rgba(255,255,255,0.3);"></div>

  <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6 reveal-element">
    <div>
      <p class="text-white/60 text-xs font-bold uppercase tracking-widest mb-2">¿Listo para empezar?</p>
      <h2 class="text-2xl md:text-3xl font-black text-white leading-tight">
        Tu sitio listo en <span class="underline decoration-2 decoration-white/40">3 a 7 días.</span>
      </h2>
    </div>
    <div class="flex items-center gap-4 flex-shrink-0">
      <a href="#contact"
        class="inline-flex items-center gap-2 px-8 py-4 rounded-xl font-bold text-sm transition-all duration-200 hover:-translate-y-1"
        style="background:#fff; color:var(--color-primary); box-shadow:0 8px 30px rgba(0,0,0,0.2);">
        Agenda gratis
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
        </svg>
      </a>
    </div>
  </div>
</div>
```

**STYLE NOTES:**
- This is NOT `id="cta"` (the final CTA section) — it uses `id="cta-banner"` and is a `<div>` not a `<section>`
- In `ultra-minimal` mode: replace gradient with solid near-black (`#111`), white button
- In `warm-local` mode: use terracotta → dark-red gradient, cream button
- The CTA text should come from `brief.cta_primary` or `seo_data.cta.button`, not hardcoded

---

### WOW-SECTION

**TRIGGER:** Render when `section_order` includes `"wow-section"` (used in `storytelling` personality between badge-grid and testimonials).

**CONCEPT:** Full-bleed emotional moment. No layout grid. Pure atmosphere. A pull quote or manifesto statement over a dark image background — the only section with no product messaging. Creates emotional resonance before the proof section (testimonials).

```html
<!-- ═══════════════════════════════════════ WOW SECTION -->
<section id="wow-section" class="relative py-28 md:py-40 overflow-hidden">

  <!-- Background image with dark overlay -->
  <div class="absolute inset-0">
    <img src="{{hero_img}}" alt="" class="w-full h-full object-cover object-center" loading="lazy">
    <div class="absolute inset-0" style="background:linear-gradient(135deg, rgba(15,23,42,0.88) 0%, rgba(15,23,42,0.70) 100%);"></div>
  </div>

  <!-- Content — centered, narrow column -->
  <div class="relative z-10 max-w-3xl mx-auto px-6 text-center reveal-element">

    <!-- Large decorative quotation mark -->
    <svg class="w-16 h-16 mx-auto mb-8 opacity-30" fill="currentColor" style="color:var(--color-primary);" viewBox="0 0 24 24">
      <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
    </svg>

    <!-- Emotional pull quote — from cta or brief emotional_hook -->
    <blockquote class="text-2xl md:text-4xl font-black text-white leading-tight mb-8">
      "{{brief.emotional_hook}}"
    </blockquote>

    <!-- Thin brand-color rule -->
    <div class="w-16 h-1 mx-auto rounded-full mb-8" style="background:var(--color-primary);"></div>

    <!-- Single CTA button — white background -->
    <a href="#contact"
      class="inline-flex items-center gap-2 px-8 py-4 rounded-xl font-bold text-sm"
      style="background:#fff; color:var(--color-primary);">
      {{cta.button}}
    </a>
  </div>

</section>
```

**CRITICAL RULES:**
- NEVER use a headline or eyebrow above the quote — only the quote itself
- The background image is the hero image (reused) — this section has no unique image requirement
- The quote comes from `brief.emotional_hook` or `cta.headline` — NEVER invent a quote
- NO section grid, NO cards, NO icons — pure typography and image
- In `luxury-dark` mode: reduce overlay to 0.75 opacity, use cyan accent rule color

---

### PRICING

**TRIGGER:** Render when `section_order` includes `"pricing"` AND `brief.pricing[]` is not empty.

**CONCEPT:** 3-column pricing tiers. The highlighted/recommended plan is visually elevated — larger border, accent color, slight vertical lift. The goal is to make the middle-tier feel like the obvious, safe choice.

```html
<!-- ═══════════════════════════════════════ PRICING -->
<section id="pricing" class="py-20 md:py-28" style="background:#F8FAFC;">
  <div class="max-w-7xl mx-auto px-6">

    <!-- Section header -->
    <div class="text-center mb-14 reveal-element">
      <span class="inline-block text-xs font-bold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4"
        style="background:rgba(var(--color-primary-rgb,79,70,229),0.08); color:var(--color-primary);">
        Planes y precios
      </span>
      <h2 class="text-3xl md:text-5xl font-black text-gray-900">Inversión transparente.<br>Sin sorpresas.</h2>
      <p class="mt-4 text-gray-500 max-w-xl mx-auto">Elige el plan que mejor se adapta a tu negocio. Sin contratos, sin costos ocultos.</p>
    </div>

    <!-- Pricing grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">

      <!-- Pricing card — repeat for each plan. Use highlighted: true for the featured plan -->
      {{#each brief.pricing}}
      <div class="relative flex flex-col rounded-2xl p-8 reveal-element"
        style="transition-delay:{{@index}}00ms;
               {{#if highlighted}}
               border:2px solid var(--color-primary);
               background:#fff;
               box-shadow:0 20px 60px rgba(var(--color-primary-rgb,79,70,229),0.15);
               transform:scale(1.04);
               {{else}}
               border:1px solid #E2E8F0;
               background:#fff;
               {{/if}}">

        <!-- "Most popular" badge — only on highlighted plan -->
        {{#if highlighted}}
        <div class="absolute -top-4 left-1/2 -translate-x-1/2">
          <span class="px-4 py-1.5 rounded-full text-xs font-bold text-white"
            style="background:var(--color-primary);">El más elegido</span>
        </div>
        {{/if}}

        <!-- Plan name -->
        <p class="text-sm font-bold uppercase tracking-widest mb-2"
          style="color:{{#if highlighted}}var(--color-primary){{else}}#94A3B8{{/if}};">
          {{name}}
        </p>

        <!-- Price -->
        <p class="text-5xl font-black text-gray-900 leading-none mb-1">{{price}}</p>
        <p class="text-xs text-gray-400 mb-6">{{description}}</p>

        <!-- Divider -->
        <div class="h-px bg-gray-100 mb-6"></div>

        <!-- Feature list -->
        <ul class="flex flex-col gap-3 flex-1 mb-8">
          {{#each features}}
          <li class="flex items-start gap-3 text-sm text-gray-600">
            <svg class="w-4 h-4 flex-shrink-0 mt-0.5" style="color:var(--color-primary);" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
            </svg>
            {{this}}
          </li>
          {{/each}}
        </ul>

        <!-- CTA button -->
        <a href="#contact"
          class="{{#if highlighted}}btn-primary{{else}}btn-outline{{/if}} w-full py-3.5 text-sm font-bold text-center rounded-xl">
          {{cta}}
        </a>

      </div>
      {{/each}}
    </div>

    <!-- Trust note below grid -->
    <p class="text-center text-xs text-gray-400 mt-10">
      Sin contratos de permanencia · Soporte incluido · Resultados garantizados
    </p>

  </div>
</section>
```

**DATA MAPPING:**
- `{{name}}` → `brief.pricing[].name`
- `{{price}}` → `brief.pricing[].price`
- `{{description}}` → `brief.pricing[].description`
- `{{features}}` → `brief.pricing[].features[]` (array of strings)
- `{{cta}}` → `brief.pricing[].cta`
- `{{highlighted}}` → `brief.pricing[].highlighted` (boolean — true = featured plan)

**PRICING CTA BUTTON RULE (CRITICAL):**
The CTA button label MUST be an action verb — NEVER the same text as the badge above it.
```html
<!-- WRONG — badge and button say the same thing -->
<span ...>El más elegido</span>   ← badge
<a ...>El más elegido</a>         ← button — FORBIDDEN

<!-- CORRECT — badge informs, button acts -->
<span ...>El más elegido</span>   ← badge
<a ...>Empezar con este plan →</a>  ← button = action verb
```
Use `brief.pricing[].cta` for the button text. If it's descriptive rather than action-oriented, rewrite it to start with a verb: "Empezar", "Elegir este plan", "Quiero este", "Comenzar ahora".

**STYLE NOTES:**
- In `luxury-dark` mode: all cards use `bg-[#1E293B]`, featured card uses `border-[var(--color-primary)]` with glow shadow
- In `ultra-minimal` mode: remove rounded corners, use `border-t-4` instead of full border, no scale transform
- The trust note below the grid MUST always render — it reduces purchase anxiety

---

### TRUST BLOCKS (CRITICAL — 3 mandatory components)

A trust section MUST include ALL of the following. Never just icons with text.

---

#### TRUST BLOCK 1 — STATS BAR (Big isolated numbers)
Numbers must be large, bold, and isolated. They must feel undeniable.
```html
<section class="py-10 bg-white border-y border-gray-100">
  <div class="max-w-7xl mx-auto px-6">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
      <div class="reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:0ms;">
        <p class="text-5xl md:text-6xl font-black leading-none" style="color:var(--color-primary);">500+</p>
        <p class="text-xs font-bold text-gray-400 mt-2 uppercase tracking-widest">Families Served</p>
      </div>
      <div class="reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:100ms;">
        <p class="text-5xl md:text-6xl font-black leading-none" style="color:var(--color-primary);">10+</p>
        <p class="text-xs font-bold text-gray-400 mt-2 uppercase tracking-widest">Years of Experience</p>
      </div>
      <div class="reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:200ms;">
        <p class="text-5xl md:text-6xl font-black leading-none" style="color:var(--color-primary);">4.9★</p>
        <p class="text-xs font-bold text-gray-400 mt-2 uppercase tracking-widest">Average Rating</p>
      </div>
      <div class="reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:300ms;">
        <p class="text-5xl md:text-6xl font-black leading-none" style="color:var(--color-primary);">24/7</p>
        <p class="text-xs font-bold text-gray-400 mt-2 uppercase tracking-widest">Available Support</p>
      </div>
    </div>
  </div>
</section>
```
RULES: Use real numbers from brief. If not provided, use conservative placeholders. NEVER invent inflated numbers.

---

#### TRUST BLOCK 2 — BADGE GRID (Visual authority signals)
Badges must feel like certifications, not decorations.
```html
<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12">
  <div class="flex flex-col items-center gap-3 p-5 rounded-2xl text-center border reveal-on-scroll opacity-0 translate-y-6"
    style="border-color:rgba(167,215,197,0.35); background:rgba(240,250,247,0.6); transition-delay:0ms;">
    <div class="w-14 h-14 rounded-full flex items-center justify-center icon-circle transition-all duration-300"
      style="background:rgba(167,215,197,0.3);">
      {{icon_svg_badge}}
    </div>
    <p class="text-sm font-bold text-gray-800 leading-tight">Background Checked</p>
  </div>
  <!-- Repeat for: Licensed & Insured / Free Consultation / 24/7 Support -->
</div>
```

---

#### TRUST BLOCK 3 — PHOTO TESTIMONIALS (Social proof with face)
At least ONE testimonial MUST include a real-looking avatar. Anonymous text quotes = zero trust.
```html
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <div class="bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 p-8 border border-gray-100 flex flex-col gap-5 reveal-on-scroll opacity-0 translate-y-6" style="transition-delay:0ms;">
    <!-- Stars -->
    <div class="flex text-amber-400 text-lg">★★★★★</div>
    <!-- Quote -->
    <p class="text-gray-600 leading-relaxed text-sm italic flex-1">
      "{{testimonial_quote}}"
    </p>
    <!-- Author with photo -->
    <div class="flex items-center gap-4 pt-4 border-t border-gray-100">
      <img src="{{avatar_url}}" alt="{{author_name}}"
        class="w-12 h-12 rounded-full object-cover ring-2 ring-offset-2"
        style="ring-color:var(--color-secondary);"
        onerror="this.style.background='var(--color-secondary)';this.removeAttribute('src')">
      <div>
        <p class="font-bold text-gray-900 text-sm">{{author_name}}</p>
        <p class="text-xs text-gray-400 mt-0.5">{{author_role}}</p>
      </div>
    </div>
  </div>
</div>
```

---

TRUST RULES:
* Stats bar is NOT optional — every site MUST have one
* Numbers must be visually dominant — text-5xl minimum
* At least one testimonial must have an avatar image with onerror fallback
* Badge grid uses icon-circle class for hover fill animation (see MICRO UX)

---

### COMPARISON

**TRIGGER:** Render this section ONLY when `brief.comparison[]` array exists AND `section_order` includes `"comparison"`.

**CONCEPT:** Two-panel split. Left panel = what traditional/competitor offers (problems, dark background). Right panel = what this brand offers (solutions, light background). Side-by-side makes the advantage undeniable without the user having to search for it.

**CRITICAL RULES:**
- Left panel MUST use the brand's dark color (`var(--color-bg-dark, #0F172A)`) — dark but NOT black
- Right panel uses white or `--color-secondary`
- Each row is a feature from `brief.comparison[]` — render ALL rows
- Left side rows: red/gray × icon + `traditional` value
- Right side rows: green/primary ✓ icon + `sitiopro` / brand value
- Section header sits ABOVE the two panels, full width, centered
- CTA button at bottom of right panel: drives to contact/pricing

```html
<!-- ═══════════════════════════════════════ COMPARISON SECTION -->
<section id="comparison" class="py-20 md:py-28" style="background:#F8FAFC;">
  <div class="max-w-7xl mx-auto px-6">

    <!-- Section header -->
    <div class="text-center mb-14 reveal-on-scroll opacity-0 translate-y-6">
      <p class="text-xs font-bold uppercase tracking-widest mb-3" style="color:var(--color-primary);">Por qué elegirnos</p>
      <h2 class="text-3xl md:text-5xl font-black text-gray-900 leading-tight">
        La diferencia es <span style="color:var(--color-primary);">clara</span>
      </h2>
      <p class="mt-4 text-gray-500 text-lg max-w-xl mx-auto">No todas las agencias son iguales. Aquí lo ves de frente.</p>
    </div>

    <!-- Split comparison panels -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-0 rounded-2xl overflow-hidden shadow-2xl reveal-on-scroll opacity-0 translate-y-6">

      <!-- LEFT — Traditional / Problems -->
      <div class="p-8 md:p-12" style="background:var(--color-bg-dark, #0F172A);">
        <div class="flex items-center gap-3 mb-8">
          <div class="w-10 h-10 rounded-full bg-red-500/20 flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </div>
          <p class="text-white/60 font-bold text-sm uppercase tracking-widest">Otras agencias</p>
        </div>
        <div class="flex flex-col gap-5">
          <!-- Repeat for each comparison row -->
          {{#each brief.comparison}}
          <div class="flex items-start gap-4 pb-5 border-b border-white/10 last:border-0 last:pb-0">
            <div class="w-6 h-6 rounded-full bg-red-500/15 flex items-center justify-center flex-shrink-0 mt-0.5">
              <svg class="w-3.5 h-3.5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="3">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </div>
            <div>
              <p class="text-white/40 text-xs uppercase tracking-wide font-semibold mb-1">{{feature}}</p>
              <p class="text-white/75 font-medium leading-snug">{{traditional}}</p>
            </div>
          </div>
          {{/each}}
        </div>
      </div>

      <!-- RIGHT — Brand / Solutions -->
      <div class="p-8 md:p-12 bg-white">
        <div class="flex items-center gap-3 mb-8">
          <div class="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0" style="background:rgba(var(--color-primary-rgb,79,70,229),0.12);">
            <svg class="w-5 h-5" style="color:var(--color-primary);" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <p class="font-bold text-sm uppercase tracking-widest" style="color:var(--color-primary);">{{business_name}}</p>
        </div>
        <div class="flex flex-col gap-5">
          {{#each brief.comparison}}
          <div class="flex items-start gap-4 pb-5 border-b border-gray-100 last:border-0 last:pb-0">
            <div class="w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5" style="background:rgba(var(--color-primary-rgb,79,70,229),0.1);">
              <svg class="w-3.5 h-3.5" style="color:var(--color-primary);" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="3">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
            <div>
              <p class="text-gray-400 text-xs uppercase tracking-wide font-semibold mb-1">{{feature}}</p>
              <p class="text-gray-900 font-semibold leading-snug">{{sitiopro}}</p>
            </div>
          </div>
          {{/each}}
        </div>
        <!-- CTA at bottom of right panel -->
        <div class="mt-8 pt-6 border-t border-gray-100">
          <a href="#contact" class="btn-primary w-full py-4 text-sm font-bold text-center">
            Empezar ahora — sin compromiso
          </a>
          <p class="text-center text-xs text-gray-400 mt-3">Sin contratos. Sin costos ocultos.</p>
        </div>
      </div>

    </div>
  </div>
</section>
```

**DATA MAPPING:**
- `{{business_name}}` → `brief.business_name`
- `{{feature}}` → each `brief.comparison[].feature`
- `{{traditional}}` → each `brief.comparison[].traditional`
- `{{sitiopro}}` → the brand's column key (may be named after the business — use whichever key is NOT `"traditional"` and NOT `"feature"`)
- If `brief.comparison` uses a different key name (e.g. `"us"`, `"sitiopro"`, `"brand"`): use the first non-feature/non-traditional key

**STYLE NOTES:**
- If `style_mode` is `luxury-dark`: flip — right panel goes dark, left stays light but muted
- If `style_mode` is `ultra-minimal`: remove card shadows, use a thin `1px border border-gray-200` instead of `shadow-2xl`
- The `--color-bg-dark` variable is set in Part 1 CSS vars — always `#0F172A` for dark modes, `#1B2334` for corporate-trust

---

### TESTIMONIALS

* shadow-md
* hover shadow-lg
* readable typography

Include:

★★★★★

---

### TRUST-BAND

**TRIGGER:** Render when `section_order` includes `"trust-band"` (typically used in `conversion-fast` personality directly below hero).

**CONCEPT:** A thin, full-width strip of 3–4 trust pills. No section heading. Pure social proof signal before the user scrolls.

```html
<!-- ═══════════════════════════════════════ TRUST BAND -->
<div class="py-4 border-y border-gray-100 bg-white">
  <div class="max-w-7xl mx-auto px-6">
    <div class="flex flex-wrap items-center justify-center gap-6 md:gap-10">
      <div class="flex items-center gap-2.5 text-gray-600 text-sm font-semibold">
        <svg class="w-5 h-5 flex-shrink-0" style="color:var(--color-primary);" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
        {{trust_signal_1}}
      </div>
      <div class="flex items-center gap-2.5 text-gray-600 text-sm font-semibold">
        <svg class="w-5 h-5 flex-shrink-0" style="color:var(--color-primary);" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
        {{trust_signal_2}}
      </div>
      <div class="flex items-center gap-2.5 text-gray-600 text-sm font-semibold">
        <svg class="w-5 h-5 flex-shrink-0" style="color:var(--color-primary);" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
        {{trust_signal_3}}
      </div>
      <div class="flex items-center gap-2.5 text-gray-600 text-sm font-semibold">
        <svg class="w-5 h-5 flex-shrink-0" style="color:var(--color-primary);" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
        {{trust_signal_4}}
      </div>
    </div>
  </div>
</div>
```
**DATA:** Use `brief.trust_signals[]` or `brief.differentiation[]` — pick the shortest, most powerful items. Max 5 words per pill.

---

### LOGO-BAND

**TRIGGER:** Render when `section_order` includes `"logo-band"` (typically used in `product` personality, after hero).

**CONCEPT:** A subtle horizontal strip showing client/partner/integration logos. Signals credibility through association. No heading needed — or a single muted label above.

```html
<!-- ═══════════════════════════════════════ LOGO BAND -->
<div class="py-10 border-y border-gray-100 bg-white overflow-hidden">
  <div class="max-w-7xl mx-auto px-6">
    <p class="text-center text-xs font-bold uppercase tracking-widest text-gray-400 mb-7">Confían en nosotros</p>
    <div class="flex flex-wrap items-center justify-center gap-6 md:gap-10">
      <!-- Logo pill — repeat for each client/partner -->
      <div class="logo-strip-item opacity-60 hover:opacity-100 transition-opacity duration-300">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/></svg>
        {{client_name}}
      </div>
      <!-- If no real logos available: use industry-relevant brand-name pills -->
    </div>
  </div>
</div>
```
**STYLE NOTES:**
- Logos should be muted (`opacity-60`) by default, full opacity on hover — feels premium, not pushy
- If `brief.testimonials[].role` mentions company names → extract those as the logo labels
- If no client logos are available: render a strip of "technology/tool" logos relevant to the business (e.g., for a web agency: Tailwind, React, Framer, Webflow)
- In `luxury-dark` mode: use `bg-transparent border-y border-white/10`, text white/40

---

### FAQ

Accordion with smooth open animation

---

### CTA

* strong contrast
* gradient optional
* ONLY one primary button

---

### CONTACT

* card form UI
* shadow-lg
* rounded-2xl
* trust microcopy

---

## HEADER

* sticky
* backdrop-blur-md
* bg-white/80
* Logo link: ALWAYS use href="#" — NEVER href="/" (causes browser to navigate to filesystem root on file:// protocol)

### LOGO TYPOGRAPHY RULE (CRITICAL)
The logo text MUST use the brand's primary font — NEVER hardcode a different font inline.
```html
<!-- CORRECT -->
<a href="#" class="flex items-center gap-1.5">
  <span class="text-xl font-black tracking-tight" style="color:var(--color-primary); font-family:'Inter',sans-serif;">{{business_name_part1}}</span>
  <span class="text-xl font-black tracking-tight" style="color:var(--color-text); font-family:'Inter',sans-serif;">{{business_name_part2}}</span>
</a>

<!-- WRONG — NEVER DO THIS -->
<span style="font-family:'Merriweather',serif;">...</span>  ← FORBIDDEN
<span style="font-family:'Playfair Display',serif;">...</span>  ← FORBIDDEN
```
RULE: Logo ALWAYS uses `font-family:'Inter',sans-serif; font-weight:900; letter-spacing:-0.03em`. No exceptions. If `style_mode` is `corporate-trust`, the logo is still Inter 900 — NOT Merriweather.

### FOOTER LOGO FALLBACK RULE
If `logo` variable is empty or missing, render the business name as typographic logo — NEVER an empty `<img>`:
```html
<!-- If logo path exists -->
<img src="{{logo_footer}}" class="h-10 w-auto brightness-0 invert" alt="{{business_name}}" loading="lazy"
  onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
<span class="text-xl font-black tracking-tight text-white" style="display:none; font-family:'Inter',sans-serif;">{{business_name}}</span>

<!-- If NO logo path provided — render text directly -->
<span class="text-xl font-black tracking-tight text-white" style="font-family:'Inter',sans-serif;">{{business_name}}</span>
```

---

## FOOTER

* dark background (bg-gray-900)
* strong contrast
* padding: pt-10 pb-6 (NOT pt-16 — too tall on mobile)
* inner grid: gap-8 md:gap-12 (responsive gap — NOT gap-12 on all screens)
* bottom bar: flex flex-col md:flex-row gap-4 (stack on mobile)

MOBILE RULE: Footer columns MUST stack cleanly on mobile with readable spacing. Never use fixed large gaps that cause excessive vertical scroll.

---

## WHATSAPP BUTTON

* floating
* pulse animation (subtle)

---

## MOBILE UX

* sticky CTA bar
* body padding bottom

---

## FORM SYSTEM

* loading state
* success feedback
* redirect to WhatsApp

---

## SEO INTEGRATION

* H1 → hero
* H2 → sections
* alt → images

---

## MULTI-CLIENT SUPPORT

Use ONLY dynamic data:

* branding
* contact_info
* whatsapp
* services

NO hardcoding

---

## 🧩 COMPONENT SYSTEM INTEGRATION (CRITICAL)

You MUST use component-system output for ALL UI components.
Ignoring component-system = INVALID OUTPUT.

### Buttons
- Apply `primary` style: radius, shadow, interaction (lift | scale | shimmer) from component-system
- Apply `secondary` style: lower visual weight, outline/ghost
- ONLY one primary CTA per section

### Cards
- Use the variation defined per section — DO NOT reuse same card style everywhere
- Example: services → elevated | benefits → minimal | testimonials → soft
- Apply radius and shadow from component-system, not from defaults

### Images
- Apply consistent radius (same across all sections)
- Apply consistent shadow and hover behavior
- Follow hover zoom rule only if component-system specifies it

### Icons
- Apply icon background type: circle | soft-square | none (from component-system)
- Apply interaction: color-change on hover (`.group:hover .icon-circle`)
- Style must be consistent across all sections

### Section Decoration
- Apply background pattern and dividers from component-system
- Maintain alternating background rhythm

---

## HARD RULES

DO NOT:

* modify JSON
* invent content
* skip sections
* break layout order

---

## FINAL VALIDATION

### DESIGN

* premium feel
* visual depth
* no repetition

### UX

* clear flow
* CTA visible

### TECH

* valid HTML
* responsive
* no JS errors

---
