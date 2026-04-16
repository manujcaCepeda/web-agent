---
name: update-agents
description: Actualiza, mejora o corrige los prompts de los agentes del pipeline (agents/ y core/). Úsame cuando el usuario quiera mejorar la calidad del output, agregar reglas, corregir comportamientos del agente, o ajustar el sistema de generación. Incluye guía para editar frontend-dev-*.md de forma eficiente.
when_to_use: Cuando el usuario mencione "mejorar el agente", "agregar regla", "el agente hace X mal", "actualizar frontend-dev", "cambiar el pipeline", o quiera mejorar sistemáticamente la calidad del output.
---

# Skill: Update Agent Prompts

## Estructura de archivos de agentes

### Agentes del pipeline (agents/)
```
agents/
  business-analyzer.md    ← Step 1: análisis de negocio
  brand-strategist.md     ← Step 2: estrategia visual y layout
  copywriter.md           ← Step 3: generación de copy
  seo-optimizer.md        ← Step 4: SEO y meta tags
  ui-designer.md          ← Step 5: diseño de UI y secciones
  frontend-dev-core.md    ← Step 6-8 (parte 1): reglas base + inputs
  frontend-dev-design.md  ← Step 6-8 (parte 2): design language + tipografía
  frontend-dev-sections.md ← Step 6-8 (parte 3): blueprints por sección
  frontend-dev-systems.md ← Step 6-8 (parte 4): imágenes + forms + UX
  frontend-dev-qa.md      ← Step 6-8 (parte 5): QA checklist
```

### Sistemas compartidos (core/)
```
core/
  style-engine.md         ← 8 modos de estilo canónicos
  output-contract.md      ← schema JSON compartido entre agentes
  art-director.md         ← reglas de dirección de arte
  hero-system.md          ← blueprints del hero section
  component-system.md     ← biblioteca de componentes
  orchestrator.md         ← orden de ejecución y validación
```

## Cómo agregar una regla nueva

### Regla de diseño (ej: "nunca usar X patrón"):
→ Agregar a `agents/frontend-dev-core.md` en la sección `## HARD RULES`

### Regla de sección específica (ej: "el pricing siempre debe tener..."):
→ Agregar a `agents/frontend-dev-sections.md` en la subsección de esa sección

### Regla de imágenes:
→ Agregar a `agents/frontend-dev-systems.md` en `## IMAGE SYSTEM`

### Regla de brand strategy (ej: "agencias no usan foto de persona"):
→ Agregar a `agents/brand-strategist.md`

### Regla global aplicable a todos los clientes:
→ Agregar a `core/output-contract.md`

## Workflow para mejorar calidad post-generación

1. **Identificar el problema** en el output generado
2. **Trazar al agente responsable** (¿en qué paso se generó ese contenido?)
3. **Leer el agente específico** (solo ese archivo, no todos)
4. **Agregar la regla** con el formato correcto:
   ```markdown
   ### REGLA: [nombre descriptivo]
   - ✅ Hacer: [comportamiento correcto]
   - ❌ No hacer: [comportamiento incorrecto]
   - Por qué: [razón]
   ```
5. **Probar** corriendo `generate.py` con el cliente de prueba

## Formato de reglas efectivas

Las reglas más efectivas son:
- **Específicas**: "En la sección pricing, el botón del plan featured DEBE decir 'Empezar con este plan →'" ✅
- **Con ejemplo**: Incluir el HTML o copy exacto esperado
- **Con anti-ejemplo**: Mostrar qué NO hacer
- **Sin ambigüedad**: Evitar "debería" o "considera" — usar "DEBE" o "NUNCA"

## frontend-dev — Referencia rápida de archivos

| Archivo | Qué contiene | Cuándo leer |
|---------|-------------|-------------|
| `frontend-dev-core.md` | Reglas base, inputs, output contract, hard rules | Siempre para troubleshooting |
| `frontend-dev-design.md` | Tipografía, colores, design language | Problemas de estilo/visual |
| `frontend-dev-sections.md` | Blueprint de cada sección HTML | Problemas de sección específica |
| `frontend-dev-systems.md` | Imágenes, formularios, animaciones, UX | Problemas de imágenes o forms |
| `frontend-dev-qa.md` | QA checklist completo | Validación final |
