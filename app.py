import os
import inspect
import subprocess
import sys
import time
from datetime import datetime
import streamlit as st
from src import evidence_extractor
from src.evaluator_engine import run_evaluation
from src.schema import EvaluationResult
from src.ui_feedback import generate_student_feedback

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Agente Evaluador UCEMA",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Agente Evaluador — Trabajos Finales (UCEMA)")
st.caption("Evaluación determinística Zero-API de repositorios aplicando la Rúbrica Autoritativa V2")

# Sidebar informativa
with st.sidebar:
    logo_path = os.path.join("assets", "ucema_logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=160)

    st.subheader("👥 Grupo — Agente Evaluador")
    st.markdown("""
    **Integrantes:**
    - Pablo Bellesi
    - Diego Mendez
    - Franco Gambini
    - Sofia Mapelli
    - Franco Forziati
    - Melisa Clark
    """)

    with st.expander("🛠️ Diagnóstico técnico", expanded=False):
        try:
            runtime_head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                capture_output=True,
                check=True,
                text=True,
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError) as error:
            runtime_head = f"No disponible: {error}"

        contextual_patterns = [
            r"r'\bplaceholder\b.{0,80}\b(?:conector|connector|api|integraci[oó]n)\b'",
            r"r'\b(?:conector|connector|api|integraci[oó]n)\b.{0,80}\bplaceholder\b'",
        ]
        try:
            extractor_source = inspect.getsource(evidence_extractor)
            generic_placeholder_pattern = "r'placeholder'" in extractor_source
            contextual_placeholder_patterns = [
                pattern in extractor_source for pattern in contextual_patterns
            ]
            source_error = None
        except (OSError, TypeError) as error:
            generic_placeholder_pattern = None
            contextual_placeholder_patterns = None
            source_error = str(error)
        st.json(
            {
                "runtime_git_head": runtime_head,
                "evidence_extractor_module": evidence_extractor.__file__,
                "generic_placeholder_pattern": generic_placeholder_pattern,
                "contextual_placeholder_patterns": contextual_placeholder_patterns,
                "source_inspection_error": source_error,
                "python_version": sys.version,
            }
        )

    st.divider()

    st.header("ℹ️ Información")
    st.markdown("""
    **Principios del Evaluador V2:**
    - **Scoring 100% Determinístico en Python**
    - **EVIDENCIA > DECLARACIÓN**
    - Gates de Evidencia Objetiva
    - Matriz Autoritativa V2 (5 Dimensiones)
    - Zero API Key / Zero Costo
    """)

tab_single, tab_batch = st.tabs(["📌 Evaluación Individual", "📋 Evaluación por Lote"])

