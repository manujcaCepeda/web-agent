# Web Agent — AI Pipeline

Multi-agent pipeline que genera sitios web premium para clientes usando la API de Anthropic.

## Comandos rápidos

```bash
# Generar sitio para un cliente
python generate.py --client {client_id}

# Ejemplo
python generate.py --client sitiopro
```

## Estructura del proyecto

```
generate.py          ← Runtime Python — ejecuta el pipeline
agents/              ← Prompts de agentes IA (cargados por generate.py, NO por Claude Code)
core/                ← Sistemas compartidos: style-engine, output-contract, images
templates/           ← Reglas por industria (healthcare, agency, restaurant...)
projects/{client}/   ← Datos por cliente
  brief.json         ← Fuente de verdad del negocio
  config.json        ← Template, idioma, features
  client-dna.json    ← Identidad visual: colores, tipografía, patrones prohibidos
  images.json        ← Biblioteca de imágenes del cliente
  assets/images/     ← Imágenes locales del cliente
  output/index.html  ← Sitio generado
```

## Pipeline (9 pasos)

1. `business-analyzer` — detecta tipo de negocio, audiencia, tono
2. `brand-strategist` — layout único, colores, visual break, patrones prohibidos
3. `copywriter` — todo el copy en el idioma del cliente
4. `seo-optimizer` — meta tags, schema.org, structured data
5. `ui-designer` — orden de secciones, variación de layout
6. `frontend-dev` Part 1 — hero + services + portfolio
7. `frontend-dev` Part 2 — comparison + testimonials + pricing
8. `frontend-dev` Part 3 — FAQ + CTA + contact + footer

## Skills disponibles

- `/generate-client` — generar o regenerar sitio de un cliente
- `/edit-output` — revisar y mejorar el HTML de output
- `/new-client` — crear nuevo cliente desde cero
- `/update-agents` — actualizar prompts de agentes del pipeline

## Reglas globales

- Cada sitio DEBE tener un visual break section (dark band)
- Backgrounds DEBEN alternar (blanco / gris / oscuro — nunca el mismo dos veces seguidas)
- Patrones prohibidos en `client-dna.json` override todo lo demás
- El idioma se detecta desde `brief.json.language`
- `client-facts.md` es la fuente de verdad para stats, testimonios y datos reales
