import sys
import types
import unittest


if "requests" not in sys.modules:
    requests_stub = types.ModuleType("requests")
    requests_stub.get = lambda *args, **kwargs: (_ for _ in ()).throw(
        AssertionError("La prueba unitaria no debe usar red")
    )
    sys.modules["requests"] = requests_stub


from src.deterministic_evaluator import evaluate_repository_deterministically
from src.github_fetcher import classify_path


def evaluate(contents):
    return evaluate_repository_deterministically({
        "repository": "synthetic/acceptance",
        "evaluated_revision": "synthetic@fixed",
        "repository_inventory": [
            classify_path(path, len(content.encode("utf-8")))
            for path, content in contents.items()
        ],
        "file_contents": contents,
    })


def level(contents, dimension_index):
    return evaluate(contents).dimensions[dimension_index].level_percent


def structure():
    return {
        "README.md": "Proyecto sintético.",
        "DECISIONES.md": "# DECISIONES\nRegistro inspeccionable.",
        "prompts/system_prompt.md": "Rol del agente. Instrucciones para procesar una solicitud concreta. " * 3,
        "prompts/user_prompt.md": "Usuario: procesar la solicitud con salida JSON. " * 3,
    }


def real_code():
    return 'async function run() { return await fetch("https://api.example.test/v1/run"); }'


def add_complete_run(contents, run, input_name="input.json", output_name="output.json"):
    contents[f"corridas/{run}/{input_name}"] = '{"case":"synthetic"}'
    contents[f"corridas/{run}/{output_name}"] = '{"result":"ok"}'
    contents[f"corridas/{run}/metadata.json"] = '{"startedAt":"2026-01-01T10:00:00Z"}'
    return contents


