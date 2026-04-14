# AI Web Builder — System Entry Point

This file is the **entry point and system index** for the AI Web Builder pipeline.

All generation logic lives in dedicated files. Do NOT duplicate logic here.

---

## ARCHITECTURE OVERVIEW

```
agent.md          ← You are here (system index / entry point)
core/
  orchestrator.md       ← Pipeline execution order and validation rules
  style-engine.md       ← Visual style mode selection (8 canonical modes)
  design-language.json  ← Design tokens per style_mode
  output-contract.md    ← Shared JSON schema between all agents
  generation-log.json   ← Tracks layout/style choices to prevent repetition
  brief.template.json   ← Starter template for new client briefs
  config.template.json  ← Starter template for new client configs
  images.json           ← Global fallback image library
agents/
  business-analyzer.md  ← Step 1: Analyze business type, goals, audience
  brand-strategist.md   ← Step 2: Define unique layout/style decisions per client
  copywriter.md         ← Step 3: Generate all copy in client language
  seo-optimizer.md      ← Step 4: Add SEO, meta tags, schema.org
  ui-designer.md        ← Step 5: Define layout, sections, component types
  frontend-dev.md       ← Steps 6–8: Generate HTML in 3 parts
templates/
  healthcare.md         ← Industry-specific rules for healthcare/care services
  agency.md             ← Industry-specific rules for digital agencies
projects/
  {client_id}/
    brief.json          ← Client business data (source of truth)
    config.json         ← Generation settings (template, language, features)
    client-dna.json     ← Brand identity: colors, forbidden patterns, inspiration
    images.json         ← Client-specific image library
    assets/images/      ← Local image assets
    output/index.html   ← Generated website output
    deploy/             ← Deployment-ready copy
generate.py             ← Python runtime — runs the full pipeline via Anthropic API
```

---

## PIPELINE EXECUTION ORDER

See `core/orchestrator.md` for the full step-by-step pipeline.

Summary:
1. Load `brief.json` + `config.json` + `client-dna.json`
2. Run `business-analyzer` → detect type, audience, tone
3. Run `brand-strategist` → unique layout, colors, visual break, forbidden patterns
4. Run `copywriter` → all copy in correct language
5. Run `seo-optimizer` → meta, schema, structured data
6. Run `ui-designer` → section order, layout variation, component decisions
7. Run `frontend-dev` (Part 1: hero + trust + services)
8. Run `frontend-dev` (Part 2: comparison + testimonials + pricing)
9. Run `frontend-dev` (Part 3: FAQ + CTA + contact + footer)
10. Validate output → check layout uniqueness, hero impact, visual break presence

---

## STYLE SYSTEM

8 canonical style modes defined in `core/style-engine.md`:

| Mode | Business Type |
|------|--------------|
| `premium-care` | Healthcare, senior care, wellness |
| `modern-clinic` | Medical clinics, dental, diagnostics |
| `luxury-service` | Law, finance, high-end consulting |
| `luxury-dark` | Tech agencies, SaaS, digital studios |
| `ultra-minimal` | Design studios, coaches, architects |
| `warm-local` | Restaurants, food, artisans |
| `corporate-trust` | Law, finance, insurance, accounting |
| `creative-bold` | Creative agencies, fashion, events |

Design tokens for each mode → `core/design-language.json`

---

## ADDING A NEW CLIENT

1. Copy `core/brief.template.json` → `projects/{client_id}/brief.json`
2. Copy `core/config.template.json` → `projects/{client_id}/config.json`
3. Create `projects/{client_id}/client-dna.json` (brand identity)
4. Create `projects/{client_id}/images.json` (image library)
5. Run: `python generate.py --client {client_id}`

---

## ADDING A NEW INDUSTRY TEMPLATE

1. Create `templates/{industry}.md`
2. Set `config.json → template: "{industry}"`
3. Define: section order, anti-patterns, required copy sections, tone rules

---

## GLOBAL RULES (apply to all clients)

- Every site MUST have a visual break section (dark band, editorial, etc.)
- Section backgrounds MUST alternate (white / gray / dark — never same twice in a row)
- Every CTA MUST include urgency + reassurance + friction reduction
- No client site should look like another — layout_variation enforces this
- Language is detected from `brief.json.language` — entire site generated in that language
- Forbidden patterns from `client-dna.json` override all other defaults

---

## OUTPUT

Each client generates:
- `projects/{client_id}/output/index.html` — full single-file website
- No external JS files unless explicitly required
