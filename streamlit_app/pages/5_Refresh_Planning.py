
import streamlit as st
from common import *

apply_page_config("Refresh Planning")
page_header(
    "Refresh Planning",
    "Multi-year investment roadmap for reducing lifecycle risk and technology debt.",
    "Investment planning",
)

refresh = read_engineered("refresh_forecast.csv")
asset = read_engineered("asset_lifecycle_analysis.csv")
bu = read_engineered("business_unit_risk.csv")

if refresh.empty:
    st.warning("Refresh forecast table not found.")
    st.stop()

total_cost = refresh["Estimated_Refresh_Cost"].sum()
peak = refresh.sort_values("Estimated_Refresh_Cost", ascending=False).iloc[0]
metric_row([
    ("Forecast refresh cost", money(total_cost), "FY2026–FY2029"),
    ("Peak funding year", f"FY{int(peak['Refresh_Year'])}", money(peak["Estimated_Refresh_Cost"])),
    ("Assets in roadmap", number(refresh["Assets"].sum())),
    ("Past-EOL refresh wave", number(refresh.loc[refresh["Refresh_Year"] == 2026, "Assets"].sum())),
    ("Average cost/asset", money(total_cost / max(refresh["Assets"].sum(), 1))),
    ("Business units", number(bu["Business_Unit_Name"].nunique()) if not bu.empty else "N/A"),
    ("Highest-cost BU", bu.sort_values("Total_Replacement_Cost", ascending=False).iloc[0]["Business_Unit_Name"] if not bu.empty else "N/A"),
    ("Highest BU cost", money(bu.sort_values("Total_Replacement_Cost", ascending=False).iloc[0]["Total_Replacement_Cost"]) if not bu.empty else "N/A"),
])

st.markdown(read_doc("refresh_planning.md"))

line_chart(refresh, "Refresh_Year", "Estimated_Refresh_Cost", "Refresh investment roadmap")

if not bu.empty:
    st.subheader("Replacement cost by business unit")
    display = bu.sort_values("Total_Replacement_Cost", ascending=True)
    bar_chart(display, "Total_Replacement_Cost", "Business_Unit_Name", "Estimated replacement cost by business unit", color="Risk_Band", orientation="h")
