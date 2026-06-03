from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "outputs" / "reports"
DOCS = ROOT / "docs"
ENGINEERED = ROOT / "data" / "engineered"

PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}

BAND_COLORS = {
    "Critical": "#ef4444",
    "High": "#f97316",
    "Medium": "#3b82f6",
    "Low": "#64748b",
}

ACCENT = {
    "blue": ("#eaf2ff", "#2563eb"),
    "red": ("#fee2e2", "#dc2626"),
    "orange": ("#ffedd5", "#ea580c"),
    "green": ("#dcfce7", "#16a34a"),
    "purple": ("#ede9fe", "#7c3aed"),
    "amber": ("#fef3c7", "#d97706"),
    "slate": ("#e2e8f0", "#334155"),
}


def setup_page(title: str = "Technology Lifecycle Governance") -> None:
    st.set_page_config(page_title=title, page_icon="🏦", layout="wide", initial_sidebar_state="expanded")
    inject_css()
    sidebar_brand()


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --eol-navy: #17233f;
            --eol-navy-2: #23395d;
            --eol-text: #1f2937;
            --eol-muted: #64748b;
            --eol-border: #e5e7eb;
            --eol-bg: #f8fafc;
        }
        .block-container {
            padding-top: 1.6rem !important;
            padding-bottom: 3rem !important;
            max-width: 1360px !important;
        }
        [data-testid="stSidebar"] {
            background: #f8fafc;
            border-right: 1px solid #e5e7eb;
        }
        [data-testid="stSidebar"] a {
            font-size: 0.96rem !important;
        }
        .eol-brand {
            padding: 0.5rem 0.5rem 1rem 0.5rem;
            margin-bottom: 0.4rem;
            border-bottom: 1px solid #e5e7eb;
        }
        .eol-brand-title {
            font-weight: 800;
            font-size: 1.05rem;
            color: #0f172a;
            margin-bottom: 0.15rem;
        }
        .eol-brand-subtitle {
            font-size: 0.82rem;
            color: #64748b;
        }
        .eol-footer {
            position: fixed;
            bottom: 1.2rem;
            left: 1.2rem;
            max-width: 250px;
            color: #64748b;
            font-size: 0.78rem;
            line-height: 1.45;
        }
        .eol-hero {
            background: linear-gradient(135deg, #081a36 0%, #17294b 55%, #253e66 100%);
            color: #fff;
            border-radius: 16px;
            padding: 28px 34px;
            margin-bottom: 1.4rem;
            box-shadow: 0 16px 38px rgba(15, 23, 42, 0.18);
            position: relative;
            overflow: hidden;
        }
        .eol-hero:after {
            content: "";
            position: absolute;
            right: -40px;
            top: -40px;
            width: 420px;
            height: 220px;
            opacity: 0.25;
            background: repeating-linear-gradient(135deg, rgba(255,255,255,0.22) 0px, rgba(255,255,255,0.22) 1px, transparent 1px, transparent 14px);
            transform: rotate(0deg);
        }
        .eol-hero-eyebrow {
            color: #60a5fa;
            font-size: 0.78rem;
            letter-spacing: 0.16em;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 0.6rem;
        }
        .eol-hero-title {
            font-size: 2.05rem;
            font-weight: 850;
            letter-spacing: -0.025em;
            line-height: 1.12;
            margin-bottom: 0.85rem;
        }
        .eol-hero-text {
            font-size: 1.02rem;
            color: #e2e8f0;
            max-width: 860px;
            line-height: 1.6;
        }
        .eol-kpi-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 15px;
            padding: 18px 18px;
            min-height: 138px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            margin-bottom: 1rem;
        }
        .eol-kpi-row {
            display: flex;
            align-items: flex-start;
            gap: 14px;
        }
        .eol-kpi-icon {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.45rem;
            flex: 0 0 auto;
        }
        .eol-kpi-label {
            color: #64748b;
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }
        .eol-kpi-value {
            color: #111827;
            font-size: 1.85rem;
            line-height: 1.1;
            font-weight: 850;
            letter-spacing: -0.02em;
            margin-bottom: 0.4rem;
        }
        .eol-kpi-caption {
            color: #64748b;
            font-size: 0.86rem;
            line-height: 1.35;
        }
        .eol-section-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 15px;
            padding: 22px 24px;
            margin-top: 1.1rem;
            margin-bottom: 1.1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        }
        .eol-section-title {
            color: #0f172a;
            font-size: 1.45rem;
            font-weight: 850;
            letter-spacing: -0.02em;
            margin-bottom: 0.4rem;
            border-bottom: 3px solid #2563eb;
            display: inline-block;
            padding-bottom: 0.25rem;
        }
        .eol-body {
            color: #263244;
            font-size: 0.96rem;
            line-height: 1.64;
        }
        .eol-insight {
            background: #fffbeb;
            border: 1px solid #fbbf24;
            border-left: 5px solid #d97706;
            border-radius: 12px;
            padding: 12px 16px;
            margin: 0.7rem 0 1.0rem 0;
            color: #334155;
            font-size: 0.93rem;
            line-height: 1.55;
        }
        .eol-insight strong { color: #92400e; }
        .eol-risk-alert {
            background: #fff1f2;
            border: 1px solid #fecdd3;
            border-left: 5px solid #ef4444;
            border-radius: 12px;
            padding: 13px 16px;
            margin: 0.7rem 0 1.0rem 0;
            color: #334155;
            font-size: 0.93rem;
            line-height: 1.55;
        }
        .eol-risk-alert strong { color: #b91c1c; }
        .eol-chart-title {
            font-size: 1.23rem;
            font-weight: 800;
            color: #111827;
            margin: 1.1rem 0 0.25rem 0;
        }
        .eol-divider {
            height: 1px;
            background: #e5e7eb;
            margin: 1.35rem 0;
        }
        .eol-mini-label {
            color: #64748b;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 800;
        }
        .eol-table-note {
            color: #64748b;
            font-size: 0.86rem;
            margin-top: -0.25rem;
            margin-bottom: 0.65rem;
        }
        h1, h2, h3 { letter-spacing: -0.025em; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand() -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="eol-brand">
                <div class="eol-brand-title">🏦 Maple Financial Bank</div>
                <div class="eol-brand-subtitle">Technology Risk Governance</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="eol-footer">
                <div>Data as of: May 31, 2025</div>
                <div style="margin-top:8px;">Technology Lifecycle Governance Dashboard v2.0</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def load_report(name: str) -> pd.DataFrame:
    path = REPORTS / name
    if path.exists():
        return pd.read_csv(path)
    # fallback for files sometimes copied into root during testing
    fallback = ROOT / name
    if fallback.exists():
        return pd.read_csv(fallback)
    return pd.DataFrame()


def load_engineered(name: str) -> pd.DataFrame:
    path = ENGINEERED / name
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def load_doc(name: str) -> str:
    path = DOCS / name
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def fmt_number(value) -> str:
    try:
        if pd.isna(value):
            return "—"
        return f"{float(value):,.0f}"
    except Exception:
        return str(value)


def fmt_money(value) -> str:
    try:
        if pd.isna(value):
            return "—"
        value = float(value)
        if abs(value) >= 1_000_000:
            return f"${value/1_000_000:,.1f}M"
        if abs(value) >= 1_000:
            return f"${value/1_000:,.1f}K"
        return f"${value:,.0f}"
    except Exception:
        return str(value)


def hero(title: str, subtitle: str, eyebrow: str = "Executive Technology Governance") -> None:
    st.markdown(
        f"""
        <div class="eol-hero">
            <div class="eol-hero-eyebrow">{eyebrow}</div>
            <div class="eol-hero-title">{title}</div>
            <div class="eol-hero-text">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, caption: str, icon: str, color: str = "blue") -> None:
    bg, fg = ACCENT.get(color, ACCENT["blue"])
    st.markdown(
        f"""
        <div class="eol-kpi-card">
            <div class="eol-kpi-row">
                <div class="eol-kpi-icon" style="background:{bg}; color:{fg};">{icon}</div>
                <div>
                    <div class="eol-kpi-label">{label}</div>
                    <div class="eol-kpi-value">{value}</div>
                    <div class="eol-kpi-caption">{caption}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_card(title: str, body_html: str) -> None:
    st.markdown(
        f"""
        <div class="eol-section-card">
            <div class="eol-section-title">{title}</div>
            <div class="eol-body">{body_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight(text: str, alert: bool = False) -> None:
    klass = "eol-risk-alert" if alert else "eol-insight"
    st.markdown(f'<div class="{klass}"><strong>What this chart shows:</strong> {text}</div>', unsafe_allow_html=True)


def chart_title(title: str) -> None:
    st.markdown(f'<div class="eol-chart-title">{title}</div>', unsafe_allow_html=True)


def clean_fig(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        title=None,
        height=height,
        margin=dict(l=10, r=10, t=8, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12, color="#334155"),
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e5e7eb", zeroline=False, title_font=dict(size=12), tickfont=dict(size=11))
    fig.update_yaxes(showgrid=False, zeroline=False, title_font=dict(size=12), tickfont=dict(size=11))
    return fig


def bar_chart(df: pd.DataFrame, x: str, y: str, orientation: str = "h", color: str | None = None, height: int = 420, text: str | None = None):
    if df.empty or x not in df.columns or y not in df.columns:
        st.info("Chart data is not available. Run the pipeline to refresh the output files.")
        return
    fig = px.bar(df, x=x, y=y, orientation=orientation, color=color if color in df.columns else None,
                 color_discrete_map=BAND_COLORS, text=text if text in df.columns else None)
    fig = clean_fig(fig, height=height)
    if orientation == "h":
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


def topn(df: pd.DataFrame, sort_col: str, n: int = 10, ascending: bool = False) -> pd.DataFrame:
    if df.empty or sort_col not in df.columns:
        return df
    return df.sort_values(sort_col, ascending=ascending).head(n)