class AcceptanceMatrixTests(unittest.TestCase):
    # D1
    def test_d1_03_sdk_instantiated_without_invocation_is_25(self):
        self.assertEqual(level({"src/agent.ts": 'import OpenAI from "openai"; const client = new OpenAI();'}, 0), 25)

    def test_d1_04_openai_responses_execution_without_supervision_is_75(self):
        contents = structure()
        contents["src/agent.ts"] = 'import OpenAI from "openai"; const client = new OpenAI(); await client.responses.create({input:"x"});'
        add_complete_run(contents, "one")
        self.assertEqual(level(contents, 0), 75)

    def test_d1_09_dummy_main_flow_is_25(self):
        contents = structure()
        contents["src/agent.ts"] = 'const api = "API placeholder"; const client = new OpenAI(); await client.responses.create({});'
        add_complete_run(contents, "one")
        self.assertEqual(level(contents, 0), 25)

    # D2
    def test_d2_02_one_substantive_decision_is_50(self):
        contents = structure()
        contents["DECISIONES.md"] = "## Decisión 1\nContexto: salida inválida. Cambio: se agregó validación. Impacto: evita publicar resultados erróneos."
        self.assertEqual(level(contents, 1), 50)

    def test_d2_06_substantive_table_row_is_50(self):
        contents = structure()
        contents["DECISIONES.md"] = "| Cambio | Motivo |\n| --- | --- |\n| Se agregó validación de esquema | Evita aceptar resultados incompletos. |"
        self.assertEqual(level(contents, 1), 50)

    def test_d2_07_duplicate_table_and_section_count_once_but_is_50(self):
        contents = structure()
        contents["DECISIONES.md"] = """| Cambio | Motivo |
| --- | --- |
| Se agregó validación de esquema de salida | Evita aceptar salidas incompletas. |
## Iteración 1
Problema: se aceptaban salidas incompletas. Cambio: se agregó validación de esquema de salida. Impacto: evita aceptar salidas incompletas.
"""
        self.assertEqual(level(contents, 1), 50)

    def test_d2_08_empty_decision_headers_are_25(self):
        contents = structure()
        contents["DECISIONES.md"] = "\n".join(f"## Decisión {index}" for index in range(1, 21))
        self.assertEqual(level(contents, 1), 25)

    def test_d2_04_complete_coherent_history_is_100(self):
        contents = structure()
        contents["DECISIONES.md"] = """## Decisión inicial
Contexto: el primer prompt omitía campos obligatorios. Cambio: se definió un esquema JSON. Impacto: permite validar las salidas. Evidencia: prompts/system_prompt.md.
## Iteración de corrección
Problema: la primera corrida falló por fecha ausente. Cambio: se agregó metadata. Motivo: asegurar trazabilidad. Resultado: corridas/run-2/metadata.json.
## Cambio de alcance
Contexto: se descartó una integración no verificable. Decisión: se adoptó fetch real. Motivo: conservar evidencia observable. Impacto: src/agent.ts y corridas/run-3/output.json.
"""
        contents["src/agent.ts"] = real_code()
        for run in ("run-1", "run-2", "run-3"):
            add_complete_run(contents, run)
        self.assertEqual(level(contents, 1), 100)

    def test_d2_11_multiple_decisions_without_links_or_corrections_are_75(self):
        contents = structure()
        contents["DECISIONES.md"] = """## Decisión 1
Contexto: salida inválida. Cambio: se agregó validación. Impacto: evita errores.
## Decisión 2
Problema: faltaban campos. Cambio: se definió un esquema. Motivo: mejorar consistencia.
## Decisión 3
Contexto: formato ambiguo. Cambio: se adoptó JSON. Impacto: facilita revisión.
## Decisión 4
Problema: respuesta extensa. Cambio: se redujo el prompt. Resultado: menor complejidad.
"""
        self.assertEqual(level(contents, 1), 75)

    def test_d2_12_decisions_and_partial_links_without_complete_history_are_75(self):
        contents = structure()
        contents["src/agent.ts"] = real_code()
        contents["DECISIONES.md"] = """## Decisión 1
Contexto: salida inválida. Cambio: se agregó validación en src/agent.ts. Impacto: evita errores.
## Decisión 2
Problema: faltaban campos. Cambio: se definió el esquema en prompts/system_prompt.md. Motivo: mejorar consistencia.
## Decisión 3
Contexto: formato ambiguo. Cambio: se adoptó JSON. Impacto: facilita revisión.
## Decisión 4
Problema: respuesta extensa. Cambio: se redujo el prompt. Resultado: menor complejidad.
"""
        self.assertEqual(level(contents, 1), 75)

    def test_d2_13_complete_history_with_links_iterations_and_scope_is_100(self):
        contents = structure()
        contents["src/agent.ts"] = real_code()
        for run in ("run-1", "run-2", "run-3"):
            add_complete_run(contents, run)
        contents["DECISIONES.md"] = """## Decisión inicial
Contexto: el primer prompt omitía campos obligatorios. Cambio: se definió un esquema JSON en prompts/system_prompt.md. Impacto: permite validar las salidas.
## Iteración de corrección
Problema: la corrida run-1 falló por fecha ausente. Cambio: se agregó metadata en corridas/run-2/metadata.json. Motivo: asegurar trazabilidad. Resultado: la corrección preserva la fecha.
## Cambio de alcance
Contexto: se descartó una integración no verificable. Decisión: se adoptó fetch real en src/agent.ts. Motivo: conservar evidencia observable. Impacto: la salida de corridas/run-3/output.json puede contrastarse.
## Consecuencia posterior
Problema: el formato impedía revisión. Cambio: se actualizó prompts/user_prompt.md. Impacto: la revisión humana es más verificable y el alcance queda documentado.
"""
        self.assertEqual(level(contents, 1), 100)

    # D3
    def test_d3_02_one_complete_run_is_50(self):
        contents = structure()
        add_complete_run(contents, "one")
        self.assertEqual(level(contents, 2), 50)

    def test_d3_04_three_directory_triads_are_100(self):
        contents = structure()
        for run in ("one", "two", "three"):
            add_complete_run(contents, run)
        self.assertEqual(level(contents, 2), 100)

    def test_d3_06_raw_output_with_explicit_input_reference_is_100(self):
        contents = structure()
        for number in ("001", "002", "003"):
            contents[f"prompts/casos/solicitud_{number}.md"] = "entrada concreta"
            contents[f"corridas/raw/raw_{number}.md"] = (
                f"Caso: solicitud_{number}.md\nFecha: 2026-01-01T10:00:00Z\nSalida completa del agente: resultado verificable. " * 4
            )
        self.assertEqual(level(contents, 2), 100)

    def test_d3_08_mixed_runs_do_not_form_a_reconstructible_run(self):
        contents = structure()
        contents["corridas/a/input.json"] = '{"case":"a"}'
        contents["corridas/b/output.json"] = '{"result":"b"}'
        contents["corridas/c/metadata.json"] = '{"startedAt":"2026-01-01T10:00:00Z"}'
        self.assertEqual(level(contents, 2), 25)

    def test_d3_09_three_runs_with_one_ambiguous_link_are_75(self):
        contents = structure()
        add_complete_run(contents, "one")
        add_complete_run(contents, "two")
        contents["corridas/three/input.json"] = '{"case":"three"}'
        contents["corridas/three/metadata.json"] = '{"startedAt":"2026-01-01T10:00:00Z"}'
        contents["corridas/shared_result.json"] = '{"result":"unknown input"}'
        self.assertEqual(level(contents, 2), 75)

    # D4
    def test_d4_04_tokens_tariff_and_cost_per_run_are_50(self):
        contents = structure()
        contents["src/agent.ts"] = real_code()
        contents["docs/analisis_economico.md"] = "Modelo: gpt-test. Tokens de entrada: 1000. Tokens de salida: 200. Tarifa: USD 0.01 por 1000 tokens. Costo por corrida: USD 0.012."
        self.assertEqual(level(contents, 3), 50)

    def test_d4_05_estimated_cost_projections_and_model_are_75(self):
        contents = structure()
        contents["src/agent.ts"] = real_code()
        contents["docs/analisis_economico.md"] = "Modelo: gpt-test elegido por costo. Estimación: Tokens de entrada: 1000. Tokens de salida: 200. Tarifa: USD 0.01 por 1000 tokens. Costo por corrida: USD 0.012. Proyección semanal: USD 1. Proyección anual: USD 52."
        self.assertEqual(level(contents, 3), 75)

    def test_d4_06_metadata_backed_economics_are_100(self):
        contents = structure()
        contents["src/agent.ts"] = real_code()
        for run in ("one", "two", "three"):
            add_complete_run(contents, run)
            contents[f"corridas/{run}/metadata.json"] = '{"model":"gpt-test","prompt_tokens":1000,"completion_tokens":200,"cost_usd":0.012,"startedAt":"2026-01-01T10:00:00Z"}'
        contents["docs/analisis_economico.md"] = "Modelo: gpt-test, el más chico adecuado por calidad observada. Tarifa: USD 0.01 por 1000 tokens. Costo por corrida: USD 0.012. Proyección semanal: USD 1 con 80 corridas. Proyección anual: USD 52 con el mismo supuesto."
        self.assertEqual(level(contents, 3), 100)

    def test_d4_09_unrelated_tokens_table_is_0(self):
        contents = structure()
        contents["docs/analisis_economico.md"] = "| Tokens | Ingresos financieros |\n| --- | --- |\n| 5000 | USD 9000 |"
        self.assertEqual(level(contents, 3), 0)

    # D5
    def test_d5_02_generic_controls_are_25(self):
        contents = structure()
        contents["docs/gobierno_riesgo.md"] = "Existe riesgo, pero el sistema será seguro."
        self.assertEqual(level(contents, 4), 25)

    def test_d5_05_five_axes_with_non_operational_review_are_75(self):
        contents = structure()
        contents["docs/gobierno_riesgo.md"] = "Datos y permisos de acceso. Riesgo de falla con consecuencia. Respuesta: mitigar. Supervisión humana. Responsable: equipo."
        self.assertEqual(level(contents, 4), 75)

    def test_d5_06_specific_operational_governance_is_100(self):
        contents = structure()
        contents["docs/gobierno_riesgo.md"] = "El agente accede sólo en lectura a datos de tickets mediante permiso restringido. Si falla la clasificación, puede priorizar mal un ticket; respuesta: bloquear envío y abrir revisión. Una persona revisa cada prioridad antes de publicar. Responsable final y firma: Analista de guardia."
        self.assertEqual(level(contents, 4), 100)


if __name__ == "__main__":
    unittest.main()
