---
name: generate-client
description: Genera o regenera el sitio web completo de un cliente usando el pipeline Python. Úsame cuando el usuario quiera correr generate.py, generar un nuevo sitio, regenerar secciones, o revisar el output generado.
when_to_use: Cuando el usuario mencione "generar", "regenerar", "correr el pipeline", "generate.py", o cuando quiera producir un nuevo index.html para un cliente.
---

# Skill: Generate Client Website

## Qué hace este skill

Orquesta la generación completa de un sitio web premium usando el pipeline multi-agente.

## Verificación previa (SIEMPRE hacer antes de ejecutar)

```bash
# 1. Confirmar que el cliente existe
ls projects/{client_id}/

# 2. Verificar archivos requeridos
# Obligatorios:
projects/{client_id}/brief.json       ← datos del negocio
projects/{client_id}/config.json      ← template, idioma, features

# Opcionales pero recomendados:
projects/{client_id}/client-dna.json  ← identidad visual
projects/{client_id}/images.json      ← biblioteca de imágenes
projects/{client_id}/client-facts.md  ← stats y datos reales (previene alucinaciones)
```

## Ejecución

```bash
python generate.py --client {client_id}
```

## Qué genera el pipeline

| Paso | Agente | Output |
|------|--------|--------|
| 1 | business-analyzer | Análisis de negocio, audiencia, tono |
| 2 | brand-strategist | Layout único, colores, visual break |
| 3 | copywriter | Todo el copy en el idioma del cliente |
| 4 | seo-optimizer | Meta tags, schema.org |
| 5 | ui-designer | Orden de secciones, variación de layout |
| 6-8 | frontend-dev (3 partes) | HTML completo del sitio |

## Output esperado

```
projects/{client_id}/output/index.html   ← sitio generado
core/generation-log.json                 ← registro de decisiones de layout
```

## Revisión post-generación

Después de generar, siempre verificar:
1. ¿El hero tiene imagen local? (`../assets/images/hero/`)
2. ¿El visual break tiene stats reales? (de `client-facts.md`)
3. ¿Las secciones alternan backgrounds? (blanco/gris/oscuro)
4. ¿El formulario de contacto tiene EmailJS configurado?
5. Abrir en browser para verificar visualmente

## Errores comunes

| Error | Causa | Fix |
|-------|-------|-----|
| `Client not found` | client_id incorrecto | Verificar nombre exacto en `projects/` |
| `brief.json missing` | Archivo no creado | Copiar de `core/brief.template.json` |
| Imágenes no cargan | Rutas incorrectas | Verificar paths en `images.json` |
| Tokens insuficientes | frontend-dev.md muy largo | Ya está optimizado en 5 partes |
