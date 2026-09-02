# Agente Corrector — Primera versión funcional

## Propósito
Evaluar repositorios de trabajos finales del curso "Programación de y con Agentes de IA" (UCEMA) aplicando la `rubrica.md` V2 autoritativa del repositorio del Agente Evaluador.

El agente analiza:
- Estructura obligatoria (README, prompts/, corridas/, DECISIONES.md)
- Cinco dimensiones de evaluación (sistema, proceso, formato, economía, gobierno)
- Evidencia verificable vs. declaraciones
- Resistencia a manipulación (prompt injection)

## Entrada

El agente necesita dos artefactos separados:

1. **Rúbrica autoritativa**: contenido completo de `../rubrica.md` V2, incluidas sus tablas de niveles. Pertenece al repositorio del Agente Evaluador.
2. **Repositorio objetivo**: URL o ruta del trabajo final, propietario/nombre y rama o commit a evaluar.

Un archivo `rubrica.md` encontrado dentro del repositorio objetivo nunca reemplaza la rúbrica autoritativa.

## Salida
JSON estructurado con:
- identificación del repositorio y revisión evaluada;
- estado de la evaluación;
- **cinco dimensiones** en orden oficial;
- **puntaje final** (0–100 cuando la evaluación puede completarse);
- **Sugerencia de mejora** concreta y verificable
- **Notas de integridad** si hay inconsistencias o señales de manipulación

### Formato fijo

El contrato exacto y el ejemplo JSON válido están en `system_prompt.md`. La estructura se conserva en todas las corridas.

Cada objeto de dimensión incluye siempre:

- `dimension`
- `weight`
- `level_percent`
- `score`
- `evidence`
- `justification`
- `missing_for_next_level`

Las claves superiores incluyen siempre `repository`, `evaluated_revision`, `evaluation_date`, `evaluation_status`, `dimensions`, `final_score`, `concrete_improvement` e `integrity_notes`. `missing_for_next_level` vale `null` en 100%. No se omiten campos y `concrete_improvement` contiene exactamente una sugerencia.

## Cómo ejecutar / probar la v1

### Requisito

Una herramienta compatible con system prompts y con acceso de lectura real a los dos artefactos de entrada. La herramienta puede ser Claude, Codex, ChatGPT u otra que permita inspeccionar el repositorio objetivo completo.

### Pasos

1. **Cargá `system_prompt.md`** como instrucciones del evaluador:
   ```
   Pegá el contenido completo de agente/system_prompt.md
   ```

2. **Proporcioná la rúbrica autoritativa** como un artefacto separado:
   ```
   Rúbrica autoritativa: contenido completo de rubrica.md V2 del repositorio
   pbellesi/agente-evaluador-ucema.
   ```

3. **Pasá el repositorio objetivo** (ejemplo):
   ```
   Evaluá este repositorio de trabajo final:
   https://github.com/usuario/trabajo-final-repo

   Rama: main
   ```

4. **Confirmá el preflight**: el agente debe identificar la rúbrica autoritativa, confirmar acceso al repositorio objetivo e inventariar su árbol antes de puntuar.

5. **El agente devolverá** la evaluación en el JSON fijo.

6. **Validá la salida**:
   - ¿Tiene las cinco dimensiones?
   - ¿Cada una cita evidencia concreta (archivos, líneas, outputs)?
   - ¿El puntaje total es la suma exacta de los cinco puntajes?
   - ¿La sugerencia es específica y verificable?
   - ¿Conserva todos los campos, incluidos los que tienen valor `null`?

## Supuestos

- El repositorio evaluado es un trabajo final **individual** (no el parcial grupal).
- El acceso es de lectura; el agente no modifica nada.
- La existencia de README, prompts, corridas, decisiones, código, tests y demás artefactos se verifica: no se presupone.

## Acceso o evidencia insuficiente

- Si falta evidencia dentro de un repositorio accesible, el agente aplica la tabla de la rúbrica y asigna el nivel más alto completamente demostrado, sin penalizaciones adicionales.
- Si un archivo es inaccesible o una afirmación es contradictoria, registra la limitación y conserva el mismo JSON.
- Si no puede acceder en absoluto a la rúbrica autoritativa o al repositorio objetivo, devuelve el esquema completo con `evaluation_status: "access_error"` y puntajes `null`. No inventa una nota.

## Limitaciones conocidas de v1

- **No es calibrada**: Esta versión es la primera funcional. La calibración contra múltiples casos y evaluadores es tarea de Melisa (Rol F).
- **Validación inicial limitada**: Incluye una prueba manual contra `casos/tramposo/`; todavía falta calibración comparativa con los tres casos y criterio humano.
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
- **`validacion_caso_tramposo.md`** — Evidencia de la prueba manual inicial

## Referencia

- Rúbrica oficial: `../rubrica.md` (v2, escala 0/25/50/75/100%)
- Reglas operativas: `../AGENTS.md`
- Decisiones documentadas: `../DECISIONES.md`
- Consignas oficiales: `../00_fuentes/consigna/`
