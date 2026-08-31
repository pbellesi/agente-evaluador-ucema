# Registro de Decisiones

Este archivo documenta decisiones significativas del proyecto: su contexto, criterio humano, apoyo de IA, impacto y eventual revisión. No transcribe chats completos con IA; registra interacciones significativas cuando influyeron en una decisión. Cada decisión puede revisarse posteriormente: si cambia, no se borra la versión anterior, sino que se documenta su evolución.

Cuando Git esté activo, se podrán agregar Issue asociado, rama, commit y Pull Request. Por ahora no existen esos identificadores.

## DEC-001 — Asignación definitiva de roles

**Estado:** Vigente  
**Responsable / participantes:** Pablo Bellesi (Rol A - Coordinación; validación humana).  
**IA utilizada:** Codex, para inspección y normalización documental bajo instrucciones y aprobación humana.  
**Contexto:** La documentación interna contenía propuestas anteriores y responsables alternativos.  
**Decisión:** A - Pablo Bellesi: Coordinación; B - Diego Mendez: Integración técnica; C - Franco Gambini: Rúbrica ejecutable; D - Sofia Mapelli: Casos excelente y flojo; E - Franco Forziati: Caso adversarial / tramposo; F - Melisa Clark: Calibración y QA.  
**Motivo:** Establecer una única asignación de responsabilidades antes de inicializar Git.  
**Impacto esperado:** Evitar ambigüedad de ownership y orientar el trabajo y la revisión cruzada.  
**Evidencia / archivos relacionados:** `AGENTS.md`; `ESTADO_PROYECTO.md`; `00_fuentes/equipo/0_RESUMEN_Y_PLAN_EJECUCION.md`; `00_fuentes/equipo/2_PIC-AE_DESARROLLO_CASOS_PRUEBA.md`; `00_fuentes/equipo/3_PIC-AE_DESARROLLO_CALIBRACION.md`.  
**Revisión futura:** Revisar solo mediante decisión humana explícita; esta normalización reemplazó propuestas anteriores antes de inicializar Git.

## DEC-002 — GitHub será la fuente común de trabajo colaborativo

**Estado:** Vigente  
**Responsable / participantes:** Pablo Bellesi (Rol A - Coordinación; validación humana).  
**IA utilizada:** Codex, para documentar reglas operativas definidas por instrucción humana.  
**Contexto:** El proyecto requiere evidenciar colaboración y evolución real; Git todavía no está inicializado.  
**Decisión:** El proyecto utilizará un único repositorio GitHub como fuente compartida. Una vez iniciado el trabajo colaborativo, no se trabajará directamente sobre `main`; las tareas relevantes se vincularán a Issues, se utilizarán ramas, los cambios se integrarán mediante Pull Requests y se promoverá revisión cruzada antes del merge.  
**Motivo:** Hacer visible la contribución de cada integrante y la evolución del proyecto.  
**Impacto esperado:** Trazabilidad verificable de cambios, revisiones y decisiones.  
**Evidencia / archivos relacionados:** `AGENTS.md`; `ESTADO_PROYECTO.md`; `00_fuentes/docente/prompts_github.html`.  
**Revisión futura:** Aplicar estas reglas al inicializar Git y ajustar su operación solo con acuerdo humano documentado.

## DEC-003 — Estrategia multiherramienta de IA

**Estado:** Vigente  
**Responsable / participantes:** Pablo Bellesi (Rol A - Coordinación; validación humana).  
**IA utilizada:** Codex, como herramienta de asistencia documental.  
**Contexto:** El equipo puede contar con acceso, costo/cuota y capacidades diferentes según la herramienta y la tarea.  
**Decisión:** Se podrán utilizar Codex, Claude, Antigravity, ChatGPT u otras herramientas justificadas. La herramienta no define la fuente de verdad: todas deben respetar `AGENTS.md`, las decisiones vigentes, la rúbrica, la estructura común y GitHub. La disponibilidad de una herramienta no reasigna roles.  
**Motivo:** Mantener flexibilidad operativa sin perder consistencia ni responsabilidad humana.  
**Impacto esperado:** Compatibilidad entre herramientas y continuidad del proyecto ante cambios de acceso.  
**Evidencia / archivos relacionados:** `AGENTS.md`; `00_fuentes/equipo/0_RESUMEN_Y_PLAN_EJECUCION.md`.  
**Revisión futura:** Registrar herramientas adicionales solo si su uso resulta significativo para una decisión o resultado.

