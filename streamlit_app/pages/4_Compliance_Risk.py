
import streamlit as st
from common import *

apply_page_config("Compliance Risk")
page_header(
    "Compliance Risk",
    "Unsupported software versions and compliance exposure across the endpoint and infrastructure estate.",
    "Software lifecycle",
)

sw = read_engineered("software_lifecycle_analysis.csv")
summary = read_report("software_compliance_risk_summary.csv")
if sw.empty:
    st.warning("Software lifecycle analysis table not found.")
    st.stop()

unsupported = int((sw["Software_EOL_Status"] == "Unsupported").sum())
high = int((sw["Software_Compliance_Risk"] == "High").sum())
medium = int((sw["Software_Compliance_Risk"] == "Medium").sum())

metric_row([
    ("Software installs", number(len(sw))),
    ("Unsupported installs", number(unsupported)),
    ("High compliance risk", number(high)),
    ("Medium compliance risk", number(medium)),
    ("Software products", number(sw["Software_Name"].nunique())),
    ("Publishers", number(sw["Publisher"].nunique())),
    ("Software categories", number(sw["Software_Category"].nunique())),
    ("Assets affected", number(sw["Asset_ID"].nunique())),
])

st.markdown(read_doc("compliance_risk.md"))

if not summary.empty:
    st.subheader("Top unsupported software versions")
    top = summary.sort_values("Installation_Count", ascending=False).head(12)
    bar_chart(top.sort_values("Installation_Count", ascending=True), "Installation_Count", "Software_Name", "Unsupported software installations", color="Software_Compliance_Risk", orientation="h")
    st.dataframe(top, use_container_width=True, hide_index=True)

st.subheader("Compliance risk distribution")
risk = sw["Software_Compliance_Risk"].value_counts().reset_index()
risk.columns = ["Software_Compliance_Risk", "Installation_Count"]
bar_chart(risk, "Software_Compliance_Risk", "Installation_Count", "Installations by compliance risk", color="Software_Compliance_Risk")
