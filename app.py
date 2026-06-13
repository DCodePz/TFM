import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

from core.workers import cargar_operarios, guardar_operarios, devolver_acciones
from core.algorithm import ejecutar_algoritmo


st.set_page_config(
    page_title="Skynet System",
    page_icon="🚛",
    layout="wide"
)

# ============================================================
#  STATE
# ============================================================

if "workers_df" not in st.session_state:
    st.session_state.workers_df = cargar_operarios()

if "operarios" not in st.session_state:
    st.session_state.operarios = None

workers_df = st.session_state.workers_df

# ============================================================
#  SIDEBAR
# ============================================================

st.sidebar.header("📋 Gestión de Tareas")

num_tareas = st.sidebar.number_input(
    "Número tareas a mostrar por usuario:",
    min_value=0,
    value=3
)

group_tareas = st.sidebar.slider(
    "Número tareas por grupo (Requiere recalculo):",
    min_value=1,
    max_value=5,
    value=2
)

mostrar_vacios = st.sidebar.checkbox(
    "Mostrar vacíos",
    value=False
)

st.sidebar.divider()

st.sidebar.header("👷 Gestión de Operarios")

edited_df = st.sidebar.data_editor(
    workers_df[["operario", "pos_x", "pos_y"]],
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Operario": st.column_config.TextColumn(
            "Operario"
        ),
        "Pos X": st.column_config.NumberColumn(
            "Pos X",
            min_value=0,
            step=1,
            format="%d"
        ),
        "Pos Y": st.column_config.NumberColumn(
            "Pos Y",
            min_value=0,
            step=1,
            format="%d"
        )
    }
)

if st.sidebar.button("💾 Guardar"):
    guardar_operarios(edited_df)
    st.session_state.workers_df = edited_df
    st.sidebar.success("Operarios guardados")

# ============================================================
#  MAIN
# ============================================================

st.title("🚛 Skynet System")
st.caption(datetime.now().strftime("%H:%M:%S"))

if st.button("🔄 Recalcular"):
    with st.spinner("Calculando..."):
        operarios = ejecutar_algoritmo(group_tareas)
        st.session_state.operarios = operarios
    
    st.success("Cálculo realizado correctamente.")

# ============================================================
#  RESULTADOS
# ============================================================

operarios = st.session_state.operarios

if operarios:
    for op in operarios:

        with st.expander(f"Operario - {op['operario']}"):

            df = pd.DataFrame(
                devolver_acciones(op, num_tareas, mostrar_vacios)
            )

            df = df.rename(columns={
                "tipo": "Tipo",
                "task_ids": "Tareas",
                "origen": "Origen",
                "destino": "Destino",
                "coste": "Coste"
            })

            df = df[["Tipo", "Origen", "Destino", "Coste", "Tareas"]]

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Coste total", df["Coste"].sum())

            with col2:
                st.metric("Posición", f"{df.iloc[-1]["Destino"]}")

            st.dataframe(df, use_container_width=True)