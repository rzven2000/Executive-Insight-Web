import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE ESTILO "EXECUTIVE INSIGHT"
st.set_page_config(page_title="Executive Insight - GTD", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    [data-testid="stSidebar"] { background-color: #0055A4; min-width: 250px; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eef2f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIÓN PARA CARGAR DATOS (EXCEL O DEFAULT)
def obtener_datos():
    # 2.1. Lógica de Carga de Archivo en Sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Cargar Datos")
    archivo_subido = st.sidebar.file_uploader("Sube tu Excel (.xlsx)", type=["xlsx"])

    if archivo_subido is not None:
        try:
            df_user = pd.read_excel(archivo_subido)
            # Asegurar formato de fechas
            df_user['Inicio'] = pd.to_datetime(df_user['Inicio'])
            if 'Fin' not in df_user.columns:
                df_user['Fin'] = df_user.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
            return df_user
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
    
    # 2.2. Datos por defecto (si no hay archivo subido)
    data = {
        'Fase': ['Inicio', 'Planificación', 'Ejecución', 'Cierre'],
        'Actividad': ['Levantamiento FO', 'Permisos', 'Instalación', 'Entrega'],
        'Sede': ['Quinta Normal', 'Maipú', 'Concepción', 'Providencia'],
        'Tecnología': ['Fibra', 'Fibra', 'Satelital', 'Multitecnología'],
        'Inicio': pd.to_datetime(['2026-04-01', '2026-04-04', '2026-04-06', '2026-04-12']),
        'Dias': [3, 10, 5, 2],
        'Progreso': [1.0, 0.4, 0.2, 0.0],
        'Salud': ['A tiempo', 'En Riesgo', 'Retrasado', 'A tiempo'],
        'Responsable': ['Stif Jara', 'A. Soto', 'G. Cerda', 'F. Penrroz']
    }
    df_def = pd.DataFrame(data)
    df_def['Fin'] = df_def.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
    return df_def

df = obtener_datos()

# 3. SIDEBAR (FILTROS DINÁMICOS)
st.sidebar.image("https://www.gtd.cl/images/logo-gtd.png", width=120)
st.sidebar.title("Panel de Control PMO")

fase_sel = st.sidebar.multiselect("Filtrar Fase", df['Fase'].unique(), default=df['Fase'].unique())
sede_sel = st.sidebar.multiselect("Filtrar Sede", df['Sede'].unique(), default=df['Sede'].unique())
escala = st.sidebar.radio("Escala de Tiempo", ["Días", "Semanas", "Meses"])

df_filt = df[(df['Fase'].isin(fase_sel)) & (df['Sede'].isin(sede_sel))]

# 4. DASHBOARD: KPIs
st.title("📊 Executive Insight: Dashboard Dinámico")
k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Progreso Global", f"{df_filt['Progreso'].mean():.1%}")
with k2:
    criticos = len(df_filt[df_filt['Salud'] == 'Retrasado'])
    st.metric("Alertas Críticas", criticos, delta=f"{criticos} Riesgos", delta_color="inverse")
with k3:
    st.metric("Total Tareas", len(df_filt))

# 5. CARTA GANTT DINÁMICA
st.markdown("---")
if not df_filt.empty:
    fig = px.timeline(
        df_filt, x_start="Inicio", x_end="Fin", y="Actividad",
        color="Salud", hover_data=["Sede", "Responsable"],
        color_discrete_map={"A tiempo": "#0055A4", "En Riesgo": "#D1D5DB", "Retrasado": "#FF0000"},
        text="Sede"
    )
    fig.update_yaxes(autorange="reversed")
    
    # Ajuste de Escala
    if escala == "Días":
        t_format, t_tick = "%d %b", "D1"
    elif escala == "Semanas":
        t_format, t_tick = "Sem %W", 604800000.0
    else:
        t_format, t_tick = "%B", "M1"

    fig.update_layout(xaxis=dict(tickformat=t_format, dtick=t_tick, title=""), plot_bgcolor="white", height=450)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Sin datos para mostrar.")

# 6. TABLA DE DATOS Y PLANTILLA
st.markdown("### Detalle de Actividades")
st.dataframe(df_filt, use_container_width=True)

# Ayuda para el usuario: Descargar plantilla
st.info("💡 **Consejo:** Para subir tareas nuevas, asegúrate de que tu Excel tenga estas columnas: `Fase, Actividad, Sede, Tecnología, Inicio, Dias, Progreso, Salud, Responsable`.")
