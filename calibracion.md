# Calibración del agente evaluador

## Metodología

La calibración se realizó sobre `main` en la revisión `ab319c6103a52391b5f3ff5cea31b4f0c40fb02d`, con `rubrica.md` V2 como fuente autoritativa y los casos `casos/excelente/`, `casos/flojo/` y `casos/tramposo/` como repositorios objetivo separados.

El orden de trabajo fue el siguiente:

1. Se inspeccionaron la rúbrica completa, el árbol y el contenido de cada caso, el código, los prompts, las corridas, la documentación y el historial Git pertinente.
2. Se cerró y registró la evaluación humana de los tres casos antes de ejecutar el agente corrector. Para cada dimensión se recorrieron los niveles desde 100% hacia 0% y se eligió el nivel más alto completamente demostrado.
3. Después se ejecutó el corrector v1 cargando `agente/system_prompt.md` como instrucciones, `rubrica.md` V2 como rúbrica autoritativa y cada carpeta de caso como repositorio objetivo. La ejecución se hizo en Codex el 2 de septiembre de 2026; la interfaz no expuso un identificador de modelo más específico.
4. Como comprobaciones auxiliares se ejecutaron los comandos documentados de los tres casos y se contrastaron las salidas guardadas con la implementación. Los comandos de Excelente, Flojo y Tramposo se ejecutaron. No se pudieron ejecutar los tests porque `pytest` no está instalado en el entorno; sus aserciones sí fueron inspeccionadas directamente.
5. Los puntajes humanos no se modificaron después de conocer los puntajes del agente.

Los valores entre paréntesis siguen el orden oficial: Sistema completo y funcionando / Proceso documentado / Formato y reproducibilidad / Análisis económico / Gobierno y riesgo.

## Caso excelente

### Evaluación humana

| Dimensión | Nivel | Puntaje | Evidencia y criterio |
|---|---:|---:|---|
| Sistema completo y funcionando | 100% | 30 | `README.md` identifica el caso de una ALyC; `prompts/system_prompt.md` y `prompts/user_prompt.md` definen contrato, herramienta, JSON y L2; `src/agente.py` implementa lectura y validación; las tres carpetas de `corridas/` conservan resultado de herramienta y salida estructurada; `docs/gobierno_riesgo.md` define revisión y firma. |
| Proceso documentado | 75% | 18,75 | `DECISIONES.md` identifica la salida inicial inconsistente, el cambio a JSON, el abandono de navegación en vivo y el reemplazo del clasificador determinístico por una invocación real a IA. El historial del caso tiene un único commit (`ba10117`), por lo que las versiones iniciales y parte de la correspondencia histórica no pueden verificarse. |
| Formato y reproducibilidad | 100% | 15 | Están `README.md`, ambos prompts, `DECISIONES.md` y tres corridas. Cada corrida conserva `entrada.json`, `resultado_herramienta.json`, `fecha.txt`, `metadata.json` y `salida.json`. Los hashes de prompts de `metadata.json` coinciden con los archivos actuales. |
| Análisis económico | 25% | 3,75 | `docs/analisis_economico.md` y los tres `metadata.json` documentan honestamente que modelo exacto, tokens, tarifa y costo no fueron expuestos. Hay proyección de volumen semanal y anual, pero no puede obtenerse costo por corrida. |
| Gobierno y riesgo | 100% | 15 | `docs/gobierno_riesgo.md` especifica recursos, permisos, límites, fallas, consecuencias, respuestas y revisión. `README.md`, `DECISIONES.md` y el prompt coinciden en L2, analista revisora y Responsable de Cumplimiento firmante. |
| **Total humano** |  | **82,5** |  |

### Evaluación del agente

El corrector asignó los mismos niveles: **30 / 18,75 / 15 / 3,75 / 15**, total **82,5**. Citó como evidencia principal los prompts, `src/agente.py`, las tres corridas con metadatos, `DECISIONES.md`, `docs/analisis_economico.md` y `docs/gobierno_riesgo.md`. Para el nivel siguiente de Proceso indicó que faltan versiones o historial que permitan contrastar las iteraciones; para Economía indicó que faltan tokens, modelo, tarifa y costo reproducible.

### Diferencias

La diferencia total es **0 puntos**. No existen cambios de nivel por dimensión.

### Análisis

