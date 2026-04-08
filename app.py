import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE ESTILO "EXECUTIVE INSIGHT"
st.set_page_config(page_title="Executive Insight - GTD", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    [data-testid="stSidebar"] { background-color: #0055A4; min-width: 250px; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eef2f6; }
    .css-1offfwp e16nr0p33 { color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE DATOS (Simulación de Infraestructura Abril 2026)
@st.cache_data
def cargar_datos_maestros():
    data = {
        'Fase': ['Inicio', 'Planificación', 'Ejecución', 'Ejecución', 'Cierre', 'Planificación', 'Ejecución', 'Inicio', 'Ejecución', 'Cierre'],
        'Actividad': [
            'Levantamiento Fibra Óptica', 'Permisos Municipales', 'Montaje Antena Starlink', 
            'Fusión de Fibra', 'Pruebas de Velocidad', 'Diseño Red Inalámbrica', 
            'Instalación Radio Enlace', 'Visita Técnica Terreno', 'Canalización Subterránea', 'Entrega de Acta'
        ],
        'Sede': ['Quinta Normal', 'Maipú', 'Concepción', 'Peñalolén', 'Viña del Mar', 'Temuco', 'Los Ángeles', 'Lampa', 'Quilpué', 'Providencia'],
        'Tecnología': ['Fibra', 'Fibra', 'Satelital', 'Fibra', 'MMOO', 'MMOO', 'MMOO', 'Starlink', 'Fibra', 'Multitecnología'],
        'Inicio': pd.to_datetime(['2026-04-01', '2026-04-04', '2026-04-05', '2026-04-06', '2026-04-10', '2026-04-02', '2026-04-07', '2026-04-01', '2026-04-08', '2026-04-12']),
        'Dias': [3, 10, 2, 5, 2, 7, 4, 2, 6, 2],
        'Progreso': [1.0, 0.4, 0.1, 0.6, 0.0, 0.8, 0.2, 1.0, 0.3, 0.0],
        'Salud': ['A tiempo', 'En Riesgo', 'Retrasado', 'A tiempo', 'A tiempo', 'En Riesgo', 'Retrasado', 'A tiempo', 'A tiempo', 'A tiempo'],
        'Responsable': ['Stif Jara', 'A. Soto', 'G. Cerda', 'M. Lara', 'F. Penrroz', 'L. Rojas', 'J. Ramírez', 'A. Soto', 'M. Lara', 'G. Cerda']
    }
    df = pd.DataFrame(data)
    df['Fin'] = df.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
    return df

df = cargar_datos_maestros()

# 3. SIDEBAR (FILTROS)
st.sidebar.image("https://www.gtd.cl/images/logo-gtd.png", width=120)
st.sidebar.title("Panel de Control PMO")

fase_sel = st.sidebar.multiselect("Filtrar Fase", df['Fase'].unique(), default=df['Fase'].unique())
sede_sel = st.sidebar.multiselect("Filtrar Sede", df['Sede'].unique(), default=df['Sede'].unique())
escala = st.sidebar.radio("Escala de Tiempo Dashboard", ["Días", "Semanas", "Meses"])

df_filt = df[(df['Fase'].isin(fase_sel)) & (df['Sede'].isin(sede_sel))]

# 4. DASHBOARD: KPIs SUPERIORES
st.title("📊 Executive Insight: Gestión de Proyectos")
st.markdown("### Dashboard Semanal de Infraestructura")

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Progreso Global", f"{df_filt['Progreso'].mean():.1%}")
with k2:
    criticos = len(df_filt[df_filt['Salud'] == 'Retrasado'])
    st.metric("Alertas Críticas", criticos, delta=f"{criticos} Riesgos", delta_color="inverse")
with k3:
    st.metric("Sedes en Obra", len(df_filt['Sede'].unique()))
with k4:
    st.metric("Total Actividades", len(df_filt))

# 5. CARTA GANTT DINÁMICA
st.markdown("---")
st.subheader(f"Cronograma Maestro - Visualización por {escala}")

if not df_filt.empty:
    # Usamos px.timeline para asegurar que las barras se vean
    fig = px.timeline(
        df_filt, 
        x_start="Inicio", 
        x_end="Fin", 
        y="Actividad",
        color="Salud",
        hover_data=["Sede", "Responsable", "Tecnología"],
        color_discrete_map={
            "A tiempo": "#0055A4",   # Azul GTD
            "En Riesgo": "#D1D5DB",  # Gris Corporativo
            "Retrasado": "#FF0000"   # Rojo Alerta
        },
        text="Sede" # Muestra el nombre de la sede sobre la barra
    )

    # Invertir eje Y (Tareas más recientes arriba)
    fig.update_yaxes(autorange="reversed", title="")

    # LÓGICA DE ESCALA DINÁMICA
    # Configuramos los "ticks" (marcas) del calendario según tu elección
    if escala == "Días":
        tick_format = "%d %b"
        dtick_val = "D1" # Un salto por día
    elif escala == "Semanas":
        tick_format = "Sem %W - %d %b"
        dtick_val = 604800000.0 # Milisegundos en una semana
    else: # Meses
        tick_format = "%B %Y"
        dtick_val = "M1" # Un salto por mes

    fig.update_layout(
        xaxis=dict(
            title="Línea de Tiempo (Abril 2026)",
            tickformat=tick_format,
            dtick=dtick_val,
            gridcolor="#E5E7EB"
        ),
        plot_bgcolor="white",
        height=500,
        showlegend=True,
        legend_title_text="Estado de Salud",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    # Resaltar Fines de Semana
    min_d = df_filt['Inicio'].min()
    max_d = df_filt['Fin'].max()
    curr = min_d
    while curr <= max_d:
        if curr.weekday() >= 5: # Sábado y Domingo
            fig.add_vrect(x0=curr, x1=curr + timedelta(days=1), fillcolor="gray", opacity=0.1, layer="below", line_width=0)
        curr += timedelta(days=1)

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Seleccione al menos una Fase o Sede para visualizar los datos.")

# 6. TABLA DE DETALLE (Dataframe Estilizado)
st.markdown("### Vista de Datos")
st.dataframe(
    df_filt[['Fase', 'Actividad', 'Sede', 'Tecnología', 'Responsable', 'Salud', 'Progreso']].style.format({'Progreso': '{:.0%}'}),
    use_container_width=True
)

# Botón de Descarga
csv = df_filt.to_csv(index=False).encode('utf-8')
st.download_button("📥 Exportar Reporte para Gerencia (CSV)", csv, "reporte_ejecutivo_gtd.csv", "text/csv")
