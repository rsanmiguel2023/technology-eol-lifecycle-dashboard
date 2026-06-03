
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "outputs" / "reports"
DOCS = ROOT / "docs"
ENGINEERED = ROOT / "data" / "engineered"

def apply_page_config(title="Technology Lifecycle Governance"):
    st.set_page_config(
        page_title=title,
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

def inject_css():
    st.markdown(
        """
        <style>
        :root {
            --navy:#0f2440;
            --navy2:#1a3660;
            --gold:#f0c040;
            --muted:#667085;
            --soft:#f6f8fb;
            --border:#d9e2ec;
            --red:#c62828;
            --orange:#ef6c00;
            --green:#2e7d32;
        }
        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 3rem;
            max-width: 1320px;
        }
        h1 {
            font-size: 2.35rem !important;
            letter-spacing: -0.03em;
            font-weight: 800 !important;
            color: #222838;
        }
        h2 {
            margin-top: 1.8rem !important;
            color:#222838;
            letter-spacing:-0.02em;
        }
        h3 { color:#293347; }
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 18px 18px;
            box-shadow: 0 3px 12px rgba(15, 36, 64, 0.06);
        }
        div[data-testid="stMetricLabel"] p {
            color: #475467;
            font-size: 0.86rem;
            font-weight: 600;
        }
        div[data-testid="stMetricValue"] {
            color: #0f2440;
            font-weight: 800;
        }
        .exec-hero {
            background: linear-gradient(135deg, #0f2440 0%, #1a3660 100%);
            border-radius: 18px;
            padding: 28px 32px;
            margin: 6px 0 22px 0;
            border-left: 7px solid #f0c040;
            box-shadow: 0 8px 28px rgba(15, 36, 64, 0.18);
        }
        .exec-hero h1, .exec-hero h2, .exec-hero h3 {
            color: #ffffff !important;
            margin: 0;
        }
        .exec-hero p {
            color: #e8eef8;
            font-size: 1.03rem;
            line-height: 1.65;
            margin-bottom: 0;
        }
        .eyebrow {
            color:#f0c040;
            font-weight:800;
            letter-spacing:0.12em;
            text-transform:uppercase;
            font-size:0.78rem;
            margin-bottom:8px;
        }
        .insight-box {
            background:#f6f8fb;
            border:1px solid #d9e2ec;
            border-left:6px solid #1a3660;
            border-radius:14px;
            padding:18px 22px;
            margin:16px 0 22px 0;
            color:#263142;
            line-height:1.65;
        }
        .alert-box {
            background:#fff7ed;
            border:1px solid #fed7aa;
            border-left:6px solid #ef6c00;
            border-radius:14px;
            padding:18px 22px;
            margin:16px 0 22px 0;
            color:#422006;
            line-height:1.65;
        }
        .risk-critical, .risk-high, .risk-medium, .risk-low {
            display:inline-block;
            border-radius:999px;
            padding:4px 10px;
            color:white;
            font-size:0.78rem;
            font-weight:700;
        }
        .risk-critical { background:#c62828; }
        .risk-high { background:#ef6c00; }
        .risk-medium { background:#616161; }
        .risk-low { background:#2e7d32; }
        section[data-testid="stSidebar"] {
            background:#f3f6fa;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            border-radius:8px;
        }
        .small-muted {
            color:#667085;
            font-size:0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def read_csv_any(*paths):
    for path in paths:
        p = Path(path)
        if p.exists():
            return pd.read_csv(p)
    return pd.DataFrame()

def read_report(name):
    return read_csv_any(REPORTS / name, ENGINEERED / name)

def read_engineered(name):
    return read_csv_any(ENGINEERED / name, REPORTS / name)

def read_doc(name):
    p = DOCS / name
    if p.exists():
        return p.read_text(encoding="utf-8")
    return ""

def money(value):
    try:
        value = float(value)
    except Exception:
        return str(value)
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"${value/1_000:.1f}K"
    return f"${value:,.0f}"

def number(value):
    try:
        return f"{int(round(float(value))):,}"
    except Exception:
        return str(value)

def pct(value):
    try:
        return f"{float(value):.1f}%"
    except Exception:
        return str(value)

def page_header(title, subtitle, eyebrow="Executive view"):
    st.markdown(
        f"""
        <div class="exec-hero">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def insight(text, kind="normal"):
    cls = "alert-box" if kind == "alert" else "insight-box"
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)

def metric_row(items, columns=4):
    cols = st.columns(columns)
    for i, item in enumerate(items):
        label, value = item[0], item[1]
        delta = item[2] if len(item) > 2 else None
        help_text = item[3] if len(item) > 3 else None
        cols[i % columns].metric(label, value, delta=delta, help=help_text)

def risk_badge(risk):
    risk = str(risk)
    cls = {
        "Critical": "risk-critical",
        "High": "risk-high",
        "Medium": "risk-medium",
        "Low": "risk-low",
    }.get(risk, "risk-medium")
    return f'<span class="{cls}">{risk}</span>'

def bar_chart(df, x, y, title, color=None, orientation="v", text=None):
    if df.empty:
        st.info("No data available for this visual. Run the pipeline first.")
        return
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        orientation=orientation,
        text=text,
        title=title,
    )
    fig.update_layout(
        title_font_size=18,
        title_font_color="#222838",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text="",
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)

def line_chart(df, x, y, title):
    if df.empty:
        st.info("No data available for this visual. Run the pipeline first.")
        return
    fig = px.line(df, x=x, y=y, markers=True, title=title)
    fig.update_layout(
        title_font_size=18,
        title_font_color="#222838",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)
