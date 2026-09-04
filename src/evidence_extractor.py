import os
import re
from typing import Dict, List, Any, Set


def extract_objective_evidence(repo_data: dict) -> dict:
    """
    Extrae evidencias objetivas y agnósticas del repositorio objetivo.
    Devuelve un diccionario estructurado con métricas de presencia,
    incompatibilidades y contradicciones verificables.
    """
    file_contents: Dict[str, str] = repo_data.get("file_contents", {})
    all_paths: Set[str] = set(file_contents.keys())

    # Normalización de paths a minúsculas para comparaciones agnósticas
    path_map = {p.lower(): p for p in all_paths}
    
    # -------------------------------------------------------------------------
    # 1. Inspección de Estructura Obligatoria
    # -------------------------------------------------------------------------
    has_readme = any("readme" in p for p in path_map)
    has_decisiones = any("decisiones" in p for p in path_map)
    has_prompts_dir = any("prompts/" in p for p in path_map)
    has_corridas_dir = any("corridas/" in p for p in path_map)
    
    mandatory_structure = {
        "readme": has_readme,
        "decisiones": has_decisiones,
        "prompts": has_prompts_dir,
        "corridas": has_corridas_dir,
        "is_complete": has_readme and has_decisiones and has_prompts_dir and has_corridas_dir
    }

    # -------------------------------------------------------------------------
    # 2. Análisis de Código e Implementación (Agnóstico de lenguaje y SDK)
    # -------------------------------------------------------------------------
    code_files = [
        p for p in all_paths 
        if any(p.endswith(ext) for ext in [".py", ".js", ".ts", ".sh", ".pyc"]) or 
           any(folder in p.lower() for folder in ["src/", "app/", "lib/", "scripts/"])
    ]

    has_code = len(code_files) > 0

    # Detección de conectores o retornos DUMMY / PLACEHOLDER en código
    dummy_patterns = [
        r'conectado"\s*:\s*false',
        r'return\s*\{\s*"conectado"\s*:\s*false',
        r'placeholder',
        r'\[simulado\]',
        r'no\s+se\s+envió\s+nada',
        r'credenciales\s+no\s+configuradas',
        r'pass\s*$'
    ]
    
    found_dummies = []
    for cf in code_files:
        content = file_contents.get(cf, "").lower()
        for pat in dummy_patterns:
            if re.search(pat, content):
                found_dummies.append(f"{cf}: detectado patrón de simulación/dummy ('{pat}')")

    has_dummy_connectors = len(found_dummies) > 0

    # Detección de llamadas a API / herramientas / procesamiento real
    real_execution_patterns = [
        r'requests\.(post|get|put)',
        r'urllib\.request',
        r'fetch\(',
        r'axios\.',
        r'client\.models',
        r'openai\.',
        r'anthropic\.',
        r'generate_content',
        r'chat_completion',
        r'clasificar_',
        r'json\.load'
    ]

    found_real_execution = []
    for cf in code_files:
        content = file_contents.get(cf, "")
        for pat in real_execution_patterns:
            if re.search(pat, content, re.IGNORECASE):
                found_real_execution.append(f"{cf}: patrón de ejecución/procesamiento ('{pat}')")

    # Clasificación objetiva del sistema
    if not has_code:
        system_type = "no_code"
    elif has_dummy_connectors and not found_real_execution:
        system_type = "dummy_placeholder_only"
    elif found_real_execution and has_dummy_connectors:
        system_type = "partial_simulated_tool"
    elif found_real_execution:
        system_type = "real_execution"
    else:
        system_type = "rule_based_local"

    # -------------------------------------------------------------------------
    # 3. Análisis de Prompts
    # -------------------------------------------------------------------------
    prompt_files = [p for p in all_paths if "prompts/" in p.lower() or "prompt" in p.lower()]
    has_substantive_prompts = False
    
    for pf in prompt_files:
        content = file_contents.get(pf, "").strip()
        # Se considera sustantivo si tiene > 100 caracteres y define rol o instrucciones
        if len(content) > 100 and any(kw in content.lower() for kw in ["rol", "tarea", "instrucción", "instrucciones", "sistema", "usuario", "prompt"]):
            has_substantive_prompts = True
            break

    # -------------------------------------------------------------------------
    # 4. Análisis de Corridas y Trazas (corridas/)
    # -------------------------------------------------------------------------
    corrida_files = [p for p in all_paths if "corridas/" in p.lower() or "runs/" in p.lower() or "outputs/" in p.lower()]
    
    # Identificar carpetas o conjuntos de corridas
    corrida_dirs = set()
    for cf in corrida_files:
        parts = cf.split("/")
        if len(parts) > 1:
            corrida_dirs.add(parts[0] + "/" + parts[1])

    corrida_count = len(corrida_dirs) if corrida_dirs else (1 if corrida_files else 0)

    # Verificar presencia de triada: entrada, salida, fecha
    has_entrada = any("entrada" in p.lower() or "input" in p.lower() for p in corrida_files)
    has_salida = any("salida" in p.lower() or "output" in p.lower() or "result" in p.lower() for p in corrida_files)
    has_fecha = any("fecha" in p.lower() or "time" in p.lower() or "date" in p.lower() or "metadata" in p.lower() for p in corrida_files)
    
    has_complete_triad = has_entrada and has_salida and has_fecha

    # -------------------------------------------------------------------------
    # 5. Análisis de Decisiones (DECISIONES.md)
    # -------------------------------------------------------------------------
    decisiones_content = ""
    decisiones_file_path = next((p for p in all_paths if "decisiones.md" in p.lower()), None)
    if decisiones_file_path:
        decisiones_content = file_contents.get(decisiones_file_path, "")

    valid_decisions = []
    if decisiones_content:
        sections = re.split(r'\n(?=#{2,3}\s+)', decisiones_content)
        for sec in sections:
            sec_text = sec.strip()
            if not sec_text or len(sec_text) < 30:
                continue
            if sec_text.startswith('# ') and not sec_text.startswith('## '):
                continue

            sec_lower = sec_text.lower()
            is_explicit = bool(re.search(r'#{2,3}\s*decisi[óo]n\s*\d*', sec_lower))

            has_context = any(kw in sec_lower for kw in [
                "contexto", "problema", "primera versión", "anteriormente", "necesitábamos", 
                "se consideró", "prueba", "situación", "desafío", "issue", "caso", "versión inicial", "primera implementación"
            ])
            has_change = any(kw in sec_lower for kw in [
                "decisión", "decidimos", "cambio", "se definió", "se definieron", "se redujo", 
                "elegimos", "migramos", "adoptamos", "incorporamos", "implementamos", "solución", "integrar", "determinó", "diseño", "se adoptó"
            ])
            has_impact = any(kw in sec_lower for kw in [
                "impacto", "motivo", "resultado", "evidencia", "efecto", "beneficio", 
                "permite", "produjo", "evita", "consecuencia", "ahorro", "mejora", "conservan", "garantizar", "asegurar", "calificación"
            ])

            if is_explicit or (has_context and has_change and has_impact):
                valid_decisions.append(sec_text)

    decision_count = len(valid_decisions)

    # -------------------------------------------------------------------------
    # 6. Análisis Económico (docs/analisis_economico.md o README)
    # -------------------------------------------------------------------------
    econ_content = ""
    econ_file_path = next((p for p in all_paths if "analisis_economico" in p.lower() or "costos" in p.lower()), None)
    if econ_file_path:
        econ_content = file_contents.get(econ_file_path, "")
    elif has_readme:
        econ_content = file_contents.get(next(p for p in all_paths if "readme" in p.lower()), "")

    has_tokens_num = bool(re.search(r'\d+[\.\,]?\d*\s*tokens', econ_content, re.IGNORECASE))
    has_cost_num = bool(re.search(r'(usd|\$)\s*\d+', econ_content, re.IGNORECASE))
    has_projections = bool(re.search(r'(semanal|anual|mes|mensual|proyección)', econ_content, re.IGNORECASE))
    has_model_choice = bool(re.search(r'(modelo|elección|chico|adecuado)', econ_content, re.IGNORECASE))

    # -------------------------------------------------------------------------
    # 7. Análisis de Gobierno y Riesgo (docs/gobierno_riesgo.md o README)
    # -------------------------------------------------------------------------
    gov_content = ""
    gov_file_path = next((p for p in all_paths if "gobierno" in p.lower() or "riesgo" in p.lower()), None)
    if gov_file_path:
        gov_content = file_contents.get(gov_file_path, "")
    elif has_readme:
        gov_content = file_contents.get(next(p for p in all_paths if "readme" in p.lower()), "")

    gov_axes = {
        "permissions": bool(re.search(r'(permiso|sistema|datos|acceso)', gov_content, re.IGNORECASE)),
        "failures": bool(re.search(r'(falla|riesgo|error|consecuencia)', gov_content, re.IGNORECASE)),
        "action_plan": bool(re.search(r'(respuesta|mitigación|acción|eventualidad)', gov_content, re.IGNORECASE)),
        "human_review": bool(re.search(r'(revisión|supervisión|humana|persona)', gov_content, re.IGNORECASE)),
        "responsible": bool(re.search(r'(responsable|firma|asume)', gov_content, re.IGNORECASE))
    }

    # -------------------------------------------------------------------------
    # 8. Detección Objetivo de CONTRADICCIONES DE EVIDENCIA
    # -------------------------------------------------------------------------
    contradictions = []
    invalidated_evidence = []

    # Contradicción D1: Salida afirma haber ejecutado acción que el código no posee
    for cf in corrida_files:
        if "salida" in cf.lower():
            c_text = file_contents.get(cf, "").lower()
            if "actualizado_en_zendesk\": true" in c_text or "conectado\": true" in c_text:
                if has_dummy_connectors:
                    contradictions.append(
                        f"{cf} afirma integración exitosa pero el código contiene conectores dummy/simulados."
                    )
                    invalidated_evidence.append(cf)

    # Contradicción D4: Afirma consumo de tokens cuando el sistema es de reglas locales o dummy sin IA real
    if has_tokens_num and (system_type in ["no_code", "rule_based_local", "dummy_placeholder_only"] or has_dummy_connectors):
        contradictions.append(
            "docs/analisis_economico.md declara consumo de tokens, pero la implementación no invoca modelos de IA."
        )
        invalidated_evidence.append("docs/analisis_economico.md (cifras de tokens invalidadas por código sin IA)")

    # Contradicción D2: DECISIONES declara integraciones o migraciones no verificables en código
    if decisiones_content:
        d_lower = decisiones_content.lower()
        claims_integration = any(kw in d_lower for kw in [
            "migramos", "integración", "zendesk", "api v2", "en tiempo real", "realtime", "modelo de lenguaje"
        ])
        if claims_integration and (has_dummy_connectors or system_type in ["no_code", "rule_based_local", "dummy_placeholder_only"]):
            contradictions.append(
                "DECISIONES.md declara integraciones de API o migraciones a modelos que la implementación observable contradice o mantiene simuladas."
            )
            invalidated_evidence.append("DECISIONES.md (declaraciones de integración/migración invalidadas por código dummy/sin IA)")

    # Contradicción D5: Si el sistema posee conectores dummy/simulados, invalidar el eje de permisos/acceso a sistemas
    if has_dummy_connectors or system_type in ["dummy_placeholder_only", "partial_simulated_tool"]:
        if gov_axes.get("permissions", False):
            contradictions.append(
                "docs/gobierno_riesgo.md declara controles sobre permisos de sistemas que la implementación mantiene simuladas/dummy."
            )
            invalidated_evidence.append("docs/gobierno_riesgo.md (eje de permisos de sistema invalidado por código simulado)")
            gov_axes["permissions"] = False

    return {
        "mandatory_structure": mandatory_structure,
        "has_code": has_code,
        "code_files": code_files,
        "found_dummies": found_dummies,
        "has_dummy_connectors": has_dummy_connectors,
        "found_real_execution": found_real_execution,
        "system_type": system_type,
        "has_substantive_prompts": has_substantive_prompts,
        "corrida_count": corrida_count,
        "has_complete_triad": has_complete_triad,
        "decision_count": decision_count,
        "econ": {
            "has_tokens_num": has_tokens_num,
            "has_cost_num": has_cost_num,
            "has_projections": has_projections,
            "has_model_choice": has_model_choice
        },
        "gov_axes": gov_axes,
        "contradictions": contradictions,
        "invalidated_evidence": invalidated_evidence
    }

