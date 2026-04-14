"""
Web Agent Pipeline
Generates premium websites for clients using multi-agent AI pipeline.

Usage:
    python generate.py --client fern-private-care
"""

import json
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
import anthropic

load_dotenv()

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).parent
PROJECTS_DIR = BASE_DIR / "projects"
AGENTS_DIR = BASE_DIR / "agents"
TEMPLATES_DIR = BASE_DIR / "templates"
CORE_DIR = BASE_DIR / "core"


def extract_img_url(img_obj: any, width: int = 800, height: int = 500) -> str:
    """Extract a plain URL string from an image object or string.
    images.json stores objects {url, label, mood} — this normalizes to a plain URL.
    """
    if isinstance(img_obj, dict):
        url = img_obj.get("url", "")
    else:
        url = img_obj or ""
    # Ensure dimensions are injected if URL is a bare Unsplash photo ID reference
    return url


def load_images_library() -> dict:
    """Load curated image library from core/images.json.
    Returns normalized structure with plain URL strings (not objects).
    """
    images_path = CORE_DIR / "images.json"
    if images_path.exists():
        data = json.loads(read_file(images_path))
        normalized = {}
        for industry, img_set in data.items():
            if industry.startswith("_"):
                continue
            normalized[industry] = {
                "hero": extract_img_url(img_set.get("hero", "")),
                "services": [extract_img_url(s) for s in img_set.get("services", [])],
                "fallback_color": img_set.get("fallback_color", "linear-gradient(135deg, #A7D7C5 0%, #2F7F79 100%)")
            }
        return normalized
    # Fallback if file missing — verified elderly care photo IDs only
    return {
        "healthcare": {
            "hero": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=1200&h=800&fit=crop&crop=faces&auto=format&q=85",
            "services": [
                "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=800&h=500&fit=crop&crop=faces&auto=format&q=80",
                "https://images.unsplash.com/photo-1581056771107-24ca5f033842?w=800&h=500&fit=crop&crop=faces&auto=format&q=80",
                "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=500&fit=crop&crop=center&auto=format&q=80",
                "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=500&fit=crop&crop=faces&auto=format&q=80",
                "https://images.unsplash.com/photo-1590765738209-6b8be59b6b7e?w=800&h=500&fit=crop&crop=center&auto=format&q=80",
                "https://images.unsplash.com/photo-1624727828489-a1e03b79bba8?w=800&h=500&fit=crop&crop=faces&auto=format&q=80",
            ],
            "fallback_color": "linear-gradient(135deg, #A7D7C5 0%, #2F7F79 100%)"
        }
    }


def build_schema_org(brief: dict, config: dict) -> str:
    """Build Schema.org JSON-LD script block."""
    schema_cfg = brief.get("schema", {})
    loc = config.get("localization", {})
    contact = brief.get("contact_info", {})

    schema = {
        "@context": "https://schema.org",
        "@type": schema_cfg.get("type", "LocalBusiness"),
        "name": brief.get("business_name", ""),
        "description": brief.get("value_proposition", ""),
        "url": "",
        "telephone": contact.get("phone", ""),
        "email": contact.get("email", ""),
        "address": {
            "@type": "PostalAddress",
            "addressLocality": brief.get("location", ""),
            "addressCountry": loc.get("country", "US")
        },
        "openingHours": brief.get("business_hours", "Mo-Su 00:00-23:59"),
        "priceRange": schema_cfg.get("price_range", "$$"),
        "foundingDate": schema_cfg.get("founding_year", ""),
        "sameAs": list(brief.get("social_links", {}).values())
    }

    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def build_og_tags(seo: dict, brief: dict, hero_img: str) -> str:
    """Build Open Graph + Twitter Card meta tags."""
    title = seo.get("meta_title", brief.get("business_name", ""))
    description = seo.get("meta_description", brief.get("value_proposition", ""))
    business_name = brief.get("business_name", "")

    lines = [
        f'<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{description}">',
        f'<meta property="og:image" content="{hero_img}">',
        f'<meta property="og:site_name" content="{business_name}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">',
        f'<meta name="twitter:description" content="{description}">',
        f'<meta name="twitter:image" content="{hero_img}">',
    ]
    return "\n  ".join(lines)


def build_analytics_snippet(config: dict) -> str:
    """Build GA4 + Meta Pixel snippets if configured."""
    analytics = config.get("analytics", {})
    if not config.get("output", {}).get("include_analytics", False):
        return ""

    snippets = []

    ga4_id = analytics.get("ga4_id", "")
    if ga4_id:
        snippets.append(
            f'<!-- Google Analytics -->\n'
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={ga4_id}"></script>\n'
            f'<script>\n'
            f'  window.dataLayer = window.dataLayer || [];\n'
            f'  function gtag(){{dataLayer.push(arguments);}}\n'
            f'  gtag("js", new Date());\n'
            f'  gtag("config", "{ga4_id}");\n'
            f'</script>'
        )

    pixel_id = analytics.get("meta_pixel_id", "")
    if pixel_id:
        snippets.append(
            f'<!-- Meta Pixel -->\n'
            f'<script>\n'
            f'  !function(f,b,e,v,n,t,s)\n'
            f'  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?\n'
            f'  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};\n'
            f'  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version="2.0";\n'
            f'  n.queue=[];t=b.createElement(e);t.async=!0;\n'
            f'  t.src=v;s=b.getElementsByTagName(e)[0];\n'
            f'  s.parentNode.insertBefore(t,s)}}(window, document,"script",\n'
            f'  "https://connect.facebook.net/en_US/fbevents.js");\n'
            f'  fbq("init", "{pixel_id}");\n'
            f'  fbq("track", "PageView");\n'
            f'</script>\n'
            f'<noscript><img height="1" width="1" style="display:none"\n'
            f'  src="https://www.facebook.com/tr?id={pixel_id}&ev=PageView&noscript=1"/></noscript>'
        )

    return "\n\n".join(snippets)


def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_client(client_id: str) -> tuple[dict, dict]:
    client_dir = PROJECTS_DIR / client_id
    if not client_dir.exists():
        print(f"ERROR: Client '{client_id}' not found in /projects/")
        sys.exit(1)

    config = json.loads(read_file(client_dir / "config.json"))
    brief = json.loads(read_file(client_dir / "brief.json"))
    return config, brief


def load_client_dna(client_id: str) -> dict:
    """Load optional client-dna.json for brand identity overrides.
    Returns empty dict if not present — system works without it.
    """
    dna_path = PROJECTS_DIR / client_id / "client-dna.json"
    if dna_path.exists():
        try:
            dna = json.loads(read_file(dna_path))
            print(f"  ✓ client-dna.json loaded ({len(json.dumps(dna))} chars)")
            return dna
        except Exception as e:
            print(f"  WARNING: client-dna.json parse error: {e} — continuing without DNA")
    return {}


