
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ENGINEERED = ROOT / "data" / "engineered"
REPORTS = ROOT / "outputs" / "reports"
DOCS = ROOT / "docs"
REPORTS.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

asset = pd.read_csv(ENGINEERED / "asset_lifecycle_analysis.csv")
cyber = pd.read_csv(REPORTS / "past_eol_critical_vulnerability_assets.csv")
refresh = pd.read_csv(REPORTS / "refresh_budget_planning_summary.csv")
op = pd.read_csv(REPORTS / "operational_impact_by_lifecycle_status.csv")
sw = pd.read_csv(ENGINEERED / "software_lifecycle_analysis.csv")
bu = pd.read_csv(REPORTS / "business_unit_eol_exposure.csv")

total_assets = len(asset)
past_eol = int((asset["Lifecycle_Status"] == "Past EOL").sum())
exp12 = int((asset["Lifecycle_Status"] == "Expiring in 12 Months").sum())
exp24 = int((asset["Lifecycle_Status"] == "Expiring in 24 Months").sum())
exp36 = int((asset["Lifecycle_Status"] == "Expiring in 36 Months").sum())
cyber_count = len(cyber)
refresh_cost = float(refresh["Estimated_Refresh_Cost"].sum())
past_downtime = float(asset.loc[asset["Lifecycle_Status"] == "Past EOL", "Downtime_Hours"].sum())
unsupported_sw = int((sw["Software_EOL_Status"] == "Unsupported").sum())
highest_risk_bu = bu.sort_values("Executive_Risk_Index", ascending=False).iloc[0]["Business_Unit_Name"]

exec_q = pd.DataFrame([
    ["Total managed technology assets", total_assets],
    ["Assets already past vendor support", past_eol],
    ["Assets expiring within 12 months", exp12],
    ["Assets expiring within 24 months", exp12 + exp24],
    ["Assets expiring within 36 months", exp12 + exp24 + exp36],
    ["Unsupported assets with critical/high vulnerabilities", cyber_count],
    ["Unsupported software installations", unsupported_sw],
    ["Estimated refresh cost for past/near-EOL assets", round(refresh_cost, 2)],
    ["Downtime hours linked to past-EOL assets", round(past_downtime, 2)],
    ["Highest lifecycle risk business unit", highest_risk_bu],
], columns=["Executive_Question", "Executive_Answer"])
exec_q.to_csv(REPORTS / "executive_questions_summary.csv", index=False)

recs = pd.DataFrame([
    ["Immediate", "Remediate unsupported assets with critical and high vulnerabilities", "Cybersecurity", "0-6 Months", "Prioritize assets outside vendor support with open high-severity findings."],
    ["Immediate", "Prioritize highest-risk business units", "Technology Governance", "0-12 Months", "Sequence action using business unit risk heatmap and operational criticality."],
    ["Near Term", "Fund lifecycle refresh roadmap", "Infrastructure", "FY2026-FY2028", "Align funding to forecasted replacement demand for past and near-EOL assets."],
    ["Near Term", "Reduce unsupported software footprint", "Enterprise Architecture", "0-12 Months", "Target unsupported operating systems, productivity tools, databases, runtimes, and development tooling."],
    ["Strategic", "Implement lifecycle governance controls", "Technology Risk", "Ongoing", "Maintain annual lifecycle forecasting, exception governance, and executive risk reporting."],
], columns=["Priority", "Recommended_Action", "Owner", "Timeframe", "Rationale"])
recs.to_csv(REPORTS / "recommendation_actions.csv", index=False)

(DOCS / "executive_summary.md").write_text(f"""# Executive Summary\n\nMaple Financial Bank maintains {total_assets:,} managed technology assets across end-user computing, infrastructure, network, cloud, and enterprise application environments.\n\nThe lifecycle analysis identifies {past_eol:,} assets already past vendor support, {exp12:,} assets expiring within the next 12 months, and {exp12 + exp24:,} assets requiring refresh planning within 24 months. These assets represent near-term operational, cybersecurity, and compliance exposure.\n\nCybersecurity analysis identifies {cyber_count:,} unsupported assets with critical or high vulnerability exposure. These should be prioritized for remediation or accelerated refresh.\n\nRefresh planning estimates ${refresh_cost:,.0f} in required investment across past and near-EOL assets. Past-EOL assets are linked to {past_downtime:,.0f} hours of downtime, demonstrating measurable operational impact.\n\nThe highest lifecycle risk business unit is **{highest_risk_bu}** based on the combination of EOL exposure, vulnerabilities, downtime, and replacement cost.\n""", encoding="utf-8")

print("Executive reports and documentation updated")
