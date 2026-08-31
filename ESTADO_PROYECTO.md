# Estado del Proyecto

## Fecha de actualización

31 de agosto de 2026.

## Fase actual

Fase 2 — Rúbrica ejecutable v1: repositorio remoto GitHub conectado, primer commit realizado, y `rubrica.md` v1 (trabajo final) en revisión vía Pull Request.

## Equipo y responsables

| Rol | Responsable | Alcance principal |
|---|---|---|
| A | Pablo Bellesi | Coordinación |
| B | Diego Mendez | Integración técnica |
| C | Franco Gambini | Rúbrica ejecutable |
| D | Sofia Mapelli | Casos excelente y flojo |
| E | Franco Forziati | Caso adversarial / tramposo |
| F | Melisa Clark | Calibración y QA |

## Completado

- Estructura base de carpetas creada.
- Fuentes oficiales cargadas en `00_fuentes/consigna/`.
- Material docente cargado en `00_fuentes/docente/`.
- Documentos internos cargados en `00_fuentes/equipo/`.
- Roles normalizados en la documentación interna.
- `AGENTS.md` creado y vigente.
- `DECISIONES.md` y README mínimo completados.
- `.gitignore` creado.
- Git local inicializado en la rama `main`; repositorio remoto GitHub conectado y primer commit realizado.
- Estructura mínima versionable creada: `calibracion.md` inicial y README mínimos en `agente/`, los tres casos y `docs/`.
- `rubrica.md` v1 (rúbrica del trabajo final, 30-25-15-15-15) redactada en la rama `feature/rubrica-v1` (Rol C), con evidencia observable por dimensión y ambigüedades documentadas para revisión humana (ver DEC-008). Pull Request #6 abierto hacia `main`, sin mergear.

## En curso

- Revisión humana del grupo sobre el Pull Request #6 (`rubrica.md` v1) y sobre las ambigüedades registradas en su sección 6.

## Pendiente inmediato

- Revisar y, si corresponde, aprobar/mergear el PR #6.
- Iniciar Rol B (agente corrector) usando `rubrica.md` v1 como base.
- Iniciar Rol D/E (casos de prueba excelente, flojo, tramposo).

## Bloqueos / inconsistencias conocidas

- Checkmarks prematuros en documentación interna que no reflejan archivos reales.
- Escalas de ejemplo inconsistentes en la guía interna de calibración.
- Referencia a un archivo PDF inexistente en el plan interno.
- Separación pendiente entre ejemplos internos y requisitos oficiales.

## Próximo milestone

Repositorio base publicado correctamente en GitHub, con reglas, estado, decisiones y estructura mínima consistente.

## Próximo paso

Revisar el PR #6 en grupo y, si se aprueba, arrancar la construcción del agente corrector (Rol B) sobre `rubrica.md` v1.
