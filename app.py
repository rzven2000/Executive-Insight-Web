import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import io

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

# 2. FUNCIÓN PARA CREAR PLANTILLA EXCEL (BOTÓN DE AYUDA)
def crear_plantilla_excel():
    output = io.BytesIO()
    # Datos de ejemplo para la plantilla
    df_template = pd.DataFrame({
        'Fase': ['Inicio', 'Planificación', 'Ejecución', 'Cierre'],
        'Actividad': ['Ejemplo: Levantamiento FO', 'Ejemplo: Permisos', 'Ejemplo: Instalación FW', 'Ejemplo: Acta Entrega'],
        'Sede': ['Sede 1', 'Sede 2', 'Sede 3', 'Sede 4'],
        'Tecnología': ['Fibra', 'Fibra', 'MMOO', 'Satelital'],
        'Inicio': ['2026-04-01', '2026-04-05', '2026-04-10', '2026-04-20'],
        'Dias': [2, 5, 3, 1],
        'Progreso': [1.0, 0.5, 0.2, 0.0],
        'Salud': ['A tiempo', 'En Riesgo', 'Retrasado', 'A tiempo'],
        'Responsable': ['Nombre 1', 'Nombre 2', 'Nombre 3', 'Nombre 4']
    })
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_template.to_excel(writer, index=False, sheet_name='Proyectos')
    return output.getvalue()

# 3. LÓGICA DE OBTENCIÓN DE DATOS
def obtener_datos():
    st.sidebar.image("https://www.gtd.cl/images/logo-gtd.png", width=120)
    st.sidebar.title("Panel de Control PMO")
    
    # Botón para descargar plantilla
    st.sidebar.subheader("1. Descargar Formato")
    plantilla = crear_plantilla_excel()
    st.sidebar.download_button(
        label="📥 Bajar Plantilla Excel",
        data=plantilla,
        file_name="plantilla_pmo_gtd.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("2. Subir Datos Actualizados")
    archivo_subido = st.sidebar.file_uploader("Arrastra tu Excel aquí", type=["xlsx"])

    if archivo_subido is not None:
        try:
            df_user = pd.read_excel(archivo_subido)
            df_user['Inicio'] = pd.to_datetime(df_user['Inicio'])
            # Cálculo automático de fecha de fin si no existe
            df_user['Fin'] = df_user.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
            return df_user
        except Exception as e:
            st.error(f"Error en el formato del archivo: {e}")
    
    # Datos por defecto (Vista Inicial)
    data = {
        'Fase': ['Ejecución', 'Planificación'],
        'Actividad': ['Instalación FW Combarbalá', 'Revisión Ruta Mapocho'],
        'Sede': ['La Granja', 'Quinta Normal'],
        'Tecnología': ['Fibra', 'Fibra'],
        'Inicio': pd.to_datetime(['2026-04-01', '2026-04-10']),
        'Dias': [1, 1],
        'Progreso': [1.0, 0.0],
        'Salud': ['A tiempo', 'En Riesgo'],
        'Responsable': ['Stif Jara', 'Javier Ramírez']
    }
    df_def = pd.DataFrame(data)
    df_def['Fin'] = df_def.apply(lambda x: x['Inicio'] + timedelta(days=x['Dias']), axis=1)
    return df_def

df = obtener_datos()

# 4. FILTROS Y ESCALA
fase_sel = st.sidebar.multiselect("Filtrar Fase", df['Fase'].unique(), default=df['Fase'].unique())
sede_sel = st.sidebar.multiselect("Filtrar Sede", df['Sede'].unique(), default=df['Sede'].unique())
escala = st.sidebar.radio("Escala de Tiempo", ["Días", "Semanas", "Meses"])

df_filt = df[(df['Fase'].isin(fase_sel)) & (df['Sede'].isin(sede_sel))]

# 5. DASHBOARD: KPIs
st.title("📊 Executive Insight: Gestión PMO")
k1, k2, k3 = st.columns(3)
with k1:
    st.metric("Progreso Global", f"{df_filt['Progreso'].mean():.1%}" if not df_filt.empty else "0%")
with k2:
    criticos = len(df_filt[df_filt['Salud'] == 'Retrasado'])
    st.metric("Alertas Críticas", criticos, delta=f"{criticos} Riesgos", delta_color="inverse")
with k3:
    st.metric("Total Tareas", len(df_filt))

# 6. CARTA GANTT DINÁMICA
st.markdown("---")
if not df_filt.empty:
    fig = px.timeline(
        df_filt, x_start="Inicio", x_end="Fin", y="Actividad",
        color="Salud", hover_data=["Sede", "Responsable"],
        color_discrete_map={"A tiempo": "#0055A4", "En Riesgo": "#D1D5DB", "Retrasado": "#FF0000"},
        text="Sede"
    )
    fig.update_yaxes(autorange="reversed")
    
    # Ajuste de Escala Dinámica
    t_format, t_tick = ("%d %b", "D1") if escala == "Días" else (("Sem %W", 604800000.0) if escala == "Semanas" else ("%B", "M1"))
    
    fig.update_layout(xaxis=dict(tickformat=t_format, dtick=t_tick, title=""), plot_bgcolor="white", height=450)
    st.plotly_chart(fig, use_container_width=True)

# 7. TABLA DE DETALLE
st.markdown("### Tabla de Actividades")
st.dataframe(df_filt.drop(columns=['Fin']), use_container_width=True)