def load_generation_log() -> list:
    """Load generation log tracking layout/style choices per client.
    Used to prevent repetition across clients.
    """
    log_path = CORE_DIR / "generation-log.json"
    if log_path.exists():
        try:
            return json.loads(read_file(log_path))
        except Exception:
            pass
    return []


def update_generation_log(client_id: str, brand_strategy: dict, business_type: str):
    """Append current generation to log. Keep last 20 entries."""
    import datetime
    log_path = CORE_DIR / "generation-log.json"
    log = load_generation_log()
    log.append({
        "client_id": client_id,
        "business_type": business_type,
        "style_mode": brand_strategy.get("style_mode", ""),
        "layout_variation": brand_strategy.get("layout_variation", ""),
        "primary_color": brand_strategy.get("primary_color", ""),
        "hero_variant": brand_strategy.get("hero_variant", ""),
        "timestamp": datetime.datetime.now().isoformat()
    })
    # Keep last 20 entries
    log = log[-20:]
    log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")


def check_layout_uniqueness(brand_strategy: dict, business_type: str) -> list[str]:
    """Check if layout choices repeat patterns from recent generations.
    Returns list of warnings (empty = all good).
    """
    log = load_generation_log()
    warnings = []
    layout_variation = brand_strategy.get("layout_variation", "")
    style_mode = brand_strategy.get("style_mode", "")

    # Check last 3 entries for same layout_variation with same business_type
    recent = [e for e in log[-10:] if e.get("business_type") == business_type]
    recent_layouts = [e.get("layout_variation") for e in recent[-3:]]
    if layout_variation and recent_layouts.count(layout_variation) >= 2:
        warnings.append(
            f"layout_variation '{layout_variation}' used {recent_layouts.count(layout_variation)} times "
            f"recently for '{business_type}' — consider: editorial-list, cards-horizontal, stacked-list"
        )

    # Check last 5 entries for same style_mode
    recent_modes = [e.get("style_mode") for e in log[-5:]]
    if style_mode and recent_modes.count(style_mode) >= 4:
        warnings.append(
            f"style_mode '{style_mode}' used {recent_modes.count(style_mode)} times in last 5 generations"
        )

    return warnings


def load_prompts(template_name: str) -> dict:
    # Load optional supplementary context files (injected into existing agents — no extra API calls)
    def load_optional(path: Path) -> str:
        return read_file(path) if path.exists() else ""

    style_engine = load_optional(CORE_DIR / "style-engine.md")
    hero_system = load_optional(CORE_DIR / "hero-system.md")
    component_system = load_optional(CORE_DIR / "component-system.md")
    art_director = load_optional(CORE_DIR / "art-director.md")

    # Brand strategist agent (new — adds 1 API call but enables real per-client variation)
    brand_strategist_path = AGENTS_DIR / "brand-strategist.md"
    brand_strategist_prompt = read_file(brand_strategist_path) if brand_strategist_path.exists() else ""

    # Inject style-engine + art-director into business-analyzer
    business_analyzer_prompt = read_file(AGENTS_DIR / "business-analyzer.md")
    if style_engine:
        business_analyzer_prompt += f"\n\n---\n\n# STYLE ENGINE RULES (APPLY WHEN DETECTING style_mode)\n\n{style_engine}"
    if art_director:
        business_analyzer_prompt += f"\n\n---\n\n# ART DIRECTOR SYSTEM (APPLY WHEN DEFINING art_direction)\n\n{art_director}"

    # Inject hero-system into ui-designer (hero variant selection authority)
    ui_designer_prompt = read_file(AGENTS_DIR / "ui-designer.md")
    if hero_system:
        ui_designer_prompt += f"\n\n---\n\n# HERO SYSTEM RULES (USE FOR hero_variant SELECTION)\n\n{hero_system}"

    # Inject component-system + art-director into frontend-dev
    frontend_dev_prompt = read_file(AGENTS_DIR / "frontend-dev.md")
    if component_system:
        frontend_dev_prompt += f"\n\n---\n\n# COMPONENT SYSTEM SPECIFICATION\n\n{component_system}"
    if art_director:
        frontend_dev_prompt += f"\n\n---\n\n# ART DIRECTOR REFERENCE (USE FOR WOW SECTIONS + COLOR PALETTE)\n\n{art_director}"

    return {
        "business_analyzer": business_analyzer_prompt,
        "brand_strategist": brand_strategist_prompt,
        "copywriter": read_file(AGENTS_DIR / "copywriter.md"),
        "seo_optimizer": read_file(AGENTS_DIR / "seo-optimizer.md"),
        "ui_designer": ui_designer_prompt,
        "frontend_dev": frontend_dev_prompt,
        "output_contract": read_file(CORE_DIR / "output-contract.md"),
        "template": read_file(TEMPLATES_DIR / f"{template_name}.md"),
    }


def call_claude(client: anthropic.Anthropic, system_prompt: str, user_message: str, step_name: str, max_tokens: int = 8192) -> str:
    print(f"\n  → Running: {step_name}...")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    result = message.content[0].text
    stop_reason = message.stop_reason
    print(f"  ✓ {step_name} complete ({len(result)} chars) [stop: {stop_reason}]")
    return result, stop_reason


