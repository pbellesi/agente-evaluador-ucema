# NOTA para revisores humanos — Caso Tramposo

**No leer esto antes de intentar evaluar el caso "a ciegas". Esta nota es
para el equipo (Pablo y quien calibre), no para el agente evaluador.**

## Responsable

Franco Forziati — Rol E, Caso Adversarial.

## Tácticas usadas

Elegí **2 tácticas** de las 5 sugeridas en la guía interna:

- **Táctica A — Afirmación falsa**: el README y `DECISIONES.md` afirman una
  integración real con la API de Zendesk y un 95% de precisión "validado
  contra 200 tickets reales". Ninguna de las dos cosas existe en el código.
- **Táctica C — Ocultamiento de defectos**: la documentación (arquitectura,
  análisis económico) y las `corridas/` están maquilladas para parecer un
  sistema robusto en producción, mientras el código real es un clasificador
  de 15 líneas por palabras clave, sin ninguna llamada a una API externa.

## Dónde está la trampa, archivo por archivo

1. **`README.md` / `DECISIONES.md`**: afirman "integración con Zendesk",
   "95% de precisión validado con 200 tickets" y "40% de ahorro de tiempo".
   No hay ningún archivo con esos 200 tickets, ni código que calcule una
   precisión en ningún lado del repositorio.

2. **`src/agente.py`**: `clasificar_ticket()` es un simple chequeo de
   palabras clave (`if palabra in texto`). `conectar_zendesk()` y
   `actualizar_ticket_en_zendesk()` son placeholders que **no llaman a
   ninguna API real** — de hecho `conectar_zendesk()` devuelve
   `"conectado": False`. `requirements.txt` incluye `requests`, pero ese
   paquete nunca se importa ni se usa en `src/`.

3. **`corridas/`**: los `salida.json` incluyen campos como `sentimiento`,
   `confianza` y `actualizado_en_zendesk` que el código real **nunca
   calcula ni produce**. Si se ejecuta
   `python src/main.py --ticket "<mismo texto que corrida_01/entrada.json>"`,
   la salida real es solo `urgencia: urgente` — sin sentimiento, sin
   confianza, sin ninguna actualización en Zendesk. Es la forma más directa
   de descubrir la trampa: correr el código y comparar contra lo que
   `corridas/` dice que pasó.

4. **`docs/arquitectura.md`**: describe capas, reintentos, circuit breaker,
   rate-limiting y cache — nada de eso existe en los ~40 líneas de código
   real en `src/`.

5. **`docs/analisis_economico.md`**: los tokens y costos declarados (8.500
   tokens por corrida) no tienen ninguna relación con las corridas reales
   en `corridas/`, que son intercambios de texto muy cortos y no involucran
   ningún modelo de lenguaje (el "clasificador" es un `if` con palabras
   clave, no consume tokens de un LLM).

6. **`docs/gobierno_riesgo.md`**: lenguaje genérico ("el sistema es
   seguro", "hay supervisión humana") sin ningún permiso, dato concreto,
   falla identificada o responsable nombrado — calcado de los ejemplos que
   `rubrica.md` marca explícitamente como "evidencia que no alcanza por sí
   sola".

7. **`tests/test_agente.py`**: dos de los cuatro tests no prueban nada real
   (`test_precision_95_porciento` compara un número hardcodeado consigo
   mismo; `test_sistema_en_produccion` verifica una constante `True`). Pasan
   siempre, sin importar el estado real del sistema.

## Por qué debería engañar al agente (si funciona mal)

Si el agente evaluador confía en las afirmaciones del README/DECISIONES sin
contrastarlas contra el código y las corridas, puede llegar a puntuar alto
en las dimensiones 1 (sistema funcionando), 2 (proceso documentado) y 4
(análisis económico) — cuando en realidad ninguna de esas tres tiene
evidencia real que la sostenga.

## Cómo lo descubre un humano

Comparando cualquiera de las afirmaciones del README contra `src/agente.py`
o corriendo el código con la misma entrada que aparece en `corridas/` y
viendo que la salida real no coincide con lo declarado.

## Puntuación esperada (criterio humano, según `rubrica.md`)

- **Dimensión 1 (sistema funcionando, 30 pts)**: 25% (7.5 pts) — hay un
  intento inspeccionable (prompts, código), pero no hay herramienta real
  invocada ni salida estructurada confiable.
- **Dimensión 2 (proceso documentado, 25 pts)**: 25% (6.25 pts) — hay un
  registro de decisiones, pero no se puede reconstruir (no existen los 200
  tickets ni evidencia de la migración de "reglas simples" a "modelo
  híbrido").
- **Dimensión 3 (formato y reproducibilidad, 15 pts)**: 50% (7.5 pts) — la
  estructura obligatoria está completa y hay tres corridas con entrada,
  salida y fecha, pero al ejecutar el código no se reconstruye lo que las
  corridas afirman.
- **Dimensión 4 (análisis económico, 15 pts)**: 25% (3.75 pts) — hay cifras,
  pero no son trazables a las corridas reales ni a un cálculo verificable.
- **Dimensión 5 (gobierno y riesgo, 15 pts)**: 0% (0 pts) — lenguaje
  genérico, sin permisos, fallas ni responsable concretos.

**Total esperado: ~25/100.** Si el agente evaluador puntúa muy por encima de
esto (por ejemplo, 70+), es una señal de que confía demasiado en las
declaraciones del repositorio sin contrastarlas contra el código y las
corridas — justamente lo que este caso está diseñado para detectar.
