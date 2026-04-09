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
    "gray_wkd":  "#ECEAE3",
    "white":     "#FFFFFF",
    "gantt_bg":  "#D9D9D9",
    "gantt_ok":  "#0055A4",
    "gantt_red": "#C0392B",
    "green":     "#1E8449",
    "green_l":   "#D5F5E3",
    "amber":     "#E67E22",
    "amber_l":   "#FDEBD0",
    "red":       "#C0392B",
    "red_l":     "#FADBD8",
    "hoy":       "#E74C3C",
}

# ══════════════════════════════════════════════════════════════
#  BASE DE DATOS — 10 Proyectos Telecom Chile
# ══════════════════════════════════════════════════════════════
@st.cache_data
def cargar_datos() -> pd.DataFrame:
    hoy  = date.today()
    base = hoy - timedelta(days=14)

    def fi(n):  return pd.Timestamp(base + timedelta(days=n))
    def ff(f, d): return f + pd.Timedelta(days=d - 1)

    registros = [
        {
            "Fase": "Inicio",
            "Actividades": "Levantamiento FO Quinta Normal",
            "Sede": "Quinta Normal",
            "Tecnologías": "Fibra Óptica",
            "Fecha Inicio": fi(0),
            "Días": 5,
            "Progreso": 1.00,
            "Responsable": "Fabián Penrroz",
            "Estado de Salud": "A tiempo",
        },
        {
            "Fase": "Inicio",
            "Actividades": "Inspección Técnica Maipú",
            "Sede": "Maipú",
            "Tecnologías": "MMOO",
            "Fecha Inicio": fi(2),
            "Días": 3,
            "Progreso": 1.00,
            "Responsable": "Rodrigo Alarcón",
            "Estado de Salud": "A tiempo",
        },
        {
            "Fase": "Planificación",
            "Actividades": "Diseño Red MMOO Sector Norte",
            "Sede": "Quinta Normal",
            "Tecnologías": "MMOO",
            "Fecha Inicio": fi(3),
            "Días": 8,
            "Progreso": 0.70,
            "Responsable": "Fabián Penrroz",
            "Estado de Salud": "En Riesgo",
        },
        {
            "Fase": "Planificación",
            "Actividades": "Config. Enlace Starlink Peñalolén",
            "Sede": "Peñalolén",
            "Tecnologías": "Starlink",
            "Fecha Inicio": fi(4),
            "Días": 6,
            "Progreso": 0.50,
            "Responsable": "Erika Ibarra",
            "Estado de Salud": "En Riesgo",
        },
        {
            "Fase": "Ejecución",
            "Actividades": "Montaje Antena Starlink Maipú",
            "Sede": "Maipú",
            "Tecnologías": "Starlink",
            "Fecha Inicio": fi(6),
            "Días": 9,
            "Progreso": 0.40,
            "Responsable": "Rodrigo Alarcón",
            "Estado de Salud": "A tiempo",
        },
        {
            "Fase": "Ejecución",
            "Actividades": "Tendido FO Troncal Sector Sur",
            "Sede": "Quinta Normal",
            "Tecnologías": "Fibra Óptica",
            "Fecha Inicio": fi(5),
            "Días": 12,
            "Progreso": 0.00,
            "Responsable": "Fabián Penrroz",
            "Estado de Salud": "Retrasado",
        },
        {
            "Fase": "Ejecución",
            "Actividades": "Instalación Router MPLS Central",
            "Sede": "Santiago Centro",
            "Tecnologías": "MPLS",
            "Fecha Inicio": fi(8),
            "Días": 7,
            "Progreso": 0.00,
            "Responsable": "Erika Ibarra",
            "Estado de Salud": "Retrasado",
        },
        {
            "Fase": "Ejecución",
            "Actividades": "Configuración Firewall Fortinet",
            "Sede": "Maipú",
            "Tecnologías": "Fortinet",
            "Fecha Inicio": fi(10),
            "Días": 5,
            "Progreso": 0.20,
            "Responsable": "Rodrigo Alarcón",
            "Estado de Salud": "A tiempo",
        },
        {
            "Fase": "Cierre",
            "Actividades": "Certificación Enlace MMOO Torre A",
            "Sede": "Peñalolén",
            "Tecnologías": "MMOO",
            "Fecha Inicio": fi(14),
            "Días": 4,
            "Progreso": 0.00,
            "Responsable": "Fabián Penrroz",
            "Estado de Salud": "A tiempo",
        },
        {
            "Fase": "Cierre",
            "Actividades": "Entrega y Cierre Técnico Proyecto",
            "Sede": "Santiago Centro",
            "Tecnologías": "MMOO",
            "Fecha Inicio": fi(17),
            "Días": 3,
            "Progreso": 0.00,
            "Responsable": "Erika Ibarra",
            "Estado de Salud": "A tiempo",
        },
    ]

    df = pd.DataFrame(registros)
    df["Fecha Final"] = df.apply(
        lambda r: r["Fecha Inicio"] + pd.Timedelta(days=r["Días"] - 1), axis=1
    )
    df["Días Completados"] = (df["Días"] * df["Progreso"]).round(1)
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