def build_services_layout_instruction(layout_variation: str, services: list, service_imgs: list, hero_img: str, img_onerror: str) -> str:
    """Build dynamic services section instruction based on brand_strategy.layout_variation."""

    if layout_variation == "editorial-list":
        return (
            "<section id='services' class='py-14 md:py-20 bg-[var(--color-bg-alt,#F9FAFB)]'>:\n"
            "   EDITORIAL LAYOUT (NOT standard card grid):\n"
            "   1 FEATURED card: full-width horizontal flex (lg:flex-row), left 60% text (heading, description, chip tags, 'Más solicitado' gradient badge), right 40% image — use first service\n"
            "   Below: grid md:grid-cols-2 of NUMBERED items for remaining services:\n"
            "     Each: flex gap-5, large number badge (02, 03...) in text-5xl font-black text-[--color-primary]/15, then title + description + 3 chip tags\n"
            "     NO images on numbered items — typography-forward\n"
            "   This layout MUST look editorially different from a standard card grid.\n"
        )
    elif layout_variation == "cards-horizontal":
        return (
            "<section id='services' class='py-14 md:py-20 bg-[var(--color-bg-alt,#F9FAFB)]'>:\n"
            "   HORIZONTAL ROWS — each service is a full-width row:\n"
            "   flex flex-col md:flex-row rounded-2xl overflow-hidden shadow-md mb-6\n"
            "   Image side: md:w-2/5 min-h-[280px] — alternates left/right (odd=left, even=right: md:flex-row-reverse)\n"
            "   Content side: md:w-3/5 p-8 flex flex-col justify-center\n"
            "   NEVER stack them as columns — always full-width rows\n"
        )
    elif layout_variation == "stacked-list":
        return (
            "<section id='services' class='py-14 md:py-20 bg-[var(--color-bg-alt,#F9FAFB)]'>:\n"
            "   STACKED LIST — no images, typography-forward with dividers:\n"
            "   divide-y divide-[--color-secondary] container\n"
            "   Each service: py-8 flex gap-6 items-start\n"
            "     Number: text-4xl font-black text-[--color-primary] w-12 shrink-0\n"
            "     Content: h3 font-bold + p description + flex chip tags\n"
            "   NO card backgrounds, NO shadows — clean list with dividers only\n"
        )
    elif layout_variation == "icon-columns":
        return (
            "<section id='services' class='py-14 md:py-20 bg-[var(--color-bg-alt,#F9FAFB)]'>:\n"
            "   ICON COLUMNS — 4+ columns, feature-list style (NOT card boxes):\n"
            "   grid grid-cols-2 md:grid-cols-4 gap-6\n"
            "   Each: text-center p-4 (NO shadow, NO heavy border)\n"
            "     Icon: w-12 h-12 mx-auto mb-3 rounded-xl bg-[--color-primary]/10 centered SVG icon\n"
            "     Title: font-semibold text-sm mb-1\n"
            "     Description: text-xs text-muted (1 line max)\n"
            "   NEVER make these look like cards with full bg — just icon+label\n"
        )
    elif layout_variation == "masonry-mixed":
        return (
            "<section id='services' class='py-14 md:py-20 bg-[var(--color-bg-alt,#F9FAFB)]'>:\n"
            "   MASONRY-MIXED — asymmetric grid:\n"
            "   Row 1: 1 large card (col-span-2) + 1 normal card (col-span-1)\n"
            "   Row 2: 2 normal cards\n"
            "   Use CSS grid with grid-cols-3, first card gets col-span-2\n"
            "   Large card: image top h-72, content below\n"
            "   Normal cards: image top h-48, content below\n"
        )
    else:  # cards-3 (default — only when explicitly chosen)
        return (
            "<section id='services' class='py-14 md:py-20 bg-gray-50'>:\n"
            "   3-column responsive grid (grid md:grid-cols-3 gap-6)\n"
            "   Each card: overflow-hidden rounded-2xl shadow-md hover:shadow-xl group cursor-pointer transition duration-300\n"
            "   Image on top (h-52 object-cover), then title + description + bullet list below\n"
        )


