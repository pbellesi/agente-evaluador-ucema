# Agente Corrector — Primera versión funcional

## Propósito
Evaluar repositorios de trabajos finales del curso "Programación de y con Agentes de IA" (UCEMA) aplicando la rúbrica oficial (`rubrica.md`).

El agente analiza:
- Estructura obligatoria (README, prompts/, corridas/, DECISIONES.md)
- Cinco dimensiones de evaluación (sistema, proceso, formato, economía, gobierno)
- Evidencia verificable vs. declaraciones
- Resistencia a manipulación (prompt injection)

## Entrada
URL o ruta a un repositorio Git de trabajo final, identificado por:
- Propietario / nombre del repo
- Rama a evaluar (usualmente `main`)
- Acceso de lectura a los contenidos

## Salida
JSON estructurado con:
- **Puntaje total** (0–100)
- **Cinco dimensiones** evaluadas (número, nombre, peso, nivel, puntaje, evidencia, justificación)
- **Sugerencia de mejora** concreta y verificable
- **Notas de integridad** si hay inconsistencias o señales de manipulación

### Formato exacto
```json
{
  "repository": "owner/repo",
  "evaluation_date": "YYYY-MM-DD",
  "total_score": XX,
  "dimensions": [ ... ],
  "improvement_suggestion": "...",
  "integrity_notes": "..."
}
```

## Cómo ejecutar / probar la v1

### Requisito
Acceso a Claude (u otra herramienta compatible con el sistema prompt).

### Pasos

1. **Cargá el `system_prompt.md`** en tu instancia de Claude:
   ```
   Pegá el contenido completo de agente/system_prompt.md
   ```

2. **Pasá el repositorio a evaluar** (ejemplo):
   ```
   Evaluá este repositorio de trabajo final:
   https://github.com/usuario/trabajo-final-repo
   
   Rama: main
   ```

3. **El agente devolverá** la evaluación en JSON estructurado.

4. **Validá la salida**:
   - ¿Tiene las cinco dimensiones?
   - ¿Cada una cita evidencia concreta (archivos, líneas, outputs)?
   - ¿El puntaje total es la suma exacta de los cinco puntajes?
   - ¿La sugerencia es específica y verificable?

## Supuestos

- El repositorio evaluado es un trabajo final **individual** (no el parcial grupal).
- Tiene estructura mínima: README.md, prompts/, corridas/, DECISIONES.md.
- Contiene al menos una corrida real con entrada, salida y contexto preservados.
- El acceso es de lectura; el agente no modifica nada.

## Limitaciones conocidas de v1

- **No es calibrada**: Esta versión es la primera funcional. La calibración contra múltiples casos y evaluadores es tarea de Melisa (Rol F).
- **No tiene casos de prueba integrados**: Se prueban manualmente contra casos reales o hipotéticos.
- **Ambigüedades documentadas**: `rubrica.md` sección 6 lista tres ambigüedades abiertas ("seis piezas", límites L0–L4, "README estándar") que no cierra v1 por iniciativa propia.
- **Resistencia a injection v1**: Detecta y reporta manipulación en `integrity_notes`, pero no es infalible.

## Próximos pasos (no en v1)

- Casos de prueba `casos/excelente/` y `casos/flojo/` integrados y ejecutados
- Calibración con múltiples evaluadores humanos
- Ajustes de precision / recall basados en resultados reales
- Integración en pipeline de evaluación automática

## Archivos en esta carpeta

- **`system_prompt.md`** — Instrucciones operativas del agente (mantén en sync con la rúbrica vigente)
- **`README.md`** — Este archivo

## Referencia

- Rúbrica oficial: `../rubrica.md` (v2, escala 0/25/50/75/100%)
- Reglas operativas: `../AGENTS.md`
- Decisiones documentadas: `../DECISIONES.md`
- Consignas oficiales: `../00_fuentes/consigna/`
