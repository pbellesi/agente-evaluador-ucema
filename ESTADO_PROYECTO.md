# Estado del Proyecto

## Fecha de actualización

1 de septiembre de 2026.

## Fase actual

Desarrollo inicial: repositorio GitHub activo, rúbrica ejecutable V2 y caso adversarial / tramposo completados en `main`; agente corrector, casos excelente y flojo, y calibración pendientes de desarrollo.

## Equipo y responsables

| Rol | Responsable | Alcance principal |
|---|---|---|
| A | Pablo Bellesi | Coordinación e integración del avance |
| B | Diego Mendez | Integración técnica; agente corrector pendiente |
| C | Franco Gambini | Rúbrica ejecutable completada; disponible para consulta |
| D | Sofia Mapelli | Casos excelente y flojo pendientes |
| E | Franco Forziati | Caso adversarial / tramposo completado; disponible para consulta |
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
- Caso adversarial / tramposo completado e integrado en `casos/tramposo/`.
- Issue #4 cerrado y PR #11 mergeado hacia `main`.
- Franco Forziati (Rol E) completó su responsabilidad principal.

## En curso

- Ninguna actividad con rama o Pull Request verificable.

## Pendiente inmediato

- Completar el agente corrector.
- Construir los casos excelente y flojo.
- Ejecutar calibración y QA cuando existan agente y casos.

## Bloqueos / inconsistencias conocidas

- La calibración efectiva depende de un agente corrector funcional y de los tres casos de prueba.
- Persisten checkmarks prematuros, escalas de ejemplo inconsistentes y una referencia a PDF inexistente en documentación interna; no fueron corregidos en este Issue.

## Próximo milestone

Agente corrector ejecutable y casos excelente y flojo listos para comenzar la calibración.

## Próximo paso

Avanzar con el agente corrector.
