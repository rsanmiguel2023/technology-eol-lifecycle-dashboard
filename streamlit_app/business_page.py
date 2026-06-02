from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
for p in [ROOT, ROOT / "streamlit_app"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from streamlit_app.doc_loader import page_content, load_doc
from streamlit_app.ui_components import inject_css, exec_banner, management_question, insight, recommendation, tip_header

REPORTS = ROOT / "outputs" / "reports"
DATA = ROOT / "data" / "processed"


def _read_report(filename):
    path = REPORTS / filename
    if not path.exists():
        st.error(f"Required report file not found: outputs/reports/{filename}")
        st.info("Run: python src/05_export_figures_and_reports.py")
        st.stop()
    return pd.read_csv(path, low_memory=False)


def _money(value):
    try:
        value = float(value)
    except Exception:
        return "N/A"
    return f"${value/1_000_000:,.1f}M" if abs(value) >= 1_000_000 else f"${value:,.0f}"


def _num(value):
    try:
        return f"{int(round(float(value))):,}"
    except Exception:
        return "N/A"


def _metric_sum(df, col, default=0):
    return df[col].sum() if col in df.columns else default


def page_header(page_key, icon):
    content = page_content(page_key)
    st.set_page_config(page_title=content["title"], page_icon=icon, layout="wide")
    inject_css()
    st.title(f"{icon} {content['title']}")
    management_question(content["management_question"])
    exec_banner(content["executive_summary"])
    return content


def show_standard_tabs(content, df, doc_file, evidence_label="Evidence table"):
    tabs = st.tabs(["📋 Management View", "📈 Analysis", "🧾 Evidence", "🎯 Actions", "📚 Documentation"])
    with tabs[0]:
        insight(content["business_interpretation"])
        recommendation(content["recommended_actions"])
    with tabs[1]:
        tip_header("How to read this page", content["tooltip"])
        st.markdown(content["dashboard_notes"])
    with tabs[2]:
        st.caption(evidence_label)
        st.dataframe(df.head(500), use_container_width=True)
    with tabs[3]:
        st.markdown("### Recommended Actions")
        st.markdown(content["recommended_actions"])
        st.markdown("### Methodology")
        st.markdown(content["methodology"])
    with tabs[4]:
        st.markdown(load_doc(doc_file))


def plot_bar(df, x, y, title, orientation="v", color=None, height=520):
    if orientation == "h":
        fig = px.bar(df, x=x, y=y, orientation="h", color=color, title=title, text=x)
        fig.update_layout(yaxis_title="", xaxis_title="", height=height)
    else:
        fig = px.bar(df, x=x, y=y, color=color, title=title, text=y)
        fig.update_layout(xaxis_title="", yaxis_title="", height=height)
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)


def load_assets():
    path = DATA / "asset_risk_model.csv"
    if not path.exists():
        st.error("Required processed file not found: data/processed/asset_risk_model.csv")
        st.info("Run: python src/02_etl_prepare_model.py")
        st.stop()
    return pd.read_csv(path, low_memory=False)
