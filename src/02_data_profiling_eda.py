
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REF = ROOT / "data" / "reference"
REPORTS = ROOT / "outputs" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

hw = pd.read_csv(RAW / "hardware_assets_raw.csv")
sw = pd.read_csv(RAW / "software_installations_raw.csv")
vuln = pd.read_csv(RAW / "vulnerabilities_raw.csv")
inc = pd.read_csv(RAW / "incidents_raw.csv")
bu = pd.read_csv(REF / "business_units.csv")
loc = pd.read_csv(REF / "locations.csv")

hw["Asset_Type"].value_counts().rename_axis("Asset_Type").reset_index(name="Asset_Count").to_csv(REPORTS / "eda_asset_type_distribution.csv", index=False)
hw.merge(bu, on="Business_Unit_ID", how="left").groupby("Business_Unit_Name").agg(Asset_Count=("Asset_ID", "count")).reset_index().sort_values("Asset_Count", ascending=False).to_csv(REPORTS / "eda_business_unit_asset_distribution.csv", index=False)
hw.merge(loc, on="Location_ID", how="left").groupby(["Region_Code", "Office_Type"]).agg(Asset_Count=("Asset_ID", "count")).reset_index().to_csv(REPORTS / "eda_region_office_distribution.csv", index=False)
sw.groupby(["Publisher", "Software_Name", "Software_Version"]).agg(Installation_Count=("Installation_ID", "count"), Asset_Count=("Asset_ID", "nunique")).reset_index().sort_values("Installation_Count", ascending=False).to_csv(REPORTS / "eda_software_installation_distribution.csv", index=False)
vuln["Severity"].value_counts().rename_axis("Severity").reset_index(name="Finding_Count").to_csv(REPORTS / "eda_vulnerability_severity_distribution.csv", index=False)
inc["Priority"].value_counts().rename_axis("Priority").reset_index(name="Incident_Count").to_csv(REPORTS / "eda_incident_priority_distribution.csv", index=False)

summary = pd.DataFrame([
    ["Total raw assets", len(hw)],
    ["Total software installations", len(sw)],
    ["Total vulnerability findings", len(vuln)],
    ["Total incidents", len(inc)],
    ["Unique business units", hw["Business_Unit_ID"].nunique()],
    ["Unique locations", hw["Location_ID"].nunique()],
], columns=["Metric", "Value"])
summary.to_csv(REPORTS / "technology_estate_summary.csv", index=False)
print("EDA reports exported")
