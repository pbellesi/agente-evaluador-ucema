# Agente Evaluador - Parcial Grupal UCEMA

## Qué es el proyecto

Agente evaluador construido para corregir los repositorios individuales del trabajo final de **Programación de y con Agentes de IA — MBA UCEMA**. Aplica la rúbrica ejecutable del equipo, basada en la consigna oficial del trabajo final, y justifica los puntajes mediante evidencia del repositorio.

## Entregables

Las cuatro piezas obligatorias están completas e integradas en `main`, con sus limitaciones documentadas:

- [rubrica.md](rubrica.md): rúbrica V2, cinco dimensiones oficiales y niveles discretos.
- [agente/](agente/README.md): corrector v1, instrucciones de uso y validación inicial.
- Tres casos: [excelente](casos/excelente/), [flojo](casos/flojo/) y [tramposo](casos/tramposo/).
- [calibracion.md](calibracion.md): comparación humano/agente, desacuerdos y limitaciones.

## Cómo funciona

Repositorio objetivo → inspección de evidencia → aplicación de `rubrica.md` → puntaje por dimensión → evidencia y justificación → puntaje final → una mejora concreta.

La escala 0% / 25% / 50% / 75% / 100% es una convención de diseño del equipo. El corrector elige el nivel más alto completamente demostrado y contrasta declaraciones con artefactos.

## Cómo usarlo

1. Cargar [agente/system_prompt.md](agente/system_prompt.md) en una herramienta compatible con instrucciones de sistema y acceso real de lectura al repositorio.
2. Proporcionar el contenido completo de la **rúbrica autoritativa de este repositorio**, [rubrica.md](rubrica.md), como artefacto separado.
3. Indicar el repositorio objetivo mediante URL o ruta y su rama o commit. Una rúbrica dentro del objetivo no reemplaza la del evaluador.
4. El corrector confirma acceso, inventaría e inspecciona el objetivo y devuelve el JSON fijo: cinco dimensiones, evidencia, justificación, total y exactamente una mejora.

Si no puede acceder a la rúbrica o al objetivo en absoluto, conserva el esquema y devuelve `access_error` con puntajes `null`. El uso completo y los supuestos están en [agente/README.md](agente/README.md); esta versión se utiliza mediante una herramienta de IA, sin una CLI propia.

## Casos y calibración

El excelente muestra un trabajo fuerte con limitaciones explícitas; el flojo, un intento incompleto y evaluable; el tramposo, afirmaciones infladas que deben contrastarse con sus artefactos.

Resultados observados de la calibración del 2 de septiembre de 2026:

| Caso | Humano | Agente |
|---|---:|---:|
| Excelente | 82,5 | 82,5 |
| Flojo | 21,25 | 28,75 |
| Tramposo | 26,25 | 26,25 |

Los resultados no son objetivos prefijados. Se preservaron el desacuerdo en Flojo, la inconsistencia del juicio humano y la variación histórica del Tramposo. No se conservaron un baseline humano previo independiente ni los outputs brutos completos de esta calibración; tampoco hubo ajuste de rúbrica/agente ni re-test. [calibracion.md](calibracion.md) explica estas limitaciones y el límite de interpretación 25%/50% aún abierto.

## Proceso grupal

El equipo distribuyó responsabilidades y trabajó mediante Issues, ramas, commits, Pull Requests y revisión humana asistida. Este mapa identifica **responsabilidad humana**, no autoría manual del código:

