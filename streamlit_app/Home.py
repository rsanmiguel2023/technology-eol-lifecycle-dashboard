
import pandas as pd
import streamlit as st
import plotly.express as px
from common import *

apply_page_config("Executive Summary")

page_header(
    "Technology Lifecycle Governance Dashboard",
    "Executive technology risk, compliance exposure, and refresh planning overview for Maple Financial Bank.",
    "Executive summary",
)

asset = read_engineered("asset_lifecycle_analysis.csv")
software = read_engineered("software_lifecycle_analysis.csv")
bu = read_engineered("business_unit_risk.csv")
cyber = read_engineered("cyber_risk_analysis.csv")
refresh = read_engineered("refresh_forecast.csv")
op = read_engineered("operational_risk_analysis.csv")

if asset.empty:
    st.warning("Run the full pipeline first. Expected engineered files were not found.")
    st.stop()

total_assets = len(asset)
past_eol = int(asset["Past_EOL_Flag"].sum())
exp12 = int(asset["Expiring_12M_Flag"].sum())
exp24 = int(asset["Expiring_24M_Flag"].sum())
exp36 = int(asset["Expiring_36M_Flag"].sum())
unsupported_sw = int((software["Software_EOL_Status"] == "Unsupported").sum()) if not software.empty else 0
cyber_assets = len(cyber)
refresh_cost = int(refresh["Estimated_Refresh_Cost"].sum()) if not refresh.empty else 0
top_bu = bu.sort_values("Executive_Risk_Index", ascending=False).iloc[0] if not bu.empty else None
past_downtime = float(op.loc[op["Lifecycle_Status"] == "Past EOL", "Downtime_Hours"].iloc[0]) if not op.empty and (op["Lifecycle_Status"] == "Past EOL").any() else 0

metric_row(
    [
        ("Managed assets", number(total_assets), None, "Total technology assets in the managed inventory."),
        ("Past vendor support", number(past_eol), f"{past_eol/total_assets:.1%} of estate", "Assets already beyond vendor support."),
        ("Expiring in 12 months", number(exp12), None, "Assets requiring near-term refresh planning."),
        ("Unsupported software", number(unsupported_sw), None, "Software installations past vendor support."),
        ("Critical/high cyber exposure", number(cyber_assets), None, "Unsupported or near-EOL assets with critical/high findings."),
        ("Refresh investment", money(refresh_cost), "FY2026–FY2029", "Estimated replacement cost for refresh forecast."),
        ("Past-EOL downtime", number(past_downtime), "hours", "Downtime hours associated with past-EOL assets."),
        ("Highest risk area", top_bu["Business_Unit_Name"] if top_bu is not None else "N/A", top_bu["Risk_Band"] if top_bu is not None else None, "Business unit with highest executive risk index."),
    ],
    columns=4,
)

insight(
    f"""
    <strong>Executive interpretation:</strong> {number(past_eol)} assets are already beyond vendor support, while 
    {number(exp12)} more expire within 12 months. The organization requires {money(refresh_cost)} in forecast refresh 
    investment and should prioritize {number(cyber_assets)} unsupported or near-EOL assets with critical/high vulnerability exposure.
    """
)

st.markdown(read_doc("executive_summary.md"))

st.subheader("Lifecycle exposure at a glance")
lifecycle_summary = (
    asset.groupby("Lifecycle_Status", as_index=False)
    .agg(Asset_Count=("Asset_ID", "count"), Replacement_Cost=("Replacement_Cost", "sum"))
)
bar_chart(
    lifecycle_summary.sort_values("Asset_Count", ascending=False),
    x="Lifecycle_Status",
    y="Asset_Count",
    title="Asset lifecycle status distribution",
    color="Lifecycle_Status",
)

st.subheader("Executive risk by business unit")
if not bu.empty:
    top = bu.sort_values("Executive_Risk_Index", ascending=True)
    bar_chart(top, x="Executive_Risk_Index", y="Business_Unit_Name", title="Executive risk index by business unit", color="Risk_Band", orientation="h")
