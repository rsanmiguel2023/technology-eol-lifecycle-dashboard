from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "outputs" / "reports"
ENGINEERED = ROOT / "data" / "engineered"

PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}

RISK_COLORS = {
    "Critical": "#ef4444",
    "High": "#f97316",
    "Medium": "#3b82f6",
    "Low": "#22c55e",
    "Unsupported": "#ef4444",
    "Past EOL": "#ef4444",
    "Expiring in 12 Months": "#f97316",
    "Expiring in 24 Months": "#f59e0b",
    "Expiring in 36 Months": "#3b82f6",
    "Supported": "#22c55e",
}

CARD_ACCENTS = {
    "blue": ("#eaf2ff", "#2563eb"),
    "red": ("#fff1f2", "#dc2626"),
    "orange": ("#fff7ed", "#ea580c"),
    "green": ("#ecfdf5", "#16a34a"),
    "purple": ("#f5f3ff", "#7c3aed"),
    "amber": ("#fffbeb", "#d97706"),
    "slate": ("#f1f5f9", "#334155"),
}


def load_csv(*names: str) -> pd.DataFrame:
    """Read the first matching CSV from outputs/reports, data/engineered, or project root."""
    for name in names:
        for base in [REPORTS, ENGINEERED, ROOT, ROOT / "outputs" / "powerbi"]:
            path = base / name
            if path.exists():
                return pd.read_csv(path)
    return pd.DataFrame()


def format_number(value) -> str:
    try:
        v = float(value)
    except Exception:
        return str(value)
    if abs(v) >= 1_000_000_000:
        return f"{v/1_000_000_000:.1f}B"
    if abs(v) >= 1_000_000:
        return f"{v/1_000_000:.1f}M"
    if abs(v) >= 10_000:
        return f"{v:,.0f}"
    if v == int(v):
        return f"{int(v):,}"
    return f"{v:,.1f}"


