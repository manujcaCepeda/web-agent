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

# ── GROUNDING RULE — injected into every frontend prompt ─────────────────────
# Prevents the LLM from hallucinating data not present in brief.json
GROUNDING_RULE = """
CONTENT GROUNDING RULES (ABSOLUTE — NO EXCEPTIONS):
- Use ONLY data provided in this prompt. NEVER invent, extrapolate, or assume content.
- NEVER invent: client names, portfolio items, case studies, revenue figures, team members, awards, certifications, partner logos, press mentions.
- STATS: Use ONLY the exact stat values from the TRUST array. NEVER inflate (e.g. if brief says "10+ years" do NOT write "15+ years").
- TESTIMONIALS: Use ONLY testimonials from the TESTIMONIALS array. NEVER generate fictional testimonials.
- PORTFOLIO: If no portfolio data is provided → DO NOT generate a portfolio section. Skip it entirely.
- SERVICES: Use ONLY service names and descriptions from the SERVICES array. Never add services not listed.
- BENEFITS: Use ONLY the benefits data provided. Never add benefit items not in the array.
- FAQ: Use ONLY the FAQ questions/answers provided. Never add questions not in the FAQ array.
- If a section has no data → skip it or use a simple placeholder, NEVER fabricate content.
"""


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


def load_client_facts(client_id: str) -> str:
    """Load optional client-facts.md — real verified client data in natural language.
    This file is the single source of truth for all stats, testimonials, and claims.
    Returns the raw text, or empty string if not present.
    """
    facts_path = PROJECTS_DIR / client_id / "client-facts.md"
    if facts_path.exists():
        try:
            facts = read_file(facts_path)
            print(f"  ✓ client-facts.md loaded ({len(facts)} chars) — grounding active")
            return facts
        except Exception as e:
            print(f"  WARNING: client-facts.md read error: {e} — continuing without facts")
    else:
        print(f"  ℹ  client-facts.md not found — add it to prevent content hallucination")
    return ""


def load_client_images(client_id: str) -> dict:
    """Auto-discover client-provided images from projects/{client_id}/assets/images/.

    Returns: {header_logo, footer_logo, services: [list of relative paths]}
    Priority over curated images.json library when client images exist.

    Naming convention (inside assets/images/):
      - File named exactly 'Logo.*'      → footer icon (compact version)
      - Any other root-level image file  → header logo (full logo with text)
      - assets/images/services/*.{png,jpg,jpeg,webp} → service photos (sorted)
    """
    assets_dir = PROJECTS_DIR / client_id / "assets" / "images"
    result = {"header_logo": "", "footer_logo": "", "services": []}
    if not assets_dir.exists():
        return result

    for f in assets_dir.iterdir():
        if f.is_file() and f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.svg', '.webp'):
            if f.stem.lower() == 'logo':
                result["footer_logo"] = f"assets/images/{f.name}"
            else:
                result["header_logo"] = f"assets/images/{f.name}"

    services_dir = assets_dir / "services"
    if services_dir.exists():
        result["services"] = sorted([
            f"assets/images/services/{f.name}"
            for f in services_dir.iterdir()
            if f.is_file() and f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp')
        ])

    if result["header_logo"] or result["footer_logo"] or result["services"]:
        print(f"  ✓ Client images: header_logo={'yes' if result['header_logo'] else 'no'} | "
              f"footer_logo={'yes' if result['footer_logo'] else 'no'} | "
              f"services={len(result['services'])} images (take priority over curated library)")
    else:
        print(f"  ℹ  No client images in assets/images/ — using curated library for all images")

    return result


def load_reference_screenshots(url: str, client_id: str) -> list[bytes]:
    """Capture the full reference site as multiple section screenshots using Playwright.

    Strategy: render at 1440px wide, measure total page height, then take
    overlapping viewport-sized clips that together cover the entire page.
    Each clip is saved as reference-screenshot-N.png for inspection.

    Returns a list of PNG bytes (one per section). Empty list on failure.
    The screenshots are cached — delete them to force a fresh capture.
    """
    if not url or not url.startswith("http"):
        return []

    ref_dir = PROJECTS_DIR / client_id
    VIEWPORT_W, VIEWPORT_H = 1440, 900

    # Check cache — all section files must exist
    cached = sorted(ref_dir.glob("reference-screenshot-*.png"))
    if cached:
        result = [f.read_bytes() for f in cached]
        print(f"  ✓ Reference screenshots (cached): {len(result)} sections from {url}")
        return result

    # Also accept the old single-file cache for backwards compat
    old_cache = ref_dir / "reference-screenshot.png"
    if old_cache.exists():
        old_cache.unlink()  # delete old single screenshot to force re-capture

    print(f"  → Capturing full reference site: {url}")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_viewport_size({"width": VIEWPORT_W, "height": VIEWPORT_H})
            page.goto(url, wait_until="networkidle", timeout=40000)
            page.wait_for_timeout(3000)  # let lazy-loaded content + animations settle

            # Measure total page height
            total_height = page.evaluate("document.documentElement.scrollHeight")
            print(f"  → Page height: {total_height}px — capturing sections...")

            # Distribute up to 6 scroll positions evenly across full page height
            MAX_SECTIONS = 6
            if total_height <= VIEWPORT_H:
                offsets = [0]
            else:
                # Evenly spaced: first at top, last near bottom
                offsets = [
                    int(i * (total_height - VIEWPORT_H) / (MAX_SECTIONS - 1))
                    for i in range(MAX_SECTIONS)
                ]

            sections = []
            for i, y_offset in enumerate(offsets):
                # Scroll to position, wait for any scroll-triggered animations
                page.evaluate(f"window.scrollTo(0, {y_offset})")
                page.wait_for_timeout(800)
                # Screenshot captures exactly what's visible in the viewport
                png = page.screenshot(full_page=False)
                path = ref_dir / f"reference-screenshot-{i+1:02d}.png"
                path.write_bytes(png)
                sections.append(png)
                print(f"  ✓ Section {i+1}/{len(offsets)}: scroll y={y_offset}px → {len(png)//1024}KB")

            browser.close()

        print(f"  ✓ Reference capture complete: {len(sections)} sections, "
              f"total {sum(len(s) for s in sections)//1024}KB")
        return sections

    except Exception as e:
        print(f"  WARNING: Could not capture reference screenshots: {e}")
        return []


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
        "page_personality": brand_strategy.get("page_personality", ""),
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


