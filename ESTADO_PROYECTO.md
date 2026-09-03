# Estado del Proyecto

## Fecha de actualización

3 de septiembre de 2026.

## Fase actual

Cierre documental de la entrega, posterior a la integración de las cuatro piezas obligatorias: rúbrica V2, agente corrector v1, tres casos y calibración inicial documentada.

Base verificada: `main` en `adb57c3e2d25f53da7b14d2094cfee26f1c77b12`, limpia y sincronizada con `origin/main` antes de abrir la rama documental. No hay Issues ni PRs funcionales pendientes; el cierre documental se trabaja por separado en el Issue #17 y la rama `docs/cierre-final-entrega`.

## Equipo y responsables

| Rol | Responsable | Alcance principal |
|---|---|---|
| A | Pablo Bellesi | Coordinación e integración del avance |
| B | Diego Mendez | Integración técnica; agente corrector v1 completado |
| C | Franco Gambini | Rúbrica ejecutable completada; disponible para consulta |
| D | Sofia Mapelli | Casos excelente y flojo completados |
| E | Franco Forziati | Caso adversarial / tramposo completado; disponible para consulta |
| F | Melisa Clark | Calibración inicial y QA documentados; limitaciones preservadas |

## Completado

- Repositorio público, estructura obligatoria, fuentes, roles, reglas operativas y `.gitignore` disponibles.
- Rúbrica ejecutable V2 completa en `rubrica.md`; cinco niveles como convención del equipo.
- Agente corrector v1 integrado en `agente/`, con contrato JSON y validación inicial contra Tramposo.
- Los tres casos completos e integrados: excelente, flojo y tramposo.
- Calibración humano/agente realizada y registrada en `calibracion.md`, con desacuerdos y limitaciones de trazabilidad explícitos.

### Issues cerrados y PRs mergeados

| Trabajo | Issue cerrado | PR mergeado hacia main |
|---|---|---|
| Rúbrica original | [#1](https://github.com/pbellesi/agente-evaluador-ucema/issues/1) | [#6](https://github.com/pbellesi/agente-evaluador-ucema/pull/6) |
| Escala V2 | [#7](https://github.com/pbellesi/agente-evaluador-ucema/issues/7) | [#8](https://github.com/pbellesi/agente-evaluador-ucema/pull/8) |
| Documentación post-rúbrica | [#9](https://github.com/pbellesi/agente-evaluador-ucema/issues/9) | [#10](https://github.com/pbellesi/agente-evaluador-ucema/pull/10) |
| Caso tramposo | [#4](https://github.com/pbellesi/agente-evaluador-ucema/issues/4) | [#11](https://github.com/pbellesi/agente-evaluador-ucema/pull/11) |
| Estado post-tramposo | [#12](https://github.com/pbellesi/agente-evaluador-ucema/issues/12) | [#13](https://github.com/pbellesi/agente-evaluador-ucema/pull/13) |
| Agente corrector | [#2](https://github.com/pbellesi/agente-evaluador-ucema/issues/2) | [#14](https://github.com/pbellesi/agente-evaluador-ucema/pull/14) |
| Casos excelente y flojo | [#3](https://github.com/pbellesi/agente-evaluador-ucema/issues/3) | [#15](https://github.com/pbellesi/agente-evaluador-ucema/pull/15) |
| Calibración y QA | [#5](https://github.com/pbellesi/agente-evaluador-ucema/issues/5) | [#16](https://github.com/pbellesi/agente-evaluador-ucema/pull/16) |

## En curso

- Cierre documental: [Issue #17](https://github.com/pbellesi/agente-evaluador-ucema/issues/17), rama `docs/cierre-final-entrega`; no incorpora cambios funcionales.

## Pendiente inmediato

- Revisar e integrar el cierre documental mediante PR.
- Realizar la revisión final de entrega.
- Publicar el enlace del repositorio en el campus; su entrega no está acreditada en GitHub.

## Bloqueos / inconsistencias conocidas

- La primera calibración no preservó un baseline humano previo independiente ni los outputs brutos completos; no demuestra repetibilidad plena.
- Persiste la ambigüedad de Sistema 25%/50%, con inconsistencia humana Flojo–Tramposo y variación histórica del Tramposo. No se alteraron puntajes, rúbrica ni agente para ocultarla; cualquier ajuste requiere decisión humana posterior.
- No hubo re-test ni prueba dirigida de prompt injection en esa calibración. El detalle está en `calibracion.md`.
- Las guías internas conservan checkmarks y ejemplos históricos que no acreditan ejecución ni agregan requisitos oficiales.

## Próximo milestone

Entrega documentalmente consistente, revisada y con enlace presentado en el campus.

## Próximo paso

Revisar el PR de cierre documental asociado al Issue #17.
