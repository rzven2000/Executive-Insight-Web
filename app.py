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
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eef2f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE CARGA DE DATOS (CON TODAS LAS COLUMNAS)
def obtener_datos():
    st.sidebar.image("https://www.gtd.cl/images/logo-gtd.png", width=120)
    st.sidebar.title("Panel de Control PMO")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Actualizar Proyectos")
    archivo = st.sidebar.file_uploader("Sube tu Excel (.xlsx)", type=["xlsx"])

    if archivo is not None:
        try:
            df_user = pd.read_excel(archivo)
            df_user['Inicio'] = pd.to_datetime(df_user['Inicio'])
            # Aseguramos que la columna Fin exista para el gráfico
            df_user['Fin'] = df_user.apply(lambda x: x['Inicio'] + timedelta(days=int(x['Dias'])), axis=1)
            return df_user
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
    
    # DATOS DE PRUEBA INICIALES (CON ESTRUCTURA COMPLETA)
    data = {
        'Fase': ['Ejecución', 'Planificación', 'Ejecución', 'Cierre', 'Inicio'],
        'Actividad': ['Instalación FW Combarbalá', 'Ruta FO Mapocho', 'Nodo Peñalolén', 'Entrega Acta Huechuraba', 'Levantamiento Maipú'],
        'Sede': ['La Granja', 'Quinta Normal', 'Peñalolén', 'Huechuraba', 'Maipú'],
        'Tecnología': ['Fibra', 'Fibra', 'MMOO', 'SD-WAN', 'Fibra'],
        'Inicio': pd.to_datetime(['2026-04-01', '2026-04-06', '2026-04-10', '2026-04-20', '2026-04-01']),
        'Dias': [4, 5, 15, 2, 3],
        'Progreso': [1.0, 0.2, 0.0, 0.0, 1.0],
        'Salud': ['A tiempo', 'En Riesgo', 'Retrasado', 'A tiempo', 'A tiempo'],
        'Responsable': ['Stif Jara', 'Javier R.', 'F. Penrroz', 'G. Cerda', 'A. Soto']
    }
    df_def = pd.DataFrame(data)
    df_def['Fin'] = df_def.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
    return df_def

df = obtener_datos()

# 3. FILTROS EN SIDEBAR (RESTAURADOS AL 100%)
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Filtros Inteligentes")

escala = st.sidebar.radio("🔍 Zoom Temporal", ["Días", "Semanas", "Meses"])

# Filtros dinámicos basados en los datos cargados
fase_sel = st.sidebar.multiselect("Filtrar por Fase", df['Fase'].unique(), default=df['Fase'].unique())
sede_sel = st.sidebar.multiselect("Filtrar por Sede", df['Sede'].unique(), default=df['Sede'].unique())
tec_sel = st.sidebar.multiselect("Filtrar por Tecnología", df['Tecnología'].unique(), default=df['Tecnología'].unique())
resp_sel = st.sidebar.multiselect("Filtrar por Responsable", df['Responsable'].unique(), default=df['Responsable'].unique())

# Aplicación de los 4 filtros
df_filt = df[
    (df['Fase'].isin(fase_sel)) & 
    (df['Sede'].isin(sede_sel)) & 
    (df['Tecnología'].isin(tec_sel)) &
    (df['Responsable'].isin(resp_sel))
]

# 4. DASHBOARD DE MÉTRICAS (KPIs)
st.title("📊 Executive Insight: Gestión PMO")
k1, k2, k3, k4 = st.columns(4)
with k1:
    prog = df_filt['Progreso'].mean() if not df_filt.empty else 0
    st.metric("Progreso Global", f"{prog:.1%}")
with k2:
    alertas = len(df_filt[df_filt['Salud'] == 'Retrasado'])
    st.metric("Alertas Críticas", alertas, delta=f"{alertas} Riesgos", delta_color="inverse")
with k3:
    st.metric("Sedes Impactadas", len(df_filt['Sede'].unique()))
with k4:
    st.metric("Total Actividades", len(df_filt))

# 5. CARTA GANTT CON ZOOM Y FINES DE SEMANA
st.markdown("---")
st.subheader(f"Cronograma Maestro - Visualización por {escala}")

if not df_filt.empty:
    # Lógica de escala para el Zoom
    if escala == "Días":
        t_format, t_tick, mostrar_finde = "%d %b", "D1", True
    elif escala == "Semanas":
        t_format, t_tick, mostrar_finde = "Sem %W", 604800000.0, True
    else: # Meses
        t_format, t_tick, mostrar_finde = "%B %Y", "M1", False

    fig = px.timeline(
        df_filt, x_start="Inicio", x_end="Fin", y="Actividad",
        color="Salud", text="Sede",
        hover_data=["Responsable", "Tecnología", "Fase", "Dias", "Progreso"],
        color_discrete_map={
            "A tiempo": "#0055A4", "En Riesgo": "#D1D5DB", "Retrasado": "#FF0000"
        }
    )

    fig.update_yaxes(autorange="reversed", title="")

    # Sombreado de Fines de Semana
    if mostrar_finde:
        min_d, max_d = df_filt['Inicio'].min() - timedelta(days=2), df_filt['Fin'].max() + timedelta(days=2)
        curr = min_d
        while curr <= max_d:
            if curr.weekday() >= 5:
                fig.add_vrect(x0=curr, x1=curr + timedelta(days=1), fillcolor="gray", opacity=0.12, layer="below", line_width=0)
            curr += timedelta(days=1)

    fig.update_layout(
        xaxis=dict(tickformat=t_format, dtick=t_tick, type='date', gridcolor="#F0F0F0"),
        plot_bgcolor="white", height=500, showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Utilice los filtros laterales para visualizar la información.")

# 6. TABLA DE DETALLE (TODAS LAS COLUMNAS RECUPERADAS)
st.markdown("### Tabla Detallada de Actividades")
# Definimos el orden exacto de todas las columnas iniciales
columnas_finales = ['Fase', 'Actividad', 'Sede', 'Tecnología', 'Responsable', 'Inicio', 'Dias', 'Fin', 'Progreso', 'Salud']
st.dataframe(
    df_filt[columnas_finales].style.format({
        'Progreso': '{:.0%}',
        'Inicio': lambda x: x.strftime('%Y-%m-%d'),
        'Fin': lambda x: x.strftime('%Y-%m-%d')
    }), 
    use_container_width=True
)