def call_claude(client: anthropic.Anthropic, system_prompt: str, user_message: str, step_name: str, max_tokens: int = 8192, image_bytes: bytes | None = None, image_bytes_list: list[bytes] | None = None) -> str:
    """Call Claude API. Supports vision via image_bytes (single) or image_bytes_list (multiple).

    When multiple images are provided, they are sent in order before the text message
    so Claude can analyze all sections of a reference site in one call.
    """
    print(f"\n  → Running: {step_name}...")

    import base64

    def _img_block(png: bytes) -> dict:
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": base64.standard_b64encode(png).decode("utf-8"),
            },
        }

    # Build content list
    images = image_bytes_list or ([image_bytes] if image_bytes else [])
    if images:
        content = []
        if len(images) > 1:
            content.append({"type": "text", "text": f"The following {len(images)} images show the reference website from top to bottom (section by section):"})
        for png in images:
            content.append(_img_block(png))
        content.append({"type": "text", "text": user_message})
        print(f"  → Vision: {len(images)} image(s) attached")
    else:
        content = user_message

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": content}],
    )

    result = message.content[0].text
    stop_reason = message.stop_reason
    print(f"  ✓ {step_name} complete ({len(result)} chars) [stop: {stop_reason}]")
    return result, stop_reason


def enforce_dna_style_mode(brand_strategy: dict, client_dna: dict) -> dict:
    """Enforce client-dna.json style_preference over brand-strategist output.

    The LLM can misread color signals (e.g. indigo primary → luxury-dark) and
    override the explicit client DNA. This function hard-corrects that.
    """
    if not client_dna:
        return brand_strategy

    dna_vi = client_dna.get("visual_identity", {})
    dna_style = dna_vi.get("style_preference", "")
    bs_style = brand_strategy.get("style_mode", "")

    if dna_style and bs_style and bs_style != dna_style:
        print(f"  ⚠  STYLE CONFLICT: client-dna='{dna_style}' vs brand-strategist='{bs_style}'")
        print(f"  → Enforcing client-dna style_mode: '{dna_style}'")
        brand_strategy["style_mode"] = dna_style

    # Enforce exact color palette from client-dna if defined
    dna_palette = client_dna.get("color_palette", {})
    if dna_palette.get("primary"):
        if brand_strategy.get("primary_color") != dna_palette["primary"]:
            print(f"  → Enforcing client-dna primary_color: {dna_palette['primary']}")
            brand_strategy["primary_color"] = dna_palette["primary"]
    if dna_palette.get("accent"):
        if brand_strategy.get("accent_color") != dna_palette["accent"]:
            brand_strategy["accent_color"] = dna_palette["accent"]

    # Enforce forbidden patterns from client-dna (additive — merge with brand-strategist list)
    dna_forbidden = client_dna.get("design_direction", {}).get("forbidden_patterns", [])
    bs_forbidden = brand_strategy.get("forbidden_patterns", [])
    if dna_forbidden:
        merged = list(dict.fromkeys(bs_forbidden + dna_forbidden))  # dedup, preserve order
        brand_strategy["forbidden_patterns"] = merged

    return brand_strategy


def load_design_tokens(style_mode: str) -> str:
    """Load CSS variables block for the active style_mode from design-language.json.

    Returns the :root {} CSS block as a string, ready to inject verbatim into <style>.
    Falls back to empty string if design-language.json is missing or mode not found.
    """
    dl_path = CORE_DIR / "design-language.json"
    if not dl_path.exists():
        return ""
    try:
        dl = json.loads(read_file(dl_path))
        mode = dl.get("style_modes", {}).get(style_mode, {})
        css_vars = mode.get("css_variables", "")
        if css_vars:
            print(f"  ✓ Design tokens loaded: {style_mode} ({len(css_vars)} chars)")
        return css_vars
    except Exception as e:
        print(f"  WARNING: Could not load design tokens for '{style_mode}': {e}")
        return ""


def build_header_instruction(style_mode: str, logo: str, phone: str, primary_color: str) -> str:
    """Build mode-aware sticky header HTML instruction.

    Dark modes (luxury-dark, luxury-service) get a dark translucent header.
    Light modes (all others) get a white/glass light header.
    Logo src is only injected if it's a non-empty string.
    """
    dark_modes = {"luxury-dark", "luxury-service"}
    is_dark = style_mode in dark_modes

    if is_dark:
        header_bg = "bg-[rgba(15,23,42,0.92)] backdrop-blur-xl border-b border-white/10 shadow-[0_1px_20px_rgba(0,0,0,0.3)]"
        nav_text = "text-slate-300 hover:text-white"
        cta_extra = "text-white"
    else:
        header_bg = "bg-white/95 backdrop-blur-md border-b border-gray-100 shadow-sm"
        nav_text = "text-gray-600 hover:text-gray-900 font-semibold"
        cta_extra = ""

    # Logo: use img tag if logo path is set, otherwise text-based logo
    if logo and logo.strip():
        logo_html = f"<img src='{logo}' alt='Logo' class='h-10 w-auto'>"
    else:
        logo_html = (
            f"<span class='text-xl font-black tracking-tight' style='color:{primary_color};'>"
            "{{business_name_first_word}}</span>"
            "<span class='text-xl font-black tracking-tight text-gray-900'>{{business_name_rest}}</span>"
        )

    return (
        f"3. Sticky <header id='main-header' class='{header_bg}' style='position:sticky;top:0;z-index:50;'>:\n"
        f"   Logo: {logo_html}\n"
        f"   Nav links ({nav_text}): Services/#services, Why Us/#benefits, Testimonials/#testimonials, FAQ/#faq, Contact/#contact\n"
        f"   Right: phone tel:{phone} with SVG phone icon, then 'Free Consultation'/'Asesoría Gratuita' btn-primary px-6 py-2.5 text-sm {cta_extra}\n"
        f"   Mobile hamburger button (lg:hidden) id='hamburger'\n"
    )


