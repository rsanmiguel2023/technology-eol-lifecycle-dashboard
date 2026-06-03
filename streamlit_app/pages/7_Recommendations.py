
import streamlit as st
from common import *

apply_page_config("Recommendations")
page_header(
    "Recommendations",
    "Prioritized management actions for reducing technology lifecycle, cybersecurity, compliance, and operational risk.",
    "Action plan",
)

recs = read_report("recommendation_actions.csv")
bu = read_engineered("business_unit_risk.csv")
cyber = read_engineered("cyber_risk_analysis.csv")
refresh = read_engineered("refresh_forecast.csv")

metric_row([
    ("Immediate actions", number((recs["Priority"] == "Immediate").sum()) if not recs.empty else "N/A"),
    ("Near-term actions", number((recs["Priority"] == "Near Term").sum()) if not recs.empty else "N/A"),
    ("Strategic actions", number((recs["Priority"] == "Strategic").sum()) if not recs.empty else "N/A"),
    ("Critical business units", number((bu["Risk_Band"] == "Critical").sum()) if not bu.empty else "N/A"),
    ("Cyber assets in scope", number(len(cyber)) if not cyber.empty else "N/A"),
    ("Refresh roadmap cost", money(refresh["Estimated_Refresh_Cost"].sum()) if not refresh.empty else "N/A"),
    ("Refresh years", number(refresh["Refresh_Year"].nunique()) if not refresh.empty else "N/A"),
    ("Governance owner", "Technology Risk"),
])

st.markdown(read_doc("recommendations.md"))

if not recs.empty:
    for _, row in recs.iterrows():
        st.markdown(
            f"""
            <div class="insight-box">
                <h3>{row['Recommended_Action']}</h3>
                <p><strong>Priority:</strong> {row['Priority']} &nbsp; | &nbsp;
                <strong>Owner:</strong> {row['Owner']} &nbsp; | &nbsp;
                <strong>Timeframe:</strong> {row['Timeframe']}</p>
                <p>{row['Rationale']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
