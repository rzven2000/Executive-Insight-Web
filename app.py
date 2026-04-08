import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Executive Insight - GTD", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #0055A4; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stMetric { background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. GENERACIÓN DE DATOS (CONSTRUCCIÓN ROBUSTA)
@st.cache_data
def get_data():
    dict_data = {
        'Fase': ['Inicio', 'Planificación', 'Ejecución', 'Ejecución', 'Cierre', 'Planificación', 'Ejecución', 'Inicio', 'Ejecución', 'Cierre'],
        'Actividad': ['Levantamiento FO', 'Permisos Municipales', 'Montaje Starlink', 'Fusión Fibra', 'Pruebas Velocidad', 'Diseño Inalámbrico', 'Instalación Radio', 'Visita Terreno', 'Canalización', 'Entrega Acta'],
        'Sede': ['Quinta Normal', 'Maipú', 'Concepción', 'Peñalolén', 'Viña', 'Temuco', 'Los Ángeles', 'Lampa', 'Quilpué', 'Providencia'],
        'Tecnología': ['Fibra', 'Fibra', 'Satelital', 'Fibra', 'MMOO', 'MMOO', 'MMOO', 'Starlink', 'Fibra', 'Multitecnología'],
        'Inicio': ['2026-04-01', '2026-04-04', '2026-04-05', '2026-04-06', '2026-04-10', '2026-04-02', '2026-04-07', '2026-04-01', '2026-04-08', '2026-04-12'],
        'Dias': [3, 10, 2, 5, 2, 7, 4, 2, 6, 2],
        'Progreso': [1.0, 0.4, 0.1, 0.6, 0.0, 0.8, 0.2, 1.0, 0.3, 0.0],
        'Salud': ['A tiempo', 'En Riesgo', 'Retrasado', 'A tiempo', 'A tiempo', 'En Riesgo', 'Retrasado', 'A tiempo', 'A tiempo', 'A tiempo']
    }
    df = pd.DataFrame(dict_data)
    # Convertir a fechas reales de Python
    df['Inicio'] = pd.to_datetime(df['Inicio'])
    df['Fin'] = df.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
    return df

df_base = get_data()

# 3. SIDEBAR / FILTROS
st.sidebar.title("Configuración PMO")
fases = st.sidebar.multiselect("Fases", df_base['Fase'].unique(), default=df_base['Fase'].unique())
sedes = st.sidebar.multiselect("Sedes", df_base['Sede'].unique(), default=df_base['Sede'].unique())
escala = st.sidebar.selectbox("Escala de Tiempo", ["Días", "Semanas", "Meses"])

# Aplicar Filtros
df_filt = df_base[(df_base['Fase'].isin(fases)) & (df_base['Sede'].isin(sedes))]

# 4. DASHBOARD DE MÉTRICAS
st.title("📊 Executive Insight: Dashboard Semanal")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Avance Promedio", f"{df_filt['Progreso'].mean():.0%}")
with c2:
    retrasos = len(df_filt[df_filt['Salud'] == 'Retrasado'])
    st.metric("Alertas Críticas", retrasos, delta=f"{retrasos} tareas", delta_color="inverse")
with c3:
    st.metric("Tareas Activas", len(df_filt))

# 5. GRÁFICO GANTT (EL MOTOR)
st.subheader(f"Cronograma Maestro (Vista por {escala})")

if not df_filt.empty:
    # Crear Gantt con Plotly Express
    fig = px.timeline(
        df_filt, 
        x_start="Inicio", 
        x_end="Fin", 
        y="Actividad", 
        color="Salud",
        text="Sede",
        hover_data=["Tecnología", "Progreso"],
        color_discrete_map={
            "A tiempo": "#0055A4",   # Azul GTD
            "En Riesgo": "#FFCC00",  # Amarillo/Gris
            "Retrasado": "#FF0000"   # Rojo Alerta
        }
    )

    # Invertir eje para que la primera tarea esté arriba
    fig.update_yaxes(autorange="reversed")

    # Configurar el eje del tiempo
    formato_fecha = "%d %b"
    tick_val = "D1"
    if escala == "Semanas": tick_val = 604800000.0
    if escala == "Meses": tick_val = "M1"

    fig.update_layout(
        xaxis=dict(title="Calendario", tickformat=formato_fecha, dtick=tick_val),
        yaxis=dict(title=""),
        plot_bgcolor="white",
        showlegend=True,
        height=450
    )

    # Sombras de Fines de Semana
    min_date = df_filt['Inicio'].min()
    max_date = df_filt['Fin'].max()
    curr = min_date
    while curr <= max_date:
        if curr.weekday() >= 5:
            fig.add_vrect(x0=curr, x1=curr + timedelta(days=1), fillcolor="gray", opacity=0.1, layer="below", line_width=0)
        curr += timedelta(days=1)

    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("No hay datos disponibles con los filtros actuales.")

# 6. TABLA DE DATOS
with st.expander("Ver tabla de datos detallada"):
    st.table(df_filt[['Fase', 'Actividad', 'Sede', 'Salud', 'Progreso']])
