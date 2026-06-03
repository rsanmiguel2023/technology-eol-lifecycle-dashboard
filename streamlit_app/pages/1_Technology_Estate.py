
import streamlit as st
import plotly.express as px
from common import *

apply_page_config("Technology Estate")
page_header(
    "Technology Estate",
    "Portfolio-level view of managed assets, software footprint, business units, and platform composition.",
    "Estate overview",
)

asset = read_engineered("asset_lifecycle_analysis.csv")
software = read_engineered("software_lifecycle_analysis.csv")

if asset.empty:
    st.warning("Engineered asset lifecycle table not found.")
    st.stop()

metric_row([
    ("Managed assets", number(len(asset))),
    ("Software installations", number(len(software)) if not software.empty else "N/A"),
    ("Asset types", number(asset["Asset_Type"].nunique())),
    ("Manufacturers", number(asset["Manufacturer"].nunique())),
    ("Business units", number(asset["Business_Unit_ID"].nunique())),
    ("Inventory sources", number(asset["Inventory_Source"].nunique())),
    ("Production assets", number((asset["Environment"] == "Production").sum())),
    ("Warranty expired", number((asset["Warranty_Status"] == "Warranty Expired").sum())),
])

st.markdown(read_doc("technology_estate.md"))

c1, c2 = st.columns(2)
with c1:
    asset_type = asset["Asset_Type"].value_counts().reset_index()
    asset_type.columns = ["Asset_Type", "Asset_Count"]
    bar_chart(asset_type.sort_values("Asset_Count", ascending=True), "Asset_Count", "Asset_Type", "Managed assets by asset type", orientation="h")
with c2:
    env = asset["Environment"].value_counts().reset_index()
    env.columns = ["Environment", "Asset_Count"]
    bar_chart(env, "Environment", "Asset_Count", "Assets by environment", color="Environment")

st.subheader("Manufacturer footprint")
mfg = asset["Manufacturer"].value_counts().reset_index()
mfg.columns = ["Manufacturer", "Asset_Count"]
bar_chart(mfg.sort_values("Asset_Count", ascending=True), "Asset_Count", "Manufacturer", "Asset count by manufacturer", orientation="h")
