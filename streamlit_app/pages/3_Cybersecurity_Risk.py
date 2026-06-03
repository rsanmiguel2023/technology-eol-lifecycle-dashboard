
import streamlit as st
from common import *

apply_page_config("Cybersecurity Risk")
page_header(
    "Cybersecurity Risk",
    "Unsupported and near-EOL assets with critical or high vulnerability exposure.",
    "Cyber exposure",
)

cyber = read_engineered("cyber_risk_analysis.csv")
summary = read_report("cybersecurity_unsupported_critical_summary.csv")
if cyber.empty:
    st.warning("Cyber risk analysis table not found.")
    st.stop()

critical = int(cyber["Critical_Vulnerability_Count"].sum()) if "Critical_Vulnerability_Count" in cyber.columns else 0
high = int(cyber["High_Vulnerability_Count"].sum()) if "High_Vulnerability_Count" in cyber.columns else 0
past = int((cyber["Lifecycle_Status"] == "Past EOL").sum()) if "Lifecycle_Status" in cyber.columns else 0
immediate = int((cyber["Remediation_Priority"] == "Immediate").sum()) if "Remediation_Priority" in cyber.columns else 0

metric_row([
    ("Assets in cyber-risk scope", number(len(cyber))),
    ("Critical vulnerabilities", number(critical)),
    ("High vulnerabilities", number(high)),
    ("Past-EOL cyber assets", number(past)),
    ("Immediate remediation", number(immediate)),
    ("Asset types affected", number(cyber["Asset_Type"].nunique())),
    ("Business units affected", number(cyber["Business_Unit_ID"].nunique())),
    ("Top asset type", cyber["Asset_Type"].value_counts().idxmax()),
])

insight(
    f"<strong>Immediate action required:</strong> {number(len(cyber))} unsupported or near-EOL assets have critical/high vulnerability exposure. Prioritize immediate remediation for past-EOL assets and accelerated refresh for assets expiring within 12 months.",
    kind="alert",
)

st.markdown(read_doc("cybersecurity_risk.md"))

if not summary.empty:
    st.subheader("Cyber exposure by asset type")
    bar_chart(summary.sort_values("Asset_Count", ascending=True), "Asset_Count", "Asset_Type", "Unsupported or near-EOL vulnerable assets", color="Cyber_Risk_Category", orientation="h")
    st.dataframe(summary, use_container_width=True, hide_index=True)

st.subheader("Remediation priority")
priority = cyber["Remediation_Priority"].value_counts().reset_index()
priority.columns = ["Remediation_Priority", "Asset_Count"]
bar_chart(priority, "Remediation_Priority", "Asset_Count", "Assets by remediation priority", color="Remediation_Priority")
