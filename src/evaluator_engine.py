import os
from datetime import datetime
from typing import Optional, Callable

from src.schema import EvaluationResult
from src.github_fetcher import fetch_repository_data
from src.deterministic_evaluator import evaluate_repository_deterministically


def run_evaluation(
    repo_url: str,
    api_key: Optional[str] = None,
    model_name: str = "deterministic",
    status_callback: Optional[Callable[[str], None]] = None
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
    
    if status_callback:
        status_callback("Evaluación determinística completada exitosamente.")

    return result
