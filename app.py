"""
╔══════════════════════════════════════════════════════════════╗
║  GTD Telecomunicaciones — Dashboard Ejecutivo PMO            ║
║  Control Semanal · MMOO · Starlink · Fibra Óptica            ║
║  Ejecutar: streamlit run app.py                              ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
import math

# ══════════════════════════════════════════════════════════════
#  PALETA CORPORATIVA GTD
# ══════════════════════════════════════════════════════════════
GTD = {
    "navy":      "#042C53",
    "navy_m":    "#0C447C",
    "blue":      "#0055A4",
    "blue_m":    "#378ADD",
    "blue_l":    "#B5D4F4",
    "blue_xl":   "#E6F1FB",
    "gray_dk":   "#2C2C2A",
    "gray_m":    "#5F5E5A",
    "gray_s":    "#888780",
    "gray_l":    "#D3D1C7",
    "gray_xl":   "#F1EFE8",
    "white":     "#FFFFFF",
    "gantt_bg":  "#D9D9D9",   # barra base gris
    "gantt_ok":  "#0055A4",   # progreso azul GTD
    "gantt_red": "#C0392B",   # retrasado rojo
    "gantt_wkd": "#ECEAE3",   # fin de semana
    "green":     "#1E8449",
    "green_l":   "#D5F5E3",
    "amber":     "#E67E22",
    "amber_l":   "#FDEBD0",
    "red":       "#C0392B",
    "red_l":     "#FADBD8",
}

# ══════════════════════════════════════════════════════════════
#  BASE DE DATOS INTERNA — 10 Proyectos Telecom Chile
# ══════════════════════════════════════════════════════════════
def cargar_datos() -> pd.DataFrame:
    hoy  = date.today()
    base = hoy - timedelta(days=18)

    def fi(n):  return base + timedelta(days=n)
    def ff(f, d): return f + timedelta(days=d - 1)

    registros = [
        {
            "Fase":            "Inicio",
            "Actividades":     "Levantamiento FO Quinta Normal",
            "Sede":            "Quinta Normal",
            "Tecnologías":     "Fibra Óptica",
            "Fecha Inicio":    fi(0),
            "Días":            5,
            "Progreso":        1.00,
            "Sitio":           "Santiago",
            "Responsable":     "Fabián Penrroz",
            "Estado de Salud": "A tiempo",
        },
        {
            "Fase":            "Inicio",
            "Actividades":     "Inspección Técnica Maipú",
            "Sede":            "Maipú",
            "Tecnologías":     "MMOO",
            "Fecha Inicio":    fi(2),
            "Días":            3,
            "Progreso":        1.00,
            "Sitio":           "Maipú",
            "Responsable":     "Rodrigo Alarcón",
            "Estado de Salud": "A tiempo",
        },
        {
            "Fase":            "Planificación",
            "Actividades":     "Diseño Red MMOO Sector Norte",
            "Sede":            "Quinta Normal",
            "Tecnologías":     "MMOO",
            "Fecha Inicio":    fi(3),
            "Días":            8,
            "Progreso":        0.70,
            "Sitio":           "Santiago",
            "Responsable":     "Fabián Penrroz",
            "Estado de Salud": "En Riesgo",
        },
        {
            "Fase":            "Planificación",
            "Actividades":     "Config. Enlace Starlink Peñalolén",
            "Sede":            "Peñalolén",
            "Tecnologías":     "Starlink",
            "Fecha Inicio":    fi(4),
            "Días":            6,
            "Progreso":        0.50,
            "Sitio":           "Peñalolén",
            "Responsable":     "Erika Ibarra",
            "Estado de Salud": "En Riesgo",
        },
        {
            "Fase":            "Ejecución",
            "Actividades":     "Montaje Antena Starlink Maipú",
            "Sede":            "Maipú",
            "Tecnologías":     "Starlink",
            "Fecha Inicio":    fi(6),
            "Días":            9,
            "Progreso":        0.40,
            "Sitio":           "Maipú",
            "Responsable":     "Rodrigo Alarcón",
            "Estado de Salud": "A tiempo",
        },
        {
            "Fase":            "Ejecución",
            "Actividades":     "Tendido FO Troncal Sector Sur",
            "Sede":            "Quinta Normal",
            "Tecnologías":     "Fibra Óptica",
            "Fecha Inicio":    fi(5),
            "Días":            12,
            "Progreso":        0.00,
            "Sitio":           "Santiago",
            "Responsable":     "Fabián Penrroz",
            "Estado de Salud": "Retrasado",
        },
        {
            "Fase":            "Ejecución",
            "Actividades":     "Instalación Router MPLS Central",
            "Sede":            "Santiago Centro",
            "Tecnologías":     "MPLS",
            "Fecha Inicio":    fi(8),
            "Días":            6,
            "Progreso":        0.00,
            "Sitio":           "Santiago",
            "Responsable":     "Erika Ibarra",
            "Estado de Salud": "Retrasado",
        },
        {
            "Fase":            "Ejecución",
            "Actividades":     "Configuración Firewall Fortinet",
            "Sede":            "Maipú",
            "Tecnologías":     "Fortinet",
            "Fecha Inicio":    fi(10),
            "Días":            5,
            "Progreso":        0.20,
            "Sitio":           "Maipú",
            "Responsable":     "Rodrigo Alarcón",
            "Estado de Salud": "A tiempo",
        },
        {
            "Fase":            "Cierre",
            "Actividades":     "Certificación Enlace MMOO Torre A",
            "Sede":            "Peñalolén",
            "Tecnologías":     "MMOO",
            "Fecha Inicio":    fi(14),
            "Días":            4,
            "Progreso":        0.00,
            "Sitio":           "Peñalolén",
            "Responsable":     "Fabián Penrroz",
            "Estado de Salud": "A tiempo",
        },
        {
            "Fase":            "Cierre",
            "Actividades":     "Entrega y Cierre Técnico Proyecto",
            "Sede":            "Santiago Centro",
            "Tecnologías":     "MMOO",
            "Fecha Inicio":    fi(17),
            "Días":            3,
            "Progreso":        0.00,
            "Sitio":           "Santiago",
            "Responsable":     "Erika Ibarra",
            "Estado de Salud": "A tiempo",
        },
    ]

    df = pd.DataFrame(registros)
    df["Fecha Final"]        = df.apply(lambda r: r["Fecha Inicio"] + timedelta(days=r["Días"] - 1), axis=1)
    df["Días Completados"]   = (df["Días"] * df["Progreso"]).round(1)
    df["Fecha Inicio"]       = pd.to_datetime(df["Fecha Inicio"])
    df["Fecha Final"]        = pd.to_datetime(df["Fecha Final"])
    return df


# ══════════════════════════════════════════════════════════════
#  CONFIGURACIÓN STREAMLIT
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="GTD · Dashboard PMO",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personalizado GTD
st.markdown(f"""
<style>
    /* Fuente base */
    html, body, [class*="css"] {{
        font-family: 'Segoe UI', Arial, sans-serif;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {GTD['navy']};
    }}
    [data-testid="stSidebar"] * {{
        color: {GTD['white']} !important;
    }}
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {{
        color: {GTD['blue_l']} !important;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    /* Header principal */
    .gtd-header {{
        background: linear-gradient(135deg, {GTD['navy']} 0%, {GTD['navy_m']} 100%);
        padding: 20px 28px 16px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    .gtd-header h1 {{
        color: {GTD['white']};
        font-size: 22px;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.02em;
    }}
    .gtd-header p {{
        color: {GTD['blue_l']};
        font-size: 12px;
        margin: 4px 0 0;
    }}

    /* KPI cards */
    .kpi-card {{
        background: {GTD['white']};
        border-radius: 10px;
        padding: 16px 20px;
        border-left: 5px solid {GTD['blue']};
        box-shadow: 0 2px 8px rgba(4,44,83,0.08);
    }}
    .kpi-card.red   {{ border-left-color: {GTD['red']};   background: {GTD['red_l']}; }}
    .kpi-card.amber {{ border-left-color: {GTD['amber']}; background: {GTD['amber_l']}; }}
    .kpi-card.green {{ border-left-color: {GTD['green']}; background: {GTD['green_l']}; }}
    .kpi-label {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {GTD['gray_m']};
        margin-bottom: 4px;
    }}
    .kpi-value {{
        font-size: 32px;
        font-weight: 800;
        color: {GTD['navy']};
        line-height: 1.1;
    }}
    .kpi-value.red   {{ color: {GTD['red']};   }}
    .kpi-value.green {{ color: {GTD['green']}; }}
    .kpi-sub {{
        font-size: 11px;
        color: {GTD['gray_s']};
        margin-top: 3px;
    }}

    /* Badge de estado */
    .badge {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
    }}
    .badge-ok     {{ background:{GTD['green_l']}; color:{GTD['green']}; }}
    .badge-risk   {{ background:{GTD['amber_l']}; color:{GTD['amber']}; }}
    .badge-late   {{ background:{GTD['red_l']};   color:{GTD['red']};   }}

    /* Sección Gantt */
    .section-title {{
        font-size: 13px;
        font-weight: 700;
        color: {GTD['navy']};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        border-bottom: 2px solid {GTD['blue']};
        padding-bottom: 6px;
        margin-bottom: 12px;
    }}

    /* Tabla de detalle */
    .stDataFrame {{ border-radius: 8px; overflow: hidden; }}

    /* Quitar padding superior de main */
    .block-container {{ padding-top: 1.5rem !important; }}

    /* Radio buttons escala */
    div[data-testid="stHorizontalBlock"] .stRadio > div {{
        flex-direction: row;
        gap: 8px;
    }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  CARGA DE DATOS
# ══════════════════════════════════════════════════════════════
df_master = cargar_datos()


# ══════════════════════════════════════════════════════════════
#  SIDEBAR — Filtros
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 10px 0 20px;">
        <div style="font-size:28px;">📡</div>
        <div style="font-size:15px; font-weight:700; color:{GTD['white']};">GTD Telecomunicaciones</div>
        <div style="font-size:11px; color:{GTD['blue_l']};">Dashboard Ejecutivo PMO</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div style='font-size:10px;font-weight:700;color:{GTD['blue_l']};letter-spacing:.1em;text-transform:uppercase;margin-bottom:14px;'>Filtros de vista</div>", unsafe_allow_html=True)

    def opciones(col, todo="Todos"):
        return [todo] + sorted(df_master[col].unique().tolist())

    f_fase   = st.selectbox("📋 Fase",        opciones("Fase"))
    f_sede   = st.selectbox("📍 Sede",        opciones("Sede"))
    f_tecn   = st.selectbox("🔧 Tecnología",  opciones("Tecnologías"))
    f_resp   = st.selectbox("👤 Responsable", opciones("Responsable"))

    st.markdown("---")
    st.markdown(f"<div style='font-size:10px;font-weight:700;color:{GTD['blue_l']};letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px;'>Escala de tiempo</div>", unsafe_allow_html=True)
    escala = st.radio("", ["Días", "Semanas", "Meses"], horizontal=False, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"<div style='font-size:10px;color:{GTD['gray_s']};'>Actualizado: {date.today().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  APLICAR FILTROS
# ══════════════════════════════════════════════════════════════
df = df_master.copy()
if f_fase != "Todos": df = df[df["Fase"]          == f_fase]
if f_sede != "Todos": df = df[df["Sede"]          == f_sede]
if f_tecn != "Todos": df = df[df["Tecnologías"]   == f_tecn]
if f_resp != "Todos": df = df[df["Responsable"]   == f_resp]


# ══════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="gtd-header">
    <h1>📊 Dashboard Ejecutivo — Control de Proyectos de Infraestructura</h1>
    <p>MMOO · Starlink · Fibra Óptica &nbsp;|&nbsp; {date.today().strftime('%A %d de %B de %Y').capitalize()}</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  KPIs
# ══════════════════════════════════════════════════════════════
def calcular_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"avance": 0, "retrasadas": 0, "en_riesgo": 0,
                "completadas": 0, "total": 0, "hito": "—", "hito_fecha": "—"}

    avance    = round((df["Progreso"] * df["Días"]).sum() / df["Días"].sum() * 100, 1) if df["Días"].sum() > 0 else 0
    retrasadas= int((df["Estado de Salud"] == "Retrasado").sum())
    en_riesgo = int((df["Estado de Salud"] == "En Riesgo").sum())
    completadas= int((df["Progreso"] == 1.0).sum())
    total     = len(df)

    pendientes = df[df["Progreso"] == 0].copy()
    if not pendientes.empty:
        idx    = pendientes["Fecha Final"].idxmin()
        hito   = pendientes.loc[idx, "Actividades"]
        hfecha = pendientes.loc[idx, "Fecha Final"].strftime("%d/%m/%Y")
    else:
        hito   = "Sin pendientes"
        hfecha = "—"

    return {"avance": avance, "retrasadas": retrasadas, "en_riesgo": en_riesgo,
            "completadas": completadas, "total": total, "hito": hito, "hito_fecha": hfecha}

kpi = calcular_kpis(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    cls = "green" if kpi["avance"] >= 70 else ("amber" if kpi["avance"] >= 40 else "red")
    st.markdown(f"""
    <div class="kpi-card {cls}">
        <div class="kpi-label">% Avance total</div>
        <div class="kpi-value {cls}">{kpi['avance']}%</div>
        <div class="kpi-sub">{kpi['completadas']} de {kpi['total']} actividades completadas</div>
    </div>""", unsafe_allow_html=True)

with col2:
    cls2 = "red" if kpi["retrasadas"] > 0 else ""
    st.markdown(f"""
    <div class="kpi-card {'red' if kpi['retrasadas'] > 0 else ''}">
        <div class="kpi-label">Alertas críticas</div>
        <div class="kpi-value {'red' if kpi['retrasadas'] > 0 else ''}">{kpi['retrasadas']}</div>
        <div class="kpi-sub">Tareas en estado Retrasado</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card {'amber' if kpi['en_riesgo'] > 0 else ''}">
        <div class="kpi-label">En Riesgo</div>
        <div class="kpi-value" style="color:{'#E67E22' if kpi['en_riesgo'] > 0 else '#0C447C'};">{kpi['en_riesgo']}</div>
        <div class="kpi-sub">Tareas que requieren atención</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Próximo hito</div>
        <div style="font-size:13px;font-weight:700;color:{GTD['navy']};line-height:1.4;margin:4px 0;">{kpi['hito']}</div>
        <div class="kpi-sub">📅 Vence: {kpi['hito_fecha']}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  CARTA GANTT (Plotly)
# ══════════════════════════════════════════════════════════════
def construir_gantt(df: pd.DataFrame, escala: str) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Sin datos para la selección actual.",
                           xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=16, color=GTD["gray_m"]))
        fig.update_layout(height=200, paper_bgcolor=GTD["white"],
                          plot_bgcolor=GTD["gray_xl"])
        return fig

    fecha_min = df["Fecha Inicio"].min()
    fecha_max = df["Fecha Final"].max()

    # Generar ticks del eje X según escala
    def generar_ticks(f_min, f_max, escala):
        ticks, labels = [], []
        cur = f_min
        i   = 1
        while cur <= f_max + timedelta(days=7):
            ticks.append(cur)
            if escala == "Días":
                labels.append(f"D{i}<br>{cur.strftime('%d/%m')}")
                cur += timedelta(days=1)
            elif escala == "Semanas":
                labels.append(f"S{i}<br>{cur.strftime('%d/%m')}")
                cur += timedelta(weeks=1)
            else:  # Meses
                labels.append(cur.strftime("%b %Y"))
                mes = cur.month + 1 if cur.month < 12 else 1
                ano = cur.year if cur.month < 12 else cur.year + 1
                cur = cur.replace(year=ano, month=mes, day=1)
            i += 1
        return ticks, labels

    ticks, tick_labels = generar_ticks(fecha_min, fecha_max, escala)

    # Calcular fines de semana del período
    fds_shapes = []
    cur = fecha_min
    while cur <= fecha_max + timedelta(days=1):
        if cur.weekday() == 5:  # sábado
            fds_shapes.append(dict(
                type="rect", xref="x", yref="paper",
                x0=cur, x1=cur + timedelta(days=2),
                y0=0, y1=1,
                fillcolor=GTD["gantt_wkd"],
                opacity=0.6, layer="below", line_width=0
            ))
        cur += timedelta(days=1)

    # Línea de hoy
    hoy = pd.Timestamp(date.today())
    fds_shapes.append(dict(
        type="line", xref="x", yref="paper",
        x0=hoy, x1=hoy, y0=0, y1=1,
        line=dict(color=GTD["gantt_red"], width=2, dash="dot")
    ))

    fig = go.Figure()

    for _, row in df.iterrows():
        fi     = row["Fecha Inicio"]
        ff     = row["Fecha Final"]
        prog   = row["Progreso"]
        estado = row["Estado de Salud"]
        act    = row["Actividades"]
        sede   = row["Sede"]
        fase   = row["Fase"]
        resp   = row["Responsable"]
        dur    = max((ff - fi).days + 1, 1)

        # Colores según estado
        if estado == "Retrasado":
            color_barra = GTD["gantt_red"]
            color_prog  = "#8B1A1A"
        elif estado == "En Riesgo":
            color_barra = "#F0A500"
            color_prog  = "#B87700"
        else:
            color_barra = GTD["gantt_bg"]
            color_prog  = GTD["gantt_ok"]

        # Barra base (duración total)
        fig.add_trace(go.Bar(
            name="",
            x=[dur],
            y=[act],
            base=[fi],
            orientation="h",
            marker=dict(color=color_barra, line=dict(color="rgba(0,0,0,0.1)", width=0.5)),
            width=0.55,
            showlegend=False,
            hovertemplate=(
                f"<b>{act}</b><br>"
                f"Sede: {sede}<br>"
                f"Fase: {fase}<br>"
                f"Responsable: {resp}<br>"
                f"Inicio: {fi.strftime('%d/%m/%Y')}<br>"
                f"Fin: {ff.strftime('%d/%m/%Y')}<br>"
                f"Duración: {dur} días<br>"
                f"Estado: {estado}<br>"
                "<extra></extra>"
            )
        ))

        # Barra de progreso (superpuesta)
        dur_prog = dur * prog
        if dur_prog > 0:
            fig.add_trace(go.Bar(
                name="",
                x=[dur_prog],
                y=[act],
                base=[fi],
                orientation="h",
                marker=dict(color=color_prog, opacity=0.92),
                width=0.55,
                showlegend=False,
                hovertemplate=(
                    f"<b>{act}</b><br>"
                    f"Progreso: {prog*100:.0f}%<br>"
                    f"Días completados: {dur_prog:.1f}<br>"
                    "<extra></extra>"
                )
            ))

        # Etiqueta de porcentaje dentro de la barra
        mid = fi + timedelta(days=dur / 2)
        fig.add_annotation(
            x=mid, y=act,
            text=f"{int(prog*100)}%",
            showarrow=False,
            font=dict(size=10, color=GTD["white"] if prog > 0.25 or estado=="Retrasado" else GTD["gray_dk"],
                      family="Segoe UI"),
            xanchor="center", yanchor="middle",
        )

    # Layout
    alto = max(300, len(df) * 52 + 120)

    fig.update_layout(
        barmode="overlay",
        height=alto,
        margin=dict(l=10, r=20, t=10, b=60),
        paper_bgcolor=GTD["white"],
        plot_bgcolor=GTD["white"],
        xaxis=dict(
            type="date",
            range=[fecha_min - timedelta(days=1), fecha_max + timedelta(days=3)],
            tickvals=ticks,
            ticktext=tick_labels,
            tickfont=dict(size=10, color=GTD["gray_dk"], family="Segoe UI"),
            gridcolor=GTD["gray_l"],
            gridwidth=0.5,
            showgrid=True,
            zeroline=False,
            showline=True,
            linecolor=GTD["gray_l"],
        ),
        yaxis=dict(
            tickfont=dict(size=11, color=GTD["gray_dk"], family="Segoe UI"),
            gridcolor="rgba(0,0,0,0)",
            showgrid=False,
            autorange="reversed",
            showline=False,
        ),
        shapes=fds_shapes,
        font=dict(family="Segoe UI"),
        hoverlabel=dict(
            bgcolor=GTD["navy"],
            font_size=12,
            font_family="Segoe UI",
            font_color=GTD["white"],
        ),
    )

    # Anotación línea de hoy
    fig.add_annotation(
        x=hoy, y=0, yref="paper",
        text="HOY",
        showarrow=False,
        yanchor="bottom",
        font=dict(size=9, color=GTD["gantt_red"], family="Segoe UI"),
        xanchor="center",
    )

    return fig


# ── Encabezado sección Gantt
st.markdown(f"""
<div class="section-title">
    📅 Carta Gantt Interactiva — Escala: {escala}
    &nbsp;&nbsp;
    <span style="font-size:11px;font-weight:400;color:{GTD['gray_m']};">
        ({len(df)} actividades · {f_sede if f_sede!='Todos' else 'Todas las sedes'})
    </span>
</div>
""", unsafe_allow_html=True)

# Leyenda de colores
leg_col1, leg_col2, leg_col3, leg_col4, _ = st.columns([1,1,1,1,4])
with leg_col1:
    st.markdown(f"<span style='font-size:11px;'>⬛ <span style='background:{GTD['gantt_bg']};padding:2px 8px;border-radius:3px;font-size:10px;'>&nbsp;&nbsp;&nbsp;</span> Duración total</span>", unsafe_allow_html=True)
with leg_col2:
    st.markdown(f"<span style='font-size:11px;'>🟦 <span style='background:{GTD['gantt_ok']};padding:2px 8px;border-radius:3px;font-size:10px;'>&nbsp;&nbsp;&nbsp;</span> Progreso</span>", unsafe_allow_html=True)
with leg_col3:
    st.markdown(f"<span style='font-size:11px;'>🔴 <span style='background:{GTD['gantt_red']};padding:2px 8px;border-radius:3px;font-size:10px;'>&nbsp;&nbsp;&nbsp;</span> Retrasado</span>", unsafe_allow_html=True)
with leg_col4:
    st.markdown(f"<span style='font-size:11px;'>🟡 <span style='background:#F0A500;padding:2px 8px;border-radius:3px;font-size:10px;'>&nbsp;&nbsp;&nbsp;</span> En Riesgo</span>", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)

# Renderizar Gantt
fig_gantt = construir_gantt(df, escala)
st.plotly_chart(fig_gantt, use_container_width=True, config={
    "displayModeBar": True,
    "modeBarButtonsToRemove": ["select2d","lasso2d","autoScale2d"],
    "displaylogo": False,
    "toImageButtonOptions": {
        "format": "png",
        "filename": f"GTD_Gantt_{date.today().isoformat()}",
        "scale": 2,
    }
})


# ══════════════════════════════════════════════════════════════
#  TABLA DETALLE
# ══════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
st.markdown(f'<div class="section-title">📋 Detalle de Actividades</div>', unsafe_allow_html=True)

if not df.empty:
    def badge_estado(est):
        cls = {"A tiempo": "badge-ok", "En Riesgo": "badge-risk", "Retrasado": "badge-late"}.get(est, "")
        return f'<span class="badge {cls}">{est}</span>'

    def barra_prog(p):
        color = GTD["gantt_red"] if p == 0 else GTD["gantt_ok"]
        return (f'<div style="background:{GTD["gantt_bg"]};border-radius:4px;height:14px;width:100%;">'
                f'<div style="background:{color};width:{p*100:.0f}%;height:100%;border-radius:4px;"></div>'
                f'</div><div style="font-size:10px;color:{GTD["gray_m"]};text-align:center;">{p*100:.0f}%</div>')

    df_tabla = df[[
        "Fase","Actividades","Sede","Tecnologías",
        "Fecha Inicio","Fecha Final","Días","Progreso","Responsable","Estado de Salud"
    ]].copy()
    df_tabla["Fecha Inicio"] = df_tabla["Fecha Inicio"].dt.strftime("%d/%m/%Y")
    df_tabla["Fecha Final"]  = df_tabla["Fecha Final"].dt.strftime("%d/%m/%Y")
    df_tabla["Progreso"]     = (df_tabla["Progreso"] * 100).round(0).astype(int).astype(str) + "%"

    # Estilo con colores por estado
    def highlight_row(row):
        est = row["Estado de Salud"]
        if est == "Retrasado": bg = "#FADBD8"
        elif est == "En Riesgo": bg = "#FDEBD0"
        else: bg = ""
        return [f"background-color: {bg}" for _ in row]

    styled = df_tabla.style\
        .apply(highlight_row, axis=1)\
        .set_properties(**{
            "font-size": "12px",
            "font-family": "Segoe UI",
        })\
        .set_table_styles([{
            "selector": "th",
            "props": [
                ("background-color", GTD["navy"]),
                ("color", GTD["white"]),
                ("font-size", "11px"),
                ("font-weight", "700"),
                ("text-transform", "uppercase"),
                ("letter-spacing", "0.05em"),
            ]
        }])

    st.dataframe(styled, use_container_width=True, height=380)
else:
    st.info("No hay actividades para la selección de filtros actual.")


# ══════════════════════════════════════════════════════════════
#  GRÁFICOS DE RESUMEN
# ══════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
st.markdown(f'<div class="section-title">📊 Resumen Ejecutivo</div>', unsafe_allow_html=True)

if not df.empty:
    col_g1, col_g2, col_g3 = st.columns(3)

    # Gráfico 1: Distribución por Estado de Salud
    with col_g1:
        conteo_estado = df["Estado de Salud"].value_counts().reset_index()
        conteo_estado.columns = ["Estado", "Cantidad"]
        colores_estado = {
            "A tiempo":  GTD["green"],
            "En Riesgo": GTD["amber"],
            "Retrasado": GTD["red"],
        }
        fig1 = go.Figure(go.Pie(
            labels=conteo_estado["Estado"],
            values=conteo_estado["Cantidad"],
            marker_colors=[colores_estado.get(e, GTD["gray_s"]) for e in conteo_estado["Estado"]],
            hole=0.55,
            textfont=dict(family="Segoe UI", size=12),
            hovertemplate="<b>%{label}</b><br>%{value} tareas (%{percent})<extra></extra>",
        ))
        fig1.update_layout(
            title=dict(text="Estado de Salud", font=dict(size=13, color=GTD["navy"], family="Segoe UI"), x=0.5),
            showlegend=True,
            legend=dict(font=dict(size=11, family="Segoe UI")),
            margin=dict(t=40, b=10, l=10, r=10),
            height=260,
            paper_bgcolor=GTD["white"],
        )
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    # Gráfico 2: Avance por Fase
    with col_g2:
        avance_fase = df.groupby("Fase").apply(
            lambda g: round((g["Progreso"] * g["Días"]).sum() / g["Días"].sum() * 100, 1)
            if g["Días"].sum() > 0 else 0
        ).reset_index()
        avance_fase.columns = ["Fase", "Avance"]
        orden_fase = ["Inicio", "Planificación", "Ejecución", "Cierre"]
        avance_fase["Fase"] = pd.Categorical(avance_fase["Fase"], categories=orden_fase, ordered=True)
        avance_fase = avance_fase.sort_values("Fase")

        fig2 = go.Figure(go.Bar(
            x=avance_fase["Avance"],
            y=avance_fase["Fase"],
            orientation="h",
            marker=dict(
                color=[GTD["blue"] if a >= 50 else GTD["amber"] for a in avance_fase["Avance"]],
                line=dict(color="rgba(0,0,0,0.1)", width=0.5)
            ),
            text=[f"{a}%" for a in avance_fase["Avance"]],
            textposition="outside",
            textfont=dict(size=11, family="Segoe UI"),
            hovertemplate="<b>%{y}</b><br>Avance: %{x}%<extra></extra>",
        ))
        fig2.update_layout(
            title=dict(text="Avance por Fase", font=dict(size=13, color=GTD["navy"], family="Segoe UI"), x=0.5),
            xaxis=dict(range=[0, 115], showgrid=True, gridcolor=GTD["gray_l"],
                       ticksuffix="%", tickfont=dict(size=10, family="Segoe UI")),
            yaxis=dict(tickfont=dict(size=11, family="Segoe UI")),
            margin=dict(t=40, b=10, l=10, r=30),
            height=260,
            paper_bgcolor=GTD["white"],
            plot_bgcolor=GTD["white"],
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # Gráfico 3: Carga por Responsable
    with col_g3:
        carga_resp = df.groupby("Responsable").agg(
            Tareas=("Actividades", "count"),
            Avance_Prom=("Progreso", "mean")
        ).reset_index()
        carga_resp["Avance_Pct"] = (carga_resp["Avance_Prom"] * 100).round(1)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name="Tareas",
            x=carga_resp["Responsable"],
            y=carga_resp["Tareas"],
            marker_color=GTD["navy_m"],
            yaxis="y",
            hovertemplate="<b>%{x}</b><br>Tareas: %{y}<extra></extra>",
        ))
        fig3.add_trace(go.Scatter(
            name="Avance %",
            x=carga_resp["Responsable"],
            y=carga_resp["Avance_Pct"],
            mode="lines+markers",
            marker=dict(color=GTD["gantt_ok"], size=8),
            line=dict(color=GTD["gantt_ok"], width=2),
            yaxis="y2",
            hovertemplate="<b>%{x}</b><br>Avance: %{y}%<extra></extra>",
        ))
        fig3.update_layout(
            title=dict(text="Carga por Responsable", font=dict(size=13, color=GTD["navy"], family="Segoe UI"), x=0.5),
            yaxis=dict(title="N° Tareas", tickfont=dict(size=10, family="Segoe UI"),
                       gridcolor=GTD["gray_l"]),
            yaxis2=dict(title="Avance %", overlaying="y", side="right",
                        range=[0,110], ticksuffix="%",
                        tickfont=dict(size=10, family="Segoe UI")),
            legend=dict(font=dict(size=10, family="Segoe UI"),
                        orientation="h", y=-0.25),
            margin=dict(t=40, b=30, l=10, r=40),
            height=260,
            paper_bgcolor=GTD["white"],
            plot_bgcolor=GTD["white"],
            xaxis=dict(tickfont=dict(size=10, family="Segoe UI")),
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center; padding:14px; background:{GTD['navy']}; border-radius:8px;
            font-size:11px; color:{GTD['blue_l']};">
    GTD Telecomunicaciones  ·  Dashboard Ejecutivo PMO  ·  MMOO · Starlink · Fibra Óptica
    &nbsp;|&nbsp;  Generado: {date.today().strftime('%d/%m/%Y')}
</div>
""", unsafe_allow_html=True)