La coincidencia es razonable y no fue forzada. El nombre “excelente” no implica 100 puntos: la ausencia deliberadamente documentada de métricas económicas limita Economía a 25%, y la falta de versiones históricas observables limita Proceso a 75%.

## Caso flojo

### Evaluación humana

| Dimensión | Nivel | Puntaje | Evidencia y criterio |
|---|---:|---:|---|
| Sistema completo y funcionando | 25% | 7,5 | `src/main.py` es un clasificador determinístico por palabras clave; los prompts no participan en la ejecución, no hay modelo ni conector real y la salida es texto libre. Existe un intento inspeccionable, pero no una ejecución usable de un sistema agéntico con herramienta real y salida estructurada. |
| Proceso documentado | 25% | 6,25 | `DECISIONES.md` reconoce el recorte a palabras clave y una mejora futura, pero no permite reconstruir la versión inicial, el problema observado, la modificación concreta y su correspondencia con artefactos. |
| Formato y reproducibilidad | 25% | 3,75 | Existen la estructura básica, una entrada y una salida relacionadas en `corridas/prueba/`, pero falta la fecha y no hay tres corridas completas. Ninguna corrida conserva conjuntamente entrada, salida y fecha. |
| Análisis económico | 0% | 0 | `docs/costos.md` sólo afirma que el sistema es económico; no hay tokens, modelo, tarifa, costo ni proyecciones verificables. |
| Gobierno y riesgo | 25% | 3,75 | `docs/riesgos.md` menciona error y revisión humana de forma genérica, sin sistemas, permisos, consecuencias operativas, momento de revisión ni responsable final. |
| **Total humano** |  | **21,25** |  |

### Evaluación del agente

El corrector asignó **15 / 6,25 / 3,75 / 0 / 3,75**, total **28,75**. Coincidió con la evaluación humana en cuatro dimensiones. En Sistema otorgó 50% porque la ejecución comprobada de `python src/main.py corridas/prueba/entrada.txt` procesa una entrada y devuelve un resultado parcial, aunque no usa los prompts, no invoca un modelo o conector y no produce salida estructurada.

### Diferencias

| Dimensión | Humano | Agente | Diferencia agente − humano |
|---|---:|---:|---:|
| Sistema completo y funcionando | 7,5 | 15 | +7,5 |
| Proceso documentado | 6,25 | 6,25 | 0 |
| Formato y reproducibilidad | 3,75 | 3,75 | 0 |
| Análisis económico | 0 | 0 | 0 |
| Gobierno y riesgo | 3,75 | 3,75 | 0 |
| **Total** | **21,25** | **28,75** | **+7,5** |

### Análisis

El desacuerdo no supera 10 puntos totales, pero sí cambia Sistema de 25% a 50%. La fila de 50% de `rubrica.md` admite que “el sistema procesa un caso real o invoca una herramienta real, pero falla o produce un resultado incompleto”. El corrector interpretó que el script local y su entrada satisfacen la primera alternativa. La evaluación humana exigió, por el objeto de la dimensión, evidencia de sistema agéntico o herramienta/conector real, que no aparece. Ambas lecturas pueden reconstruirse; la regla actual no resuelve inequívocamente si un script determinístico que sólo lee un archivo alcanza 50%.

## Caso tramposo

### Evaluación humana

| Dimensión | Nivel | Puntaje | Evidencia y criterio |
|---|---:|---:|---|
| Sistema completo y funcionando | 50% | 15 | `src/main.py` procesa texto y produce una clasificación parcial verificable. Sin embargo, `src/agente.py` declara que Zendesk es un placeholder sin llamada real; el ejecutable no usa el modelo, no calcula sentimiento o confianza y no produce el JSON guardado en `corridas/`. |
| Proceso documentado | 0% | 0 | `DECISIONES.md` declara API real, 95% validado, producción y reducción del 40%, pero el código y los tests lo contradicen. `test_precision_95_porciento` y `test_sistema_en_produccion` sólo comparan constantes; no existe una historia real reconstruible. |
| Formato y reproducibilidad | 25% | 3,75 | Están las piezas y tres conjuntos con entrada, salida y fecha, pero las salidas no pueden provenir de la implementación: el comando sólo imprime `urgencia: ...`. Son un intento estructural, no corridas reales reconstruibles. |
| Análisis económico | 25% | 3,75 | `docs/analisis_economico.md` aporta tokens totales, un costo y proyecciones, pero no separa entrada/salida, no identifica modelo ni tarifa y no los vincula con metadatos de corridas. El cálculo no es reproducible. |
| Gobierno y riesgo | 25% | 3,75 | `docs/gobierno_riesgo.md` contiene afirmaciones genéricas de seguridad, revisión y respuesta; no identifica permisos concretos, consecuencias, controles aplicables, momento de revisión ni firmante. |
| **Total humano** |  | **26,25** |  |

