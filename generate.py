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

# Verified curated images per industry — never use source.unsplash.com (deprecated)
# All IDs confirmed as elderly/healthcare appropriate
CURATED_IMAGES = {
    "healthcare": {
        "hero": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=900&h=700&fit=crop&crop=faces&auto=format&q=85",
        "services": [
            "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=800&h=500&fit=crop&crop=faces&auto=format&q=80",
            "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=800&h=500&fit=crop&crop=top&auto=format&q=80",
            "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=800&h=500&fit=crop&crop=bottom&auto=format&q=80",
            "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=800&h=500&fit=crop&crop=right&auto=format&q=80",
            "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=800&h=500&fit=crop&crop=left&auto=format&q=80",
            "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=800&h=500&fit=crop&crop=entropy&auto=format&q=80",
        ]
    },
    "restaurant": {
        "hero": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=900&h=700&fit=crop&auto=format&q=85",
        "services": []
    },
    "ecommerce": {
        "hero": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=900&h=700&fit=crop&auto=format&q=85",
        "services": []
    }
}


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


def load_prompts(template_name: str) -> dict:
    return {
        "business_analyzer": read_file(AGENTS_DIR / "business-analyzer.md"),
        "copywriter": read_file(AGENTS_DIR / "copywriter.md"),
        "seo_optimizer": read_file(AGENTS_DIR / "seo-optimizer.md"),
        "ui_designer": read_file(AGENTS_DIR / "ui-designer.md"),
        "frontend_dev": read_file(AGENTS_DIR / "frontend-dev.md"),
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


def generate_frontend(client: anthropic.Anthropic, system_prompt: str, brief: dict, config: dict, seo_data: dict, layout_data: dict) -> str:
    """Generate frontend HTML in two focused parts to avoid token limits."""

    primary_color = brief.get("branding", {}).get("primary_color", "#2F7F79")
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

    shared_context = (
        f"Business: {business_name}\n"
        f"Primary color: {primary_color} | Secondary: {secondary_color}\n"
        f"Logo: {logo}\n"
        f"WhatsApp: {whatsapp} | Phone: {phone} | Email: {email} | Address: {address}\n"
        f"Meta title: {seo.get('meta_title', '')}\n"
        f"Meta description: {seo.get('meta_description', '')}\n"
    )

    # Load curated images for this template
    template_key = config.get("template", "healthcare")
    img_set = CURATED_IMAGES.get(template_key, CURATED_IMAGES["healthcare"])
    hero_img = img_set["hero"]
    service_imgs = img_set["services"]
    # Inject image URLs into each service
    for i, svc in enumerate(services):
        svc["_image_url"] = service_imgs[i % len(service_imgs)] if service_imgs else hero_img

    services_json = json.dumps(services, indent=2)
    benefits_json = json.dumps(benefits, indent=2)
    trust_json = json.dumps(trust, indent=2)
    testimonials_json = json.dumps(testimonials, indent=2)
    faq_json = json.dumps(faq, indent=2)
    cta_json = json.dumps(cta, indent=2)
    hero_json = json.dumps(hero, indent=2)

    # ── PART 1: DOCTYPE + HEAD + CSS + HEADER + HERO ─────────────────────────
    print("\n  → Part 1: Head + Header + Hero...")
    part1_msg = (
        f"Generate ONLY Part 1 of a premium index.html. Be concise — no inline comments.\n\n"
        f"CONTEXT: {shared_context}\n"
        f"HERO: {hero_json}\n\n"
        f"OUTPUT:\n"
        f"1. <!DOCTYPE html> + <head>: charset, viewport, title='{seo.get('meta_title','')}', "
        f"meta description, Tailwind CDN, Google Fonts Inter, "
        f"<style> block with: scroll animations (.reveal {{ opacity:0; transform:translateY(24px); transition:0.7s }}), "
        f".reveal.visible and .reveal-element.visible {{opacity:1;transform:none}}, "
        f"FAQ accordion (.faq-answer {{max-height:0;overflow:hidden;transition:0.4s}}), "
        f".faq-item.open .faq-answer {{max-height:500px}}, "
        f"WhatsApp pulse @keyframes, mobile CTA bar, sticky header, custom scrollbar, "
        f"brand CSS vars (--color-primary:{primary_color}; --color-secondary:{secondary_color})\n"
        f"2. <body> opens (NO padding-bottom on body — mobile CTA handles its own spacing)\n"
        f"3. Sticky <header>: logo img src='{logo}' h-10, brand name text next to logo, "
        f"nav links (Services href='#services' / Why Us href='#benefits' / Testimonials href='#testimonials' / FAQ href='#faq' / Contact href='#contact'), "
        f"phone tel:{phone}, 'Free Consultation' CTA button, mobile hamburger\n"
        f"4. Mobile nav dropdown (hidden by default)\n"
        f"5. Hero <section id='hero'>: split grid (text 60%/image 40%), trust badge pill, H1 headline, "
        f"subheadline, 2 CTA buttons, 3 trust microcopy items, floating badge on image\n"
        f"   Hero image: src='{hero_img}' — MUST use this exact URL\n"
        f"6. End with comment <!-- END PART 1 --> — DO NOT close body or html."
    )
    part1_raw, _ = call_claude(client, system_prompt, part1_msg, "Frontend Part 1 (Head+Hero)", max_tokens=8000)
    part1_html = extract_html(part1_raw)

    # ── PART 2: SERVICES + CTA1 + BENEFITS + TRUST ───────────────────────────
    print("\n  → Part 2: Services + Benefits + Trust...")

    # Build service cards with pre-assigned image URLs
    service_cards_instruction = ""
    for i, svc in enumerate(services):
        img_url = svc.get("_image_url", hero_img)
        service_cards_instruction += f"  Card {i+1}: title='{svc.get('title','')}', image src='{img_url}' (USE THIS EXACT URL)\n"

    part2_msg = (
        f"Generate ONLY Part 2 of an index.html. Start immediately after <!-- END PART 1 -->.\n"
        f"NO DOCTYPE, NO html tag, NO head tag. Start directly with a <section> tag.\n\n"
        f"CONTEXT: {shared_context}\n"
        f"SERVICES ({len(services)} cards — use EXACT image URLs below):\n"
        f"{service_cards_instruction}\n"
        f"FULL SERVICES DATA: {services_json}\n"
        f"BENEFITS: {benefits_json}\n"
        f"TRUST: {trust_json}\n\n"
        f"CRITICAL RULES:\n"
        f"- Use ONLY the image URLs listed above for each service card. DO NOT use source.unsplash.com\n"
        f"- Do NOT use Tailwind 'opacity-0' or 'translate-y-10' inline classes — use class='reveal-element' instead\n"
        f"- Every <section> MUST have opening AND closing tags\n\n"
        f"OUTPUT (complete all items before ending):\n"
        f"1. <section id='services' class='py-20 md:py-28 bg-gray-50'>: 3-column card grid, "
        f"each card has the specified image, title, description, 2-3 bullet benefits, hover shadow\n"
        f"2. CTA banner: gradient, headline, subheadline, button → href='#contact'\n"
        f"3. <section id='benefits' class='py-20 md:py-28 bg-white'>: MUST be fully generated — "
        f"6 benefit cards (icon + title + description), 3-column grid\n"
        f"4. <section id='trust' class='py-16 bg-gray-50'>: 4 stat cards (500+ Families, 10+ Years, 24/7 Available, 4.9 Rating)\n"
        f"5. End with comment <!-- END PART 2 --> — DO NOT close body or html."
    )
    part2_raw, _ = call_claude(client, system_prompt, part2_msg, "Frontend Part 2 (Services+Benefits)", max_tokens=8000)
    part2_html = extract_html(part2_raw)

    # ── PART 3: TESTIMONIALS + FAQ + CTA + CONTACT + FOOTER + SCRIPTS ────────
    print("\n  → Part 3: Testimonials + FAQ + Contact + Footer + JS...")
    part3_msg = (
        f"Generate ONLY Part 3 (final part) of an index.html. Start immediately after <!-- END PART 2 -->.\n"
        f"NO DOCTYPE, NO html, NO head. Start with a <section> tag. MUST end with </body></html>.\n\n"
        f"CONTEXT: {shared_context}\n"
        f"TESTIMONIALS: {testimonials_json}\n"
        f"FAQ: {faq_json}\n"
        f"CTA: {cta_json}\n\n"
        f"OUTPUT:\n"
        f"1. Testimonials <section id='testimonials'>: gradient background, card grid, star ratings (★★★★★), name, text\n"
        f"2. FAQ <section id='faq'>: bg-white, accordion items (click to expand), smooth animation\n"
        f"3. Final CTA section: dark gradient, headline, subheadline, primary button, reassurance text\n"
        f"4. Contact <section id='contact'>: bg-gray-50, split layout: left=form(name/phone/message/submit), "
        f"right=contact info (phone:{phone}, email:{email}, address:{address}, hours:24/7)\n"
        f"5. Footer: dark bg, logo, nav links, social icons (FB/IG/LinkedIn all href='#'), copyright\n"
        f"6. WhatsApp floating button (bottom-right, pulse animation, href=https://wa.me/{whatsapp})\n"
        f"7. Mobile sticky CTA bar (bottom, hidden on md+)\n"
        f"8. ONE <script> block with: IntersectionObserver reveal, FAQ accordion toggle, "
        f"mobile menu toggle, sticky header shadow on scroll, form submit redirects to WhatsApp\n"
        f"9. Close with </body></html>"
    )
    part3_raw, stop3 = call_claude(client, system_prompt, part3_msg, "Frontend Part 3 (Footer+JS)", max_tokens=8000)
    part3_html = extract_html(part3_raw)

    if stop3 == "max_tokens" and "</html>" not in part3_html:
        part3_html += "\n</body>\n</html>"

    full_html = part1_html + "\n" + part2_html + "\n" + part3_html
    print(f"  ✓ Frontend complete: {len(part1_html):,} + {len(part2_html):,} + {len(part3_html):,} = {len(full_html):,} chars total")
    return full_html


def extract_json(text: str) -> str:
    """Extract JSON block from LLM response."""
    # Try to find JSON between ```json ... ``` blocks
    if "```json" in text:
        start = text.find("```json") + 7
        end = text.find("```", start)
        return text[start:end].strip()
    # Try to find raw JSON object
    if text.strip().startswith("{"):
        return text.strip()
    # Try to find first { to last }
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        return text[start:end]
    return text


def extract_html(text: str) -> str:
    """Extract HTML from LLM response."""
    if "```html" in text:
        start = text.find("```html") + 7  # skip "```html\n"
        end = text.find("```", start)
        if end == -1:
            return text[start:].strip()
        return text[start:end].strip()
    if "<!DOCTYPE" in text or "<html" in text:
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
    print("\n[1/6] Loading client data...")
    config, brief = load_client(client_id)
    template_name = config["template"]
    prompts = load_prompts(template_name)
    brief_str = json.dumps(brief, indent=2)
    print(f"  ✓ Template: {template_name} | Language: {config['language']} | Goal: {config['goal']}")

    # STEP 1 — Business Analysis
    print("\n[2/6] Business Analysis")
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

    # STEP 2 — Copywriting
    print("\n[3/6] Copy Generation")
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

    # Validate contract
    errors = validate_copy_json(copy_data)
    if errors:
        print(f"  WARNING: Contract violations found:")
        for e in errors:
            print(f"    - {e}")
    else:
        print("  ✓ Output contract validated")

    # STEP 3 — SEO Optimization
    print("\n[4/6] SEO Optimization")
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

    # Merge branding from brief into data
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
    print("\n[5/6] UI Layout Design")
    layout_raw, _ = call_claude(
        client,
        system_prompt=prompts["ui_designer"],
        user_message=(
            f"Design the layout for this website. Return JSON with layout_style, visual_intensity, and sections array.\n\n"
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

    # STEP 5 — Frontend Generation (2-part strategy)
    print("\n[6/6] Frontend Generation")
    html_content = generate_frontend(client, prompts["frontend_dev"], brief, config, seo_data, layout_data)

    # Save output
    output_dir = PROJECTS_DIR / client_id / "output"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "index.html"
    output_file.write_text(html_content, encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  PIPELINE COMPLETE")
    print(f"  Output: projects/{client_id}/output/index.html")
    print(f"  Size: {len(html_content):,} characters")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Agent - AI Website Generator")
    parser.add_argument("--client", required=True, help="Client ID (folder name in /projects/)")
    args = parser.parse_args()
    run_pipeline(args.client)
