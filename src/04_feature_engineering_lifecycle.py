from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
REF = ROOT / "data" / "reference"
ENGINEERED = ROOT / "data" / "engineered"
REPORTS = ROOT / "outputs" / "reports"
ENGINEERED.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)
ANALYSIS_DATE = pd.Timestamp("2026-06-02")

# -----------------------------------------------------------------------------
# Load cleaned source extracts and reference tables
# -----------------------------------------------------------------------------
hw = pd.read_csv(
    PROCESSED / "hardware_assets.csv",
    parse_dates=["Purchase_Date", "Install_Date", "Warranty_End_Date", "Last_Discovered_Date"],
)
href = pd.read_csv(
    REF / "hardware_model_reference.csv",
    parse_dates=["Model_Release_Date", "Vendor_Support_End_Date"],
)
vuln = pd.read_csv(PROCESSED / "vulnerabilities.csv")
inc = pd.read_csv(PROCESSED / "incidents.csv", parse_dates=["Opened_DateTime", "Closed_DateTime"])
sw = pd.read_csv(PROCESSED / "software_installations.csv")
sref = pd.read_csv(
    REF / "software_lifecycle_reference.csv",
    parse_dates=["Release_Date", "Vendor_Support_End_Date"],
)

# -----------------------------------------------------------------------------
# Hardware lifecycle feature engineering
# Lifecycle fields are deliberately created here, not stored in raw data.
# -----------------------------------------------------------------------------
asset = hw.merge(href, on=["Asset_Type", "Manufacturer", "Model"], how="left")
asset["Asset_Age_Years"] = ((ANALYSIS_DATE - asset["Install_Date"]).dt.days / 365.25).round(2)
asset["Warranty_Status"] = np.where(
    asset["Warranty_End_Date"] < ANALYSIS_DATE,
    "Warranty Expired",
    "Under Warranty",
)

asset["Months_To_EOL"] = ((asset["Vendor_Support_End_Date"] - ANALYSIS_DATE).dt.days / 30.44).round(1)

conditions = [
    asset["Vendor_Support_End_Date"] < ANALYSIS_DATE,
    asset["Vendor_Support_End_Date"] <= ANALYSIS_DATE + pd.DateOffset(months=12),
    asset["Vendor_Support_End_Date"] <= ANALYSIS_DATE + pd.DateOffset(months=24),
    asset["Vendor_Support_End_Date"] <= ANALYSIS_DATE + pd.DateOffset(months=36),
]
choices = [
    "Past EOL",
    "Expiring in 12 Months",
    "Expiring in 24 Months",
    "Expiring in 36 Months",
]
asset["Lifecycle_Status"] = np.select(conditions, choices, default="Supported")
asset["Past_EOL_Flag"] = (asset["Lifecycle_Status"] == "Past EOL").astype(int)
asset["Expiring_12M_Flag"] = (asset["Lifecycle_Status"] == "Expiring in 12 Months").astype(int)
asset["Expiring_24M_Flag"] = (asset["Lifecycle_Status"] == "Expiring in 24 Months").astype(int)
asset["Expiring_36M_Flag"] = (asset["Lifecycle_Status"] == "Expiring in 36 Months").astype(int)

# Replacement cost is engineered from the model reference table and purchase cost.
asset["Replacement_Cost"] = asset["Standard_Replacement_Cost"].fillna(asset["Purchase_Cost"] * 1.15).round(2)

# -----------------------------------------------------------------------------
# Vulnerability aggregation
# -----------------------------------------------------------------------------
open_v = vuln[vuln["Remediation_Status"].isin(["Open", "In Progress", "Exception Requested"])]
vagg = open_v.groupby("Asset_ID").agg(
    Open_Vulnerability_Count=("Finding_ID", "count"),
    Critical_Vulnerability_Count=("Severity", lambda x: int((x == "Critical").sum())),
    High_Vulnerability_Count=("Severity", lambda x: int((x == "High").sum())),
).reset_index()
asset = asset.merge(vagg, on="Asset_ID", how="left")
for col in ["Open_Vulnerability_Count", "Critical_Vulnerability_Count", "High_Vulnerability_Count"]:
    asset[col] = asset[col].fillna(0).astype(int)

