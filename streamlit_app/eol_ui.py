from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def project_root(current_file: str) -> Path:
    p = Path(current_file).resolve()
    if p.parent.name == 'pages':
        return p.parents[2]
    return p.parents[1]


def setup_page(title: str):
    st.set_page_config(page_title=title, page_icon='🏦', layout='wide', initial_sidebar_state='expanded')
    st.markdown(CSS, unsafe_allow_html=True)
    sidebar_brand()


def sidebar_brand():
    with st.sidebar:
        st.markdown('<div class="sidebar-brand"><div class="bank-icon">🏦</div><div><b>Maple Financial Bank</b><br><span>Technology Risk Governance</span></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-foot">Data as of: May 31, 2026<br>Dashboard v2.0</div>', unsafe_allow_html=True)


def read_csv_any(root: Path, names):
    paths = []
    for name in names if isinstance(names, (list, tuple)) else [names]:
        paths += [root / 'outputs' / 'reports' / name, root / 'data' / 'engineered' / name, root / 'outputs' / 'powerbi' / name]
    for path in paths:
        if path.exists():
            try:
                return pd.read_csv(path)
            except Exception:
                pass
    return pd.DataFrame()


def fmt_int(x):
    try: return f"{int(round(float(x))):,}"
    except Exception: return '—'


def fmt_money(x):
    try:
        v = float(x)
        return f"${v/1_000_000:.1f}M" if abs(v) >= 1_000_000 else f"${v:,.0f}"
    except Exception: return '—'


def fmt_pct(x):
    try: return f"{float(x):.1f}%"
    except Exception: return '—'


def hero(title, subtitle, eyebrow='EXECUTIVE TECHNOLOGY GOVERNANCE'):
    st.markdown(f'''
    <section class="hero">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </section>
    ''', unsafe_allow_html=True)


def kpi_card(label, value, caption='', tone='blue', icon='●'):
    st.markdown(f'''
    <div class="kpi-card">
      <div class="kpi-icon {tone}">{icon}</div>
      <div class="kpi-body">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-caption">{caption}</div>
      </div>
    </div>
    ''', unsafe_allow_html=True)


def insight_box(title, text):
    st.markdown(f'''
    <div class="insight-card">
      <h3>{title}</h3>
      <div class="accent-line"></div>
      <p>{text}</p>
    </div>
    ''', unsafe_allow_html=True)


def chart_note(text):
    st.markdown(f'<div class="chart-note"><b>What this chart shows:</b> {text}</div>', unsafe_allow_html=True)


def clean_fig(fig, height=430):
    fig.update_layout(
        title=None, title_text='', height=height, margin=dict(l=10,r=10,t=10,b=10),
        font=dict(family='Arial, sans-serif', size=13, color='#263248'),
        paper_bgcolor='white', plot_bgcolor='white',
        legend_title_text='',
    )
    fig.update_xaxes(showgrid=True, gridcolor='#E9EEF6', zeroline=False, title_font=dict(size=12), tickfont=dict(size=12))
    fig.update_yaxes(showgrid=False, zeroline=False, title_font=dict(size=12), tickfont=dict(size=12))
    return fig


def plot_bar(df, x, y, orientation='h', color=None, labels=None, height=430):
    if df.empty or x not in df.columns or y not in df.columns:
        st.info('Chart data is not available. Run the pipeline to refresh output files.')
        return
    fig = px.bar(df, x=x, y=y, orientation=orientation, color=color if color in df.columns else None, labels=labels or {})
    fig = clean_fig(fig, height)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


CSS = '''
<style>
/* Do not override Streamlit icon fonts. Keep CSS scoped to custom classes only. */
.block-container {max-width: 1320px; padding-top: 2rem; padding-bottom: 3rem;}
.hero {background: linear-gradient(135deg,#0E1B36 0%,#23395D 68%,#29486F 100%); color:#fff; border-radius: 16px; padding: 30px 36px; margin: 0 0 24px 0; box-shadow: 0 18px 42px rgba(17,34,64,.18); position:relative; overflow:hidden;}
.hero:after {content:""; position:absolute; right:-120px; top:-80px; width:520px; height:260px; background: repeating-linear-gradient(135deg, rgba(255,255,255,.12) 0, rgba(255,255,255,.12) 1px, transparent 1px, transparent 14px); transform:rotate(0deg); opacity:.35;}
.hero .eyebrow {font-size:.78rem; letter-spacing:.22em; color:#7DB4FF; font-weight:800; margin-bottom:12px;}
.hero h1 {font-size:2.15rem; line-height:1.2; margin:0 0 14px 0; font-weight:800; color:white;}
.hero p {font-size:1rem; line-height:1.65; max-width:900px; margin:0; color:#EFF6FF;}
.kpi-card {display:flex; gap:16px; align-items:center; background:white; border:1px solid #E4EAF3; border-radius:16px; padding:20px 20px; box-shadow:0 10px 28px rgba(15,23,42,.06); min-height:126px; margin-bottom:16px;}
.kpi-icon {width:52px; height:52px; min-width:52px; display:flex; align-items:center; justify-content:center; border-radius:50%; font-weight:900; font-size:1.25rem;}
.kpi-icon.blue {background:#EAF2FF; color:#2563EB}.kpi-icon.red {background:#FDECEC; color:#DC2626}.kpi-icon.orange {background:#FFF3DF; color:#EA580C}.kpi-icon.green {background:#E7F8EC; color:#16A34A}.kpi-icon.purple {background:#F1EAFF; color:#7C3AED}.kpi-icon.gray {background:#EEF2F7; color:#475569}
.kpi-label {font-size:.74rem; color:#63708A; letter-spacing:.10em; text-transform:uppercase; font-weight:800; margin-bottom:6px;}
.kpi-value {font-size:1.65rem; font-weight:850; color:#172033; line-height:1.15;}
.kpi-caption {font-size:.86rem; color:#69758A; line-height:1.4; margin-top:7px;}
.insight-card {background:white; border:1px solid #E4EAF3; border-radius:16px; padding:24px 28px; box-shadow:0 10px 28px rgba(15,23,42,.05); margin:18px 0 24px 0;}
.insight-card h3 {font-size:1.35rem; margin:0; color:#172033; font-weight:850;}
.accent-line {width:120px; height:4px; background:#2563EB; border-radius:4px; margin:12px 0 14px 0;}
.insight-card p, .insight-card li {font-size:1rem; line-height:1.65; color:#293449;}
.chart-note {background:#FFF9EA; border:1px solid #F4B04A; border-left:5px solid #D97706; border-radius:10px; padding:12px 16px; margin:8px 0 14px 0; color:#293449; font-size:.96rem; line-height:1.5;}
.sidebar-brand {border-top:1px solid #D7DDE8; border-bottom:1px solid #D7DDE8; margin-top:22px; padding:18px 8px; display:flex; gap:12px; align-items:center; color:#172033;}
.sidebar-brand span {font-size:.82rem; color:#64748B;}.bank-icon {width:34px;height:34px;border-radius:50%;background:#EAF2FF;display:flex;align-items:center;justify-content:center}.sidebar-foot {position:fixed; bottom:18px; left:18px; color:#64748B; font-size:.78rem; line-height:1.6;}
h2, h3 {color:#172033; font-weight:800;} 
</style>
'''
