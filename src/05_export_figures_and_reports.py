
"""Export executive-ready EOL figures and report CSVs.

Run from project root:
    python src/05_export_figures_and_reports.py

Outputs:
    outputs/figures/*.png
    outputs/reports/*.csv
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "outputs" / "figures"
REP = ROOT / "outputs" / "reports"
FIG.mkdir(parents=True, exist_ok=True)
REP.mkdir(parents=True, exist_ok=True)

assets = pd.read_csv(ROOT / "data" / "processed" / "asset_risk_model.csv", parse_dates=["Expected_EOL"], low_memory=False)
soft = pd.read_csv(ROOT / "data" / "processed" / "software_installations_model.csv", parse_dates=["Software_EOL_Date"], low_memory=False)
refresh = pd.read_csv(ROOT / "data" / "raw" / "refresh_projects.csv", low_memory=False)
vulns = pd.read_csv(ROOT / "data" / "raw" / "vulnerabilities.csv", low_memory=False)

# Summary tables
lifecycle_summary = assets.groupby("Lifecycle_Status").agg(assets=("Asset_ID","count"), replacement_cost=("Replacement_Cost_CAD","sum"), critical_vulns=("Critical_Vuln_Count","sum"), incidents=("Incident_Count","sum"), downtime_hours=("Total_Downtime_Hours","sum")).reset_index()
lifecycle_summary.to_csv(REP / "executive_lifecycle_summary.csv", index=False)

bu_exposure = assets.groupby("Business_Unit").agg(total_assets=("Asset_ID","count"), past_eol=("Lifecycle_Status", lambda s: (s=="Past EOL").sum()), critical_vulns=("Critical_Vuln_Count","sum"), replacement_cost=("Replacement_Cost_CAD","sum"), downtime_hours=("Total_Downtime_Hours","sum")).reset_index()
bu_exposure["past_eol_rate_pct"] = bu_exposure["past_eol"] / bu_exposure["total_assets"] * 100
bu_exposure.sort_values("past_eol", ascending=False).to_csv(REP / "business_unit_eol_exposure.csv", index=False)

noncomp = soft[soft["Compliance_Status"].ne("Compliant")]
software_risk = noncomp.groupby(["Software_Name","Version","Category","Software_Lifecycle_Status"]).agg(non_compliant_installs=("Install_ID","count")).reset_index().sort_values("non_compliant_installs", ascending=False)
software_risk.to_csv(REP / "software_compliance_risk_summary.csv", index=False)

critical_overlap = assets[(assets["Lifecycle_Status"].eq("Past EOL")) & (assets["Critical_Vuln_Count"].fillna(0) > 0)]
critical_overlap.to_csv(REP / "past_eol_critical_vulnerability_assets.csv", index=False)

refresh_scope = assets[assets["Lifecycle_Status"].isin(["Past EOL","EOL within 12 months","EOL within 24 months"])].copy()
refresh_scope["EOL_Year"] = refresh_scope["Expected_EOL"].dt.year
budget_plan = refresh_scope.groupby(["EOL_Year","Asset_Type","Region"]).agg(assets=("Asset_ID","count"), estimated_replacement_cost=("Replacement_Cost_CAD","sum")).reset_index()
budget_plan.to_csv(REP / "refresh_budget_planning_summary.csv", index=False)

ops = assets.groupby("Lifecycle_Status").agg(assets=("Asset_ID","count"), incidents=("Incident_Count","sum"), downtime_hours=("Total_Downtime_Hours","sum")).reset_index()
ops["incident_rate_per_asset"] = ops["incidents"] / ops["assets"]
ops["downtime_per_asset"] = ops["downtime_hours"] / ops["assets"]
ops.to_csv(REP / "incident_downtime_by_lifecycle.csv", index=False)

# Helper
def save_bar(df, x, y, title, filename, horizontal=False, top=None):
    if top:
        df = df.head(top).copy()
    plt.figure(figsize=(11, 6))
    if horizontal:
        plt.barh(df[y].astype(str), df[x])
        plt.xlabel(x.replace('_',' ').title())
        plt.ylabel(y.replace('_',' ').title())
    else:
        plt.bar(df[x].astype(str), df[y])
        plt.xlabel(x.replace('_',' ').title())
        plt.ylabel(y.replace('_',' ').title())
        plt.xticks(rotation=35, ha='right')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(FIG / filename, dpi=180)
    plt.close()

# Figures
life = lifecycle_summary.sort_values("assets", ascending=False)
save_bar(life, "Lifecycle_Status", "assets", "Assets by Lifecycle Status", "fig_01_assets_by_lifecycle_status.png")

atype = assets[assets["Lifecycle_Status"].eq("Past EOL")].groupby("Asset_Type").size().reset_index(name="past_eol_assets").sort_values("past_eol_assets", ascending=True)
save_bar(atype, "past_eol_assets", "Asset_Type", "Past EOL Assets by Asset Type", "fig_02_past_eol_by_asset_type.png", horizontal=True)

bu = bu_exposure.sort_values("past_eol", ascending=True).tail(12)
save_bar(bu, "past_eol", "Business_Unit", "Top Business Units by Past EOL Assets", "fig_03_business_unit_eol_exposure.png", horizontal=True)

sw = software_risk.sort_values("non_compliant_installs", ascending=True).tail(15)
save_bar(sw, "non_compliant_installs", "Software_Name", "Top Software Compliance Risks", "fig_04_software_compliance_risk.png", horizontal=True)

co = critical_overlap.groupby("Asset_Type").size().reset_index(name="critical_overlap_assets").sort_values("critical_overlap_assets", ascending=True)
save_bar(co, "critical_overlap_assets", "Asset_Type", "Past EOL Assets with Critical Vulnerabilities", "fig_05_critical_vulnerability_overlap.png", horizontal=True)

yearly = refresh_scope.groupby("EOL_Year").agg(estimated_replacement_cost=("Replacement_Cost_CAD","sum")).reset_index()
save_bar(yearly, "EOL_Year", "estimated_replacement_cost", "Refresh Budget Need by EOL Year", "fig_06_refresh_budget_by_year.png")

ops_plot = ops.copy()
save_bar(ops_plot, "Lifecycle_Status", "downtime_per_asset", "Downtime per Asset by Lifecycle Status", "fig_07_downtime_by_lifecycle_status.png")

print(f"Exported reports to {REP}")
print(f"Exported figures to {FIG}")