def validate_html(html: str, brand_strategy: dict, brief: dict) -> list[str]:
    """Run structural checks against generated HTML.

    Returns a list of findings (FAIL/WARN/OK). FAIL = regeneration candidate.
    These are real grep-style checks, not aspirational documentation.
    """
    findings = []
    html_lower = html.lower()

    # ── CHECK 1: Editorial-list service duplication ──────────────────────────
    if brand_strategy.get("layout_variation") == "editorial-list":
        # First service should appear in featured card AND NOT repeated in numbered list with image
        services = brief.get("services", [])
        if services:
            svc0_name = services[0].get("name", "")
            # Count occurrences: if svc0_name appears 3+ times it's likely duplicated
            count = html_lower.count(svc0_name.lower())
            if count >= 3:
                findings.append(f"WARN: Service '{svc0_name}' appears {count}x — possible duplication in editorial-list")

    # ── CHECK 2: Visual break presence ───────────────────────────────────────
    vb_type = brand_strategy.get("visual_break", {}).get("type", "")
    if vb_type:
        dark_indicators = ["section-dark", "bg-[--color-bg-dark]", "#0f172a", "#1a3a37", "bg-[var(--color-bg-dark"]
        has_dark_section = any(ind in html_lower for ind in dark_indicators)
        if not has_dark_section:
            findings.append(f"FAIL: Visual break type '{vb_type}' — no dark section found in HTML")
        else:
            findings.append(f"OK: Visual break section present")

    # ── CHECK 3: Hallucinated portfolio guard ────────────────────────────────
    has_portfolio_data = bool(brief.get("portfolio", []))
    has_portfolio_section = 'id="portfolio"' in html or "id='portfolio'" in html
    if has_portfolio_section and not has_portfolio_data:
        findings.append("CRITICAL: Portfolio section generated but NO portfolio data in brief.json — hallucination risk")

    # ── CHECK 4: Stats grounding ──────────────────────────────────────────────
    trust_items = brief.get("trust", [])
    for item in trust_items:
        stat = item.get("stat", "").strip()
        if stat and stat not in html:
            # Try without + sign
            stat_clean = stat.replace("+", "").replace("%", "").strip()
            if stat_clean and stat_clean not in html:
                findings.append(f"WARN: Stat '{stat}' from brief.json not found in HTML — possible inflation")

    # ── CHECK 5: Hero variant structural match ────────────────────────────────
    hero_variant = brand_strategy.get("hero_variant", "")
    if hero_variant == "split-emotional":
        has_split = "lg:grid-cols-2" in html or "md:grid-cols-2" in html
        if not has_split:
            findings.append("WARN: split-emotional hero variant — no 2-column grid found in hero area")

    # ── CHECK 6: Back-to-back dark sections ──────────────────────────────────
    dark_section_class = "section-dark"
    positions = [i for i in range(len(html)) if html[i:i+len(dark_section_class)] == dark_section_class]
    if len(positions) >= 2:
        # Check if two dark sections are within 500 chars of each other
        for i in range(len(positions) - 1):
            if positions[i+1] - positions[i] < 800:
                findings.append("WARN: Two dark sections appear back-to-back (< 800 chars apart) — alternation violated")
                break

    return findings


