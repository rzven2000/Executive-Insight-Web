import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# 1. ESTILO Y CONFIGURACIÓN
st.set_page_config(page_title="Executive Insight - GTD", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    [data-testid="stSidebar"] { background-color: #0055A4; min-width: 250px; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE DATOS Y PLANTILLA
def crear_plantilla_excel():
    output = io.BytesIO()
    df_template = pd.DataFrame({
        'Fase': ['Ejecución', 'Planificación'], 'Actividad': ['Tarea 1', 'Tarea 2'],
        'Sede': ['Sede A', 'Sede B'], 'Tecnología': ['Fibra', 'MMOO'],
        'Inicio': ['2026-04-01', '2026-04-05'], 'Dias': [5, 15],
        'Progreso': [0.5, 0.1], 'Salud': ['A tiempo', 'Retrasado'], 'Responsable': ['Stif Jara', 'Javier R.']
    })
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_template.to_excel(writer, index=False, sheet_name='Data')
    return output.getvalue()

def obtener_datos():
    st.sidebar.image("https://www.gtd.cl/images/logo-gtd.png", width=120)
    st.sidebar.subheader("1. Formato")
    st.sidebar.download_button("📥 Bajar Plantilla", crear_plantilla_excel(), "plantilla_gtd.xlsx")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("2. Cargar Proyectos")
    archivo = st.sidebar.file_uploader("Subir Excel", type=["xlsx"])

    if archivo:
        df_user = pd.read_excel(archivo)
        df_user['Inicio'] = pd.to_datetime(df_user['Inicio'])
        df_user['Fin'] = df_user.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
        return df_user
    
    # Datos iniciales de ejemplo
    df_def = pd.DataFrame({
        'Fase': ['Ejecución']*3, 'Actividad': ['Instalación Combarbalá', 'Ruta Mapocho', 'Nodo Peñalolén'],
        'Sede': ['La Granja', 'Quinta Normal', 'Peñalolén'], 'Tecnología': ['Fibra', 'Fibra', 'MMOO'],
        'Inicio': pd.to_datetime(['2026-04-01', '2026-04-06', '2026-04-10']),
        'Dias': [3, 5, 20], 'Progreso': [1.0, 0.2, 0.0],
        'Salud': ['A tiempo', 'Retrasado', 'En Riesgo'], 'Responsable': ['Stif Jara', 'Javier R.', 'Stif Jara']
    })
    df_def['Fin'] = df_def.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
    return df_def

df = obtener_datos()

# 3. FILTROS Y ESCALA (ZOOM)
escala = st.sidebar.radio("🔍 Zoom del Cronograma (Escala)", ["Días", "Semanas", "Meses"])
fases = st.sidebar.multiselect("Fases", df['Fase'].unique(), default=df['Fase'].unique())
df_filt = df[df['Fase'].isin(fases)]

# 4. DASHBOARD
st.title("📊 Executive Insight: Control Proyectos")
k1, k2, k3 = st.columns(3)
k1.metric("Progreso Medio", f"{df_filt['Progreso'].mean():.1%}" if not df_filt.empty else "0%")
k2.metric("Alertas Críticas", len(df_filt[df_filt['Salud'] == 'Retrasado']))
k3.metric("Total Sedes", len(df_filt['Sede'].unique()))

# 5. CARTA GANTT CON ZOOM ESTRUCTURADO
st.markdown("---")
if not df_filt.empty:
    # Definir parámetros de escala (Zoom)
    if escala == "Días":
        t_format = "%d %b"
        t_tick = "D1"        # Salto de 1 día exacto
        mostrar_finde = True
    elif escala == "Semanas":
        t_format = "Sem %W"
        t_tick = 604800000.0 # Salto de 7 días (milisegundos)
        mostrar_finde = True
    else: # Meses
        t_format = "%B %Y"
        t_tick = "M1"        # Salto de 1 mes
        mostrar_finde = False

    fig = px.timeline(
        df_filt, x_start="Inicio", x_end="Fin", y="Actividad",
        color="Salud", text="Sede",
        hover_data=["Responsable", "Dias"],
        color_discrete_map={"A tiempo": "#0055A4", "En Riesgo": "#D1D5DB", "Retrasado": "#FF0000"}
    )

    # Marcaje de Fines de Semana (Solo si el zoom es Días o Semanas)
    if mostrar_finde:
        min_date = df_filt['Inicio'].min() - timedelta(days=2)
        max_date = df_filt['Fin'].max() + timedelta(days=2)
        curr = min_date
        while curr <= max_date:
            if curr.weekday() >= 5: # 5=Sábado, 6=Domingo
                fig.add_vrect(x0=curr, x1=curr + timedelta(days=1), fillcolor="gray", opacity=0.15, layer="below", line_width=0)
            curr += timedelta(days=1)

    fig.update_yaxes(autorange="reversed", title="")
    fig.update_layout(
        xaxis=dict(
            tickformat=t_format, 
            dtick=t_tick, 
            type='date',
            tickangle=0 if escala != "Días" else -45,
            gridcolor="#EEEEEE"
        ),
        plot_bgcolor="white",
        height=500,
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

# 6. TABLA DETALLE
st.markdown("### Detalle Técnico")
st.dataframe(df_filt.drop(columns=['Fin']), use_container_width=True)