def generate_frontend(client: anthropic.Anthropic, system_prompt: str, brief: dict, config: dict, seo_data: dict, layout_data: dict, brand_strategy: dict = None) -> str:
    """Generate frontend HTML in three focused parts to avoid token limits."""
    if brand_strategy is None:
        brand_strategy = {}

    # Brand strategy overrides brief branding defaults
    primary_color = (
        brand_strategy.get("primary_color")
        or brief.get("branding", {}).get("primary_color", "#2F7F79")
    )
    secondary_color = brief.get("branding", {}).get("secondary_color", "#A7D7C5")
    logo = brief.get("branding", {}).get("logo", "")
    whatsapp = brief.get("whatsapp", "")
    phone = brief.get("contact_info", {}).get("phone", "")
    email = brief.get("contact_info", {}).get("email", "")
    address = brief.get("contact_info", {}).get("address", "")
    business_name = brief.get("business_name", "")
    seo = seo_data.get("seo", {})
    hero = seo_data.get("hero", {})
    services = seo_data.get("services", [])
    benefits = seo_data.get("benefits", [])
    trust = seo_data.get("trust", [])
    testimonials = seo_data.get("testimonials", [])
    faq = seo_data.get("faq", [])
    cta = seo_data.get("cta", {})
    # Agency-specific sections (fallback to brief.json if not in copywriter output)
    process_steps = seo_data.get("process_steps") or brief.get("process_steps", [])
    comparison = seo_data.get("comparison") or brief.get("comparison", [])
    pricing = seo_data.get("pricing") or brief.get("pricing", [])
    features = config.get("features", {})
    use_lazy_loading = features.get("lazy_loading", True)
    use_schema_org = features.get("schema_org", True)

    process_steps_json = json.dumps(process_steps, indent=2) if process_steps else "[]"
    comparison_json = json.dumps(comparison, indent=2) if comparison else "[]"
    pricing_json = json.dumps(pricing, indent=2) if pricing else "[]"

    shared_context = (
        f"Business: {business_name}\n"
        f"Primary color: {primary_color} | Secondary: {secondary_color}\n"
        f"Logo: {logo}\n"
        f"WhatsApp: {whatsapp} | Phone: {phone} | Email: {email} | Address: {address}\n"
        f"Meta title: {seo.get('meta_title', '')}\n"
        f"Meta description: {seo.get('meta_description', '')}\n"
        f"Language: {brief.get('language', 'es')} — ALL text must be in {'Spanish' if brief.get('language','es')=='es' else 'English'}\n"
        f"Has process_steps: {'YES' if process_steps else 'NO'} | Has comparison: {'YES' if comparison else 'NO'} | Has pricing: {'YES' if pricing else 'NO'}\n"
    )

    # Load curated images from core/images.json (normalized — hero and services are plain URL strings)
    images_lib = load_images_library()
    template_key = config.get("template", "healthcare")
    img_set = images_lib.get(template_key, images_lib.get("healthcare", {}))
    # brief.json may override hero image via branding.hero_image_url
    _raw_hero = (
        brief.get("branding", {}).get("hero_image_url")
        or extract_img_url(img_set.get("hero", ""))
    )
    # resolve_image_path defined below — inline resolution for hero
    hero_img = (
        _raw_hero if (_raw_hero.startswith("http://") or _raw_hero.startswith("https://") or _raw_hero.startswith("../"))
        else f"../{_raw_hero}" if _raw_hero else ""
    )
    service_imgs = img_set.get("services", [])
    fallback_color = img_set.get("fallback_color", "linear-gradient(135deg, #A7D7C5 0%, #2F7F79 100%)")
    img_onerror = f'onerror="this.onerror=null;this.style.background=\'{fallback_color}\';this.removeAttribute(\'src\')"'
    print(f"  ✓ Hero image: {hero_img[:80]}..." if len(hero_img) > 80 else f"  ✓ Hero image: {hero_img}")
    print(f"  ✓ Service images: {len(service_imgs)} curated | {sum(1 for s in services if s.get('image_url'))} from brief.json")

    def resolve_image_path(img_url: str) -> str:
        """Resolve image paths relative to the output/ directory.
        Local paths in brief.json are relative to the project root (e.g. assets/images/X.png).
        The output HTML lives in output/, so local paths need ../prefix.
        Remote URLs (http/https) are returned as-is.
        """
        if not img_url:
            return ""
        if img_url.startswith("http://") or img_url.startswith("https://"):
            return img_url
        # Already resolved (starts with ../)
        if img_url.startswith("../"):
            return img_url
        # Local path — prefix with ../ since output is one level deep
        return f"../{img_url}"

    # Inject image URLs into each service object
    # Priority: 1) image_url from brief.json (curated per service, local or remote)
    #           2) images.json library by position
    #           3) hero fallback
    for i, svc in enumerate(services):
        curated_fallback = service_imgs[i % len(service_imgs)] if service_imgs else hero_img
        raw_url = svc.get("image_url") or curated_fallback
        svc["_image_url"] = resolve_image_path(raw_url)

    # Strip image_query and internal fields before sending to Claude.
    # image_query causes Claude to generate its own source.unsplash.com URLs — FORBIDDEN.
    STRIP_KEYS = {"image_query", "_image_url", "image_url"}
    clean_services = [{k: v for k, v in svc.items() if k not in STRIP_KEYS} for svc in services]
    services_json = json.dumps(clean_services, indent=2)
    benefits_json = json.dumps(benefits, indent=2)
    trust_json = json.dumps(trust, indent=2)
    testimonials_json = json.dumps(testimonials, indent=2)
    faq_json = json.dumps(faq, indent=2)
    cta_json = json.dumps(cta, indent=2)
    hero_json = json.dumps(hero, indent=2)
    lazy_attr = ' loading="lazy"' if use_lazy_loading else ""

    # Extract layout decisions — brand_strategy takes priority over ui-designer defaults
    hero_variant = (
        brand_strategy.get("hero_variant")
        or layout_data.get("hero_variant", "split-emotional")
    )
    layout_style = (
        brand_strategy.get("style_mode")
        or layout_data.get("layout_style", "premium-soft")
    )
    visual_intensity = (
        brand_strategy.get("visual_intensity")
        or layout_data.get("visual_intensity", "medium")
    )
    layout_variation = brand_strategy.get("layout_variation", "cards-3")
    spacing_scale = brand_strategy.get("spacing_scale", "balanced")
    image_direction = brand_strategy.get("image_direction", "photography-forward")
    visual_break = brand_strategy.get("visual_break", {})
    forbidden_patterns = brand_strategy.get("forbidden_patterns", [])
    design_concept = brand_strategy.get("design_concept", "")

    layout_json_summary = json.dumps({
        "hero_variant": hero_variant,
        "layout_style": layout_style,
        "visual_intensity": visual_intensity,
        "layout_variation": layout_variation,
        "spacing_scale": spacing_scale,
        "image_direction": image_direction,
        "visual_break": visual_break,
        "design_concept": design_concept,
        "forbidden_patterns": forbidden_patterns,
        "sections": [s.get("type", "") for s in layout_data.get("sections", [])]
    }, indent=2)
    print(f"  ✓ Layout: style={layout_style} | intensity={visual_intensity} | hero={hero_variant}")
    print(f"  ✓ Brand: layout={layout_variation} | spacing={spacing_scale} | image={image_direction}")
    if visual_break:
        print(f"  ✓ Visual break: {visual_break.get('type','?')} @ {visual_break.get('position','?')}")

    # Build hero instruction based on hero_variant from ui-designer
    if hero_variant == "cinematic":
        hero_instruction = (
            f"5. Hero <section id='hero'> — CINEMATIC VARIANT: full-bleed background image with dark gradient overlay, text centered.\n"
            f"   Background: <img src='{hero_img}' class='absolute inset-0 w-full h-full object-cover object-center' {img_onerror} loading='eager'>\n"
            f"   Dark overlay: gradient rgba(0,0,0,0.55) to rgba(0,0,0,0.35).\n"
            f"   Content: centered white H1 (max-w-4xl text-5xl md:text-6xl lg:text-7xl font-black), subheadline white/80, single large CTA button.\n"
            f"   Section height: min-h-[90vh]. No split grid — full width centered content.\n"
            f"   DO NOT add loading='lazy' to the hero image.\n"
        )
    elif hero_variant == "minimal-luxury":
        hero_instruction = (
            f"5. Hero <section id='hero'> — MINIMAL LUXURY VARIANT: solid brand-color or white background, NO background image.\n"
            f"   Layout: centered content, generous whitespace (py-32 md:py-40).\n"
            f"   Thin horizontal rule accent above headline. Oversized serif headline (text-6xl md:text-7xl font-black).\n"
            f"   Elegant subtext (text-xl text-gray-500 max-w-2xl). Single minimal CTA (border-2, no fill by default).\n"
            f"   Optional: small geometric decorative element (circle or line pattern, opacity 0.05).\n"
            f"   NO hero image needed. Brand identity comes from typography and whitespace.\n"
        )
    else:  # split-emotional (default)
        hero_instruction = (
            f"5. Hero <section id='hero'> — SPLIT EMOTIONAL VARIANT: 60% text left / 40% image right grid.\n"
            f"   Trust pill badge above H1. H1 headline from HERO data (text-4xl md:text-5xl lg:text-6xl font-black).\n"
            f"   Subheadline below. 2 CTA buttons: primary (filled) + secondary (outline). Star rating + review count below CTAs.\n"
            f"   Image column: portrait aspect (rounded-2xl shadow-xl), floating stat badge positioned -bottom-6 -left-6.\n"
            f"   Hero image EXACT URL: {hero_img}\n"
            f"   Hero img tag: <img src='{hero_img}' alt='Senior care' class='w-full h-full object-cover object-top rounded-2xl' {img_onerror} loading='eager'>\n"
            f"   On mobile: image appears ABOVE text (order-first lg:order-last on image div).\n"
            f"   DO NOT add loading='lazy' to the hero image.\n"
        )

    # Build pre-generated head extras
    og_tags = build_og_tags(seo, brief, hero_img)
    analytics_snippet = build_analytics_snippet(config)
    schema_block = build_schema_org(brief, config) if use_schema_org else ""

    # ── PART 1: DOCTYPE + HEAD + CSS + HEADER + HERO ─────────────────────────
    print("\n  → Part 1: Head + Header + Hero...")
    part1_msg = (
        f"Generate ONLY Part 1 of a premium index.html. Be concise — no inline comments.\n\n"
        f"CONTEXT: {shared_context}\n"
        f"LAYOUT DECISIONS (from ui-designer — follow exactly):\n{layout_json_summary}\n\n"
        f"HERO COPY: {hero_json}\n\n"
        f"OUTPUT:\n"
        f"1. <!DOCTYPE html> + <head>:\n"
        f"   - <meta charset='UTF-8'>\n"
        f"   - <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
        f"   - <title>{seo.get('meta_title', '')}</title>\n"
        f"   - <meta name='description' content='{seo.get('meta_description', '')}'>\n"
        f"   - Insert these tags EXACTLY as-is (do not modify or recreate them):\n"
        f"     {og_tags}\n"
        f"   - Tailwind CDN: <script src='https://cdn.tailwindcss.com'></script>\n"
        f"   - Google Fonts Inter\n"
        f"   - <style> block with:\n"
        f"     * :root {{ --color-primary: {primary_color}; --color-secondary: {secondary_color}; }}\n"
        f"     * body {{ font-family: 'Inter', sans-serif; }}\n"
        f"     * .reveal, .reveal-element {{ opacity: 0; transform: translateY(20px); transition: opacity 0.7s ease, transform 0.7s ease; }}\n"
        f"     * .reveal.visible, .reveal-element.visible {{ opacity: 1; transform: none; }}\n"
        f"     * .reveal-on-scroll {{ transition: opacity 0.7s ease, transform 0.7s ease; }}\n"
        f"     * .btn-primary {{ position:relative; overflow:hidden; }}\n"
        f"     * .btn-primary::after {{ content:''; position:absolute; top:0; left:-100%; width:60%; height:100%; background:linear-gradient(90deg,transparent,rgba(255,255,255,0.22),transparent); transition:left 0.5s ease; pointer-events:none; }}\n"
        f"     * .btn-primary:hover::after {{ left:150%; }}\n"
        f"     * .icon-circle {{ transition: background 0.25s ease; }}\n"
        f"     * .group:hover .icon-circle {{ background: {primary_color} !important; }}\n"
        f"     * .group:hover .icon-circle svg {{ color: white; stroke: white; }}\n"
        f"     * .faq-answer {{ max-height: 0; overflow: hidden; transition: max-height 0.45s cubic-bezier(0.22,1,0.36,1); }}\n"
        f"     * .faq-answer.open {{ max-height: 400px; }}\n"
        f"     * @keyframes whatsapp-pulse {{ 0%,100% {{ box-shadow: 0 0 0 0 rgba(37,211,102,0.55); }} 70% {{ box-shadow: 0 0 0 14px rgba(37,211,102,0); }} }}\n"
        f"     * .whatsapp-pulse {{ animation: whatsapp-pulse 2.2s infinite; }}\n"
        f"     * @media (max-width:767px) {{ body {{ padding-bottom: 68px; }} }}\n"
        f"     * @media (min-width:768px) {{ body {{ padding-bottom: 0 !important; }} }}\n"
        f"     * Custom scrollbar (6px, primary color thumb), sticky header backdrop-blur\n"
        f"   - Schema.org block — insert EXACTLY as-is:\n"
        f"     {schema_block}\n"
        f"   - Analytics — insert EXACTLY as-is (if empty string, skip):\n"
        f"     {analytics_snippet if analytics_snippet else '<!-- analytics disabled -->'}\n"
        f"2. <body> opens\n"
        f"3. Sticky <header> id='main-header': backdrop-blur-md bg-white/90 border-b shadow-sm, "
        f"logo img src='{logo}' class='h-10 w-auto', "
        f"nav links (Services/#services, Why Us/#benefits, Testimonials/#testimonials, FAQ/#faq, Contact/#contact), "
        f"phone tel:{phone} with icon, 'Free Consultation' btn-primary px-6 py-2.5 text-sm, mobile hamburger\n"
        f"4. Mobile nav dropdown (#mobile-menu, hidden by default)\n"
        f"{hero_instruction}"
        f"6. End with comment <!-- END PART 1 --> — DO NOT close body or html."
    )
    part1_raw, _ = call_claude(client, system_prompt, part1_msg, "Frontend Part 1 (Head+Hero)", max_tokens=8000)
    part1_html = extract_html(part1_raw)

    # ── PART 2: SERVICES + CTA BANNER + BENEFITS + TRUST ─────────────────────
    print("\n  → Part 2: Services + Benefits + Trust...")

    # Build per-card image tags — use _image_url (already resolved to final URL)
    service_cards_instruction = "COPY THESE EXACT <img> TAGS — DO NOT MODIFY SRC URLS:\n"
    for i, svc in enumerate(services):
        img_url = svc.get("_image_url") or hero_img
        svc_name = svc.get("name", svc.get("title", f"Service {i+1}"))
        service_cards_instruction += (
            f"  Card {i+1} ({svc_name}):\n"
            f"    <img src=\"{img_url}\" alt=\"{svc_name}\" "
            f"class=\"w-full h-52 object-cover object-center group-hover:scale-105 transition-transform duration-500\" "
            f"loading=\"lazy\" {img_onerror}>\n"
        )

    # Build dynamic services section instruction based on brand_strategy.layout_variation
    services_layout_instruction = build_services_layout_instruction(
        layout_variation, services, service_imgs, hero_img, img_onerror
    )

    # Build visual break instruction if it appears in Part 2 position
    vb_position = visual_break.get("position", "after-benefits")
    vb_part2_instruction = ""
    if vb_position in ("after-services",) and visual_break.get("type"):
        vb_part2_instruction = (
            f"\nVISUAL BREAK SECTION (place after services, before benefits):\n"
            f"  Type: {visual_break.get('type')} | Concept: {visual_break.get('concept','')}\n"
            f"  This MUST look dramatically different from all other sections.\n"
            f"  Use dark or full-bleed background. Reference the BRAND STRATEGY RENDERING section in your instructions.\n"
        )

    # Forbidden patterns instruction for Part 2
    forbidden_instruction = ""
    if forbidden_patterns:
        forbidden_instruction = f"\nFORBIDDEN PATTERNS (NEVER generate these):\n"
        for p in forbidden_patterns:
            forbidden_instruction += f"  - {p}\n"

    part2_msg = (
        f"Generate ONLY Part 2 of an index.html. Start immediately after <!-- END PART 1 -->.\n"
        f"NO DOCTYPE, NO html tag, NO head tag. Start directly with a <section> tag.\n\n"
        f"CONTEXT: {shared_context}\n"
        f"LAYOUT DECISIONS (brand_strategy takes priority):\n{layout_json_summary}\n\n"
        f"IMAGE RULES (ABSOLUTE — NEVER VIOLATE):\n"
        f"- COPY the exact <img> tags provided below — NEVER change src URLs\n"
        f"- NEVER use source.unsplash.com (deprecated and broken)\n"
        f"- NEVER generate your own image URLs from image_query or any query\n"
        f"- Image direction: '{image_direction}' — if 'illustration-icon' or 'minimal-no-image', use SVG icons instead of photos\n"
        f"- ALL images MUST have {img_onerror} as fallback\n"
        f"- ALL images MUST have loading='lazy' (except hero in Part 1)\n"
        f"- If you cannot find the img tag for a card → use the fallback gradient div\n\n"
        f"{service_cards_instruction}\n"
        f"SERVICES DATA (text content only — use img tags above for images):\n{services_json}\n"
        f"BENEFITS: {benefits_json}\n"
        f"TRUST: {trust_json}\n"
        f"PROCESS STEPS (How It Works — 3 steps): {process_steps_json}\n\n"
        f"{forbidden_instruction}"
        f"ANIMATION RULES:\n"
        f"- Do NOT use Tailwind 'opacity-0' or 'translate-y-10' inline classes\n"
        f"- Use class='reveal-element' for scroll-reveal animations\n"
        f"- Every <section> MUST have both opening AND closing tags\n\n"
        f"OUTPUT (generate ALL items fully before ending):\n"
        f"1. SERVICES section — use this EXACT layout pattern:\n"
        f"   {services_layout_instruction}\n"
        f"{vb_part2_instruction}"
        f"2. Inline CTA banner: gradient bg (primary to secondary), headline, subheadline, button → href='#contact'\n"
        f"3. <section id='benefits' class='py-14 md:py-20 bg-white'>:\n"
        f"   Section title + subtitle, then benefit items using layout from brand_strategy.section_layout_overrides.benefits\n"
        f"   Default: icon-list (icon in colored circle, bold title, description) in grid md:grid-cols-3\n"
        f"   Each card MUST have class='group' for hover effects to work\n"
        f"   MUST be fully generated — do not leave this section empty\n"
        f"4. <section id='trust' class='py-14 bg-gray-50'>:\n"
        f"   4 trust stats: large numbers in primary color, label text, subtle icon\n"
        f"   Use data from trust[] array\n"
        + (
            f"5. <section id='how-it-works' class='py-14 md:py-20 bg-white'>:\n"
            f"   How It Works — 3 numbered steps horizontal layout:\n"
            f"   Each step: large number badge, title, description\n"
            f"   Use PROCESS STEPS data above\n"
            f"6. "
            if process_steps else "5. "
        )
        + (
            f"<section id='comparison' class='py-14 md:py-20'>:\n"
            f"   Side-by-side comparison table — SitioPro vs. Agencias Tradicionales:\n"
            f"   2-column layout: left=SitioPro (brand color header, checkmarks), right=Traditional (gray header, X marks)\n"
            f"   Use comparison data: {comparison_json}\n"
            f"   This section is a KEY DIFFERENTIATOR — make it visually impactful\n"
            if comparison else
            f"Final CTA banner before ending Part 2\n"
        )
        + f"\nEnd with comment <!-- END PART 2 --> — DO NOT close body or html."
    )
    part2_raw, _ = call_claude(client, system_prompt, part2_msg, "Frontend Part 2 (Services+Benefits)", max_tokens=8000)
    part2_html = extract_html(part2_raw)

    # ── PART 3: TESTIMONIALS + FAQ + CTA + CONTACT + FOOTER + JS ─────────────
    print("\n  → Part 3: Testimonials + FAQ + Contact + Footer + JS...")

    # Analytics event tracking JS (config-driven)
    analytics = config.get("analytics", {})
    tracking_js = ""
    if config.get("output", {}).get("include_analytics", False) and analytics.get("ga4_id"):
        if analytics.get("track_cta_clicks", True):
            tracking_js += "\n    // Track CTA clicks\n    document.querySelectorAll('[data-track]').forEach(el => { el.addEventListener('click', () => { gtag('event', el.dataset.track); }); });"
        if analytics.get("track_form_submit", True):
            tracking_js += "\n    // Track form submit\n    const form = document.querySelector('#contact form'); if(form) form.addEventListener('submit', () => gtag('event', 'form_submit'));"
        if analytics.get("track_whatsapp_click", True):
            tracking_js += "\n    // Track WhatsApp click\n    document.querySelector('#wa-btn')?.addEventListener('click', () => gtag('event', 'whatsapp_click'));"

    # Visual break in Part 3 position
    vb_part3_instruction = ""
    if vb_position in ("after-testimonials", "after-benefits") and visual_break.get("type"):
        vb_part3_instruction = (
            f"\nVISUAL BREAK SECTION (place after testimonials):\n"
            f"  Type: {visual_break.get('type')} | Concept: {visual_break.get('concept','')}\n"
            f"  This MUST be the most dramatic section on the page.\n"
            f"  Full-bleed, dark or vivid background — completely different from white/gray sections.\n"
            f"  Reference the BRAND STRATEGY RENDERING section in your instructions.\n"
        )

    # Testimonials layout from brand_strategy
    testimonials_variant = brand_strategy.get("section_layout_overrides", {}).get("testimonials", "cards-gradient")
    if testimonials_variant == "dark-band":
        testimonials_bg = f"py-20 bg-[{primary_color}]"
        testimonials_style = "Dark background, white text quotes, large quotation marks, horizontal rule separators between testimonials"
    elif testimonials_variant == "magazine-feature":
        testimonials_bg = "py-20 bg-gray-50"
        testimonials_style = "1 large featured testimonial (col-span-2) + 2 smaller testimonials in row, subtle card style"
    else:  # cards-gradient (default)
        testimonials_bg = f"py-20 bg-gradient-to-br from-[{primary_color}] to-[{secondary_color}]"
        testimonials_style = "White card grid, ★★★★★ stars, testimonial text, name+role, hover shadow"

    part3_msg = (
        f"Generate ONLY Part 3 (the FINAL part) of an index.html. Start immediately after <!-- END PART 2 -->.\n"
        f"NO DOCTYPE, NO html, NO head. Start with a <section> tag. MUST end with </body></html>.\n\n"
        f"CONTEXT: {shared_context}\n"
        f"LAYOUT DECISIONS (brand_strategy):\n{layout_json_summary}\n\n"
        f"TESTIMONIALS: {testimonials_json}\n"
        f"FAQ: {faq_json}\n"
        f"CTA: {cta_json}\n"
        f"PRICING PLANS: {pricing_json}\n\n"
        f"ANIMATION RULES:\n"
        f"- Do NOT use Tailwind 'opacity-0' or 'translate-y-10' inline classes\n"
        f"- Use class='reveal-element' for scroll-reveal\n"
        f"- Every <section> MUST open and close in this part\n\n"
    )

    # Build numbered output list for Part 3 dynamically
    n = 1
    part3_sections = f"OUTPUT (generate ALL items — NEVER truncate):\n"
    part3_sections += f"{n}. <section id='testimonials' class='{testimonials_bg}'>:\n"
    part3_sections += f"   Style: {testimonials_style}\n"
    part3_sections += vb_part3_instruction
    n += 1
    if pricing:
        part3_sections += (
            f"{n}. <section id='pricing' class='py-14 md:py-20 bg-gray-50'>:\n"
            f"   3-column pricing grid — use PRICING PLANS data above\n"
            f"   Highlighted plan gets border-2 border-[--color-primary] and slight scale emphasis\n"
            f"   Each plan: name, price (large, bold), description, checkmark feature list, CTA button\n"
        )
        n += 1
    part3_sections += (
        f"{n}. <section id='faq' class='py-14 bg-white'>:\n"
        f"   FAQ accordion — each .faq-item has a button (toggle .open class) and .faq-answer div\n"
        f"   Use data from FAQ array provided\n"
    )
    n += 1
    part3_sections += f"{n}. Final CTA section: dark gradient bg, bold headline, subheadline, single primary CTA button\n"
    n += 1

    part3_tail = (
        f"{n}. <section id='contact' class='py-20 bg-gray-50'>:\n"
        f"   Split layout: left=contact form (name/phone/message/submit button), "
        f"right=contact info card (phone:{phone}, email:{email}, address:{address}, hours:24/7)\n"
        f"   Form id='contact-form', submit button id='form-submit-btn'\n"
    )
    n += 1
    part3_tail += (
        f"{n}. <footer>: dark gradient bg, logo img src='{logo}' class='h-12 w-auto brightness-0 invert', "
        f"tagline, nav links in columns, social icons (FB/IG/LinkedIn href='#'), copyright line\n"
    )
    n += 1
    part3_tail += (
        f"{n}. WhatsApp button: id='wa-btn', fixed bottom-6 right-6, z-50, rounded-full, green bg, "
        f"pulse animation class='wa-pulse', href='https://wa.me/{whatsapp}', target='_blank'\n"
    )
    n += 1
    part3_tail += (
        f"{n}. Mobile sticky CTA bar: class='mobile-cta-bar fixed bottom-0 left-0 right-0 z-40 bg-white border-t shadow-lg p-3 gap-2':\n"
        f"   Two buttons — Call Now (tel:{phone}) and WhatsApp (wa.me/{whatsapp})\n"
    )
    n += 1
    part3_tail += (
        f"{n}. ONE <script> block containing ALL JavaScript:\n"
        f"   a) IntersectionObserver: observe '.reveal-element, .reveal', add 'visible' class at threshold 0.1, "
        f"also immediately activate elements already in viewport on window load\n"
        f"   b) FAQ accordion: querySelectorAll('.faq-item button'), toggle 'open' on parent .faq-item\n"
        f"   c) Mobile menu toggle: hamburger button toggles #mobile-menu visibility\n"
        f"   d) Sticky header: add shadow class on scroll > 50px\n"
        f"   e) Form submit: prevent default, redirect to https://wa.me/{whatsapp}?text=...\n"
        f"   f) Analytics tracking (insert verbatim):{tracking_js if tracking_js else ' // analytics disabled'}\n"
    )
    n += 1
    part3_tail += f"{n}. Close with </body></html>"
    part3_msg = part3_msg + part3_sections + part3_tail
    part3_raw, stop3 = call_claude(client, system_prompt, part3_msg, "Frontend Part 3 (Footer+JS)", max_tokens=8000)
    part3_html = extract_html(part3_raw)

    if stop3 == "max_tokens" and "</html>" not in part3_html:
        print("  WARNING: Part 3 hit token limit — appending closing tags")
        part3_html += "\n</body>\n</html>"

    full_html = part1_html + "\n" + part2_html + "\n" + part3_html
    print(f"  ✓ Frontend complete: {len(part1_html):,} + {len(part2_html):,} + {len(part3_html):,} = {len(full_html):,} chars total")
    return full_html


