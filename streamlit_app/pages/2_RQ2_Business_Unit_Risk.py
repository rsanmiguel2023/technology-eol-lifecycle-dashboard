import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
for p in [ROOT, ROOT / "streamlit_app"]:
    if str(p) not in sys.path: sys.path.insert(0, str(p))
from streamlit_app.doc_loader import rq_content, load_doc
from streamlit_app.ui_components import inject_css, tip_header, exec_banner, insight, recommendation

st.set_page_config(page_title="RQ2 — Technology EOL", page_icon="📊", layout="wide")
inject_css()
rq = rq_content(2)
st.title(rq["title"])
st.markdown(f"**Research Question:** {rq['question']}")
st.markdown(rq["hypotheses"])
exec_banner(rq["executive_summary"])

DATA_PATHS = [ROOT / "outputs" / "reports" / "business_unit_eol_exposure.csv", ROOT / "data" / "processed" / "business_unit_eol_exposure.csv"]
df = None
for p in DATA_PATHS:
    if p.exists():
        df = pd.read_csv(p)
        break
if df is None:
    st.error("Required data file was not found: business_unit_eol_exposure.csv")
    st.stop()

# KPI row
c1,c2,c3,c4 = st.columns(4)
c1.metric("Rows Analyzed", f"{len(df):,}", help="Number of records used in this RQ view.")
if "assets" in df.columns: c2.metric("Assets", f"{int(df['assets'].sum()):,}", help=rq['tooltip'])
elif "total_assets" in df.columns: c2.metric("Assets", f"{int(df['total_assets'].sum()):,}", help=rq['tooltip'])
elif "non_compliant_installs" in df.columns: c2.metric("Non-Compliant Installs", f"{int(df['non_compliant_installs'].sum()):,}", help=rq['tooltip'])
else: c2.metric("Records", f"{len(df):,}", help=rq['tooltip'])
if "replacement_cost" in df.columns: c3.metric("Replacement Exposure", f"${df['replacement_cost'].sum()/1_000_000:,.1f}M", help="Estimated replacement cost for the assets in scope.")
elif "estimated_replacement_cost" in df.columns: c3.metric("Refresh Cost", f"${df['estimated_replacement_cost'].sum()/1_000_000:,.1f}M", help="Estimated refresh funding required.")
elif "Critical_Vuln_Count" in df.columns: c3.metric("Critical Vulnerabilities", f"{int(df['Critical_Vuln_Count'].sum()):,}", help="Critical vulnerabilities in scope.")
else: c3.metric("Columns", f"{len(df.columns):,}", help="Available analytical fields.")
if "downtime_hours" in df.columns: c4.metric("Downtime Hours", f"{df['downtime_hours'].sum():,.0f}", help="Total downtime linked to the current RQ view.")
elif "Total_Downtime_Hours" in df.columns: c4.metric("Downtime Hours", f"{df['Total_Downtime_Hours'].sum():,.0f}", help="Total downtime linked to assets.")
else: c4.metric("Data Source", "CSV", help="Streamlit page reads from processed/exported CSV files.")

st.divider()
tabs = st.tabs(["📋 Overview", "📈 Analysis", "🧾 Evidence Table", "🎯 Interpretation & Recommendations", "📚 Documentation"])
with tabs[0]:
    st.subheader("Management Question")
    st.markdown(rq["question"])
    insight(rq["interpretation"])
    recommendation(rq["recommendations"])
with tabs[1]:
    tip_header("Executive Visual", rq["tooltip"])
    chart_df = df.copy()
    # choose chart dynamically
    xkey = "Business_Unit"
    ykey = "past_eol_rate_pct"
    if xkey in chart_df.columns and ykey in chart_df.columns:
        if pd.api.types.is_numeric_dtype(chart_df[ykey]):
            plot_df = chart_df.sort_values(ykey, ascending=False).head(15)
            fig = px.bar(plot_df, x=xkey, y=ykey, title=rq["question"], text_auto=True)
            fig.update_layout(xaxis_title="", yaxis_title="", height=520)
            st.plotly_chart(fig, use_container_width=True)
        else:
            counts = chart_df[xkey].value_counts().reset_index()
            counts.columns=[xkey,'count']
            fig = px.bar(counts.head(15), x=xkey, y='count', title=rq["question"], text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
    elif "Lifecycle_Status" in chart_df.columns:
        counts = chart_df["Lifecycle_Status"].value_counts().reset_index()
        counts.columns=["Lifecycle_Status", "count"]
        fig = px.bar(counts, x="Lifecycle_Status", y="count", title=rq["question"], text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.dataframe(chart_df.head(20), use_container_width=True)
with tabs[2]:
    st.dataframe(df.head(500), use_container_width=True)
with tabs[3]:
    st.markdown("### Interpretation")
    st.markdown(rq["interpretation"])
    st.markdown("### Recommended Actions")
    st.markdown(rq["recommendations"])
    st.markdown("### Methodology")
    st.markdown(rq["methodology"])
with tabs[4]:
    st.markdown(load_doc(rq["file"]))