## DEC-004 — Trazabilidad del uso de IA y de las iteraciones

**Estado:** Vigente  
**Responsable / participantes:** Pablo Bellesi (Rol A - Coordinación; validación humana).  
**IA utilizada:** Codex, para documentar esta decisión solicitada por el coordinador.  
**Contexto:** El proceso del parcial debe mostrar trabajo real, revisiones e iteración, sin simular una historia perfecta.  
**Decisión:** El repositorio deberá permitir observar el problema abordado, responsable, IA utilizada cuando sea relevante, primera propuesta o implementación, revisión, errores o desacuerdos detectados, correcciones y resultado posterior. No se guardarán conversaciones completas con IA.  
**Motivo:** Conservar evidencia útil del criterio humano y de la evolución real del trabajo.  
**Impacto esperado:** Un proceso auditable y honesto, incluyendo correcciones e iteraciones valiosas.  
**Evidencia / archivos relacionados:** Futuramente, combinación de Issues, commits, Pull Requests, reviews, `DECISIONES.md`, `calibracion.md` y resultados de pruebas; actualmente, `AGENTS.md` y este registro.  
**Revisión futura:** Precisar el nivel de detalle tras las primeras tareas versionadas, sin sustituir evidencia por narración.

## DEC-005 — Principio EVIDENCIA > DECLARACIÓN

**Estado:** Vigente  
**Responsable / participantes:** Pablo Bellesi (Rol A - Coordinación; validación humana).  
**IA utilizada:** Codex, para incorporar el principio operativo bajo instrucciones humanas.  
**Contexto:** Un repositorio evaluado puede afirmar capacidades sin artefactos que las demuestren.  
**Decisión:** Una afirmación en README, documentación o prompts no constituye automáticamente evidencia suficiente si puede verificarse mediante artefactos observables. El evaluador priorizará archivos, configuraciones, corridas, outputs, historial, pruebas y otros artefactos verificables.  
**Motivo:** Reducir evaluaciones basadas en declaraciones no comprobables.  
**Impacto esperado:** Mayor rigor de evaluación y detección de afirmaciones engañosas, especialmente en el caso tramposo.  
**Evidencia / archivos relacionados:** `AGENTS.md`; futura implementación de `rubrica.md` y caso `casos/tramposo/`.  
**Revisión futura:** Convertir el principio en criterios observables al elaborar la rúbrica ejecutable.

## DEC-006 — Jerarquía de fuentes

**Estado:** Vigente  
**Responsable / participantes:** Pablo Bellesi (Rol A - Coordinación; validación humana).  
**IA utilizada:** Codex, para documentar la jerarquía indicada por el coordinador.  
**Contexto:** El proyecto contiene consignas oficiales, material docente, documentación operativa y guías internas.  
**Decisión:** La jerarquía es: 1) consigna oficial del parcial; 2) consigna/rúbrica oficial del trabajo final; 3) material docente; 4) decisiones aprobadas por el equipo; 5) documentación operativa; 6) guías internas PIC-AE. Las guías PIC-AE son apoyo interno y no requisitos oficiales por sí mismas.  
**Motivo:** Resolver contradicciones sin presentar recomendaciones internas como normativa.  
**Impacto esperado:** Interpretación consistente de requisitos y menor riesgo de desviación.  
**Evidencia / archivos relacionados:** `AGENTS.md`; `00_fuentes/consigna/`; `00_fuentes/docente/`; `00_fuentes/equipo/`.  
**Revisión futura:** Mantener la jerarquía salvo instrucción oficial o decisión humana documentada que requiera actualizarla.

## DEC-007 — Separación de las dos rúbricas