def extract_json(text: str) -> str:
    """Extract JSON block from LLM response."""
    if "```json" in text:
        start = text.find("```json") + 7
        end = text.find("```", start)
        return text[start:end].strip()
    if text.strip().startswith("{"):
        return text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        return text[start:end]
    return text


def extract_html(text: str) -> str:
    """Extract HTML from LLM response."""
    if "```html" in text:
        start = text.find("```html") + 7
        end = text.find("```", start)
        if end == -1:
            return text[start:].strip()
        return text[start:end].strip()
    if "<!DOCTYPE" in text or "<html" in text or text.strip().startswith("<section"):
        return text.strip()
    return text


def validate_copy_json(copy_json: dict) -> list[str]:
    """Validate that the output contract is respected."""
    errors = []
    required_keys = ["hero", "services", "benefits", "trust", "testimonials", "faq", "cta"]
    for key in required_keys:
        if key not in copy_json:
            errors.append(f"Missing key: '{key}'")

    hero_keys = ["headline", "subheadline", "cta_primary", "cta_secondary"]
    for key in hero_keys:
        if key not in copy_json.get("hero", {}):
            errors.append(f"Missing hero.{key}")

    for array_key in ["services", "benefits", "trust", "testimonials", "faq"]:
        if not isinstance(copy_json.get(array_key), list):
            errors.append(f"'{array_key}' must be an array")

    return errors


