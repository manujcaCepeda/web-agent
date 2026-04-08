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
  }
}
```

---

## RULES (CRITICAL)

### 1. STRUCTURE IS MANDATORY

* No field can be removed
* No new fields without system update
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
