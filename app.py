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

# 2. LÓGICA DE CARGA DE DATOS
def obtener_datos():
    st.sidebar.image("https://www.gtd.cl/images/logo-gtd.png", width=120)
    st.sidebar.title("Panel de Control PMO")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Cargar Proyectos")
    archivo = st.sidebar.file_uploader("Sube tu archivo Excel (.xlsx)", type=["xlsx"])

    if archivo is not None:
        try:
            df_user = pd.read_excel(archivo)
            # Limpieza y formato de fechas
            df_user['Inicio'] = pd.to_datetime(df_user['Inicio'])
            # Si no viene la columna Fin, la calculamos por ti
            if 'Fin' not in df_user.columns:
                df_user['Fin'] = df_user.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
            return df_user
        except Exception as e:
            st.error(f"Error al leer el archivo. Revisa que los encabezados sean correctos. Detalle: {e}")
    
    # DATOS DE PRUEBA (Se muestran si no has subido nada aún)
    df_def = pd.DataFrame({
        'Fase': ['Ejecución', 'Planificación', 'Ejecución'],
        'Actividad': ['Instalación FW Combarbalá', 'Ruta FO Mapocho', 'Nodo Peñalolén'],
        'Sede': ['La Granja', 'Quinta Normal', 'Peñalolén'],
        'Tecnología': ['Fibra', 'Fibra', 'MMOO'],
        'Inicio': pd.to_datetime(['2026-04-01', '2026-04-06', '2026-04-10']),
        'Dias': [4, 5, 15],
        'Progreso': [1.0, 0.2, 0.0],
        'Salud': ['A tiempo', 'En Riesgo', 'Retrasado'],
        'Responsable': ['Stif Jara', 'Javier R.', 'F. Penrroz']
    })
    df_def['Fin'] = df_def.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
    return df_def

df = obtener_datos()

# 3. FILTROS Y ZOOM (LÓGICA DEL EJE X)
escala = st.sidebar.radio("🔍 Zoom del Cronograma", ["Días", "Semanas", "Meses"])
fases_disponibles = df['Fase'].unique()
fase_sel = st.sidebar.multiselect("Filtrar por Fase", fases_disponibles, default=fases_disponibles)

df_filt = df[df['Fase'].isin(fase_sel)]

# 4. DASHBOARD DE MÉTRICAS
st.title("📊 Executive Insight: Gestión de Infraestructura")
k1, k2, k3 = st.columns(3)
with k1:
    progreso_promedio = df_filt['Progreso'].mean() if not df_filt.empty else 0
    st.metric("Progreso Global", f"{progreso_promedio:.1%}")
with k2:
    alertas = len(df_filt[df_filt['Salud'] == 'Retrasado'])
    st.metric("Alertas Críticas", alertas, delta=f"{alertas} Riesgos", delta_color="inverse")
with k3:
    st.metric("Total de Actividades", len(df_filt))

# 5. CARTA GANTT CON SOMBREADO DE FINES DE SEMANA Y ZOOM
st.markdown("---")
if not df_filt.empty:
    # Ajuste dinámico de etiquetas y saltos de cuadrícula
    if escala == "Días":
        t_format, t_tick = "%d %b", "D1"
        mostrar_finde = True
    elif escala == "Semanas":
        t_format, t_tick = "Sem %W", 604800000.0  # 7 días en ms
        mostrar_finde = True
    else: # Meses
        t_format, t_tick = "%B %Y", "M1"
        mostrar_finde = False

    fig = px.timeline(
        df_filt, x_start="Inicio", x_end="Fin", y="Actividad",
        color="Salud", text="Sede",
        hover_data=["Responsable", "Tecnología", "Dias"],
        color_discrete_map={
            "A tiempo": "#0055A4",   # Azul GTD
            "En Riesgo": "#D1D5DB",  # Gris
            "Retrasado": "#FF0000"   # Rojo
        }
    )

    # Invertir eje Y para orden cronológico
    fig.update_yaxes(autorange="reversed", title="")

    # DIBUJAR FINES DE SEMANA (Sombreado Gris)
    if mostrar_finde:
        min_date = df_filt['Inicio'].min() - timedelta(days=2)
        max_date = df_filt['Fin'].max() + timedelta(days=2)
        curr = min_date
        while curr <= max_date:
            if curr.weekday() >= 5: # Sábado=5, Domingo=6
                fig.add_vrect(x0=curr, x1=curr + timedelta(days=1), fillcolor="gray", opacity=0.12, layer="below", line_width=0)
            curr += timedelta(days=1)

    # APLICAR ZOOM AL EJE X
    fig.update_layout(
        xaxis=dict(
            tickformat=t_format, 
            dtick=t_tick, 
            type='date',
            gridcolor="#F0F0F0"
        ),
        plot_bgcolor="white",
        height=500,
        showlegend=True,
        legend_title_text="Salud del Proyecto"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay datos para mostrar con los filtros seleccionados.")

# 6. TABLA DE DATOS
st.markdown("### Detalle de Actividades")
st.dataframe(df_filt.drop(columns=['Fin']), use_container_width=True)
