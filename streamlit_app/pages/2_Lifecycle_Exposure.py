
import streamlit as st
from common import *

apply_page_config("Lifecycle Exposure")
page_header(
    "Lifecycle Exposure",
    "Where unsupported and near-end-of-life technology is concentrated across the organization.",
    "Lifecycle governance",
)

asset = read_engineered("asset_lifecycle_analysis.csv")
bu = read_engineered("business_unit_risk.csv")
asset_type = read_engineered("asset_lifecycle_by_type.csv")
if asset.empty:
    st.warning("Asset lifecycle analysis not found.")
    st.stop()

total = len(asset)
past = int(asset["Past_EOL_Flag"].sum())
exp12 = int(asset["Expiring_12M_Flag"].sum())
near = int(asset["Expiring_12M_Flag"].sum() + asset["Expiring_24M_Flag"].sum() + asset["Expiring_36M_Flag"].sum())

metric_row([
    ("Past EOL assets", number(past), f"{past/total:.1%} of estate"),
    ("Expiring in 12 months", number(asset["Expiring_12M_Flag"].sum())),
    ("Expiring in 24 months", number(asset["Expiring_24M_Flag"].sum())),
    ("Expiring in 36 months", number(asset["Expiring_36M_Flag"].sum())),
    ("Near-term exposure", number(near), "within 36 months"),
    ("Highest risk unit", bu.sort_values("Executive_Risk_Index", ascending=False).iloc[0]["Business_Unit_Name"] if not bu.empty else "N/A"),
    ("Critical risk bands", number((bu["Risk_Band"] == "Critical").sum()) if not bu.empty else "N/A"),
    ("High risk bands", number((bu["Risk_Band"] == "High").sum()) if not bu.empty else "N/A"),
])

st.markdown(read_doc("lifecycle_exposure.md"))

if not bu.empty:
    st.subheader("Business unit exposure")
    display = bu[["Business_Unit_Name", "Total_Assets", "Past_EOL_Assets", "Expiring_12M_Assets", "Near_Term_Exposure_Pct", "Executive_Risk_Index", "Risk_Band"]].sort_values("Executive_Risk_Index", ascending=False)
    st.dataframe(display, use_container_width=True, hide_index=True)
    bar_chart(display.sort_values("Executive_Risk_Index", ascending=True), "Executive_Risk_Index", "Business_Unit_Name", "Executive lifecycle risk index", color="Risk_Band", orientation="h")

st.subheader("Lifecycle by asset type")
if not asset_type.empty:
    bar_chart(asset_type, "Asset_Type", "Asset_Count", "Lifecycle exposure by asset type", color="Lifecycle_Status")
