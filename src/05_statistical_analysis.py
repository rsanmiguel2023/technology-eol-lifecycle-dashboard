from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ENGINEERED = ROOT / "data" / "engineered"
REF = ROOT / "data" / "reference"
REPORTS = ROOT / "outputs" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

asset = pd.read_csv(ENGINEERED / "asset_lifecycle_analysis.csv")
sw = pd.read_csv(ENGINEERED / "software_lifecycle_analysis.csv")
bu = pd.read_csv(REF / "business_units.csv")
loc = pd.read_csv(REF / "locations.csv")

a = asset.merge(bu, on="Business_Unit_ID", how="left").merge(loc, on="Location_ID", how="left")

# -----------------------------------------------------------------------------
# Business unit lifecycle exposure and risk heatmap
# -----------------------------------------------------------------------------
bu_sum = a.groupby(["Business_Unit_ID", "Business_Unit_Name", "Business_Criticality"]).agg(
    Total_Assets=("Asset_ID", "count"),
    Past_EOL_Assets=("Past_EOL_Flag", "sum"),
    Expiring_12M_Assets=("Expiring_12M_Flag", "sum"),
    Expiring_24M_Assets=("Expiring_24M_Flag", "sum"),
    Expiring_36M_Assets=("Expiring_36M_Flag", "sum"),
    Critical_Vulnerability_Count=("Critical_Vulnerability_Count", "sum"),
    High_Vulnerability_Count=("High_Vulnerability_Count", "sum"),
    Total_Replacement_Cost=("Replacement_Cost", "sum"),
    Total_Downtime_Hours=("Downtime_Hours", "sum"),
    Incident_Count=("Incident_Count", "sum"),
    Avg_Risk_Score=("Lifecycle_Risk_Score", "mean"),
).reset_index()

bu_sum["Past_EOL_Pct"] = (bu_sum["Past_EOL_Assets"] / bu_sum["Total_Assets"] * 100).round(2)
bu_sum["Near_Term_Exposure_Pct"] = ((bu_sum["Past_EOL_Assets"] + bu_sum["Expiring_12M_Assets"]) / bu_sum["Total_Assets"] * 100).round(2)

# Executive risk index combines scale, cyber exposure, cost, downtime, and business criticality.
# This avoids a flat heatmap when percentages are similar across business units.
criticality_weight = {"Critical": 20, "High": 12, "Medium": 6, "Low": 0}
for col in [
    "Past_EOL_Assets",
    "Expiring_12M_Assets",
    "Critical_Vulnerability_Count",
    "Total_Replacement_Cost",
    "Total_Downtime_Hours",
]:
    min_v = bu_sum[col].min()
    max_v = bu_sum[col].max()
    bu_sum[f"{col}_Norm"] = ((bu_sum[col] - min_v) / (max_v - min_v) * 100) if max_v > min_v else 0

bu_sum["Executive_Risk_Index"] = (
    bu_sum["Past_EOL_Assets_Norm"] * 0.20
    + bu_sum["Expiring_12M_Assets_Norm"] * 0.15
    + bu_sum["Critical_Vulnerability_Count_Norm"] * 0.25
    + bu_sum["Total_Replacement_Cost_Norm"] * 0.20
    + bu_sum["Total_Downtime_Hours_Norm"] * 0.10
    + bu_sum["Business_Criticality"].map(criticality_weight).fillna(0)
).round(2)

bu_sum["Risk_Band"] = pd.cut(
    bu_sum["Executive_Risk_Index"],
    [-1, 20, 45, 85, 200],
    labels=["Low", "Medium", "High", "Critical"],
)

bu_sum.to_csv(REPORTS / "business_unit_eol_exposure.csv", index=False)
bu_sum.to_csv(REPORTS / "risk_heatmap_business_unit.csv", index=False)
bu_sum.to_csv(ENGINEERED / "business_unit_risk.csv", index=False)

# -----------------------------------------------------------------------------
# Cybersecurity risk: unsupported/near unsupported assets with open severe vulns
# -----------------------------------------------------------------------------
cyber = asset[
    (asset["Lifecycle_Status"].isin(["Past EOL", "Expiring in 12 Months"]))
    & ((asset["Critical_Vulnerability_Count"] > 0) | (asset["High_Vulnerability_Count"] > 1))
].copy()
cyber["Remediation_Priority"] = np.where(cyber["Lifecycle_Status"] == "Past EOL", "Immediate", "Accelerated")
cyber["Cyber_Risk_Category"] = np.where(
    cyber["Asset_Type"].isin([
        "Server", "Firewall", "Router", "Core Switch", "Distribution Switch", "Access Switch",
        "Storage", "Wireless AP", "Wireless Controller"
    ]),
    "Infrastructure / Network",
    "End User Computing / Branch",
)
cyber.to_csv(REPORTS / "past_eol_critical_vulnerability_assets.csv", index=False)
cyber.to_csv(ENGINEERED / "cyber_risk_analysis.csv", index=False)
cyber.groupby(["Asset_Type", "Cyber_Risk_Category"]).agg(
    Asset_Count=("Asset_ID", "count"),
    Critical_Vulnerabilities=("Critical_Vulnerability_Count", "sum"),
    High_Vulnerabilities=("High_Vulnerability_Count", "sum"),
).reset_index().to_csv(REPORTS / "cybersecurity_unsupported_critical_summary.csv", index=False)

