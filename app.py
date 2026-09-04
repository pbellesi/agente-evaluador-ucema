import os
import streamlit as st
from src.evaluator_engine import run_evaluation

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
    st.header("ℹ️ Información")
    st.markdown("""
    **Principios del Evaluador V2:**
    - **Scoring 100% Determinístico en Python**
    - **EVIDENCIA > DECLARACIÓN**
    - Gates de Evidencia Objetiva
    - Matriz Autoritativa V2 (5 Dimensiones)
    - Zero API Key / Zero Costo
    """)

# Campo principal para ingresar la URL del repositorio objetivo
repo_url = st.text_input(
    "URL pública del repositorio objetivo en GitHub",
    placeholder="https://github.com/propietario/trabajo-final",
    help="Ingresa la URL del repositorio individual o subcarpeta (/tree/branch/subpath) a evaluar"
)

if st.button("🚀 Evaluar Repositorio", type="primary", use_container_width=True):
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

        # Resumen superior
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

        # Alerta de Notas de Integridad si existen
        if result.integrity_notes:
            st.warning("⚠️ **Notas de Integridad y Alertas:**")
            for note in result.integrity_notes:
                st.write(f"- {note}")

        # Sugerencia de mejora concreta
        st.info(f"💡 **Sugerencia de Mejora Concreta:**\n\n{result.concrete_improvement}")

        # Desglose de las 5 Dimensiones
        st.subheader("📊 Desglose por Dimensiones Oficiales")

        if not result.dimensions:
            st.error("No se obtuvieron dimensiones evaluadas debido a un error de acceso.")
        else:
            for dim in result.dimensions:
                with st.expander(
                    f"**{dim.dimension}** — Puntaje: `{dim.score if dim.score is not None else 0}` / {dim.weight} pts (Nivel {dim.level_percent if dim.level_percent is not None else 0}%)",
                    expanded=True
                ):
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
