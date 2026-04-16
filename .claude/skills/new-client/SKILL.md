---
name: new-client
description: Configura un nuevo cliente desde cero en el pipeline. Crea la estructura de carpetas, los archivos de configuración (brief.json, config.json, client-dna.json, images.json) y prepara todo para ejecutar generate.py. Úsame cuando el usuario quiera agregar un nuevo cliente al sistema.
when_to_use: Cuando el usuario mencione "nuevo cliente", "agregar cliente", "configurar cliente", o proporcione información de un nuevo negocio para crear un sitio web.
---

# Skill: New Client Setup

## Paso 1 — Crear estructura de carpetas

```bash
mkdir projects/{client_id}
mkdir projects/{client_id}/assets
mkdir projects/{client_id}/assets/images
mkdir projects/{client_id}/output
```

**Naming convention para client_id:**
- Lowercase, guiones en lugar de espacios
- Ejemplos: `mariscos-don-pepe`, `clinica-dental-sonrisa`, `ferreteria-el-clavo`

## Paso 2 — Copiar templates base

```bash
cp core/brief.template.json projects/{client_id}/brief.json
cp core/config.template.json projects/{client_id}/config.json
```

## Paso 3 — Llenar brief.json

Campos OBLIGATORIOS a completar con datos reales del cliente:

```json
{
  "business_name": "",          ← nombre del negocio
  "business_type": "",          ← "services" | "ecommerce" | "restaurant" | "healthcare"
  "industry": "",               ← industria específica
  "location": "",               ← ciudad, país
  "language": "es",             ← "es" | "en" | "pt"
  "goal": "leads",              ← "leads" | "sales" | "awareness"
  "value_proposition": "",      ← propuesta de valor única (1-2 oraciones)
  "services": [],               ← lista de servicios con precio
  "pricing": [],                ← planes de precios
  "contact_info": {},           ← teléfono, email, dirección
  "whatsapp": ""                ← número para botón WhatsApp
}
```

## Paso 4 — Llenar config.json

```json
{
  "template": "agency",         ← template de industria (ver templates/)
  "language": "es",
  "features": {
    "whatsapp_button": true,
    "contact_form": true,
    "emailjs": false            ← true si se configura EmailJS
  }
}
```

## Paso 5 — Crear client-dna.json (recomendado)

Define la identidad visual y reglas de diseño específicas del cliente.

Campos clave:
```json
{
  "color_palette": {
    "primary": "#4F46E5",
    "accent": "#F59E0B",
    "bg_dark": "#0F172A"
  },
  "design_direction": {
    "hero_preference": "split-emotional",
    "forbidden_patterns": []    ← patrones que NO quiere el cliente
  },
  "section_order": ["hero", "services", "portfolio", "visual-break", ...]
}
```

## Paso 6 — Crear client-facts.md (CRÍTICO para calidad)

Previene que el pipeline invente datos. Incluir:
- Número real de clientes atendidos
- Años de operación
- Casos de éxito con nombres reales
- Precios reales
- Testimonios verificados

```markdown
# Datos verificados — {Nombre del Negocio}

## Métricas reales
- X clientes atendidos
- Y años de experiencia

## Testimonios reales
> "..." — Nombre Apellido, Empresa
```

## Paso 7 — Agregar imágenes (si hay)

```
projects/{client_id}/assets/images/
  hero/          ← fotos para el hero
  portafolio/    ← screenshots de trabajos
  servicios/     ← imágenes de servicios
  LogoCliente.png
```

Luego crear `projects/{client_id}/images.json` con las rutas.

## Paso 8 — Ejecutar pipeline

```bash
python generate.py --client {client_id}
```

## Checklist final antes de ejecutar

- [ ] `brief.json` completado con datos reales
- [ ] `config.json` tiene template correcto
- [ ] `client-facts.md` existe con datos verificados
- [ ] Imágenes subidas (si hay)
- [ ] `client-dna.json` tiene colores y section_order
