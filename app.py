import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 1. ESTILO Y CONFIGURACIÓN "EXECUTIVE"
st.set_page_config(page_title="Executive Insight - GTD", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    [data-testid="stSidebar"] { background-color: #0055A4; min-width: 260px; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eef2f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE ESTADO DE DATOS (Session State)
# Esto permite que los cambios que hagas en la tabla se mantengan mientras la página esté abierta.
if 'df_proyectos' not in st.session_state:
    data_inicial = {
        'Fase': ['Ejecución', 'Planificación', 'Inicio'],
        'Actividad': ['Instalación FW Combarbalá', 'Ruta FO Mapocho', 'Levantamiento Peñalolén'],
        'Sede': ['La Granja', 'Quinta Normal', 'Peñalolén'],
        'Tecnología': ['Fibra', 'Fibra', 'MMOO'],
        'Inicio': [datetime(2026, 4, 1), datetime(2026, 4, 6), datetime(2026, 4, 10)],
        'Dias': [4, 5, 12],
        'Progreso': [1.0, 0.2, 0.0],
        'Salud': ['A tiempo', 'En Riesgo', 'Retrasado'],
        'Responsable': ['Stif Jara', 'Javier R.', 'F. Penrroz']
    }
    st.session_state.df_proyectos = pd.DataFrame(data_inicial)

# 3. SIDEBAR: CONTROL DE VISTA
st.sidebar.image("https://www.gtd.cl/images/logo-gtd.png", width=120)
st.sidebar.title("Panel de Control PMO")
escala = st.sidebar.radio("🔍 Zoom del Cronograma", ["Días", "Semanas", "Meses"])

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Resetear a Datos de Ejemplo"):
    del st.session_state.df_proyectos
    st.rerun()

# 4. DASHBOARD DE MÉTRICAS (Dinámico al editor)
st.title("📊 Executive Insight: Gestión en Tiempo Real")

# Recalcular Fin basado en cambios del editor
df_actual = st.session_state.df_proyectos.copy()
df_actual['Inicio'] = pd.to_datetime(df_actual['Inicio'])
df_actual['Fin'] = df_actual.apply(lambda x: x['Inicio'] + timedelta(days=int(x['Dias'])), axis=1)

k1, k2, k3 = st.columns(3)
with k1:
    progreso = df_actual['Progreso'].mean() if not df_actual.empty else 0
    st.metric("Progreso Global", f"{progreso:.1%}")
with k2:
    alertas = len(df_actual[df_actual['Salud'] == 'Retrasado'])
    st.metric("Alertas Críticas", alertas, delta=f"{alertas} Riesgos", delta_color="inverse")
with k3:
    st.metric("Total Actividades", len(df_actual))

# 5. EDITOR DE DATOS (LA TABLA INTERACTIVA)
st.markdown("### 📝 Editor de Actividades")
st.info("💡 **Tips:** Haz doble clic en cualquier celda para editar. Para agregar filas, ve al final de la tabla y presiona el botón '+'.")

# El componente clave: st.data_editor
df_editado = st.data_editor(
    st.session_state.df_proyectos,
    num_rows="dynamic", # Permite agregar y borrar filas
    use_container_width=True,
    column_config={
        "Progreso": st.column_config.NumberColumn(format="%.2f", min_value=0, max_value=1),
        "Salud": st.column_config.SelectboxColumn(options=["A tiempo", "En Riesgo", "Retrasado"]),
        "Tecnología": st.column_config.SelectboxColumn(options=["Fibra", "Satelital", "MMOO", "SD-WAN"]),
        "Inicio": st.column_config.DateColumn(),
        "Dias": st.column_config.NumberColumn(min_value=1)
    },
    key="editor_proyectos"
)

# Guardar cambios del editor en el estado de la sesión
if not df_editado.equals(st.session_state.df_proyectos):
    st.session_state.df_proyectos = df_editado
    st.rerun()

# 6. CARTA GANTT (Reflejando cambios del editor)
st.markdown("---")
st.subheader(f"Cronograma Maestro (Vista: {escala})")

if not df_actual.empty:
    # Lógica de escala
    t_format, t_tick = ("%d %b", "D1") if escala == "Días" else (("Sem %W", 604800000.0) if escala == "Semanas" else ("%B %Y", "M1"))
    
    fig = px.timeline(
        df_actual, x_start="Inicio", x_end="Fin", y="Actividad",
        color="Salud", text="Sede",
        hover_data=["Responsable", "Dias"],
        color_discrete_map={"A tiempo": "#0055A4", "En Riesgo": "#D1D5DB", "Retrasado": "#FF0000"}
    )
    
    fig.update_yaxes(autorange="reversed", title="")
    
    # Sombreado de Fines de Semana
    if escala != "Meses":
        min_date = df_actual['Inicio'].min() - timedelta(days=2)
        max_date = df_actual['Fin'].max() + timedelta(days=2)
        curr = min_date
        while curr <= max_date:
            if curr.weekday() >= 5:
                fig.add_vrect(x0=curr, x1=curr + timedelta(days=1), fillcolor="gray", opacity=0.1, layer="below", line_width=0)
            curr += timedelta(days=1)

    fig.update_layout(xaxis=dict(tickformat=t_format, dtick=t_tick, type='date'), plot_bgcolor="white", height=450)
    st.plotly_chart(fig, use_container_width=True)
