import os
from datetime import datetime
from typing import Optional, Callable

from src.schema import EvaluationResult
from src.evidence_extractor import extract_objective_evidence
from src.github_fetcher import fetch_repository_data
from src.deterministic_evaluator import evaluate_repository_deterministically


def run_evaluation(
    repo_url: str,
    api_key: Optional[str] = None,
    model_name: str = "deterministic",
    status_callback: Optional[Callable[[str], None]] = None,
    diagnostics_callback: Optional[Callable[[dict], None]] = None,
) -> EvaluationResult:
    """
    Ejecuta la evaluación determinística Zero-API de un repositorio público de GitHub.
    - Carga e inspecciona el árbol y contenido del repositorio objetivo.
    - Aplica la Matriz por Gates de Evidencia Objetiva de rubrica.md V2 en Python.
    - Funciona al 100% sin requerir claves de API generativas.
    - Retorna el contrato Pydantic EvaluationResult.
    """
    if status_callback:
        status_callback("Descargando e inspeccionando árbol del repositorio...")

    # 1. Descargar e inspeccionar datos del repositorio objetivo
    try:
        repo_data = fetch_repository_data(repo_url)
    except Exception as e:
        return EvaluationResult(
            repository=repo_url,
            evaluated_revision="unknown",
            evaluation_date=datetime.now().strftime("%Y-%m-%d"),
            evaluation_status="access_error",
            dimensions=[],
            final_score=None,
            concrete_improvement="Verificar que la URL del repositorio de GitHub sea pública y accesible.",
            integrity_notes=[f"Error al acceder o descargar el repositorio objetivo: {str(e)}"]
        )

    if status_callback:
        status_callback("Aplicando Matriz de Gates de Evidencia Objetiva en Python...")

    # 2. Ejecutar evaluación determinística en Python
    result = evaluate_repository_deterministically(repo_data)

    if diagnostics_callback:
        try:
            evidence = extract_objective_evidence(repo_data)
            retrieval_audit = repo_data.get("retrieval_audit", {})
            diagnostics_callback(
                {
                    "evaluated_revision": result.evaluated_revision,
                    "resolved_ref": repo_data.get("branch"),
                    "repository_inventory_count": len(repo_data.get("repository_inventory", [])),
                    "retrieval": {
                        "loaded_count": retrieval_audit.get("loaded_count"),
                        "skipped_count": retrieval_audit.get("skipped_count"),
                        "bytes_loaded": retrieval_audit.get("bytes_loaded"),
                    },
                    "found_dummies": evidence["found_dummies"],
                    "has_dummy_connectors": evidence["has_dummy_connectors"],
                    "system_type": evidence["system_type"],
                    "contradictions": evidence["contradictions"],
                    "invalidated_evidence": evidence["invalidated_evidence"],
                }
            )
        except Exception as error:
            try:
                diagnostics_callback({"diagnostic_error": str(error)})
            except Exception:
                pass
    
    if status_callback:
        status_callback("Evaluación determinística completada exitosamente.")

    return result
