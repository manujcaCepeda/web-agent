# OUTPUT CONTRACT — AI WEB BUILDER

This file defines the universal data structure shared across ALL agents.

All agents MUST:

* Read from this structure
* Write to this structure
* NEVER break this format

---

## GLOBAL STRUCTURE (STRICT JSON)

```json
{
  "business": {
    "name": "",
    "type": "",
    "location": "",
    "phone": "",
    "whatsapp": ""
  },
  "branding": {
    "logo": "",
    "primary_color": "",
    "secondary_color": ""
  },
  "seo": {
    "meta_title": "",
    "meta_description": "",
    "keywords": []
  },
  "hero": {
    "headline": "",
    "subheadline": "",
    "cta_primary": "",
    "cta_secondary": "",
    "background_image": ""
  },
  "services": [
    {
      "title": "",
      "description": "",
      "benefits": [],
      "image": ""
    }
  ],
  "benefits": [
    {
      "title": "",
      "description": ""
    }
  ],
  "trust": [
    {
      "title": "",
      "description": "",
      "icon": ""
    }
  ],
  "testimonials": [
    {
      "name": "",
      "text": "",
      "rating": 5
    }
  ],
  "faq": [
    {
      "question": "",
      "answer": ""
    }
  ],
  "cta": {
    "headline": "",
    "subheadline": "",
    "button": ""
  },
  "contact": {
    "phone": "",
    "email": "",
    "address": ""
  },
  "process_steps": [
    {
      "step": "",
      "title": "",
      "description": ""
    }
  ],
  "comparison": [
    {
      "feature": "",
      "sitiopro": "",
      "traditional": ""
    }
  ],
  "pricing": [
    {
      "name": "",
      "price": "",
      "description": "",
      "features": [],
      "cta": "",
      "highlighted": false
    }
  ]
}
```

---

## OPTIONAL SECTIONS (AGENCY / SERVICES)

`process_steps` — How it works (3 numbered steps). Required for agency template.
`comparison` — Side-by-side comparison rows (us vs. traditional). Required for agency template.
`pricing` — Pricing tiers (2–3 plans). Required for agency template.

These fields are OPTIONAL for healthcare/restaurant templates but REQUIRED for agency template.

---

## RULES (CRITICAL)

### 1. STRUCTURE IS MANDATORY

* Core fields cannot be removed: hero, services, benefits, trust, testimonials, faq, cta, contact
* Optional fields (process_steps, comparison, pricing) must be present for agency template
* Arrays must always exist (even if empty)

---

### 2. COPY RULES

* Must be emotional
* Must be benefit-driven
* Must be concise (max 2 lines per field)

---

### 3. IMAGE RULES

* Must match industry (from template)
* Must include real human interaction (healthcare)

---

### 4. SEO RULES

* Must include primary keyword
* Must be natural (no keyword stuffing)

---

### 5. CTA RULES

Every CTA must include:

* urgency
* reassurance
* friction reduction

---

## AGENT RESPONSIBILITIES

### business-analyzer

Fills:

* business
* branding

---

### copywriter

Fills:

* hero
* services
* benefits
* testimonials
* faq
* cta
* process_steps (agency template)
* comparison (agency template)
* pricing (agency template — copy from brief.json if provided)

---

### seo-optimizer

Fills:

* seo

---

### ui-designer

Enhances:

* structure clarity
* section grouping
* visual hints (optional fields)

---

### frontend-dev

Uses:

* ALL data to generate HTML

NEVER modifies content.

---

## FINAL RULE

If output does not match this contract:

→ REJECT
→ REGENERATE