st.markdown(f"""
<style>
  html, body, [class*="css"] {{
      font-family: 'Segoe UI', Arial, sans-serif;
  }}
  [data-testid="stSidebar"] {{
      background-color: {GTD['navy']};
  }}
  [data-testid="stSidebar"] * {{
      color: {GTD['white']} !important;
  }}
  [data-testid="stSidebar"] label {{
      color: {GTD['blue_l']} !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      text-transform: uppercase;
      letter-spacing: .06em;
  }}
  .block-container {{ padding-top: 1.2rem !important; }}

  /* Header */
  .gtd-header {{
      background: {GTD['navy']};
      padding: 18px 24px 14px;
      border-radius: 10px;
      margin-bottom: 18px;
  }}
  .gtd-header h1 {{
      color: {GTD['white']};
      font-size: 20px;
      font-weight: 700;
      margin: 0;
  }}
  .gtd-header p {{
      color: {GTD['blue_l']};
      font-size: 12px;
      margin: 4px 0 0;
  }}

  /* KPI cards */
  .kpi {{
      background: {GTD['white']};
      border-radius: 10px;
      padding: 14px 18px;
      border-left: 5px solid {GTD['blue']};
      box-shadow: 0 1px 6px rgba(4,44,83,.07);
      height: 90px;
  }}
  .kpi.red   {{ border-left-color:{GTD['red']};   background:{GTD['red_l']};   }}
  .kpi.amber {{ border-left-color:{GTD['amber']}; background:{GTD['amber_l']}; }}
  .kpi.green {{ border-left-color:{GTD['green']}; background:{GTD['green_l']}; }}
  .kpi-label {{
      font-size: 10px; font-weight: 700;
      text-transform: uppercase; letter-spacing: .08em;
      color: {GTD['gray_m']}; margin-bottom: 3px;
  }}
  .kpi-value {{
      font-size: 30px; font-weight: 800; color: {GTD['navy']}; line-height: 1.1;
  }}
  .kpi-value.red   {{ color: {GTD['red']};   }}
  .kpi-value.green {{ color: {GTD['green']}; }}
  .kpi-value.amber {{ color: {GTD['amber']}; }}
  .kpi-sub  {{ font-size: 10px; color: {GTD['gray_s']}; margin-top: 2px; }}

  /* Section title */
  .stitle {{
      font-size: 12px; font-weight: 700; color: {GTD['navy']};
      text-transform: uppercase; letter-spacing: .08em;
      border-bottom: 2px solid {GTD['blue']};
      padding-bottom: 5px; margin-bottom: 10px;
  }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  DATOS
# ══════════════════════════════════════════════════════════════
df_master = cargar_datos()


# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:8px 0 18px;">
        <div style="font-size:26px;">📡</div>
        <div style="font-size:14px;font-weight:700;color:{GTD['white']};">GTD Telecomunicaciones</div>
        <div style="font-size:10px;color:{GTD['blue_l']};">Dashboard Ejecutivo PMO</div>
    </div>
    <hr style="border-color:rgba(255,255,255,.15);margin:0 0 14px;">
    """, unsafe_allow_html=True)

    def opts(col):
        return ["Todos"] + sorted(df_master[col].dropna().unique().tolist())

    f_fase = st.selectbox("📋 Fase",        opts("Fase"))
    f_sede = st.selectbox("📍 Sede",        opts("Sede"))
    f_tecn = st.selectbox("🔧 Tecnología",  opts("Tecnologías"))
    f_resp = st.selectbox("👤 Responsable", opts("Responsable"))

    st.markdown("<hr style='border-color:rgba(255,255,255,.15);margin:14px 0;'>", unsafe_allow_html=True)
    escala = st.radio("⏱ Escala de tiempo", ["Días", "Semanas", "Meses"])

    st.markdown(
        f"<div style='font-size:10px;color:{GTD['gray_s']};margin-top:10px;'>"
        f"Actualizado: {date.today().strftime('%d/%m/%Y')}</div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════
#  FILTRAR
# ══════════════════════════════════════════════════════════════
df = df_master.copy()
if f_fase != "Todos": df = df[df["Fase"]         == f_fase]
if f_sede != "Todos": df = df[df["Sede"]         == f_sede]
if f_tecn != "Todos": df = df[df["Tecnologías"]  == f_tecn]
if f_resp != "Todos": df = df[df["Responsable"]  == f_resp]


# ══════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="gtd-header">
  <h1>📊 Dashboard Ejecutivo — Control Semanal de Infraestructura</h1>
  <p>MMOO · Starlink · Fibra Óptica &nbsp;|&nbsp;
     {date.today().strftime('%d de %B de %Y').capitalize()}</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  KPIs
# ══════════════════════════════════════════════════════════════
def kpis(df):
    if df.empty:
        return dict(avance=0, retrasadas=0, riesgo=0, completadas=0,
                    total=0, hito="—", hito_fecha="—")
    total  = len(df)
    avance = 0.0
    if df["Días"].sum() > 0:
        avance = round(
            (df["Progreso"] * df["Días"]).sum() / df["Días"].sum() * 100, 1
        )
    retrasadas  = int((df["Estado de Salud"] == "Retrasado").sum())
    riesgo      = int((df["Estado de Salud"] == "En Riesgo").sum())
    completadas = int((df["Progreso"] == 1.0).sum())

    pend = df[df["Progreso"] == 0]
    if not pend.empty:
        idx    = pend["Fecha Final"].idxmin()
        hito   = pend.loc[idx, "Actividades"]
        hfecha = pend.loc[idx, "Fecha Final"].strftime("%d/%m/%Y")
    else:
        hito, hfecha = "Sin pendientes", "—"

    return dict(avance=avance, retrasadas=retrasadas, riesgo=riesgo,
                completadas=completadas, total=total, hito=hito, hito_fecha=hfecha)

k = kpis(df)

c1, c2, c3, c4 = st.columns(4)

av_cls = "green" if k["avance"] >= 70 else ("amber" if k["avance"] >= 40 else "red")
with c1:
    st.markdown(f"""
    <div class="kpi {av_cls}">
      <div class="kpi-label">% Avance total</div>
      <div class="kpi-value {av_cls}">{k['avance']}%</div>
      <div class="kpi-sub">{k['completadas']}/{k['total']} actividades listas</div>
    </div>""", unsafe_allow_html=True)

with c2:
    rt_cls = "red" if k["retrasadas"] > 0 else ""
    st.markdown(f"""
    <div class="kpi {'red' if k['retrasadas'] > 0 else ''}">
      <div class="kpi-label">Alertas críticas</div>
      <div class="kpi-value {'red' if k['retrasadas'] > 0 else ''}">{k['retrasadas']}</div>
      <div class="kpi-sub">Tareas en estado Retrasado</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi {'amber' if k['riesgo'] > 0 else ''}">
      <div class="kpi-label">En riesgo</div>
      <div class="kpi-value {'amber' if k['riesgo'] > 0 else ''}">{k['riesgo']}</div>
      <div class="kpi-sub">Requieren atención inmediata</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi">
      <div class="kpi-label">Próximo hito</div>
      <div style="font-size:12px;font-weight:700;color:{GTD['navy']};margin:3px 0 2px;
                  line-height:1.3;">{k['hito']}</div>
      <div class="kpi-sub">📅 {k['hito_fecha']}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:22px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  CARTA GANTT
#
#  FIX CLAVE:
#  En Plotly, cuando el eje X es de tipo "date", el parámetro
#  `x` de go.Bar debe ser la FECHA FINAL (no la duración en días).
#  Plotly calcula el ancho de la barra como: x - base.
#  Si se pasa `x=[dur_días]`, Plotly lo interpreta como
#  dur_días milisegundos → barras de ancho invisible.
#  Solución: x=[Fecha_Final], base=[Fecha_Inicio]
# ══════════════════════════════════════════════════════════════
def construir_gantt(df: pd.DataFrame, escala: str) -> go.Figure:
    fig = go.Figure()

    if df.empty:
        fig.add_annotation(
            text="Sin actividades para los filtros seleccionados.",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=15, color=GTD["gray_m"], family="Segoe UI"),
        )
        fig.update_layout(
            height=200,
            paper_bgcolor=GTD["white"],
            plot_bgcolor=GTD["gray_xl"],
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            margin=dict(l=10, r=10, t=10, b=10),
        )
        return fig

    fecha_min = df["Fecha Inicio"].min()
    fecha_max = df["Fecha Final"].max()
    hoy       = pd.Timestamp(date.today())

    # ── Generar ticks del eje X según escala
    def generar_ticks(f_min, f_max, escala):
        ticks, labels = [], []
        cur = f_min
        n   = 1
        lim = f_max + pd.Timedelta(days=10)
        while cur <= lim:
            ticks.append(cur)
            if escala == "Días":
                labels.append(f"D{n}<br>{cur.strftime('%d/%m')}")
                cur += pd.Timedelta(days=1)
            elif escala == "Semanas":
                labels.append(f"S{n}<br>{cur.strftime('%d/%m')}")
                cur += pd.Timedelta(weeks=1)
            else:
                labels.append(cur.strftime("%b %Y"))
                mes = cur.month + 1 if cur.month < 12 else 1
                ano = cur.year if cur.month < 12 else cur.year + 1
                cur = cur.replace(year=ano, month=mes, day=1)
            n += 1
        return ticks, labels

    ticks, tick_labels = generar_ticks(fecha_min, fecha_max, escala)

    # ── Shapes: fines de semana + línea HOY
    shapes = []
    cur = fecha_min.normalize()
    while cur <= fecha_max + pd.Timedelta(days=1):
        if cur.weekday() == 5:   # sábado
            shapes.append(dict(
                type="rect", xref="x", yref="paper",
                x0=cur, x1=cur + pd.Timedelta(days=2),
                y0=0, y1=1,
                fillcolor=GTD["gray_wkd"],
                opacity=0.55, layer="below", line_width=0,
            ))
        cur += pd.Timedelta(days=1)

    shapes.append(dict(
        type="line", xref="x", yref="paper",
        x0=hoy, x1=hoy, y0=0, y1=1,
        line=dict(color=GTD["hoy"], width=2, dash="dot"),
    ))

    # ── Trazas de barras
    # Orden de actividades: invertir para que la primera quede arriba
    df_plot = df.iloc[::-1].reset_index(drop=True)

    for _, row in df_plot.iterrows():
        fi_ts  = row["Fecha Inicio"]         # pd.Timestamp
        ff_ts  = row["Fecha Final"]           # pd.Timestamp
        prog   = float(row["Progreso"])
        estado = row["Estado de Salud"]
        act    = row["Actividades"]
        sede   = row["Sede"]
        fase   = row["Fase"]
        resp   = row["Responsable"]
        dias   = int(row["Días"])

        # Colores por estado de salud
        if estado == "Retrasado":
            c_base = GTD["gantt_red"]
            c_prog = "#8B1A1A"
        elif estado == "En Riesgo":
            c_base = "#F0A500"
            c_prog = "#A06800"
        else:
            c_base = GTD["gantt_bg"]
            c_prog = GTD["gantt_ok"]

        tooltip = (
            f"<b>{act}</b><br>"
            f"Sede: {sede}  ·  Fase: {fase}<br>"
            f"Responsable: {resp}<br>"
            f"Inicio: {fi_ts.strftime('%d/%m/%Y')}<br>"
            f"Fin: {ff_ts.strftime('%d/%m/%Y')}<br>"
            f"Duración: {dias} días<br>"
            f"Progreso: {prog*100:.0f}%<br>"
            f"Estado: <b>{estado}</b><br>"
            "<extra></extra>"
        )

        # ── BARRA BASE (duración total)
        # FIX: x=ff_ts (fecha final), base=fi_ts (fecha inicio)
        # Plotly calcula ancho = ff_ts - fi_ts automáticamente
        fig.add_trace(go.Bar(
            name="",
            x=[ff_ts],          # ← fecha final
            base=[fi_ts],       # ← fecha inicio
            y=[act],
            orientation="h",
            marker=dict(
                color=c_base,
                line=dict(color="rgba(0,0,0,0.12)", width=0.5),
            ),
            width=0.55,
            showlegend=False,
            hovertemplate=tooltip,
        ))

        # ── BARRA DE PROGRESO (superpuesta)
        if prog > 0:
            ff_prog = fi_ts + (ff_ts - fi_ts) * prog
            fig.add_trace(go.Bar(
                name="",
                x=[ff_prog],    # ← fecha hasta donde llega el progreso
                base=[fi_ts],   # ← misma fecha inicio
                y=[act],
                orientation="h",
                marker=dict(color=c_prog, opacity=0.90),
                width=0.55,
                showlegend=False,
                hovertemplate=(
                    f"<b>{act}</b><br>"
                    f"Progreso: {prog*100:.0f}%<br>"
                    f"Días completados: {dias*prog:.1f}<br>"
                    "<extra></extra>"
                ),
            ))

        # ── Etiqueta % en el centro de la barra
        mid_ts = fi_ts + (ff_ts - fi_ts) * 0.5
        txt_col = GTD["white"] if (prog > 0.3 or estado in ("Retrasado","En Riesgo")) else GTD["gray_dk"]
        fig.add_annotation(
            x=mid_ts,
            y=act,
            text=f"<b>{int(prog*100)}%</b>",
            showarrow=False,
            font=dict(size=10, color=txt_col, family="Segoe UI"),
            xanchor="center",
            yanchor="middle",
        )

    # ── Anotación HOY
    fig.add_annotation(
        x=hoy, y=1, yref="paper",
        text="HOY",
        showarrow=False,
        yanchor="bottom",
        font=dict(size=9, color=GTD["hoy"], family="Segoe UI"),
        xanchor="center",
    )

    # ── Layout
    alto = max(320, len(df) * 54 + 100)

    fig.update_layout(
        barmode="overlay",
        height=alto,
        margin=dict(l=10, r=20, t=30, b=50),
        paper_bgcolor=GTD["white"],
        plot_bgcolor=GTD["white"],
        shapes=shapes,
        font=dict(family="Segoe UI"),
        xaxis=dict(
            type="date",
            range=[
                fecha_min - pd.Timedelta(days=1),
                fecha_max + pd.Timedelta(days=4),
            ],
            tickvals=ticks,
            ticktext=tick_labels,
            tickfont=dict(size=10, color=GTD["gray_dk"], family="Segoe UI"),
            gridcolor=GTD["gray_l"],
            gridwidth=0.5,
            showgrid=True,
            zeroline=False,
            showline=True,
            linecolor=GTD["gray_l"],
            fixedrange=False,
        ),
        yaxis=dict(
            tickfont=dict(size=11, color=GTD["gray_dk"], family="Segoe UI"),
            showgrid=False,
            autorange=True,          # La inversión la maneja el orden de df_plot
            showline=False,
            fixedrange=False,
        ),
        hoverlabel=dict(
            bgcolor=GTD["navy"],
            font_size=12,
            font_family="Segoe UI",
            font_color=GTD["white"],
            bordercolor=GTD["blue_m"],
        ),
    )

    return fig


# ── Render
st.markdown(f"""
<div class="stitle">
  📅 Carta Gantt — Escala: {escala}
  &nbsp;&nbsp;
  <span style="font-size:11px;font-weight:400;color:{GTD['gray_m']};">
    ({len(df)} actividades mostradas)
  </span>
</div>
""", unsafe_allow_html=True)

# Leyenda
leg = st.columns([1, 1, 1, 1, 5])
leyendas = [
    (GTD["gantt_bg"],  "Duración total"),
    (GTD["gantt_ok"],  "Progreso"),
    (GTD["gantt_red"], "Retrasado"),
    ("#F0A500",        "En Riesgo"),
]
_c_texto = GTD["gray_dk"]
for col, (color, texto) in zip(leg, leyendas):
    with col:
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:6px;font-size:11px;"
            f"color:{_c_texto};margin-bottom:8px;'>"
            f"<div style='width:16px;height:12px;background:{color};"
            f"border-radius:2px;border:1px solid rgba(0,0,0,0.1);'></div>"
            f"{texto}</div>",
            unsafe_allow_html=True,
        )

st.plotly_chart(
    construir_gantt(df, escala),
    use_container_width=True,
    config={
        "displayModeBar": True,
        "modeBarButtonsToRemove": ["select2d", "lasso2d", "autoScale2d"],
        "displaylogo": False,
        "toImageButtonOptions": {
            "format": "png",
            "filename": f"GTD_Gantt_{date.today().isoformat()}",
            "scale": 2,
        },
    },
)


# ══════════════════════════════════════════════════════════════
#  TABLA DETALLE
# ══════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
st.markdown(f'<div class="stitle">📋 Detalle de Actividades</div>', unsafe_allow_html=True)

if not df.empty:
    df_tabla = df[[
        "Fase", "Actividades", "Sede", "Tecnologías",
        "Fecha Inicio", "Fecha Final", "Días", "Progreso",
        "Responsable", "Estado de Salud",
    ]].copy()

    df_tabla["Fecha Inicio"] = df_tabla["Fecha Inicio"].dt.strftime("%d/%m/%Y")
    df_tabla["Fecha Final"]  = df_tabla["Fecha Final"].dt.strftime("%d/%m/%Y")
    df_tabla["Progreso"]     = (df_tabla["Progreso"] * 100).round(0).astype(int).astype(str) + "%"

    def colorear_fila(row):
        est = row["Estado de Salud"]
        bg  = {"Retrasado": "#FADBD8", "En Riesgo": "#FDEBD0"}.get(est, "")
        return [f"background-color:{bg}" if bg else "" for _ in row]

    styled = (
        df_tabla.style
        .apply(colorear_fila, axis=1)
        .set_properties(**{"font-size": "12px", "font-family": "Segoe UI"})
        .set_table_styles([{
            "selector": "th",
            "props": [
                ("background-color", GTD["navy"]),
                ("color",            GTD["white"]),
                ("font-size",        "11px"),
                ("font-weight",      "700"),
                ("text-transform",   "uppercase"),
                ("letter-spacing",   "0.05em"),
            ],
        }])
    )
    st.dataframe(styled, use_container_width=True, height=360)
else:
    st.info("No hay actividades para los filtros seleccionados.")


# ══════════════════════════════════════════════════════════════
#  GRÁFICOS DE RESUMEN
# ══════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:18px;'></div>", unsafe_allow_html=True)
st.markdown(f'<div class="stitle">📊 Resumen Ejecutivo</div>', unsafe_allow_html=True)

if not df.empty:
    cg1, cg2, cg3 = st.columns(3)

    # 1. Donut estado de salud
    with cg1:
        cnt = df["Estado de Salud"].value_counts().reset_index()
        cnt.columns = ["Estado", "N"]
        c_mapa = {"A tiempo": GTD["green"], "En Riesgo": GTD["amber"], "Retrasado": GTD["red"]}
        fig1 = go.Figure(go.Pie(
            labels=cnt["Estado"],
            values=cnt["N"],
            marker_colors=[c_mapa.get(e, GTD["gray_s"]) for e in cnt["Estado"]],
            hole=0.55,
            textfont=dict(family="Segoe UI", size=12),
            hovertemplate="<b>%{label}</b><br>%{value} tareas (%{percent})<extra></extra>",
        ))
        fig1.update_layout(
            title=dict(text="Estado de salud", font=dict(size=13, color=GTD["navy"]), x=0.5),
            margin=dict(t=40, b=10, l=10, r=10), height=240,
            paper_bgcolor=GTD["white"],
            legend=dict(font=dict(size=11, family="Segoe UI")),
        )
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    # 2. Avance por fase
    with cg2:
        af = df.groupby("Fase").apply(
            lambda g: round((g["Progreso"] * g["Días"]).sum() / g["Días"].sum() * 100, 1)
            if g["Días"].sum() > 0 else 0.0
        ).reset_index()
        af.columns = ["Fase", "Avance"]
        orden = ["Inicio", "Planificación", "Ejecución", "Cierre"]
        af["Fase"] = pd.Categorical(af["Fase"], categories=orden, ordered=True)
        af = af.sort_values("Fase")

        fig2 = go.Figure(go.Bar(
            x=af["Avance"], y=af["Fase"],
            orientation="h",
            marker=dict(
                color=[GTD["blue"] if v >= 50 else GTD["amber"] for v in af["Avance"]],
                line=dict(color="rgba(0,0,0,.08)", width=0.5),
            ),
            text=[f"{v}%" for v in af["Avance"]],
            textposition="outside",
            textfont=dict(size=11, family="Segoe UI"),
            hovertemplate="<b>%{y}</b><br>Avance: %{x}%<extra></extra>",
        ))
        fig2.update_layout(
            title=dict(text="Avance por fase", font=dict(size=13, color=GTD["navy"]), x=0.5),
            xaxis=dict(range=[0, 118], ticksuffix="%", gridcolor=GTD["gray_l"],
                       tickfont=dict(size=10, family="Segoe UI")),
            yaxis=dict(tickfont=dict(size=11, family="Segoe UI")),
            margin=dict(t=40, b=10, l=10, r=30), height=240,
            paper_bgcolor=GTD["white"], plot_bgcolor=GTD["white"],
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # 3. Carga por responsable
    with cg3:
        cr = df.groupby("Responsable").agg(
            Tareas=("Actividades", "count"),
            Avance=("Progreso", "mean"),
        ).reset_index()
        cr["Avance"] = (cr["Avance"] * 100).round(1)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name="Tareas", x=cr["Responsable"], y=cr["Tareas"],
            marker_color=GTD["navy_m"],
            hovertemplate="<b>%{x}</b><br>Tareas: %{y}<extra></extra>",
        ))
        fig3.add_trace(go.Scatter(
            name="Avance %", x=cr["Responsable"], y=cr["Avance"],
            mode="lines+markers",
            marker=dict(color=GTD["gantt_ok"], size=8),
            line=dict(color=GTD["gantt_ok"], width=2),
            yaxis="y2",
            hovertemplate="<b>%{x}</b><br>Avance: %{y}%<extra></extra>",
        ))
        fig3.update_layout(
            title=dict(text="Carga por responsable", font=dict(size=13, color=GTD["navy"]), x=0.5),
            yaxis=dict(title="N° Tareas", gridcolor=GTD["gray_l"],
                       tickfont=dict(size=10, family="Segoe UI")),
            yaxis2=dict(title="Avance %", overlaying="y", side="right",
                        range=[0, 115], ticksuffix="%",
                        tickfont=dict(size=10, family="Segoe UI")),
            legend=dict(font=dict(size=10, family="Segoe UI"),
                        orientation="h", y=-0.28),
            xaxis=dict(tickfont=dict(size=10, family="Segoe UI")),
            margin=dict(t=40, b=30, l=10, r=40), height=240,
            paper_bgcolor=GTD["white"], plot_bgcolor=GTD["white"],
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center;padding:12px;background:{GTD['navy']};border-radius:8px;
            font-size:11px;color:{GTD['blue_l']};">
  GTD Telecomunicaciones &nbsp;·&nbsp; Dashboard Ejecutivo PMO
  &nbsp;·&nbsp; MMOO · Starlink · Fibra Óptica
  &nbsp;|&nbsp; {date.today().strftime('%d/%m/%Y')}
</div>
""", unsafe_allow_html=True)