# -----------------------------------------------------------------------------
# Software compliance risk summary
# -----------------------------------------------------------------------------
sw_sum = sw.groupby([
    "Software_Name", "Software_Version", "Publisher", "Software_Category",
    "Software_EOL_Status", "Software_Compliance_Risk"
]).agg(
    Installation_Count=("Installation_ID", "count"),
    Asset_Count=("Asset_ID", "nunique"),
).reset_index()

risk_order = {"High": 0, "Medium": 1, "Low": 2}
sw_sum["Risk_Sort"] = sw_sum["Software_Compliance_Risk"].map(risk_order).fillna(9)
sw_sum = sw_sum.sort_values(["Risk_Sort", "Installation_Count"], ascending=[True, False]).drop(columns=["Risk_Sort"])
sw_sum.to_csv(REPORTS / "software_compliance_risk_summary.csv", index=False)
sw_sum.to_csv(REPORTS / "compliance_software_versions_summary.csv", index=False)

# -----------------------------------------------------------------------------
# Lifecycle exposure by type and refresh forecast
# -----------------------------------------------------------------------------
lifecycle_type = asset.groupby(["Asset_Type", "Lifecycle_Status"]).agg(
    Asset_Count=("Asset_ID", "count"),
    Replacement_Cost=("Replacement_Cost", "sum"),
).reset_index()
lifecycle_type.to_csv(REPORTS / "lifecycle_exposure_by_asset_type.csv", index=False)

refresh = asset[asset["Lifecycle_Status"].isin([
    "Past EOL", "Expiring in 12 Months", "Expiring in 24 Months", "Expiring in 36 Months"
])].copy()
refresh["Refresh_Year"] = np.select(
    [
        refresh["Lifecycle_Status"] == "Past EOL",
        refresh["Lifecycle_Status"] == "Expiring in 12 Months",
        refresh["Lifecycle_Status"] == "Expiring in 24 Months",
    ],
    [2026, 2027, 2028],
    default=2029,
)
refresh_fcst = refresh.groupby("Refresh_Year").agg(
    Assets=("Asset_ID", "count"),
    Estimated_Refresh_Cost=("Replacement_Cost", "sum"),
).reset_index()
refresh_fcst.to_csv(REPORTS / "refresh_budget_planning_summary.csv", index=False)
refresh_fcst.to_csv(ENGINEERED / "refresh_forecast.csv", index=False)

# -----------------------------------------------------------------------------
# Operational impact by lifecycle status
# Keep actual incident/downtime metrics and add an executive disruption index.
# -----------------------------------------------------------------------------
op = asset.groupby("Lifecycle_Status").agg(
    Asset_Count=("Asset_ID", "count"),
    Incident_Count=("Incident_Count", "sum"),
    Downtime_Hours=("Downtime_Hours", "sum"),
    Avg_Downtime_Per_Asset=("Downtime_Hours", "mean"),
    Avg_Incidents_Per_Asset=("Incident_Count", "mean"),
).reset_index()

impact_weight = {
    "Past EOL": 1.35,
    "Expiring in 12 Months": 1.15,
    "Expiring in 24 Months": 1.05,
    "Expiring in 36 Months": 1.00,
    "Supported": 0.85,
}
op["Lifecycle_Impact_Weight"] = op["Lifecycle_Status"].map(impact_weight).fillna(1.0)
op["Operational_Disruption_Index"] = (
    (op["Avg_Incidents_Per_Asset"] * 10 + op["Avg_Downtime_Per_Asset"])
    * op["Lifecycle_Impact_Weight"]
).round(2)

op.to_csv(REPORTS / "operational_impact_by_lifecycle_status.csv", index=False)
op.to_csv(REPORTS / "incident_downtime_by_lifecycle.csv", index=False)
op.to_csv(ENGINEERED / "operational_risk_analysis.csv", index=False)

print("Statistical and executive analysis reports exported")
print("Lifecycle distribution:")
print(asset["Lifecycle_Status"].value_counts())
print("Risk bands:")
print(bu_sum[["Business_Unit_Name", "Past_EOL_Pct", "Near_Term_Exposure_Pct", "Executive_Risk_Index", "Risk_Band"]])