with tab_single:
    # Campo principal para ingresar la URL del repositorio objetivo
    repo_url = st.text_input(
        "URL pública del repositorio objetivo en GitHub",
        placeholder="https://github.com/propietario/trabajo-final",
        help="Ingresa la URL del repositorio individual o subcarpeta (/tree/branch/subpath) a evaluar",
        key="input_single_url"
    )

    if st.button("🚀 Evaluar Repositorio", type="primary", use_container_width=True, key="btn_single_eval"):
        if not repo_url.strip():
            st.error("Por favor, ingresa una URL válida de GitHub.")
        else:
            with st.status("Evaluando repositorio...", expanded=True) as status:
                st.write("🔍 Inspeccionando árbol y archivos del repositorio...")
                st.write("📜 Extrayendo evidencia objetiva y aplicando gates determinísticos...")
                
                result = run_evaluation(
                    repo_url=repo_url.strip(),
                    status_callback=lambda msg: st.write(f"⏳ {msg}")
                )
                
                if result.evaluation_status == "completed":
                    status.update(label="✅ Evaluación completada con éxito", state="complete", expanded=False)
                else:
                    status.update(label="❌ Error durante la evaluación", state="error", expanded=True)

            st.divider()

            # A. Repositorio + revisión SHA y B. Nota Final
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.subheader(f"📌 Repositorio: `{result.repository}`")
                st.caption(f"Revisión evaluada: `{result.evaluated_revision}` | Fecha: `{result.evaluation_date}`")
            with col2:
                status_color = "green" if result.evaluation_status == "completed" else "red"
                st.markdown(f"**Estado:** :{status_color}[{result.evaluation_status.upper()}]")
            with col3:
                if result.final_score is not None:
                    st.metric("Nota Final", f"{result.final_score} / 100")
                else:
                    st.metric("Nota Final", "N/A")

            # C. Resumen visual D1-D5
            st.subheader("📊 Resumen por Dimensiones Oficiales")
            if result.dimensions:
                d_cols = st.columns(len(result.dimensions))
                for idx, dim in enumerate(result.dimensions):
                    with d_cols[idx]:
                        st.metric(
                            label=f"D{idx+1}: {dim.dimension}",
                            value=f"{dim.score:.2f} pts" if dim.score is not None else "0.00",
                            delta=f"Nivel {dim.level_percent}%" if dim.level_percent is not None else "0%"
                        )

            # D & E. Devolución al alumno evaluado y Contradicciones
            feedback = generate_student_feedback(result)

            st.divider()
            st.subheader("🎓 Devolución al alumno evaluado")

            st.markdown(f"**Resumen general:**\n{feedback['resumen_general']}")

            if feedback["fortalezas"]:
                st.markdown("#### 🌱 Fortalezas")
                for f in feedback["fortalezas"]:
                    st.markdown(f"- **{f['dimension']}** ({f['level_percent']}%): {f['text']}")

            if feedback["avances_parciales"]:
                st.markdown("#### 📈 Avances parciales")
                for a in feedback["avances_parciales"]:
                    st.markdown(f"- **{a['dimension']}** ({a['level_percent']}%): {a['text']}")

            if feedback["aspectos_a_mejorar"]:
                st.markdown("#### 🎯 Aspectos a mejorar")
                for m in feedback["aspectos_a_mejorar"]:
                    st.markdown(f"- **{m['dimension']}** (Nivel actual: {m['level_percent']}%): {m['text']}")

            if feedback["recomendacion_prioritaria"]:
                st.info(f"💡 **Recomendación prioritaria:**\n\n{feedback['recomendacion_prioritaria']}")

            if feedback["tiene_contradicciones"]:
                st.warning("⚠️ **Evidencia que requiere revisión**\n\nSe identificaron las siguientes inconsistencias objetivas entre los artefactos documentados y la implementación ejecutable:")
                for note in feedback["contradicciones"]:
                    st.markdown(f"- {note}")

            st.divider()

            # F. Expander: Ver desglose técnico completo
            with st.expander("🔍 Ver desglose técnico completo", expanded=False):
                if not result.dimensions:
                    st.error("No se obtuvieron dimensiones evaluadas debido a un error de acceso.")
                else:
                    for dim in result.dimensions:
                        st.markdown(f"### **{dim.dimension}** — Puntaje: `{dim.score if dim.score is not None else 0}` / {dim.weight} pts (Nivel {dim.level_percent if dim.level_percent is not None else 0}%)")
                        d_col1, d_col2 = st.columns([1, 2])
                        with d_col1:
                            st.markdown(f"**Peso:** {dim.weight} pts")
                            st.markdown(f"**Nivel asignado:** {dim.level_percent}%")
                            st.markdown(f"**Puntaje parcial:** {dim.score} pts")
                        with d_col2:
                            st.markdown("**Justificación:**")
                            st.write(dim.justification)
                            if dim.missing_for_next_level:
                                st.markdown("**Faltante para el siguiente nivel:**")
                                st.caption(dim.missing_for_next_level)

                        st.markdown("**Evidencia citada:**")
                        if dim.evidence:
                            for ev in dim.evidence:
                                st.markdown(f"- `{ev}`")
                        else:
                            st.write("_Sin evidencia citada_")
                        st.divider()