def build_services_layout_instruction(layout_variation: str, services: list, service_imgs: list, hero_img: str, img_onerror: str) -> str:
    """Build dynamic services section instruction based on brand_strategy.layout_variation."""

    if layout_variation == "editorial-list":
        return (
            "<section id='services' class='py-14 md:py-20 bg-[var(--color-bg-alt,#F9FAFB)]'>:\n"
            "   EDITORIAL LAYOUT — NOT a standard card grid:\n"
            "   ──────────────────────────────────────────────────────────────────\n"
            "   FEATURED CARD (services[0] ONLY): full-width horizontal lg:flex-row\n"
            "     Left 60%: 'Más solicitado' badge, h3 headline, description, chip tags\n"
            "     Right 40%: image from services[0]\n"
            "   ──────────────────────────────────────────────────────────────────\n"
            "   NUMBERED GRID (services[1], services[2] ... services[N]):\n"
            "   ⚠ CRITICAL: Do NOT include services[0] here — it is already shown above.\n"
            "   ⚠ Start numbering at 02 for services[1], 03 for services[2], etc.\n"
            "   Grid: grid md:grid-cols-2 gap-5\n"
            "     Each item: flex gap-5 — number badge (02,03...) text-5xl font-black opacity-15 | title + description + 3 chip tags\n"
            "     NO images in numbered items — typography-forward\n"
            "   ──────────────────────────────────────────────────────────────────\n"
            "   Result: 1 featured card + all remaining services as numbered items = ALL services shown exactly once.\n"
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


def build_section_flow(page_personality: str, section_order: list, has_process: bool, has_comparison: bool, has_pricing: bool) -> dict:
    """Derive which sections to generate in Part 2 and Part 3 based on page_personality.

    Returns a dict with keys:
      part2_sections: list of section IDs to include in Part 2
      part3_sections: list of section IDs to include in Part 3
      skip_faq: bool — True when page_personality is conversion-fast
    """
    # Default full flow if section_order is empty (backwards compat)
    if not section_order:
        if page_personality == "conversion-fast":
            section_order = ["hero", "trust-band", "services", "visual-break", "testimonials", "cta", "contact"]
        elif page_personality == "authority":
            section_order = ["hero", "stats-bar", "services", "visual-break", "benefits", "badge-grid", "testimonials", "cta", "contact"]
        elif page_personality == "product":
            section_order = ["hero", "services", "how-it-works", "visual-break", "comparison", "testimonials", "pricing", "faq", "contact"]
        else:  # storytelling (default)
            section_order = ["hero", "services", "how-it-works", "cta-banner", "stats-bar", "benefits", "badge-grid", "wow-section", "testimonials", "faq", "cta", "contact"]

    # Part 1 always: hero (fixed)
    # Part 2: services-region sections
    part2_ids = {"services", "cta-banner", "benefits", "trust-band", "stats-bar", "how-it-works", "comparison", "badge-grid"}
    # Part 3: testimonials-region sections
    part3_ids = {"testimonials", "wow-section", "faq", "pricing", "cta", "visual-break", "contact"}

    part2 = [s for s in section_order if s in part2_ids]
    part3 = [s for s in section_order if s in part3_ids]

    # Always ensure contact is last in part3
    if "contact" not in part3:
        part3.append("contact")

    # visual-break: place it in part2 or part3 based on position in section_order
    # (if it's before testimonials, put in part2; if after, put in part3)
    testimonials_idx = section_order.index("testimonials") if "testimonials" in section_order else 999
    services_idx = section_order.index("services") if "services" in section_order else 0
    vb_idx = section_order.index("visual-break") if "visual-break" in section_order else 999
    if "visual-break" in section_order:
        if vb_idx < testimonials_idx:
            if "visual-break" not in part2:
                part2.append("visual-break")
        else:
            if "visual-break" not in part3:
                part3.insert(0, "visual-break")

    skip_faq = "faq" not in section_order
    return {
        "part2_sections": part2,
        "part3_sections": part3,
        "skip_faq": skip_faq,
        "section_order": section_order,
    }


def generate_frontend(client: anthropic.Anthropic, system_prompt: str, brief: dict, config: dict, seo_data: dict, layout_data: dict, brand_strategy: dict = None, client_facts: str = "", client_images: dict = None) -> str:
    """Generate frontend HTML in three focused parts to avoid token limits."""
    if brand_strategy is None:
        brand_strategy = {}
    if client_images is None:
        client_images = {}

    # Resolve active style_mode (brand_strategy is already DNA-enforced at this point)
    active_style_mode = brand_strategy.get("style_mode", "premium-care")

    # Load design tokens from design-language.json — inject as hardcoded CSS (not LLM choice)
    design_tokens_css = load_design_tokens(active_style_mode)

    # Brand strategy overrides brief branding defaults
    primary_color = (
        brand_strategy.get("primary_color")
        or brief.get("branding", {}).get("primary_color", "#2F7F79")
    )
    secondary_color = brief.get("branding", {}).get("secondary_color", "#A7D7C5")

    # Image priority: client-provided images > brief.json branding > empty
    logo = (
        client_images.get("header_logo")
        or brief.get("branding", {}).get("logo", "")
        or ""
    )
    # Footer logo: compact icon version (e.g. Logo.png) — fallback to header logo
    logo_footer = (
        client_images.get("footer_logo")
        or brief.get("branding", {}).get("logo_footer", "")
        or logo
    )
    whatsapp = brief.get("whatsapp", "")
    phone = brief.get("contact_info", {}).get("phone", "")
    email = brief.get("contact_info", {}).get("email", "")
    address = brief.get("contact_info", {}).get("address", "")
    business_name = brief.get("business_name", "")

    # EmailJS config — optional, read from config.json
    emailjs_cfg = config.get("emailjs", {})
    emailjs_public_key = emailjs_cfg.get("public_key", "")
    emailjs_service_id = emailjs_cfg.get("service_id", "")
    emailjs_template_id = emailjs_cfg.get("template_id", "")
    has_emailjs = bool(emailjs_public_key and emailjs_service_id and emailjs_template_id
                       and not emailjs_public_key.startswith("YOUR_"))
    if has_emailjs:
        print(f"  ✓ EmailJS configured: service={emailjs_service_id} | template={emailjs_template_id}")
    else:
        print(f"  ℹ  EmailJS not configured — add emailjs keys to config.json to enable email on form submit")
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

    # Build verified facts block — injected into all 3 parts as single source of truth
    facts_section = (
        f"\nVERIFIED CLIENT FACTS (highest priority — use verbatim, never contradict):\n"
        f"{'='*60}\n{client_facts}\n{'='*60}\n"
        if client_facts else ""
    )

    shared_context = (
        f"Business: {business_name}\n"
        f"Primary color: {primary_color} | Secondary: {secondary_color}\n"
        f"Logo: {logo}\n"
        f"WhatsApp: {whatsapp} | Phone: {phone} | Email: {email} | Address: {address}\n"
        f"Meta title: {seo.get('meta_title', '')}\n"
        f"Meta description: {seo.get('meta_description', '')}\n"
        f"Language: {brief.get('language', 'es')} — ALL text must be in {'Spanish' if brief.get('language','es')=='es' else 'English'}\n"
        f"Has process_steps: {'YES' if process_steps else 'NO'} | Has comparison: {'YES' if comparison else 'NO'} | Has pricing: {'YES' if pricing else 'NO'}\n"
        f"{facts_section}"
    )

    # Load curated images from core/images.json (normalized — hero and services are plain URL strings)
    # Selection priority: style_mode key → template key → "healthcare" fallback
    # This ensures luxury-dark gets tech images, warm-local gets artisanal, etc.
    images_lib = load_images_library()
    template_key = config.get("template", "healthcare")
    img_set = (
        images_lib.get(active_style_mode)          # 1st: exact style_mode match (e.g. "luxury-dark")
        or images_lib.get(template_key)             # 2nd: template key (e.g. "healthcare")
        or images_lib.get("healthcare", {})         # 3rd: safe fallback
    )
    if images_lib.get(active_style_mode):
        print(f"  ✓ Image library: style_mode='{active_style_mode}' key matched — mood-specific images loaded")
    else:
        print(f"  ✓ Image library: template='{template_key}' key used (no style_mode override in images.json)")
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
    print(f"  ✓ Service images: {len(client_service_imgs)} client | {sum(1 for s in services if s.get('image_url'))} brief.json | {len(service_imgs)} curated")

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
    # Priority: 1) image_url from brief.json (explicit per-service assignment)
    #           2) client-provided images by position (assets/images/services/)
    #           3) curated images.json library by position
    #           4) hero image as last fallback
    client_service_imgs = client_images.get("services", [])
    for i, svc in enumerate(services):
        if svc.get("image_url"):
            raw_url = svc["image_url"]
        elif i < len(client_service_imgs):
            raw_url = client_service_imgs[i]
        elif service_imgs:
            raw_url = service_imgs[i % len(service_imgs)]
        else:
            raw_url = hero_img
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
    page_personality = brand_strategy.get("page_personality", "storytelling")
    section_order = brand_strategy.get("section_order", [])

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
        "page_personality": page_personality,
        "section_order": section_order,
        "sections": [s.get("type", "") for s in layout_data.get("sections", [])]
    }, indent=2)
    print(f"  ✓ Layout: style={layout_style} | intensity={visual_intensity} | hero={hero_variant}")
    print(f"  ✓ Brand: layout={layout_variation} | spacing={spacing_scale} | image={image_direction}")
    print(f"  ✓ Page personality: {page_personality} | sections: {len(section_order) if section_order else 'default'}")
    if visual_break:
        print(f"  ✓ Visual break: {visual_break.get('type','?')} @ {visual_break.get('position','?')}")

    # ── PAGE PERSONALITY: derive section flow ────────────────────────────────
    flow = build_section_flow(
        page_personality=page_personality,
        section_order=section_order,
        has_process=bool(process_steps),
        has_comparison=bool(comparison),
        has_pricing=bool(pricing),
    )
    skip_faq = flow["skip_faq"]
    part2_sections = flow["part2_sections"]
    part3_sections = flow["part3_sections"]
    print(f"  ✓ Section flow — part2: {part2_sections}")
    print(f"  ✓ Section flow — part3: {part3_sections} | skip_faq={skip_faq}")

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

    # ── FASE 2: Mode-aware header + CSS token injection ───────────────────────
    header_instruction = build_header_instruction(active_style_mode, resolve_image_path(logo), phone, primary_color)

    # CSS root block: design tokens from design-language.json override LLM defaults
    # Then patch primary/accent color with DNA-enforced values (regex replace — cascade-safe)
    if design_tokens_css:
        import re as _re
        css_root_block = design_tokens_css
        # Replace the first --color-primary value with the DNA-enforced one
        if primary_color:
            css_root_block = _re.sub(
                r'--color-primary:\s*[^;]+;',
                f'--color-primary: {primary_color};',
                css_root_block, count=1
            )
        # Replace accent color if brand_strategy provides one
        accent_color = brand_strategy.get("accent_color", "")
        if accent_color:
            css_root_block = _re.sub(
                r'--color-accent:\s*[^;]+;',
                f'--color-accent: {accent_color};',
                css_root_block, count=1
            )
        css_root_note = f"mode={active_style_mode} — tokens from design-language.json (primary={primary_color})"
    else:
        css_root_block = f":root {{ --color-primary: {primary_color}; --color-secondary: {secondary_color}; }}"
        css_root_note = "fallback — design-language.json missing"

    # ── PART 1: DOCTYPE + HEAD + CSS + HEADER + HERO ─────────────────────────
    print("\n  → Part 1: Head + Header + Hero...")
    part1_msg = (
        f"Generate ONLY Part 1 of a premium index.html. Be concise — no inline comments.\n\n"
        f"{GROUNDING_RULE}\n"
        f"CONTEXT: {shared_context}\n"
        f"ACTIVE STYLE MODE: {active_style_mode}\n"
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
        f"   - Google Fonts: use the font pair for style_mode='{active_style_mode}' from your TYPOGRAPHY SYSTEM BY MODE section.\n"
        f"     Inject the EXACT Google Fonts <link> tags for this mode BEFORE Tailwind CDN.\n"
        f"   - <style> block:\n"
        f"     STEP 1 — Copy this :root block VERBATIM as the FIRST CSS rule ({css_root_note}):\n"
        f"     {css_root_block}\n"
        f"     STEP 2 — Add these utility classes AFTER the :root block:\n"
        f"     * body {{ font-family: 'Inter', sans-serif; background: var(--color-bg, #fff); color: var(--color-text, #111); }}\n"
        f"     * .reveal, .reveal-element {{ opacity:0; transform:translateY(20px); transition:opacity 0.7s ease, transform 0.7s ease; }}\n"
        f"     * .reveal.visible, .reveal-element.visible {{ opacity:1; transform:none; }}\n"
        f"     * .btn-primary {{ background:var(--color-primary); color:#fff; font-weight:700; border-radius:var(--radius-button,0.5rem); box-shadow:var(--shadow-button,none); position:relative; overflow:hidden; display:inline-flex; align-items:center; justify-content:center; text-decoration:none; transition:transform 0.2s ease,box-shadow 0.2s ease; }}\n"
        f"     * .btn-primary::after {{ content:''; position:absolute; top:0; left:-100%; width:60%; height:100%; background:linear-gradient(90deg,transparent,rgba(255,255,255,0.22),transparent); transition:left 0.5s ease; pointer-events:none; }}\n"
        f"     * .btn-primary:hover::after {{ left:150%; }}\n"
        f"     * .btn-primary:hover {{ transform:translateY(-2px); }}\n"
        f"     * .btn-outline {{ background:transparent; color:var(--color-primary); border:2px solid var(--color-primary); border-radius:var(--radius-button,0.5rem); font-weight:600; display:inline-flex; align-items:center; text-decoration:none; transition:all 0.2s; }}\n"
        f"     * .btn-outline:hover {{ background:var(--color-primary); color:#fff; }}\n"
        f"     * .icon-circle {{ transition:background 0.25s ease; }}\n"
        f"     * .group:hover .icon-circle {{ background:var(--color-primary) !important; }}\n"
        f"     * .group:hover .icon-circle svg {{ color:white; stroke:white; }}\n"
        f"     * .faq-answer {{ max-height:0; overflow:hidden; transition:max-height 0.45s cubic-bezier(0.22,1,0.36,1); }}\n"
        f"     * .faq-answer.open {{ max-height:400px; }}\n"
        f"     * @keyframes whatsapp-pulse {{ 0%,100% {{ box-shadow:0 0 0 0 rgba(37,211,102,0.55); }} 70% {{ box-shadow:0 0 0 14px rgba(37,211,102,0); }} }}\n"
        f"     * .whatsapp-pulse {{ animation:whatsapp-pulse 2.2s infinite; }}\n"
        f"     * @media (max-width:767px) {{ body {{ padding-bottom:68px; }} }}\n"
        f"     * @media (min-width:768px) {{ body {{ padding-bottom:0 !important; }} }}\n"
        f"     * ::-webkit-scrollbar {{ width:5px; }} ::-webkit-scrollbar-thumb {{ background:var(--color-primary); border-radius:3px; }}\n"
        f"   - SVG favicon: data URL using brand initial '{business_name[0].upper() if business_name else 'W'}' and primary color\n"
        f"   - Schema.org block — insert EXACTLY as-is:\n"
        f"     {schema_block}\n"
        f"   - Analytics — insert EXACTLY as-is:\n"
        f"     {analytics_snippet if analytics_snippet else '<!-- analytics disabled -->'}\n"
        + (
            f"   - EmailJS library — insert EXACTLY as-is (required for contact form email):\n"
            f"     <script src='https://cdn.jsdelivr.net/npm/emailjs-com@3/dist/email.min.js'></script>\n"
            if has_emailjs else ""
        )
        + f"2. <body> opens\n"
        f"{header_instruction}"
        f"4. Mobile nav dropdown (#mobile-menu hidden by default, same bg as header)\n"
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

    # Portfolio guard — prevent hallucination if no portfolio data in brief
    has_portfolio = bool(brief.get("portfolio", []))
    portfolio_guard = (
        "\nPORTFOLIO: You have portfolio data — include it.\n"
        if has_portfolio else
        "\nPORTFOLIO GUARD: There is NO portfolio data in this brief. DO NOT generate any portfolio section, case study section, or work gallery. Skip it entirely.\n"
    )

    # ── Build Part 2 section list dynamically from page_personality ─────────
    p2_items = []
    p2_n = 1
    # Services is always first in Part 2
    p2_items.append(
        f"{p2_n}. SERVICES section — use EXACT layout pattern:\n"
        f"   {services_layout_instruction}\n"
        f"{vb_part2_instruction}"
    )
    p2_n += 1
    if "cta-banner" in part2_sections:
        p2_items.append(
            f"{p2_n}. Inline CTA banner: gradient bg (primary to secondary), headline, subheadline, button → href='#contact'\n"
        )
        p2_n += 1
    if "benefits" in part2_sections:
        p2_items.append(
            f"{p2_n}. <section id='benefits' class='py-14 md:py-20 bg-white'>:\n"
            f"   Section title + subtitle, then benefit items using layout from brand_strategy.section_layout_overrides.benefits\n"
            f"   Default: icon-list (icon in colored circle, bold title, description) in grid md:grid-cols-3\n"
            f"   Each card MUST have class='group' for hover effects to work\n"
        )
        p2_n += 1
    if "stats-bar" in part2_sections or "trust-band" in part2_sections:
        p2_items.append(
            f"{p2_n}. <section id='trust' class='py-14 bg-gray-50'>:\n"
            f"   4 trust stats: large numbers (text-5xl+) in primary color, label text, stagger animation\n"
            f"   Use data from trust[] array — EXACT values, no inflation\n"
        )
        p2_n += 1
    if "how-it-works" in part2_sections and process_steps:
        p2_items.append(
            f"{p2_n}. <section id='how-it-works' class='py-14 md:py-20 bg-white'>:\n"
            f"   How It Works — 3 numbered steps horizontal layout\n"
            f"   Each step: large number badge, title, description. Use PROCESS STEPS data.\n"
        )
        p2_n += 1
    if "badge-grid" in part2_sections:
        p2_items.append(
            f"{p2_n}. Badge grid: 4 authority badges with icons (Background Checked, Licensed & Insured, Free Consultation, 24/7 Support)\n"
        )
        p2_n += 1
    if "comparison" in part2_sections and comparison:
        p2_items.append(
            f"{p2_n}. <section id='comparison' class='py-14 md:py-20'>:\n"
            f"   Side-by-side comparison table — use comparison data: {comparison_json}\n"
            f"   2-column: left=brand (brand color header, checkmarks), right=competitors (gray, X marks)\n"
            f"   KEY DIFFERENTIATOR — make visually impactful\n"
        )
        p2_n += 1
    p2_items.append(f"\nEnd with comment <!-- END PART 2 --> — DO NOT close body or html.")

    part2_msg = (
        f"Generate ONLY Part 2 of an index.html. Start immediately after <!-- END PART 1 -->.\n"
        f"NO DOCTYPE, NO html tag, NO head tag. Start directly with a <section> tag.\n\n"
        f"TOKEN DISCIPLINE (ABSOLUTE RULE): If you are running low on output space:\n"
        f"  1. STOP adding new content immediately\n"
        f"  2. Close ALL currently open tags: </p></div></div></section>\n"
        f"  3. Then write <!-- END PART 2 --> and stop\n"
        f"  NEVER cut a section mid-content — an unclosed <section> destroys the layout.\n"
        f"  A missing section is better than a broken one.\n\n"
        f"PAGE PERSONALITY: {page_personality} — include ONLY the sections listed below.\n"
        f"  Skip any section not in this list — do NOT add sections just because they exist in the template.\n\n"
        f"{GROUNDING_RULE}\n"
        f"{portfolio_guard}\n"
        f"CONTEXT: {shared_context}\n"
        f"LAYOUT DECISIONS (brand_strategy takes priority):\n{layout_json_summary}\n\n"
        f"IMAGE RULES (ABSOLUTE — NEVER VIOLATE):\n"
        f"- COPY the exact <img> tags provided below — NEVER change src URLs\n"
        f"- NEVER use source.unsplash.com (deprecated and broken)\n"
        f"- Image direction: '{image_direction}' — if 'illustration-icon' or 'minimal-no-image', use SVG icons instead of photos\n"
        f"- ALL images MUST have {img_onerror} as fallback\n"
        f"- ALL images MUST have loading='lazy' (except hero in Part 1)\n\n"
        f"{service_cards_instruction}\n"
        f"SERVICES DATA (text content only — use img tags above for images):\n{services_json}\n"
        f"BENEFITS: {benefits_json}\n"
        f"TRUST STATS (use EXACT values — do NOT change numbers): {trust_json}\n"
        f"PROCESS STEPS (How It Works): {process_steps_json}\n\n"
        f"{forbidden_instruction}"
        f"ANIMATION RULES:\n"
        f"- Do NOT use Tailwind 'opacity-0' or 'translate-y-10' inline classes\n"
        f"- Use class='reveal-element' for scroll-reveal animations\n"
        f"- Every <section> MUST have both opening AND closing tags\n\n"
        f"OUTPUT (generate ONLY these sections in this order):\n"
        + "\n".join(p2_items)
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
        f"TOKEN DISCIPLINE (ABSOLUTE RULE): If you are running low on output space:\n"
        f"  1. STOP the current section immediately — close all open tags\n"
        f"  2. Skip any remaining optional sections\n"
        f"  3. These sections are NON-NEGOTIABLE and MUST always be generated (even if short):\n"
        f"     → #contact (form + contact info)\n"
        f"     → <footer>\n"
        f"     → WhatsApp floating button (#wa-btn)\n"
        f"     → Mobile sticky CTA bar\n"
        f"     → ONE <script> block with ALL JavaScript\n"
        f"     → </body></html>\n"
        f"  NEVER end this part without contact, footer, and the script block.\n\n"
        f"{GROUNDING_RULE}\n"
        f"{portfolio_guard}\n"
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

    # Language-aware strings — defined here so they're available for both
    # part3_output_items and part3_tail (previously defined too late → NameError)
    _is_es   = brief.get("language", "es") == "es"
    _sending = "Enviando…" if _is_es else "Sending…"
    _sent    = "✓ ¡Enviado!" if _is_es else "✓ Sent!"
    _hello   = "¡Hola" if _is_es else "Hello"
    _phone_l = "Teléfono" if _is_es else "Phone"
    _wa_fallback = (
        f"`{_hello} {business_name}! Me interesa sus servicios.`"
        if _is_es else
        f"`{_hello} {business_name}! I'd like to learn more about your services.`"
    )
    _success_text = "✓ ¡Mensaje enviado! Te contactamos en breve." if _is_es else "✓ Message sent! We'll contact you shortly."

    # Build numbered output list for Part 3 dynamically from section_order
    n = 1
    part3_output_items = [f"OUTPUT (generate ONLY these sections in this order — NEVER truncate):"]
    if "testimonials" in part3_sections:
        part3_output_items.append(
            f"{n}. <section id='testimonials' class='{testimonials_bg}'>:\n"
            f"   Style: {testimonials_style}"
        )
        part3_output_items.append(vb_part3_instruction)
        n += 1
    if "wow-section" in part3_sections:
        part3_output_items.append(
            f"{n}. <section id='wow-section'> — Full-bleed emotional quote section:\n"
            f"   Large decorative quotation mark SVG, dark overlay image, single emotional quote, brand CTA"
        )
        n += 1
    if "pricing" in part3_sections and pricing:
        part3_output_items.append(
            f"{n}. <section id='pricing' class='py-14 md:py-20 bg-gray-50'>:\n"
            f"   3-column pricing grid — use PRICING PLANS data\n"
            f"   Highlighted plan gets border-2 border-[--color-primary] + scale emphasis\n"
            f"   Each plan: name, price (large), description, checkmark feature list, CTA button"
        )
        n += 1
    if not skip_faq and "faq" in part3_sections:
        part3_output_items.append(
            f"{n}. <section id='faq' class='py-14 bg-white'>:\n"
            f"   FAQ accordion — each .faq-item has button (toggle .open class) and .faq-answer div\n"
            f"   Use data from FAQ array"
        )
        n += 1
    elif skip_faq:
        part3_output_items.append(f"   ⚠ PAGE PERSONALITY '{page_personality}': skip FAQ — not in section_order")
    if "cta" in part3_sections:
        part3_output_items.append(
            f"{n}. Final CTA section: dark gradient bg, bold headline, subheadline, single primary CTA button"
        )
        n += 1

    part3_tail = (
        f"{n}. <section id='contact' class='py-20 bg-gray-50'>:\n"
        f"   Split layout: left=contact form, right=contact info card (phone:{phone}, email:{email}, address:{address}, hours:24/7)\n"
        f"   Form MUST have:\n"
        f"     - id='contact-form'\n"
        f"     - Name field:    <input type='text' name='from_name' required ...>\n"
        f"     - Phone field:   <input type='tel' name='phone' ...>\n"
        f"     - Message field: <textarea name='message' ...></textarea>\n"
        f"     - Submit button id='form-submit-btn'\n"
        f"     - Success message (hidden by default): <p id='form-success' class='hidden text-sm font-semibold text-center py-2' style='color:{{primary_color}};'>{_success_text}</p>\n"
    )
    n += 1
    part3_tail += (
        f"{n}. <footer>: dark gradient bg, logo img src='{resolve_image_path(logo_footer)}' class='h-12 w-auto brightness-0 invert', "
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
    # (_is_es, _sending, _sent, _hello, _phone_l, _wa_fallback already defined above)

    # Build the form submit JS block based on whether EmailJS is configured
    if has_emailjs:
        _form_submit_js = (
            f"   e) Contact form — EmailJS + WhatsApp (COPY VERBATIM — do not modify):\n"
            f"      emailjs.init('{emailjs_public_key}');\n"
            f"      const form = document.getElementById('contact-form');\n"
            f"      if (form) {{\n"
            f"        form.addEventListener('submit', function(e) {{\n"
            f"          e.preventDefault();\n"
            f"          const btn = document.getElementById('form-submit-btn');\n"
            f"          const successMsg = document.getElementById('form-success');\n"
            f"          const origText = btn.textContent;\n"
            f"          btn.disabled = true; btn.textContent = '{_sending}';\n"
            f"          btn.classList.add('opacity-75','cursor-not-allowed');\n"
            f"          emailjs.sendForm('{emailjs_service_id}', '{emailjs_template_id}', form)\n"
            f"            .then(function() {{\n"
            f"              if (successMsg) successMsg.classList.remove('hidden');\n"
            f"              btn.textContent = '{_sent}';\n"
            f"              setTimeout(function() {{\n"
            f"                const name    = form.querySelector('[name=\"from_name\"]')?.value || '';\n"
            f"                const phone   = form.querySelector('[name=\"phone\"]')?.value     || '';\n"
            f"                const message = form.querySelector('[name=\"message\"]')?.value   || '';\n"
            f"                const waText  = encodeURIComponent(\n"
            f"                  `{_hello} {business_name}! ${{name ? ('{('Soy' if _is_es else 'I am')} ' + name + '.') : ''}}` +\n"
            f"                  (phone   ? `\\n{_phone_l}: ${{phone}}.` : '') +\n"
            f"                  (message ? `\\n\\n${{message}}` : '')\n"
            f"                );\n"
            f"                window.open(`https://wa.me/{whatsapp}?text=${{waText}}`, '_blank');\n"
            f"                form.reset();\n"
            f"                btn.disabled = false; btn.textContent = origText;\n"
            f"                btn.classList.remove('opacity-75','cursor-not-allowed');\n"
            f"                if (successMsg) successMsg.classList.add('hidden');\n"
            f"              }}, 1500);\n"
            f"            }})\n"
            f"            .catch(function(err) {{\n"
            f"              console.error('EmailJS error:', err);\n"
            f"              btn.disabled = false; btn.textContent = origText;\n"
            f"              btn.classList.remove('opacity-75','cursor-not-allowed');\n"
            f"              const name = form.querySelector('[name=\"from_name\"]')?.value || '';\n"
            f"              window.open(`https://wa.me/{whatsapp}?text=${{encodeURIComponent({_wa_fallback})}}`, '_blank');\n"
            f"            }});\n"
            f"        }});\n"
            f"      }}\n"
        )
    else:
        _form_submit_js = (
            f"   e) Contact form — WhatsApp only (no EmailJS configured):\n"
            f"      const form = document.getElementById('contact-form');\n"
            f"      if (form) {{\n"
            f"        form.addEventListener('submit', function(e) {{\n"
            f"          e.preventDefault();\n"
            f"          const name    = form.querySelector('[name=\"from_name\"]')?.value || '';\n"
            f"          const phone   = form.querySelector('[name=\"phone\"]')?.value     || '';\n"
            f"          const message = form.querySelector('[name=\"message\"]')?.value   || '';\n"
            f"          const waText  = encodeURIComponent(\n"
            f"            `{_hello} {business_name}! ${{name ? ('{('Soy' if _is_es else 'I am')} ' + name + '.') : ''}}` +\n"
            f"            (phone   ? `\\n{_phone_l}: ${{phone}}.` : '') +\n"
            f"            (message ? `\\n\\n${{message}}` : '')\n"
            f"          );\n"
            f"          window.open(`https://wa.me/{whatsapp}?text=${{waText}}`, '_blank');\n"
            f"        }});\n"
            f"      }}\n"
        )

    part3_tail += (
        f"{n}. ONE <script> block containing ALL JavaScript:\n"
        f"   a) IntersectionObserver: observe '.reveal-element, .reveal', add 'visible' class at threshold 0.1, "
        f"also immediately activate elements already in viewport on window load\n"
        f"   b) FAQ accordion: querySelectorAll('.faq-item button'), toggle 'open' on parent .faq-item\n"
        f"   c) Mobile menu toggle: hamburger button toggles #mobile-menu visibility\n"
        f"   d) Sticky header: add shadow class on scroll > 50px\n"
        + _form_submit_js
        + f"   f) Analytics tracking (insert verbatim):{tracking_js if tracking_js else ' // analytics disabled'}\n"
    )
    n += 1
    part3_tail += f"{n}. Close with </body></html>"
    part3_msg = part3_msg + "\n".join(part3_output_items) + "\n" + part3_tail
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
    client_facts = load_client_facts(client_id)
    client_images = load_client_images(client_id)
    template_name = config["template"]
    prompts = load_prompts(template_name)
    brief_str = json.dumps(brief, indent=2)
    dna_str = json.dumps(client_dna, indent=2) if client_dna else "{}"

    # Extract reference inspiration from DNA — used to ground brand-strategist decisions
    ref_inspiration = client_dna.get("reference_inspiration", {}) if client_dna else {}
    ref_url = ref_inspiration.get("url", "")
    ref_screenshots: list[bytes] = []
    if ref_url:
        ref_screenshots = load_reference_screenshots(ref_url, client_id)

    # Build a formatted design reference block — injected prominently into brand-strategist
    if ref_inspiration:
        _what_take = ref_inspiration.get("what_to_take", "")
        _what_improve = ref_inspiration.get("what_to_improve", "")
        _avoid = ref_inspiration.get("avoid", "")
        reference_design_block = (
            f"\n{'='*60}\n"
            f"DESIGN REFERENCE (MANDATORY — translate every point into JSON decisions):\n"
            f"  URL: {ref_url}\n"
            f"  TAKE (replicate these structural patterns):\n    {_what_take}\n"
            f"  IMPROVE (go further than the reference here):\n    {_what_improve}\n"
            f"  AVOID (do NOT copy these literally):\n    {_avoid}\n"
            + (f"  ⚠ {len(ref_screenshots)} screenshots of the full reference site are attached in order\n"
               f"    (top → bottom). Analyze every section: hero, services, metrics, testimonials,\n"
               f"    footer. Extract layout grid, spacing rhythm, color palette, and typography scale.\n"
               if ref_screenshots else "")
            + f"{'='*60}\n"
        )
        print(f"  ✓ Reference inspiration loaded: {ref_url} | {len(ref_screenshots)} sections captured")
    else:
        reference_design_block = ""

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
    if client_facts: active_systems.append("client-facts")
    if client_images.get("header_logo") or client_images.get("services"): active_systems.append("client-images")
    if ref_url: active_systems.append(f"reference-site({len(ref_screenshots)} sections)" if ref_screenshots else "reference-site(text-only)")
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
        brand_msg = (
            f"Define brand strategy and design decisions for this client. Return ONLY valid JSON.\n\n"
            f"BUSINESS ANALYSIS:\n{json.dumps(analysis, indent=2)}\n\n"
            f"CLIENT BRIEF:\n{brief_str}\n\n"
            f"CLIENT DNA:\n{dna_str}\n\n"
            + reference_design_block
            + f"Return JSON with: style_mode, design_concept, hero_variant, layout_variation, "
            f"visual_intensity, spacing_scale, image_direction, primary_color, accent_color, "
            f"visual_break, section_layout_overrides, forbidden_patterns, layout_notes, reference_applied"
        )
        brand_raw, _ = call_claude(
            client,
            system_prompt=prompts["brand_strategist"],
            user_message=brand_msg,
            step_name="Brand Strategist",
            image_bytes_list=ref_screenshots if ref_screenshots else None,
        )
        brand_json_str = extract_json(brand_raw)
        try:
            brand_strategy = json.loads(brand_json_str)

            # ── FASE 1: DNA enforcement — MUST run before anything else ─────
            brand_strategy = enforce_dna_style_mode(brand_strategy, client_dna)

            # Layout uniqueness check
            warnings = check_layout_uniqueness(brand_strategy, analysis.get("business_type", ""))
            for w in warnings:
                print(f"  ⚠  UNIQUENESS WARNING: {w}")
            print(f"  ✓ Brand: {brand_strategy.get('style_mode')} | "
                  f"layout={brand_strategy.get('layout_variation')} | "
                  f"hero={brand_strategy.get('hero_variant')} | "
                  f"color={brand_strategy.get('primary_color')}")
            if brand_strategy.get("reference_applied"):
                print(f"  ✓ Reference applied: {brand_strategy['reference_applied'][:100]}")
        except json.JSONDecodeError:
            print("  WARNING: Brand strategist returned invalid JSON — continuing without brand strategy")
            brand_strategy = {}
    else:
        print("\n  ℹ  brand-strategist.md not found — skipping brand strategy step")

    # STEP 2 — Copywriting
    print("\n[3/7] Copy Generation")
    facts_block = (
        f"\nVERIFIED CLIENT FACTS (use these verbatim — highest priority source):\n"
        f"{'='*60}\n{client_facts}\n{'='*60}\n"
        if client_facts else ""
    )
    copy_raw, _ = call_claude(
        client,
        system_prompt=prompts["copywriter"],
        user_message=(
            f"Generate the website copy using this data:\n\n"
            f"BUSINESS ANALYSIS:\n{json.dumps(analysis, indent=2)}\n\n"
            f"INDUSTRY TEMPLATE:\n{prompts['template']}\n\n"
            f"CLIENT BRIEF:\n{brief_str}\n\n"
            f"{facts_block}"
            f"OUTPUT CONTRACT:\n{prompts['output_contract']}\n\n"
            f"GROUNDING RULE: Use ONLY data from CLIENT BRIEF and VERIFIED CLIENT FACTS above. "
            f"Never invent statistics, testimonials, certifications, client names, or results not present in these sources.\n\n"
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
        client, prompts["frontend_dev"], brief, config, seo_data, layout_data, brand_strategy,
        client_facts=client_facts, client_images=client_images
    )

    # ── FASE 1: Real HTML validation (structural checks) ─────────────────────
    print("\n  → Running structural validation...")
    html_findings = validate_html(html_content, brand_strategy, brief)
    critical_count = 0
    for finding in html_findings:
        prefix = "  🔴" if finding.startswith("CRITICAL") else "  🟠" if finding.startswith("FAIL") else "  🟡" if finding.startswith("WARN") else "  🟢"
        print(f"{prefix} {finding}")
        if finding.startswith("CRITICAL") or finding.startswith("FAIL"):
            critical_count += 1
    if not html_findings:
        print("  🟢 All structural checks passed")
    elif critical_count > 0:
        print(f"  ⚠  {critical_count} critical/fail findings — review output before deploying")
    else:
        print(f"  ✓ {len(html_findings)} warnings (no critical failures)")

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
