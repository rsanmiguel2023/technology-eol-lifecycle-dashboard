
import streamlit as st
from common import *

apply_page_config("Operational Impact")
page_header(
    "Operational Impact",
    "Incident and downtime patterns by lifecycle status, translated into management-level disruption indicators.",
    "Service resilience",
)

op = read_engineered("operational_risk_analysis.csv")
if op.empty:
    st.warning("Operational risk analysis table not found.")
    st.stop()

past = op[op["Lifecycle_Status"] == "Past EOL"].iloc[0] if (op["Lifecycle_Status"] == "Past EOL").any() else op.iloc[0]
highest = op.sort_values("Operational_Disruption_Index", ascending=False).iloc[0]

metric_row([
    ("Past-EOL incidents", number(past["Incident_Count"])),
    ("Past-EOL downtime", number(past["Downtime_Hours"]), "hours"),
    ("Past-EOL disruption index", f"{past['Operational_Disruption_Index']:.1f}"),
    ("Highest disruption status", highest["Lifecycle_Status"]),
    ("Highest disruption index", f"{highest['Operational_Disruption_Index']:.1f}"),
    ("Avg downtime/asset", f"{past['Avg_Downtime_Per_Asset']:.1f}", "hours"),
    ("Avg incidents/asset", f"{past['Avg_Incidents_Per_Asset']:.2f}"),
    ("Lifecycle statuses", number(op["Lifecycle_Status"].nunique())),
])

st.markdown(read_doc("operational_impact.md"))

bar_chart(op.sort_values("Operational_Disruption_Index", ascending=True), "Operational_Disruption_Index", "Lifecycle_Status", "Operational disruption index by lifecycle status", orientation="h")
bar_chart(op.sort_values("Downtime_Hours", ascending=False), "Lifecycle_Status", "Downtime_Hours", "Downtime hours by lifecycle status", color="Lifecycle_Status")

st.dataframe(op, use_container_width=True, hide_index=True)
