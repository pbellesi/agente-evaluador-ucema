# Estado del Proyecto

## Fecha de actualización

31 de agosto de 2026.

## Fase actual

Desarrollo inicial: repositorio GitHub activo y rúbrica ejecutable V2 completada en `main`; agente, casos y calibración pendientes de desarrollo.

## Equipo y responsables

| Rol | Responsable | Alcance principal |
|---|---|---|
| A | Pablo Bellesi | Coordinación e integración del avance |
| B | Diego Mendez | Integración técnica; agente corrector en desarrollo |
| C | Franco Gambini | Rúbrica ejecutable completada; disponible para consulta |
| D | Sofia Mapelli | Casos excelente y flojo |
| E | Franco Forziati | Caso adversarial / tramposo |
| F | Melisa Clark | Calibración y QA, dependiente de agente y casos |

## Completado

- Estructura base de carpetas creada.
- Fuentes oficiales cargadas en `00_fuentes/consigna/`.
- Material docente cargado en `00_fuentes/docente/`.
- Documentos internos cargados en `00_fuentes/equipo/`.
- Roles normalizados en la documentación interna.
- `AGENTS.md`, `DECISIONES.md` y README mínimo creados.
- `.gitignore` creado.
- Git local inicializado, con rama `main`, commits y remoto GitHub configurado.
- Estructura mínima versionable creada: `calibracion.md` inicial y README mínimos en `agente/`, los tres casos y `docs/`.
- Repositorio base publicado en GitHub.
- Rúbrica ejecutable V2 completada en `rubrica.md` y disponible en `main`.
- Issue #1 y Issue #7 cerrados.
- PR #6 y PR #8 mergeados hacia `main`.

## En curso

- Agente corrector: en desarrollo (responsable principal: Diego Mendez, Rol B).

## Pendiente inmediato

- Completar el agente corrector.
- Construir los casos excelente y flojo.
- Construir el caso adversarial / tramposo.
- Ejecutar calibración y QA cuando existan agente y casos.

## Bloqueos / inconsistencias conocidas

- La calibración efectiva depende de un agente corrector funcional y de los tres casos de prueba.
- Persisten checkmarks prematuros, escalas de ejemplo inconsistentes y una referencia a PDF inexistente en documentación interna; no fueron corregidos en este Issue.

## Próximo milestone

Agente corrector ejecutable y casos de prueba iniciales listos para comenzar la calibración.

## Próximo paso

Avanzar con el agente corrector.