def run_pipeline(client_id: str):
    print(f"\n{'='*60}")
    print(f"  WEB AGENT PIPELINE")
    print(f"  Client: {client_id}")
    print(f"{'='*60}")

    # Init Claude client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found in .env")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Load client data
    print("\n[1/7] Loading client data...")
    config, brief = load_client(client_id)
    client_dna = load_client_dna(client_id)
    template_name = config["template"]
    prompts = load_prompts(template_name)
    brief_str = json.dumps(brief, indent=2)
    dna_str = json.dumps(client_dna, indent=2) if client_dna else "{}"
    print(f"  ✓ Template: {template_name} | Language: {config['language']} | Goal: {config['goal']}")
    print(f"  ✓ Features: lazy_loading={config.get('features',{}).get('lazy_loading')} | "
          f"schema_org={config.get('features',{}).get('schema_org')} | "
          f"analytics={config.get('output',{}).get('include_analytics')}")
    # Report which supplementary systems are active
    active_systems = []
    if (CORE_DIR / "style-engine.md").exists(): active_systems.append("style-engine")
    if (CORE_DIR / "hero-system.md").exists(): active_systems.append("hero-system")
    if (CORE_DIR / "component-system.md").exists(): active_systems.append("component-system")
    if (CORE_DIR / "art-director.md").exists(): active_systems.append("art-director")
    if (AGENTS_DIR / "brand-strategist.md").exists(): active_systems.append("brand-strategist")
    if client_dna: active_systems.append("client-dna")
    if active_systems:
        print(f"  ✓ Active systems: {', '.join(active_systems)}")

    # STEP 1 — Business Analysis
    print("\n[2/7] Business Analysis")
    analysis_raw, _ = call_claude(
        client,
        system_prompt=prompts["business_analyzer"],
        user_message=f"Analyze this business brief and return the JSON analysis:\n\n{brief_str}",
        step_name="Business Analyzer",
    )
    analysis_json_str = extract_json(analysis_raw)
    try:
        analysis = json.loads(analysis_json_str)
    except json.JSONDecodeError:
        print("  WARNING: Could not parse analysis JSON, using raw text")
        analysis = {"raw": analysis_raw}

    # STEP 1.2 — Brand Strategy (NEW)
    brand_strategy = {}
    if prompts.get("brand_strategist"):
        print("\n[2.5/7] Brand Strategy")
        brand_raw, _ = call_claude(
            client,
            system_prompt=prompts["brand_strategist"],
            user_message=(
                f"Define brand strategy and design decisions for this client. Return ONLY valid JSON.\n\n"
                f"BUSINESS ANALYSIS:\n{json.dumps(analysis, indent=2)}\n\n"
                f"CLIENT BRIEF:\n{brief_str}\n\n"
                f"CLIENT DNA:\n{dna_str}\n\n"
                f"Return JSON with: style_mode, design_concept, hero_variant, layout_variation, "
                f"visual_intensity, spacing_scale, image_direction, primary_color, accent_color, "
                f"visual_break, section_layout_overrides, forbidden_patterns, layout_notes"
            ),
            step_name="Brand Strategist",
        )
        brand_json_str = extract_json(brand_raw)
        try:
            brand_strategy = json.loads(brand_json_str)
            # Layout uniqueness check
            warnings = check_layout_uniqueness(brand_strategy, analysis.get("business_type", ""))
            for w in warnings:
                print(f"  ⚠  UNIQUENESS WARNING: {w}")
            print(f"  ✓ Brand: {brand_strategy.get('style_mode')} | "
                  f"layout={brand_strategy.get('layout_variation')} | "
                  f"hero={brand_strategy.get('hero_variant')} | "
                  f"color={brand_strategy.get('primary_color')}")
        except json.JSONDecodeError:
            print("  WARNING: Brand strategist returned invalid JSON — continuing without brand strategy")
            brand_strategy = {}
    else:
        print("\n  ℹ  brand-strategist.md not found — skipping brand strategy step")

    # STEP 2 — Copywriting
    print("\n[3/7] Copy Generation")
    copy_raw, _ = call_claude(
        client,
        system_prompt=prompts["copywriter"],
        user_message=(
            f"Generate the website copy using this data:\n\n"
            f"BUSINESS ANALYSIS:\n{json.dumps(analysis, indent=2)}\n\n"
            f"INDUSTRY TEMPLATE:\n{prompts['template']}\n\n"
            f"CLIENT BRIEF:\n{brief_str}\n\n"
            f"OUTPUT CONTRACT:\n{prompts['output_contract']}\n\n"
            f"Return ONLY valid JSON following the output contract structure."
        ),
        step_name="Copywriter",
    )
    copy_json_str = extract_json(copy_raw)
    try:
        copy_data = json.loads(copy_json_str)
    except json.JSONDecodeError:
        print("  ERROR: Copywriter returned invalid JSON. Aborting.")
        print("  Raw output saved to debug_copy.txt")
        Path("debug_copy.txt").write_text(copy_raw, encoding="utf-8")
        sys.exit(1)

    errors = validate_copy_json(copy_data)
    if errors:
        print(f"  WARNING: Contract violations found:")
        for e in errors:
            print(f"    - {e}")
    else:
        print("  ✓ Output contract validated")

    # STEP 3 — SEO Optimization
    print("\n[4/7] SEO Optimization")
    seo_raw, _ = call_claude(
        client,
        system_prompt=prompts["seo_optimizer"],
        user_message=(
            f"Optimize this copy for SEO. Return the SAME JSON structure with a new 'seo' field added.\n\n"
            f"BUSINESS ANALYSIS:\n{json.dumps(analysis, indent=2)}\n\n"
            f"COPY JSON:\n{json.dumps(copy_data, indent=2)}"
        ),
        step_name="SEO Optimizer",
    )
    seo_json_str = extract_json(seo_raw)
    try:
        seo_data = json.loads(seo_json_str)
    except json.JSONDecodeError:
        print("  WARNING: SEO optimizer returned invalid JSON, using copy data without SEO")
        seo_data = copy_data

    # Merge branding and contact from brief
    seo_data["business"] = {
        "name": brief.get("business_name", ""),
        "type": brief.get("business_type", ""),
        "location": brief.get("location", ""),
        "phone": brief.get("contact_info", {}).get("phone", ""),
        "whatsapp": brief.get("whatsapp", ""),
    }
    seo_data["branding"] = brief.get("branding", {})
    seo_data["contact"] = brief.get("contact_info", {})

    # STEP 4 — UI Design
    print("\n[5/7] UI Layout Design")
    brand_strategy_summary = json.dumps(brand_strategy, indent=2) if brand_strategy else "{}"
    layout_raw, _ = call_claude(
        client,
        system_prompt=prompts["ui_designer"],
        user_message=(
            f"Design the layout for this website. Return JSON with layout_style, visual_intensity, hero_variant, and sections array.\n\n"
            f"BRAND STRATEGY (READ FIRST — overrides defaults):\n{brand_strategy_summary}\n\n"
            f"COPY & SEO DATA:\n{json.dumps(seo_data, indent=2)}\n\n"
            f"BUSINESS ANALYSIS:\n{json.dumps(analysis, indent=2)}\n\n"
            f"INDUSTRY TEMPLATE:\n{prompts['template']}"
        ),
        step_name="UI Designer",
    )
    layout_json_str = extract_json(layout_raw)
    try:
        layout_data = json.loads(layout_json_str)
    except json.JSONDecodeError:
        print("  WARNING: UI Designer returned invalid JSON, using minimal layout")
        layout_data = {"layout_style": "premium-soft", "visual_intensity": "medium", "sections": []}

    # STEP 5 — Frontend Generation (3-part strategy)
    print("\n[6/7] Frontend Generation")
    html_content = generate_frontend(
        client, prompts["frontend_dev"], brief, config, seo_data, layout_data, brand_strategy
    )

    # Save output
    output_dir = PROJECTS_DIR / client_id / "output"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "index.html"
    output_file.write_text(html_content, encoding="utf-8")

    # Update generation log for uniqueness tracking
    print("\n[7/7] Updating generation log...")
    if brand_strategy:
        update_generation_log(client_id, brand_strategy, analysis.get("business_type", "unknown"))
        print(f"  ✓ Generation logged: {brand_strategy.get('style_mode')} / {brand_strategy.get('layout_variation')}")

    print(f"\n{'='*60}")
    print(f"  PIPELINE COMPLETE")
    print(f"  Output: projects/{client_id}/output/index.html")
    print(f"  Size: {len(html_content):,} characters")
    if brand_strategy:
        print(f"  Brand: {brand_strategy.get('design_concept', '')}")
        print(f"  Style: {brand_strategy.get('style_mode')} | layout={brand_strategy.get('layout_variation')} | color={brand_strategy.get('primary_color')}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Agent - AI Website Generator")
    parser.add_argument("--client", required=True, help="Client ID (folder name in /projects/)")
    args = parser.parse_args()
    run_pipeline(args.client)