**Estado:** Vigente  
**Responsable / participantes:** Pablo Bellesi (Rol A - Coordinación; validación humana).  
**IA utilizada:** Codex, para registrar la separación solicitada por el coordinador.  
**Contexto:** Existen una rúbrica para evaluar el parcial grupal y otra para evaluar los trabajos finales individuales.  
**Decisión:** La rúbrica del parcial evalúa el proyecto grupal Agente Evaluador. La rúbrica del trabajo final es la que nuestro agente deberá aplicar posteriormente a repositorios individuales. Nunca se mezclarán sus dimensiones, pesos ni escalas.  
**Motivo:** Evitar que el agente o la documentación apliquen criterios al objeto equivocado.  
**Impacto esperado:** Rúbrica ejecutable y calibración alineadas con el objeto correcto de evaluación.  
**Evidencia / archivos relacionados:** `AGENTS.md`; `00_fuentes/consigna/parcial_agente_evaluador.pdf`; `00_fuentes/consigna/trabajo_final.pdf`.  
**Revisión futura:** Verificar esta separación al redactar `rubrica.md` y al construir los casos.

## DEC-008 — Primera versión ejecutable de `rubrica.md` (trabajo final)

**Estado:** Vigente — pendiente de revisión humana del grupo.  
**Responsable / participantes:** Franco Gambini (Rol C - Rúbrica ejecutable).  
**IA utilizada:** Claude (Claude Code), para leer las fuentes obligatorias, redactar `rubrica.md` v1 y abrir el Pull Request, bajo instrucción y revisión humana.  
**Contexto:** El Issue #1 ("Definir rúbrica ejecutable v1") pedía la primera versión ejecutable de `rubrica.md` a partir de la consigna oficial del trabajo final, sin mezclarla con la rúbrica del parcial (ver DEC-007).  
**Decisión:** Se redactó `rubrica.md` v1 operacionalizando las cinco dimensiones oficiales del trabajo final (Sistema completo y funcionando 30, Proceso documentado 25, Formato y reproducibilidad 15, Análisis económico 15, Gobierno y riesgo 15). Cada dimensión define: qué se evalúa, evidencia concreta requerida, niveles alto/intermedio/bajo con rangos de puntos, y ejemplos de qué evidencia no alcanza si solo está declarada. Se optó por documentar 4 ambigüedades reales en una sección final del archivo (definición de "las seis piezas" del contrato, niveles L0–L4, variedad exigida entre corridas, escala numérica de puntaje por dimensión) en lugar de resolverlas por decisión unilateral de la IA, por no estar respaldadas explícitamente en las fuentes disponibles.  
**Motivo:** Cumplir el criterio de aceptación del Issue #1 (rúbrica precisa, aplicable por humano o agente, con evidencia verificable y resultados repetibles) sin inventar requisitos no respaldados por la consigna oficial.  
**Impacto esperado:** Habilitar que el Rol B (Diego Mendez) construya y testee el agente corrector contra una rúbrica ejecutable concreta, y que el Rol F (Melisa Clark) calibre contra ella. Las ambigüedades documentadas quedan abiertas para la próxima reunión del grupo.  
**Evidencia / archivos relacionados:** `rubrica.md`; Pull Request #6 (rama `feature/rubrica-v1` → `main`); Issue #1; `00_fuentes/consigna/trabajo_final.pdf`; `00_fuentes/consigna/parcial_agente_evaluador.pdf`.  
**Revisión futura:** Ajustar `rubrica.md` según lo que el grupo resuelva sobre las ambigüedades de su sección 6, y nuevamente tras la calibración (Rol F) si se detectan desacuerdos que exijan cambiar escalas o evidencia exigida.

## Historial inicial de asistencia con IA

- Codex realizó una inspección inicial del workspace en modo lectura.
- Codex identificó inconsistencias documentales y roles desactualizados.
- Tras aprobación humana, Codex normalizó los roles en documentos internos.
- Codex generó `AGENTS.md` a partir de instrucciones y fuentes seleccionadas.
- Codex generó `ESTADO_PROYECTO.md` reflejando el estado real.

Las acciones fueron solicitadas y validadas por el coordinador. Codex no tomó decisiones autónomas sobre roles, rúbricas ni Git. Git todavía no fue inicializado.