### Evaluación del agente

El corrector asignó **15 / 0 / 3,75 / 3,75 / 3,75**, total **26,25**. Registró como notas de integridad las contradicciones entre README/decisiones/documentación y código/tests: la conexión a Zendesk es un placeholder, las salidas JSON no son generadas por `main.py`, y los tests de 95% y producción sólo validan constantes.

### Diferencias

La diferencia total es **0 puntos**. No existen cambios de nivel por dimensión.

### Análisis

La coincidencia muestra que el corrector aplicó `EVIDENCIA > DECLARACIÓN` y no obedeció ni premió afirmaciones infladas. El 50% en Sistema reconoce únicamente el procesamiento local parcial comprobable; no valida la integración, el modelo, la precisión ni el despliegue declarados.

## Comparación global

La diferencia se calcula como **Agente − Humano**.

| Caso | Humano | Agente | Diferencia | Resultado |
|---|---:|---:|---:|---|
| Excelente | 82,5 | 82,5 | 0 | Coincidencia total |
| Flojo | 21,25 | 28,75 | +7,5 | Desacuerdo relevante en una dimensión; diferencia total dentro de ±10 |
| Tramposo | 26,25 | 26,25 | 0 | Coincidencia total y detección de contradicciones |

No hubo diferencias totales superiores a ±10 puntos. La diferencia absoluta media fue **2,5 puntos** y la diferencia absoluta máxima fue **7,5 puntos**.

## Desacuerdos relevantes

Se detectó un único cambio de nivel: Sistema del caso Flojo, humano 25% frente a agente 50%.

- **Problema:** el límite entre 25% y 50% no determina de manera inequívoca si “procesa un caso real” incluye un script determinístico que lee un archivo, sin modelo, conector ni herramienta agéntica real.
- **Evidencia:** `casos/flojo/src/main.py` procesa el texto con dos condiciones; `casos/flojo/prompts/` no participa en la ejecución; `corridas/prueba/salida.txt` coincide con el script, pero no es estructurada y carece de fecha.
- **Impacto:** diferencia de un nivel y 7,5 puntos en la dimensión de mayor peso. No cambia la lectura global del caso como insuficiente, pero reduce la repetibilidad entre evaluadores.
- **Ajuste recomendado:** consultar a Pablo para definir si el umbral de 50% requiere evidencia agéntica o herramienta/conector real, o si cualquier procesamiento ejecutable de un caso alcanza. Sólo después, y con decisión humana, ajustar `rubrica.md` o `agente/system_prompt.md` si corresponde.

También se observó una limitación operativa: el corrector v1 es un prompt y no un ejecutable con modelo y parámetros fijados. La corrida fue real y quedó identificada por fecha, revisión e interfaz, pero la interfaz no expuso un ID de modelo específico. Se recomienda que una futura versión conserve runner, modelo, parámetros y salida JSON cruda para mejorar la repetibilidad. Esta recomendación no cambia los puntajes actuales.

## Ajustes propuestos o realizados

No se realizó ningún ajuste a la rúbrica, al agente ni a los casos. Se propone únicamente consultar a Pablo sobre el umbral 25%/50% de Sistema y, en una iteración posterior autorizada, estandarizar los metadatos de ejecución del corrector.

## Resultado posterior a ajustes

No hubo ajustes ni una segunda ejecución. Los resultados posteriores son, por lo tanto, los mismos resultados reales iniciales: Excelente 82,5; Flojo 28,75; Tramposo 26,25 para el agente.

## Conclusión de calibración

El corrector coincide exactamente con la evaluación humana en dos de los tres casos y detecta las contradicciones del caso Tramposo. La única diferencia es trazable a una ambigüedad del umbral de Sistema en el caso Flojo; no se corrigió ni se ocultó. Con la evidencia actual no corresponde modificar otros archivos sin una decisión conceptual de Pablo.
