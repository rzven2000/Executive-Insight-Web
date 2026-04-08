import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 1. ESTILO Y CONFIGURACIÓN "EXECUTIVE"
st.set_page_config(page_title="Executive Insight - GTD", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    [data-testid="stSidebar"] { background-color: #0055A4; min-width: 280px; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #eef2f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAR DATOS EN MEMORIA
if 'df_datos' not in st.session_state:
    st.session_state.df_datos = pd.DataFrame({
        'Fase': ['Ejecución', 'Planificación', 'Ejecución', 'Cierre', 'Inicio'],
        'Actividad': ['Instalación FW Combarbalá', 'Ruta FO Mapocho', 'Nodo Peñalolén', 'Entrega Acta Huechuraba', 'Levantamiento Maipú'],
        'Sede': ['La Granja', 'Quinta Normal', 'Peñalolén', 'Huechuraba', 'Maipú'],
        'Tecnología': ['Fibra', 'Fibra', 'MMOO', 'SD-WAN', 'Fibra'],
        'Inicio': pd.to_datetime(['2026-04-01', '2026-04-06', '2026-04-10', '2026-04-20', '2026-04-01']),
        'Dias': [4, 14, 30, 2, 3], 
        'Progreso': [1.0, 0.2, 0.0, 0.0, 1.0],
        'Salud': ['A tiempo', 'En Riesgo', 'Retrasado', 'A tiempo', 'A tiempo'],
        'Responsable': ['Stif Jara', 'Javier R.', 'F. Penrroz', 'G. Cerda', 'A. Soto']
    })

# 3. SIDEBAR: FILTROS Y ESCALA
st.sidebar.image("https://www.gtd.cl/images/logo-gtd.png", width=120)
st.sidebar.title("Panel PMO")

st.sidebar.markdown("---")
escala = st.sidebar.radio("🔍 Unidad de Cuadrícula (Zoom)", ["Días", "Semanas", "Meses"])

st.sidebar.markdown("---")
df = st.session_state.df_datos

# Filtros Multi-selección
fase_sel = st.sidebar.multiselect("Filtrar Fase", df['Fase'].unique(), default=df['Fase'].unique())
sede_sel = st.sidebar.multiselect("Filtrar Sede", df['Sede'].unique(), default=df['Sede'].unique())
tec_sel = st.sidebar.multiselect("Filtrar Tecnología", df['Tecnología'].unique(), default=df['Tecnología'].unique())
resp_sel = st.sidebar.multiselect("Filtrar Responsable", df['Responsable'].unique(), default=df['Responsable'].unique())

df_filt = df[
    (df['Fase'].isin(fase_sel)) & 
    (df['Sede'].isin(sede_sel)) & 
    (df['Tecnología'].isin(tec_sel)) &
    (df['Responsable'].isin(resp_sel))
].copy()

# Cálculo de Fin dinámico
df_filt['Inicio'] = pd.to_datetime(df_filt['Inicio'])
df_filt['Fin'] = df_filt.apply(lambda x: x['Inicio'] + timedelta(days=int(x['Dias'])), axis=1)

# 4. DASHBOARD: KPIs
st.title("📊 Executive Insight: Control en Vivo")
k1, k2, k3, k4 = st.columns(4)
with k1:
    prog = df_filt['Progreso'].mean() if not df_filt.empty else 0
    st.metric("Progreso Global", f"{prog:.1%}")
with k2:
    alertas = len(df_filt[df_filt['Salud'] == 'Retrasado'])
    st.metric("Alertas Críticas", alertas, delta=f"{alertas} Riesgos", delta_color="inverse")
with k3:
    st.metric("Sedes Activas", len(df_filt['Sede'].unique()))
with k4:
    st.metric("Total Tareas", len(df_filt))

# 5. EDITOR DE DATOS DESPLEGABLE
with st.expander("✏️ Editar Datos del Proyecto (Clic para abrir)"):
    st.info("Los cambios realizados aquí se reflejarán inmediatamente en el gráfico inferior.")
    df_editado = st.data_editor(
        st.session_state.df_datos,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Progreso": st.column_config.NumberColumn(format="%.2f", min_value=0.0, max_value=1.0),
            "Dias": st.column_config.NumberColumn(min_value=1),
            "Inicio": st.column_config.DateColumn(format="YYYY-MM-DD")
        }
    )
    if not df_editado.equals(st.session_state.df_datos):
        st.session_state.df_datos = df_editado
        st.rerun()

# 6. CARTA GANTT COMPLETA
st.markdown("---")

if not df_filt.empty:
    # Lógica de escala y sombreado
    mostrar_finde = False
    if escala == "Días":
        t_format, t_tick, mostrar_finde = "%d %b", 86400000.0, True
    elif escala == "Semanas":
        t_format, t_tick, mostrar_finde = "Sem %W", 604800000.0, True
    else: # Meses
        t_format, t_tick = "%B %Y", "M1"

    fig = px.timeline(
        df_filt, x_start="Inicio", x_end="Fin", y="Actividad",
        color="Salud", text="Sede",
        hover_data=["Responsable", "Tecnología", "Dias"],
        color_discrete_map={"A tiempo": "#0055A4", "En Riesgo": "#D1D5DB", "Retrasado": "#FF0000"}
    )
    fig.update_yaxes(autorange="reversed", title="")

    # SOMBREADO DE FINES DE SEMANA
    if mostrar_finde:
        min_date = df_filt['Inicio'].min() - timedelta(days=7)
        max_date = df_filt['Fin'].max() + timedelta(days=7)
        curr = min_date
        while curr <= max_date:
            if curr.weekday() >= 5: # 5=Sábado, 6=Domingo
                fig.add_vrect(
                    x0=curr.strftime("%Y-%m-%d"), 
                    x1=(curr + timedelta(days=1)).strftime("%Y-%m-%d"), 
                    fillcolor="gray", opacity=0.15, layer="below", line_width=0
                )
            curr += timedelta(days=1)

    # LÍNEA DE HOY
    hoy = datetime.now()
    fig.add_vline(
        x=hoy.timestamp() * 1000, line_width=2, line_dash="dash", line_color="#FF4B4B",
        annotation_text="Hoy", annotation_position="top right"
    )

    fig.update_layout(
        xaxis=dict(tickformat=t_format, dtick=t_tick, type='date', gridcolor="#E0E0E0", showgrid=True),
        plot_bgcolor="white", height=500, showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Sin datos para mostrar.")

# 7. TABLA DE RESUMEN
st.markdown("### Resumen Detallado")
columnas_vista = ['Fase', 'Actividad', 'Sede', 'Tecnología', 'Responsable', 'Inicio', 'Dias', 'Fin', 'Progreso', 'Salud']
st.dataframe(
    df_filt[columnas_vista].style.format({
        'Progreso': '{:.0%}', 
        'Inicio': lambda x: x.strftime('%Y-%m-%d'), 
        'Fin': lambda x: x.strftime('%Y-%m-%d')
    }), 
    use_container_width=True
)
