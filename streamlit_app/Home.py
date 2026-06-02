import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
for p in [ROOT, ROOT / "streamlit_app"]:
    if str(p) not in sys.path: sys.path.insert(0, str(p))
from streamlit_app.doc_loader import load_doc, rq_content
from streamlit_app.ui_components import inject_css, exec_banner

st.set_page_config(page_title="Technology EOL Executive Dashboard", page_icon="🏦", layout="wide")
inject_css()

REPORTS = ROOT / "outputs" / "reports"
summary = pd.read_csv(REPORTS / "executive_lifecycle_summary.csv")
assets = int(summary["assets"].sum())
past = int(summary.loc[summary["Lifecycle_Status"].eq("Past EOL"), "assets"].sum())
critical = int(summary["critical_vulns"].sum())
downtime = float(summary["downtime_hours"].sum())
replacement = float(summary["replacement_cost"].sum())

st.title("🏦 Technology End-of-Life Lifecycle Management")
st.caption("Synthetic banking portfolio project | Executive-ready Streamlit dashboard | Documentation-driven RQ pages")
exec_banner(load_doc("executive_summary.md").split("## Management Message")[-1].strip())

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total Assets", f"{assets:,}", help="All hardware and infrastructure assets in the analytical model.")
c2.metric("Past EOL Assets", f"{past:,}", help="Assets already past expected vendor support or internal lifecycle date.")
c3.metric("Critical Vulnerabilities", f"{critical:,}", help="Total critical vulnerabilities linked to assets in the model.")
c4.metric("Downtime Hours", f"{downtime:,.0f}", help="Total incident downtime linked to assets.")
c5.metric("Replacement Exposure", f"${replacement/1_000_000:,.1f}M", help="Estimated replacement cost across lifecycle groups.")

st.divider()
st.subheader("Primary Research Questions")
for i in range(1,7):
    rq = rq_content(i)
    with st.expander(f"RQ{i}: {rq['question']}", expanded=i==1):
        st.markdown(rq['executive_summary'])
        st.markdown("**Hypothesis framing**")
        st.markdown(rq['hypotheses'])
        st.markdown("**Recommended action**")
        st.markdown(rq['recommendations'])

st.divider()
st.subheader("Documentation Library")
st.markdown(load_doc("analytics.md"))