def format_money(value) -> str:
    try:
        v = float(value)
    except Exception:
        return str(value)
    if abs(v) >= 1_000_000:
        return f"${v/1_000_000:.1f}M"
    if abs(v) >= 1_000:
        return f"${v/1_000:.1f}K"
    return f"${v:,.0f}"


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1320px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
            border-right: 1px solid #e2e8f0;
        }
        section[data-testid="stSidebar"] a {
            border-radius: 10px !important;
            margin: 3px 8px !important;
        }
        .eol-bankmark {
            display:flex; align-items:center; gap:12px; padding: 18px 8px 22px 8px;
            color:#0f172a;
        }
        .eol-bank-icon {
            width:40px; height:40px; border-radius:12px; background:#e0edff; color:#0b4bcc;
            display:flex; align-items:center; justify-content:center; font-size:22px;
            border:1px solid #c7dcff;
        }
        .eol-bank-title { font-weight:800; font-size:1.02rem; line-height:1.1; }
        .eol-bank-sub { color:#64748b; font-size:.78rem; margin-top:2px; }
        .eol-hero {
            background: radial-gradient(circle at 85% 20%, rgba(37,99,235,.35), transparent 24%),
                        linear-gradient(135deg, #061936 0%, #102a54 55%, #1e3a5f 100%);
            border-radius: 18px;
            padding: 30px 36px;
            color:white;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
            margin-bottom: 24px;
            position: relative;
            overflow:hidden;
        }
        .eol-hero:after {
            content:"";
            position:absolute;
            right:-90px; top:-70px;
            width:360px; height:260px;
            background: repeating-linear-gradient(150deg, rgba(255,255,255,.14) 0px, rgba(255,255,255,.14) 1px, transparent 2px, transparent 13px);
            transform: rotate(-8deg);
            opacity:.55;
        }
        .eol-kicker {
            color:#60a5fa;
            text-transform:uppercase;
            letter-spacing:.17em;
            font-weight:800;
            font-size:.78rem;
            margin-bottom:12px;
        }
        .eol-hero h1 {
            margin:0 0 12px 0;
            font-size:2.15rem;
            line-height:1.08;
            font-weight:900;
            letter-spacing:-.03em;
        }
        .eol-hero p {
            margin:0;
            max-width:780px;
            font-size:1rem;
            line-height:1.65;
            color:#e5efff;
        }
        .eol-kpi-grid {
            display:grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap:16px;
            margin-bottom:22px;
        }
        .eol-kpi-card {
            background:white;
            border:1px solid #e2e8f0;
            border-radius:16px;
            padding:20px 20px;
            box-shadow:0 8px 22px rgba(15,23,42,.06);
            min-height:128px;
            display:flex;
            gap:16px;
            align-items:flex-start;
        }
        .eol-kpi-icon {
            min-width:48px;
            width:48px; height:48px;
            border-radius:50%;
            display:flex; align-items:center; justify-content:center;
            font-size:24px;
            font-weight:700;
        }
        .eol-kpi-label {
            font-size:.78rem;
            text-transform:uppercase;
            color:#64748b;
            letter-spacing:.08em;
            font-weight:800;
            margin-bottom:8px;
        }
        .eol-kpi-value {
            font-size:1.7rem;
            line-height:1.05;
            color:#0f172a;
            font-weight:900;
            letter-spacing:-.03em;
            margin-bottom:8px;
        }
        .eol-kpi-caption {
            font-size:.83rem;
            color:#64748b;
            line-height:1.35;
        }
        .eol-panel {
            background:white;
            border:1px solid #e2e8f0;
            border-radius:18px;
            padding:24px 28px;
            box-shadow:0 10px 28px rgba(15,23,42,.05);
            margin-bottom:22px;
        }
        .eol-panel h2, .eol-section-title {
            color:#0f172a;
            font-weight:900;
            letter-spacing:-.03em;
            margin:0 0 14px 0;
            font-size:1.55rem;
        }
        .eol-panel h3 {
            color:#0f172a;
            font-weight:800;
            margin: 8px 0 10px;
        }
        .eol-summary-row {
            display:grid;
            grid-template-columns: 38px 1fr;
            gap:14px;
            margin:14px 0;
            align-items:flex-start;
        }
        .eol-mini-icon {
            width:34px; height:34px;
            border-radius:50%;
            display:flex; align-items:center; justify-content:center;
            font-size:17px;
            font-weight:800;
        }
        .eol-summary-row p {
            margin:0;
            color:#1f2937;
            line-height:1.55;
        }
        .eol-chart-note {
            background:#fffbeb;
            border:1px solid #fed7aa;
            border-left:6px solid #d97706;
            border-radius:14px;
            padding:13px 16px;
            margin: 8px 0 16px 0;
            color:#334155;
            line-height:1.45;
            font-size:.94rem;
        }
        .eol-chart-note strong { color:#92400e; }
        .eol-risk-pill {
            display:inline-block;
            border-radius:999px;
            padding:4px 10px;
            color:#fff;
            font-weight:800;
            font-size:.78rem;
        }
        .eol-muted { color:#64748b; }
        .eol-divider { border-top:1px solid #e2e8f0; margin:26px 0; }
        @media (max-width: 1100px) { .eol-kpi-grid { grid-template-columns: repeat(2, minmax(0,1fr)); } }
        @media (max-width: 720px) { .eol-kpi-grid { grid-template-columns: 1fr; } .eol-hero h1 {font-size:1.7rem;} }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand() -> None:
    st.sidebar.markdown(
        """
        <div class="eol-bankmark">
            <div class="eol-bank-icon">🏦</div>
            <div>
                <div class="eol-bank-title">Maple Financial Bank</div>
                <div class="eol-bank-sub">Technology Risk Governance</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.divider()


def hero(title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="eol-hero">
            <div class="eol-kicker">Executive Technology Governance</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, caption: str, icon: str = "•", color: str = "blue") -> str:
    bg, fg = CARD_ACCENTS.get(color, CARD_ACCENTS["blue"])
    return f"""
    <div class="eol-kpi-card">
        <div class="eol-kpi-icon" style="background:{bg}; color:{fg};">{icon}</div>
        <div>
            <div class="eol-kpi-label">{label}</div>
            <div class="eol-kpi-value">{value}</div>
            <div class="eol-kpi-caption">{caption}</div>
        </div>
    </div>
    """


def kpi_grid(cards: list[dict]) -> None:
    html = '<div class="eol-kpi-grid">'
    for c in cards:
        html += kpi_card(**c)
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def panel_start(title: str | None = None) -> None:
    st.markdown('<div class="eol-panel">', unsafe_allow_html=True)
    if title:
        st.markdown(f'<h2>{title}</h2>', unsafe_allow_html=True)


def panel_end() -> None:
    st.markdown('</div>', unsafe_allow_html=True)


def summary_panel(title: str, rows: list[tuple[str, str, str, str]]) -> None:
    """Rows: icon, text, bg, fg"""
    html = f'<div class="eol-panel"><h2>{title}</h2>'
    for icon, text, bg, fg in rows:
        html += f'''
        <div class="eol-summary-row">
            <div class="eol-mini-icon" style="background:{bg}; color:{fg};">{icon}</div>
            <p>{text}</p>
        </div>'''
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def chart_note(text: str) -> None:
    st.markdown(f'<div class="eol-chart-note"><strong>What this chart shows:</strong> {text}</div>', unsafe_allow_html=True)


def plot_bar(df: pd.DataFrame, x: str, y: str, color: str | None = None, orientation: str = "h", labels: dict | None = None, height: int = 430, color_discrete_map: dict | None = None):
    if df.empty or x not in df.columns or y not in df.columns:
        st.info("Chart data is not available. Run the pipeline and refresh this page.")
        return
    fig = px.bar(df, x=x, y=y, color=color, orientation=orientation, labels=labels or {}, color_discrete_map=color_discrete_map)
    fig.update_layout(
        title=None,
        template="plotly_white",
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Arial", size=12, color="#334155"),
        legend_title_text="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e2e8f0", zeroline=False)
    fig.update_yaxes(showgrid=False)
    if orientation == "h":
        fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


def plot_line(df: pd.DataFrame, x: str, y: str, markers: bool = True, labels: dict | None = None, height: int = 420):
    if df.empty or x not in df.columns or y not in df.columns:
        st.info("Chart data is not available. Run the pipeline and refresh this page.")
        return
    fig = px.line(df, x=x, y=y, markers=markers, labels=labels or {})
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(title=None, template="plotly_white", height=height, margin=dict(l=10, r=10, t=10, b=10), font=dict(family="Arial", size=12, color="#334155"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="#e2e8f0", zeroline=False)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


def page_header(title: str, subtitle: str) -> None:
    st.markdown(f"<div class='eol-section-title'>{title}</div><p class='eol-muted'>{subtitle}</p>", unsafe_allow_html=True)


def risk_color_map() -> dict:
    return {"Critical":"#ef4444", "High":"#f97316", "Medium":"#60a5fa", "Low":"#2563eb"}