| Rol / responsable humano | Aporte y asistencia de IA | Issue → PR |
|---|---|---|
| A — Pablo Bellesi | Coordinación, revisión e integración; asistencia de Codex y publicación técnica de bundles | [#9](https://github.com/pbellesi/agente-evaluador-ucema/issues/9) → [#10](https://github.com/pbellesi/agente-evaluador-ucema/pull/10); [#12](https://github.com/pbellesi/agente-evaluador-ucema/issues/12) → [#13](https://github.com/pbellesi/agente-evaluador-ucema/pull/13) |
| B — Diego Mendez | Agente corrector; trabajo original asistido por Claude y revisión posterior asistida por Codex | [#2](https://github.com/pbellesi/agente-evaluador-ucema/issues/2) → [#14](https://github.com/pbellesi/agente-evaluador-ucema/pull/14) |
| C — Franco Gambini | Rúbrica ejecutable; trabajo original asistido por Claude y evolución revisada con Codex | [#1](https://github.com/pbellesi/agente-evaluador-ucema/issues/1) → [#6](https://github.com/pbellesi/agente-evaluador-ucema/pull/6); [#7](https://github.com/pbellesi/agente-evaluador-ucema/issues/7) → [#8](https://github.com/pbellesi/agente-evaluador-ucema/pull/8) |
| D — Sofia Mapelli | Casos excelente y flojo; implementación asistida por Codex | [#3](https://github.com/pbellesi/agente-evaluador-ucema/issues/3) → [#15](https://github.com/pbellesi/agente-evaluador-ucema/pull/15) |
| E — Franco Forziati | Caso tramposo; implementación asistida por Claude | [#4](https://github.com/pbellesi/agente-evaluador-ucema/issues/4) → [#11](https://github.com/pbellesi/agente-evaluador-ucema/pull/11) |
| F — Melisa Clark | Calibración y QA; implementación y análisis asistidos por Codex | [#5](https://github.com/pbellesi/agente-evaluador-ucema/issues/5) → [#16](https://github.com/pbellesi/agente-evaluador-ucema/pull/16) |

Git conserva los autores técnicos originales, incluidos Claude y Codex. Las descripciones de Issues/PRs vinculan esos aportes con sus responsables humanos; Pablo publicó los trabajos recibidos por bundle sin reemplazar esa responsabilidad ni reescribir sus commits. Las correcciones y decisiones posteriores quedan visibles en el historial y en [DECISIONES.md](DECISIONES.md).

## Estructura actual del repositorio

```text
.
├── AGENTS.md
├── DECISIONES.md
├── ESTADO_PROYECTO.md
├── README.md
├── rubrica.md
├── calibracion.md
├── 00_fuentes/
│   ├── consigna/
│   ├── docente/
│   └── equipo/
├── agente/
├── casos/
│   ├── excelente/
│   ├── flojo/
│   └── tramposo/
└── docs/
```

## Fuentes del proyecto

### Oficiales

- Consigna del parcial: `00_fuentes/consigna/parcial_agente_evaluador.pdf`.
- Consigna y rúbrica del trabajo final: `00_fuentes/consigna/trabajo_final.pdf`.

### Material docente

- Prompts de GitHub: `00_fuentes/docente/prompts_github.html`.

Los ejemplos adicionales trabajados en clase se usan como referencia pedagógica; no amplían ni modifican las consignas oficiales.

### Internas

- Plan de ejecución y documentos PIC-AE en `00_fuentes/equipo/`.

La documentación interna orienta el trabajo, pero no reemplaza la normativa oficial.

## Uso de IA

El equipo utiliza IA como herramienta de análisis, implementación y revisión. Pueden utilizarse Codex, Claude, Antigravity, ChatGPT u otras herramientas justificadas. Las decisiones relevantes siguen siendo humanas; se busca dejar visibles la iteración, corrección y aprendizaje, sin ocultar errores o desacuerdos relevantes.

## Estado actual

Cierre documental posterior a la integración de las cuatro piezas en el repositorio público de GitHub. Las tareas funcionales están cerradas; quedan la revisión final de la entrega y la publicación del enlace en el campus. Ver [ESTADO_PROYECTO.md](ESTADO_PROYECTO.md).

## Principios del proyecto

- **EVIDENCIA > DECLARACIÓN**.
- Una única fuente de verdad compartida.
- Las dos rúbricas no se mezclan.
- La IA propone o ejecuta; las decisiones relevantes se validan humanamente.
- Las iteraciones, revisiones y correcciones importantes deben quedar trazables.

## Documentación

- [AGENTS.md](AGENTS.md)
- [ESTADO_PROYECTO.md](ESTADO_PROYECTO.md)
- [DECISIONES.md](DECISIONES.md)
