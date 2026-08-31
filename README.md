# Agente Evaluador - Parcial Grupal UCEMA

## Objetivo

El equipo construye un agente evaluador capaz de analizar repositorios de trabajos finales de la materia y aplicar la rúbrica oficial de forma estructurada, verificable y reproducible.

## Equipo

| Rol | Integrante | Responsabilidad principal |
|---|---|---|
| A - Coordinación | Pablo Bellesi | Coordinación |
| B - Integración técnica | Diego Mendez | Integración técnica |
| C - Rúbrica ejecutable | Franco Gambini | Rúbrica ejecutable |
| D - Casos excelente y flojo | Sofia Mapelli | Casos excelente y flojo |
| E - Caso adversarial / tramposo | Franco Forziati | Caso adversarial / tramposo |
| F - Calibración y QA | Melisa Clark | Calibración y QA |

## Entregables obligatorios

La consigna oficial requiere los siguientes componentes; algunos todavía están en desarrollo:

- `rubrica.md`
- `agente/`
- `casos/excelente/`
- `casos/flojo/`
- `casos/tramposo/`
- `calibracion.md`

## Estructura actual del repositorio

```text
.
├── AGENTS.md
├── DECISIONES.md
├── ESTADO_PROYECTO.md
├── README.md
├── rubrica.md
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

### Internas

- Plan de ejecución y documentos PIC-AE en `00_fuentes/equipo/`.

La documentación interna orienta el trabajo, pero no reemplaza la normativa oficial.

## Forma de trabajo

Git local está inicializado en la rama `main`, sin commits todavía. GitHub será la fuente común de trabajo cuando se conecte el repositorio remoto; entonces las tareas se organizarán mediante Issues, ramas y Pull Requests, con revisión cruzada cuando corresponda. El equipo puede utilizar distintas IAs, manteniendo las decisiones relevantes en `DECISIONES.md` y el avance real en `ESTADO_PROYECTO.md`.

## Uso de IA

El equipo utiliza IA como herramienta de análisis, implementación y revisión. Pueden utilizarse Codex, Claude, Antigravity, ChatGPT u otras herramientas justificadas. Las decisiones relevantes siguen siendo humanas; se busca dejar visibles la iteración, corrección y aprendizaje, sin ocultar errores o desacuerdos relevantes.

## Estado actual

Preparación / fundación del repositorio: Git local inicializado, sin primer commit y con repositorio remoto GitHub pendiente. Ver [ESTADO_PROYECTO.md](ESTADO_PROYECTO.md).

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