# -----------------------------------------------------------------------------
# Incident aggregation
# -----------------------------------------------------------------------------
inc["Downtime_Hours"] = ((inc["Closed_DateTime"] - inc["Opened_DateTime"]).dt.total_seconds() / 3600).fillna(0)
incagg = inc.groupby("Asset_ID").agg(
    Incident_Count=("Incident_ID", "count"),
    Downtime_Hours=("Downtime_Hours", "sum"),
).reset_index()
asset = asset.merge(incagg, on="Asset_ID", how="left")
asset["Incident_Count"] = asset["Incident_Count"].fillna(0).astype(int)
asset["Downtime_Hours"] = asset["Downtime_Hours"].fillna(0).round(2)

# -----------------------------------------------------------------------------
# Lifecycle risk model
# -----------------------------------------------------------------------------
asset["Lifecycle_Risk_Score"] = (
    asset["Past_EOL_Flag"] * 35
    + asset["Expiring_12M_Flag"] * 18
    + asset["Expiring_24M_Flag"] * 10
    + asset["Expiring_36M_Flag"] * 5
    + np.minimum(asset["Critical_Vulnerability_Count"], 5) * 8
    + np.minimum(asset["High_Vulnerability_Count"], 5) * 4
    + np.minimum(asset["Incident_Count"], 10) * 2
    + np.minimum(asset["Downtime_Hours"], 100) * 0.05
).clip(0, 100).round(2)
asset["Refresh_Priority"] = pd.cut(
    asset["Lifecycle_Risk_Score"],
    [-1, 30, 55, 75, 100],
    labels=["Low", "Medium", "High", "Critical"],
)
asset.to_csv(ENGINEERED / "asset_lifecycle_analysis.csv", index=False)

# -----------------------------------------------------------------------------
# Software lifecycle and compliance feature engineering
# -----------------------------------------------------------------------------
sw_eng = sw.merge(
    sref,
    left_on=["Publisher", "Software_Name", "Software_Version"],
    right_on=["Publisher", "Software_Name", "Version"],
    how="left",
)
sw_eng["Months_To_Software_EOL"] = ((sw_eng["Vendor_Support_End_Date"] - ANALYSIS_DATE).dt.days / 30.44).round(1)
sw_eng["Software_EOL_Status"] = np.select(
    [
        sw_eng["Vendor_Support_End_Date"] < ANALYSIS_DATE,
        sw_eng["Vendor_Support_End_Date"] <= ANALYSIS_DATE + pd.DateOffset(months=12),
        sw_eng["Vendor_Support_End_Date"] <= ANALYSIS_DATE + pd.DateOffset(months=24),
    ],
    ["Unsupported", "Support Ending in 12 Months", "Support Ending in 24 Months"],
    default="Supported",
)
sw_eng["Software_Compliance_Risk"] = np.select(
    [
        sw_eng["Software_EOL_Status"] == "Unsupported",
        sw_eng["Software_EOL_Status"] == "Support Ending in 12 Months",
        sw_eng["Software_EOL_Status"] == "Support Ending in 24 Months",
    ],
    ["High", "Medium", "Medium"],
    default="Low",
)
sw_eng.to_csv(ENGINEERED / "software_lifecycle_analysis.csv", index=False)

asset.groupby(["Asset_Type", "Lifecycle_Status"]).agg(
    Asset_Count=("Asset_ID", "count"),
    Replacement_Cost=("Replacement_Cost", "sum"),
).reset_index().to_csv(ENGINEERED / "asset_lifecycle_by_type.csv", index=False)

print("Engineered lifecycle and software compliance datasets exported to data/engineered")
print(asset["Lifecycle_Status"].value_counts())