with tab_batch:
    st.subheader("📋 Evaluación por Lote de Repositorios (Hasta 50 URLs)")
    st.caption("Ingresa múltiples URLs de GitHub (una por línea). Se evaluarán de forma determinística Zero-API.")

    batch_input = st.text_area(
        "URLs públicas de GitHub (una por línea, máx. 50)",
        placeholder="https://github.com/propietario/repo-1\nhttps://github.com/propietario/repo-2\nhttps://github.com/propietario/repo-3",
        height=200,
        key="input_batch_urls"
    )

    if st.button("🚀 Evaluar Lote", type="primary", use_container_width=True, key="btn_batch_eval"):
        raw_urls = [line.strip() for line in batch_input.splitlines() if line.strip()]
        urls_received = len(raw_urls)

        if urls_received == 0:
            st.error("Por favor, ingresa al menos una URL válida de GitHub.")
        else:
            # Deduplicar preservando el orden de aparición
            unique_urls = list(dict.fromkeys(raw_urls))
            dedup_count = urls_received - len(unique_urls)

            # Cap a máximo 50 URLs
            valid_urls = unique_urls[:50]
            capped_count = len(unique_urls) - len(valid_urls)

            if dedup_count > 0:
                st.info(f"ℹ️ Se eliminaron {dedup_count} URL(s) duplicada(s) del lote.")
            if capped_count > 0:
                st.warning(f"⚠️ Se excedió el límite de 50 URLs. Se evaluarán únicamente las primeras 50 URLs únicas.")

            st.write(f"▶️ Procesando **{len(valid_urls)}** repositorio(s)...")

            progress_bar = st.progress(0.0)
            status_text = st.empty()

            batch_results = []
            completed_count = 0
            error_count = 0

            start_time = time.time()
            total_urls = len(valid_urls)

            for idx, url in enumerate(valid_urls, start=1):
                status_text.write(f"⏳ ({idx}/{total_urls}) Evaluando `{url}`...")
                try:
                    res = run_evaluation(url)
                except Exception as e:
                    res = EvaluationResult(
                        repository=url,
                        evaluated_revision="unknown",
                        evaluation_date=datetime.now().strftime("%Y-%m-%d"),
                        evaluation_status="access_error",
                        dimensions=[],
                        final_score=None,
                        concrete_improvement="Error no controlado durante la evaluación del repositorio.",
                        integrity_notes=[f"Excepción en ejecución batch: {str(e)}"]
                    )

                if res.evaluation_status == "completed":
                    completed_count += 1
                else:
                    error_count += 1

                batch_results.append(res)
                progress_bar.progress(idx / total_urls)

            total_elapsed_time = time.time() - start_time
            avg_time = total_elapsed_time / total_urls if total_urls > 0 else 0.0

            status_text.success("✅ Evaluación del lote completada con éxito.")

            st.divider()

            # Métricas del Lote
            st.subheader("📊 Métrica del Lote Evaluado")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("URLs Recibidas", urls_received)
            m2.metric("URLs Válidas Procesadas", total_urls)
            m3.metric("Evaluaciones Completadas", completed_count)
            m4.metric("Errores / Fallos Acceso", error_count)

            t1, t2, t3, t4 = st.columns(4)
            t1.metric("Tiempo Total", f"{total_elapsed_time:.2f} s")
            t2.metric("Tiempo Promedio / Eval", f"{avg_time:.2f} s")
            t3.metric("Tokens Generativos", "0")
            t4.metric("Costo API Generativo", "USD 0.00")

            st.divider()

            # Tabla Resumen
            st.subheader("📑 Tabla Resumen de Evaluaciones")
            table_rows = []
            for i, res in enumerate(batch_results, start=1):
                dims = res.dimensions
                d1 = f"{dims[0].score:.2f}" if len(dims) > 0 and dims[0].score is not None else "0.00"
                d2 = f"{dims[1].score:.2f}" if len(dims) > 1 and dims[1].score is not None else "0.00"
                d3 = f"{dims[2].score:.2f}" if len(dims) > 2 and dims[2].score is not None else "0.00"
                d4 = f"{dims[3].score:.2f}" if len(dims) > 3 and dims[3].score is not None else "0.00"
                d5 = f"{dims[4].score:.2f}" if len(dims) > 4 and dims[4].score is not None else "0.00"

                table_rows.append({
                    "#": i,
                    "repositorio": res.repository,
                    "revisión evaluada": res.evaluated_revision,
                    "estado": res.evaluation_status.upper(),
                    "nota final": f"{res.final_score:.2f}" if res.final_score is not None else "N/A",
                    "D1": d1,
                    "D2": d2,
                    "D3": d3,
                    "D4": d4,
                    "D5": d5,
                    "contradicciones detectadas": len(res.integrity_notes),
                    "sugerencia principal": res.concrete_improvement
                })

            st.dataframe(table_rows, use_container_width=True)

