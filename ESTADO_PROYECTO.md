# Estado del Proyecto

## Fecha de actualización

Estado técnico verificado en `main` (`8b11d81`), sincronizado con `origin/main`.

## Fase actual

Cierre de entrega: motor final integrado y congelado, con las cuatro piezas obligatorias preservadas y validación posterior documentada.

La versión integrada en `main` incluye el motor determinístico validado por PR #31. No hay trabajo funcional pendiente.

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
- Runtime final determinístico integrado en `src/` y expuesto por `app.py`: no usa APIs generativas, registra la revisión SHA evaluada y trata el contenido objetivo como evidencia.
- Los tres casos completos e integrados: excelente, flojo y tramposo.
- Calibración humano/agente realizada y registrada en `calibracion.md`, con desacuerdos y limitaciones de trazabilidad explícitos.
- Contrato sintético de aceptación completado: 31/31 acceptance tests y 69/69 pruebas de la suite completa.
- Casos oficiales coherentes: Excelente 88,75; Flojo 28,75; Tramposo 21,25.
- Regresión externa completada: PULSO 85,0; SACME 96,25; Lapeque26 92,5; tubidj10 85,0; SilA066 85,0; FSio 92,5; El-Diegote 92,5.

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

- Cierre documental y revisión de presentación; no incorpora cambios funcionales.

## Pendiente inmediato

- Limpieza final de la interfaz Streamlit.
- Revisión de despliegue y documentación de uso.
- Preparación de defensa y entrega; la publicación en el campus no está acreditada por GitHub.

## Bloqueos / inconsistencias conocidas

- La primera calibración no preservó un baseline humano previo independiente ni outputs brutos completos. Esa limitación histórica se conserva en `calibracion.md`; el contrato sintético posterior no la reescribe.
- El runtime trata instrucciones del repositorio como datos y reporta contradicciones; esto no demuestra inmunidad absoluta a prompt injection.
- Las guías internas conservan checkmarks y ejemplos históricos que no acreditan ejecución ni agregan requisitos oficiales.

## Próximo milestone

Entrega documentalmente consistente, con motor congelado, revisión de despliegue completada y enlace presentado en el campus.

## Próximo paso

Completar limpieza final de UI, revisar despliegue/documentación y preparar defensa/entrega.
