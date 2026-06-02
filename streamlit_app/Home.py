from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
for p in [ROOT, ROOT / "streamlit_app"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from streamlit_app.doc_loader import load_doc
from streamlit_app.ui_components import inject_css, exec_banner, management_question, insight, recommendation, tip_header

st.set_page_config(page_title="Technology Lifecycle Executive Summary", page_icon="🏦", layout="wide")
inject_css()
REPORTS = ROOT / "outputs" / "reports"
questions = pd.read_csv(REPORTS / "executive_questions_summary.csv")
lifecycle = pd.read_csv(REPORTS / "executive_lifecycle_summary.csv")
bu = pd.read_csv(REPORTS / "business_unit_eol_exposure.csv")
recs = pd.read_csv(REPORTS / "recommendation_actions.csv")

st.title("🏦 Technology Lifecycle Executive Summary")
management_question("What is the current lifecycle risk position of the bank's technology estate, and what decisions are required from leadership?")
exec_banner(load_doc("executive_summary.md").split("## Management Message")[-1].split("## Executive Questions")[0].strip())

past = int(lifecycle.loc[lifecycle["Lifecycle_Status"].eq("Past EOL"), "assets"].sum())
exp12 = int(lifecycle.loc[lifecycle["Lifecycle_Status"].isin(["0-6 Months", "6-12 Months"]), "assets"].sum())
critical_vulns = int(lifecycle["critical_vulns"].sum())
downtime = float(lifecycle["downtime_hours"].sum())
replacement = float(lifecycle["replacement_cost"].sum())
top_bu = bu.iloc[0]["Business_Unit"]

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Past EOL", f"{past:,}", help="Assets already beyond expected support or lifecycle date.")
c2.metric("Due <12 Months", f"{exp12:,}", help="Assets reaching EOL within the next 12 months.")
c3.metric("Critical Vulns", f"{critical_vulns:,}", help="Critical vulnerabilities linked to assets in the model.")
c4.metric("Refresh Exposure", f"${replacement/1_000_000:,.1f}M", help="Estimated replacement exposure across lifecycle groups.")
c5.metric("Highest Risk BU", str(top_bu), help="Business unit with the highest combined lifecycle, vulnerability, and downtime score.")
c6.metric("Downtime Hours", f"{downtime:,.0f}", help="Total downtime linked to assets in the synthetic model.")

st.divider()
left, right = st.columns([1.15, .85])
with left:
    tip_header("Executive questions and answers", "These are the business questions the dashboard is designed to answer for senior management.", level=2)
    st.dataframe(questions[["business_question", "executive_answer", "source_file"]], use_container_width=True, hide_index=True)
with right:
    tip_header("Top management actions", "Prioritized actions generated from lifecycle, vulnerability, budget, software, and incident reports.", level=2)
    for _, row in recs.head(5).iterrows():
        st.markdown(f"<div class='priority-card'><div class='priority-title'>Priority {int(row['priority'])}: {row['action']}</div>{row['rationale']}<div class='footer-note'>Owner: {row['owner']} | Timeframe: {row['timeframe']}</div></div>", unsafe_allow_html=True)

st.divider()
fig = px.bar(bu.sort_values("risk_rank_score", ascending=True).tail(10), x="risk_rank_score", y="Business_Unit", orientation="h", title="Top Business Units by Lifecycle Risk Score", text="risk_rank_score")
fig.update_layout(xaxis_title="Risk score", yaxis_title="", height=520)
st.plotly_chart(fig, use_container_width=True)

insight("The executive summary should be used as the first page in leadership discussions. It shows the size of the unsupported estate, the near-term refresh demand, the business areas with the greatest exposure, and the immediate remediation priorities.")
recommendation("Use the Recommendations page to convert this view into a 30-60-90 day remediation plan and a funded 24-month refresh roadmap.")
