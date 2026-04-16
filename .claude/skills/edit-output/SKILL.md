---
name: edit-output
description: Revisa y mejora el HTML generado en projects/{client}/output/index.html. Úsame para auditorías UX, corrección de bugs visuales, edición directa de secciones, actualización de imágenes o contenido, y refinamientos premium post-generación.
when_to_use: Cuando el usuario quiera mejorar, editar, corregir, o auditar el index.html de un cliente. También cuando mencione "ver el sitio", "revisar el output", "cambiar una sección", o "mejorar el diseño".
---

# Skill: Edit Output HTML

## Flujo de trabajo para editar output

### 1. Identificar el archivo objetivo

```
projects/{client_id}/output/index.html
```

### 2. Antes de editar — leer el contexto necesario

Solo leer lo que realmente se necesita para la edición:

```
# Para editar contenido/copy:
projects/{client_id}/brief.json         ← datos del negocio

# Para editar diseño/colores:
projects/{client_id}/client-dna.json    ← identidad visual

# Para cambiar imágenes:
projects/{client_id}/images.json        ← rutas de imágenes locales

# Para datos reales (stats, testimonios):
projects/{client_id}/client-facts.md    ← fuente de verdad
```

**NO leer** `agents/frontend-dev.md` ni otros archivos de agentes — son para generate.py, no para edición directa.

### 3. Auditoría UX rápida (checklist)

Verificar en el HTML:
- [ ] Hero: imagen local (no Unsplash), headline potente, CTA visible
- [ ] Visual break: stats reales en grande, background oscuro
- [ ] Secciones: backgrounds alternados (blanco/gris/oscuro, nunca iguales seguidos)
- [ ] Portfolio: imágenes locales de `../assets/images/portafolio/`
- [ ] Formulario: `id="contact-form"` único, campos reales (no placeholders)
- [ ] Logo header: imagen local con fallback tipográfico
- [ ] IDs: sin duplicados (verificar `id="contact"`, `id="contact-form"`)
- [ ] Secciones balanceadas: cada `<section>` tiene su `</section>`

### 4. Ediciones directas recomendadas (sin regenerar)

**Cambiar imagen hero:**
```html
<!-- Buscar y reemplazar src de la imagen hero -->
<img src="../assets/images/hero/hero5.jpg" ...>
```

**Cambiar stats del visual break:**
```html
<!-- Buscar section id="visual-break" -->
<p ...>47</p>  ← número real de clientes
<p ...>7</p>   ← días de entrega
```

**Corregir form duplicado:**
- Solo puede haber UN `<form id="contact-form">` en el documento
- Verificar con Node: `lines.filter(l => l.includes('<form id="contact-form"')).length === 1`

### 5. Verificación post-edición

```bash
# Contar secciones (debe ser 0 — todas abren y cierran)
# Verificar IDs únicos
# Abrir en browser para confirmar visualmente
```

## Reglas de edición directa

1. **Preferir Edit tool** sobre Write para cambios parciales
2. **Usar Node.js** para operaciones de búsqueda/reemplazo en archivos grandes
3. **No regenerar** si se puede editar directamente — ahorra tokens y tiempo
4. Los cambios en HTML **no se pierden** al regenerar si se documenta en `client-dna.json`
