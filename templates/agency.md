# AGENCY TEMPLATE — DIGITAL AGENCY / WEB STUDIO

This template is for digital agencies, web design studios, SaaS tools, and professional service providers in the tech/digital space.

---

## BUSINESS PROFILE

* Business type: digital agency, web studio, tech services
* Decision maker: business owner, marketing manager, entrepreneur
* Primary goal: leads (free consultation / demo)
* Trust model: portfolio results + process transparency + speed proof
* Language: Spanish (Ecuador context)

---

## CRITICAL DESIGN RULES FOR AGENCY SITES

* Hero MUST feel like a premium digital product — NOT a freelancer's portfolio
* Services section MUST use editorial-list or stacked-list — NEVER identical 3-col photo cards
* Must have at least 1 DARK section with glowing/electric accent elements
* Results and numbers MUST be prominently displayed (trust through proof)
* Comparison section (vs. traditional agencies) is a HIGH-CONVERTING unique pattern — include it
* Portfolio/results section MUST show actual outcomes (% improvement, time saved, revenue)

---

## RECOMMENDED SECTION ORDER

```
1. hero          — Centered, generous whitespace, punchy headline + stats below
2. trust-bar     — Horizontal strip: key numbers (clients, delivery speed, satisfaction)
3. process       — How it works (3 steps, horizontal or vertical numbered)
4. services      — Editorial layout: 1 featured + numbered list (NOT photo cards)
5. portfolio     — Results showcase with metrics (before/after, stats per project)
6. comparison    — Side-by-side: SitioPro vs. traditional agencies (table or split layout)
7. testimonials  — Client quotes with role + company
8. faq           — Accordion, 5-7 questions about process, pricing, guarantees
9. cta           — Final conversion section (dark background, bold offer)
10. contact      — Form + contact info
```

---

## HERO REQUIREMENTS (CRITICAL)

The hero must communicate:

1. What you do (crystal clear, 1 sentence max)
2. The result you deliver (not "we design" — "you get X clients")
3. Speed/ease proof (delivery time, no technical skills needed)
4. Primary CTA: Agenda tu asesoría gratuita
5. Secondary CTA: Ver planes y precios

Hero variants for agency:
* `cinematic` — Full-bleed dark background with browser mockup showcase, electric accent glow
* `minimal-luxury` — Oversized headline on white, secondary text, generous space
* `split-emotional` — Left: headline + stats + CTA | Right: browser frame with portfolio preview

PREFERRED: cinematic or split-emotional for agency context.

---

## SERVICES SECTION (CRITICAL — NOT PHOTO CARDS)

Agency services should NOT use identical photo+bullet cards.

Instead use `editorial-list`:

```
1 FEATURED service (Landing Pages):
- Horizontal layout: 60% content / 40% visual
- Badge: "Más solicitado" or "Más popular"
- Short description + 3-4 feature chips

4 NUMBERED services:
- Large faded number (02, 03, 04, 05) as visual anchor
- Title + 2-line description + feature chips
- NO images — typography-forward
```

---

## PORTFOLIO / RESULTS SECTION

Show 3 project results with metrics:

```
Project card:
- Client industry label (eyebrow)
- Site type built
- KEY METRIC: "+X% conversión" or "3 días entrega"
- Optional: browser mockup thumbnail
```

---

## COMPARISON SECTION (HIGH-VALUE PATTERN)

Two-column table:

```
SitioPro | Agencias Tradicionales
✓ 3–7 días | ✗ 4–8 semanas
✓ Diseño a medida | ✗ Plantillas genéricas
✓ Enfoque en conversión | ✗ Solo estética
✓ Precio transparente | ✗ Costos ocultos
✓ Soporte personalizado | ✗ Soporte tickets
✓ Resultados medibles | ✗ Sin garantías
```

---

## TRUST SIGNALS (PRIORITY ORDER)

1. Delivery speed (días, no semanas)
2. Custom design (no templates)
3. Real results (testimonials with specific outcomes)
4. Process transparency (cómo trabajamos)
5. Ecuador-based + accessible

---

## COPY TONE GUIDELINES

* Direct and results-focused — NOT corporate jargon
* Spanish (Ecuador / Latinoamérica) — natural, not formal
* Lead with OUTCOMES not features
* Use numbers whenever possible ("3 días", "100% responsive", "$299")
* CTA language: action + benefit ("Agenda tu asesoría — es gratis")

---

## PRICING SECTION

If pricing is included:

* 3-tier structure: Básico / Profesional / Avanzado
* Highlighted card for recommended plan
* Price prominently displayed (remove friction around cost)
* Feature list — use checkmarks

---

## SCHEMA.ORG

Type: `ProfessionalService`
Or: `WebPage` + `LocalBusiness`

---

## OUTPUT CONTRACT FIELDS REQUIRED

The copywriter MUST generate:

* hero.headline — punchy, outcome-focused, Spanish
* hero.subheadline — 2 lines max, explains HOW
* hero.cta_primary — action verb + benefit
* hero.cta_secondary — secondary option
* hero.trust_pill — short trust signal above headline
* services[] — 5 items with name + description + features
* benefits[] — 6 items with icon_concept + title + description
* trust[] — 4 stats (number + label)
* testimonials[] — 3 clients with specific outcome mentioned
* faq[] — 5-7 questions about process, pricing, results
* cta — headline + subheadline + button text
* process_steps[] — 3 steps (icon + title + description)
* comparison[] — array of comparison rows (sitiopro vs traditional)
* pricing[] — 3 plans if available from brief

---

## ANTI-PATTERNS (NEVER DO)

* Hero with stock photo of smiling person at laptop
* Services section as 5 identical photo cards
* Generic "Contáctanos" as the only CTA
* Blue (Tailwind default) as primary color
* Same background (white/gray) for all sections
* Missing mobile sticky CTA
* No WhatsApp float button
* Testimonials without specific outcomes mentioned
