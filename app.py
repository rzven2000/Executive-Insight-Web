import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Executive Insight - GTD", layout="wide")

# Estilos CSS para el look Ejecutivo y colores GTD
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #0055A4; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS INTERNA (10 Casos Reales Telecom)
@st.cache_data
def cargar_datos():
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
        'Dias': [3, 10, 2, 5, 1, 7, 4, 1, 6, 1],
        'Progreso': [1.0, 0.4, 0.1, 0.6, 0.0, 0.8, 0.2, 1.0, 0.3, 0.0],
        'Responsable': ['J. Pérez', 'A. Soto', 'G. Cerda', 'M. Lara', 'J. Pérez', 'L. Rojas', 'G. Cerda', 'A. Soto', 'M. Lara', 'J. Pérez'],
        'Salud': ['A tiempo', 'En Riesgo', 'Retrasado', 'A tiempo', 'A tiempo', 'En Riesgo', 'Retrasado', 'A tiempo', 'A tiempo', 'A tiempo']
    }
    df = pd.DataFrame(data)
    df['Fin'] = df.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
    return df

df = cargar_datos()

# 3. SIDEBAR (FILTROS / SLICERS)
st.sidebar.image("https://www.gtd.cl/images/logo-gtd.png", width=100) # Logo genérico GTD
st.sidebar.title("Filtros de Gestión")

fase_filt = st.sidebar.multiselect("Filtrar por Fase", options=df['Fase'].unique(), default=df['Fase'].unique())
sede_filt = st.sidebar.multiselect("Filtrar por Sede", options=df['Sede'].unique(), default=df['Sede'].unique())
tec_filt = st.sidebar.multiselect("Filtrar por Tecnología", options=df['Tecnología'].unique(), default=df['Tecnología'].unique())
salud_filt = st.sidebar.multiselect("Estado de Salud", options=df['Salud'].unique(), default=df['Salud'].unique())

escala = st.sidebar.radio("Escala de Tiempo", ["Días", "Semanas", "Meses"])

# Filtrado de Datos
df_filt = df[
    (df['Fase'].isin(fase_filt)) & 
    (df['Sede'].isin(sede_filt)) & 
    (df['Tecnología'].isin(tec_filt)) & 
    (df['Salud'].isin(salud_filt))
]

# 4. DASHBOARD PRINCIPAL
st.title("📊 Executive Insight: Control de Infraestructura")
st.subheader("Dashboard Semanal de Gestión PMO")

# KPIs
col1, col2, col3, col4 = st.columns(4)
avg_prog = df_filt['Progreso'].mean() if not df_filt.empty else 0
retrasados = len(df_filt[df_filt['Salud'] == 'Retrasado'])

col1.metric("Progreso Total", f"{avg_prog:.1%}")
col2.metric("Alertas Críticas", retrasados, delta=-retrasados, delta_color="inverse")
col3.metric("Sedes Activas", len(df_filt['Sede'].unique()))
col4.metric("Tecnologías", len(df_filt['Tecnología'].unique()))

# 5. CARTA GANTT INTERACTIVA (Versión Corregida)
st.markdown("---")
st.write(f"### Cronograma Maestro - Vista por {escala}")

if not df_filt.empty:
    # Usamos px.timeline para que reconozca fechas automáticamente
    fig = px.timeline(
        df_filt, 
        x_start="Inicio", 
        x_end="Fin", 
        y="Actividad",
        color="Salud",
        hover_data=["Sede", "Responsable", "Progreso"],
        color_discrete_map={
            "A tiempo": "#0055A4",   # Azul GTD
            "En Riesgo": "#D9D9D9",  # Gris
            "Retrasado": "#FF0000"   # Rojo Alerta
        }
    )

    # Invertir el eje Y para que la primera tarea aparezca arriba
    fig.update_yaxes(autorange="reversed")

    # Resaltado de Fines de Semana (Sombreado dinámico)
    start_date = df_filt['Inicio'].min()
    end_date = df_filt['Fin'].max()
    curr = start_date
    while curr <= end_date:
        if curr.weekday() >= 5: # 5=Sábado, 6=Domingo
            fig.add_vrect(
                x0=curr, x1=curr + timedelta(days=1), 
                fillcolor="gray", opacity=0.1, 
                layer="below", line_width=0
            )
        curr += timedelta(days=1)

    # Ajuste de escala según selección
    dtick_map = {"Días": "D1", "Semanas": 604800000.0, "Meses": "M1"}
    
    fig.update_layout(
        height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(type='date', dtick=dtick_map[escala], tickformat="%d %b"),
        plot_bgcolor='white',
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")




# 6. TABLA DE DETALLE (Espejo de Excel)
st.write("### Detalle de Actividades")
st.dataframe(df_filt.style.format({'Progreso': '{:.0%}'}), use_container_width=True)

# 7. BOTÓN DE DESCARGA
csv = df_filt.to_csv(index=False).encode('utf-8')
st.download_button("📥 Descargar Reporte en CSV", data=csv, file_name="reporte_gtd.csv", mime="text/csv")
