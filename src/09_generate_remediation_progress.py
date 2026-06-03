"""
Generate remediation progress tracking data for the Technology Lifecycle Governance dashboard.

Purpose
-------
This is a quick executive-governance layer built from the engineered lifecycle dataset.
It does not modify raw source extracts. It creates a realistic remediation tracker for
assets that are already past vendor support, approaching EOL, or carrying elevated risk.

Outputs
-------
- data/raw/remediation_tracker_raw.csv
- data/engineered/remediation_progress.csv
- outputs/reports/remediation_progress_summary.csv
- outputs/reports/remediation_progress_by_business_unit.csv
- outputs/reports/remediation_progress_by_status.csv
- outputs/powerbi/remediation_progress*.csv
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
ENGINEERED = ROOT / "data" / "engineered"
REPORTS = ROOT / "outputs" / "reports"
POWERBI = ROOT / "outputs" / "powerbi"
REFERENCE = ROOT / "data" / "reference"

for p in [RAW, ENGINEERED, REPORTS, POWERBI]:
    p.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)
AS_OF_DATE = pd.Timestamp("2026-05-31")


def read_first(paths: list[Path]) -> pd.DataFrame:
    for path in paths:
        if path.exists():
            return pd.read_csv(path)
    raise FileNotFoundError("Could not find any of: " + ", ".join(str(p) for p in paths))


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    return df


def load_business_units() -> pd.DataFrame:
    candidates = [
        REFERENCE / "business_units.csv",
        REPORTS / "business_unit_eol_exposure.csv",
        ENGINEERED / "business_unit_risk.csv",
        POWERBI / "business_unit_risk.csv",
    ]
    for path in candidates:
        if path.exists():
            df = normalize_columns(pd.read_csv(path))
            if {"Business_Unit_ID", "Business_Unit_Name"}.issubset(df.columns):
                return df[["Business_Unit_ID", "Business_Unit_Name"]].drop_duplicates()
    return pd.DataFrame(columns=["Business_Unit_ID", "Business_Unit_Name"])


def priority_from_asset(row: pd.Series) -> str:
    crit = float(row.get("Critical_Vulnerability_Count", 0) or 0)
    high = float(row.get("High_Vulnerability_Count", 0) or 0)
    risk = float(row.get("Lifecycle_Risk_Score", 0) or 0)
    past = int(row.get("Past_EOL_Flag", 0) or 0)
    exp12 = int(row.get("Expiring_12M_Flag", 0) or 0)

    if past == 1 and crit > 0:
        return "P1 - Critical"
    if past == 1 or (crit > 0 and risk >= 35):
        return "P2 - High"
    if exp12 == 1 or high > 0 or risk >= 25:
        return "P3 - Medium"
    return "P4 - Planned"


def remediation_type(asset_type: str) -> str:
    s = str(asset_type).lower()
    if "server" in s:
        return "Server Refresh / OS Upgrade"
    if "firewall" in s or "router" in s or "switch" in s or "wireless" in s:
        return "Network Hardware Refresh"
    if "storage" in s:
        return "Storage Platform Refresh"
    if "vdi" in s:
        return "VDI Image / Platform Refresh"
    return "Endpoint Refresh"


def assigned_team(asset_type: str) -> str:
    s = str(asset_type).lower()
    if "server" in s or "storage" in s or "vdi" in s:
        return "Infrastructure Services"
    if "firewall" in s or "router" in s or "switch" in s or "wireless" in s:
        return "Network Services"
    return "End User Computing"


def choose_status(priority: str) -> str:
    # Active governance program: not yet mature, but work is underway.
    # Higher priority items are more likely to be in progress, not silently deferred.
    if priority == "P1 - Critical":
        statuses = ["Completed", "In Progress", "Not Started", "Exception Approved"]
        probs = [0.24, 0.54, 0.18, 0.04]
    elif priority == "P2 - High":
        statuses = ["Completed", "In Progress", "Not Started", "Exception Approved"]
        probs = [0.30, 0.47, 0.18, 0.05]
    elif priority == "P3 - Medium":
        statuses = ["Completed", "In Progress", "Not Started", "Deferred"]
        probs = [0.34, 0.42, 0.19, 0.05]
    else:
        statuses = ["Completed", "In Progress", "Not Started", "Deferred"]
        probs = [0.38, 0.35, 0.22, 0.05]
    return rng.choice(statuses, p=probs)


def target_date_for(priority: str) -> pd.Timestamp:
    if priority == "P1 - Critical":
        return AS_OF_DATE + pd.to_timedelta(int(rng.integers(15, 91)), unit="D")
    if priority == "P2 - High":
        return AS_OF_DATE + pd.to_timedelta(int(rng.integers(60, 181)), unit="D")
    if priority == "P3 - Medium":
        return AS_OF_DATE + pd.to_timedelta(int(rng.integers(120, 366)), unit="D")
    return AS_OF_DATE + pd.to_timedelta(int(rng.integers(180, 540)), unit="D")


def actual_date_for(status: str, target: pd.Timestamp) -> str:
    if status != "Completed":
        return ""
    offset = int(rng.integers(-60, 31))
    return (target + pd.to_timedelta(offset, unit="D")).strftime("%Y-%m-%d")


def main() -> None:
    assets = read_first([
        ENGINEERED / "asset_lifecycle_analysis.csv",
        POWERBI / "asset_lifecycle_analysis.csv",
        REPORTS / "asset_lifecycle_analysis.csv",
    ])
    assets = normalize_columns(assets)

    required = {"Asset_ID", "Asset_Type", "Business_Unit_ID", "Lifecycle_Status"}
    missing = required - set(assets.columns)
    if missing:
        raise ValueError(f"asset_lifecycle_analysis.csv is missing required columns: {sorted(missing)}")

    # Eligible remediation population: unsupported, near-EOL, or elevated-risk assets.
    for col in ["Past_EOL_Flag", "Expiring_12M_Flag", "Expiring_24M_Flag", "Expiring_36M_Flag"]:
        if col not in assets.columns:
            assets[col] = 0
    if "Lifecycle_Risk_Score" not in assets.columns:
        assets["Lifecycle_Risk_Score"] = 0
    if "Replacement_Cost" not in assets.columns:
        assets["Replacement_Cost"] = assets.get("Purchase_Cost", 0)

    eligible = assets[
        (assets["Past_EOL_Flag"].fillna(0).astype(int) == 1)
        | (assets["Expiring_12M_Flag"].fillna(0).astype(int) == 1)
        | (assets["Expiring_24M_Flag"].fillna(0).astype(int) == 1)
        | (assets["Expiring_36M_Flag"].fillna(0).astype(int) == 1)
        | (pd.to_numeric(assets["Lifecycle_Risk_Score"], errors="coerce").fillna(0) >= 30)
    ].copy()

    if eligible.empty:
        raise ValueError("No remediation-eligible assets were found. Run feature engineering first.")

    bu = load_business_units()
    if not bu.empty:
        eligible = eligible.merge(bu, on="Business_Unit_ID", how="left")
    if "Business_Unit_Name" not in eligible.columns:
        eligible["Business_Unit_Name"] = eligible["Business_Unit_ID"]
    eligible["Business_Unit_Name"] = eligible["Business_Unit_Name"].fillna(eligible["Business_Unit_ID"])

    rows = []
    for idx, row in eligible.reset_index(drop=True).iterrows():
        priority = priority_from_asset(row)
        status = choose_status(priority)
        target = target_date_for(priority)
        actual = actual_date_for(status, target)
        cost_base = float(row.get("Replacement_Cost", 0) or 0)
        remediation_cost = round(cost_base * float(rng.uniform(0.90, 1.18)), 2)
        rid = f"REM-{idx+1:06d}"
        rows.append({
            "Remediation_ID": rid,
            "Asset_ID": row["Asset_ID"],
            "Business_Unit_ID": row.get("Business_Unit_ID", ""),
            "Business_Unit_Name": row.get("Business_Unit_Name", ""),
            "Asset_Type": row.get("Asset_Type", ""),
            "Lifecycle_Status": row.get("Lifecycle_Status", ""),
            "Lifecycle_Risk_Score": round(float(row.get("Lifecycle_Risk_Score", 0) or 0), 2),
            "Remediation_Type": remediation_type(row.get("Asset_Type", "")),
            "Priority": priority,
            "Assigned_Team": assigned_team(row.get("Asset_Type", "")),
            "Target_Completion_Date": target.strftime("%Y-%m-%d"),
            "Actual_Completion_Date": actual,
            "Remediation_Status": status,
            "Remediation_Cost": remediation_cost,
            "Risk_Reduction_Category": "Lifecycle + Cyber" if (float(row.get("Critical_Vulnerability_Count", 0) or 0) + float(row.get("High_Vulnerability_Count", 0) or 0)) > 0 else "Lifecycle",
        })

    remediation = pd.DataFrame(rows)
    remediation["Target_Completion_Date"] = pd.to_datetime(remediation["Target_Completion_Date"])
    remediation["Actual_Completion_Date"] = pd.to_datetime(remediation["Actual_Completion_Date"], errors="coerce")
    remediation["Days_To_Target"] = (remediation["Target_Completion_Date"] - AS_OF_DATE).dt.days
    remediation["Completed_Flag"] = (remediation["Remediation_Status"] == "Completed").astype(int)
    remediation["Overdue_Flag"] = ((remediation["Remediation_Status"] != "Completed") & (remediation["Target_Completion_Date"] < AS_OF_DATE)).astype(int)
    remediation["Remediation_Progress_Group"] = remediation["Remediation_Status"].replace({"Deferred": "Deferred / Exception", "Exception Approved": "Deferred / Exception"})

    raw_cols = ["Remediation_ID", "Asset_ID", "Business_Unit_ID", "Remediation_Type", "Priority", "Assigned_Team", "Target_Completion_Date", "Actual_Completion_Date", "Remediation_Status", "Remediation_Cost", "Risk_Reduction_Category"]
    remediation[raw_cols].to_csv(RAW / "remediation_tracker_raw.csv", index=False)

    remediation.to_csv(ENGINEERED / "remediation_progress.csv", index=False)

    status_summary = remediation.groupby("Remediation_Progress_Group", as_index=False).agg(
        Asset_Count=("Asset_ID", "count"),
        Remediation_Cost=("Remediation_Cost", "sum"),
    )
    total = status_summary["Asset_Count"].sum()
    status_summary["Progress_Pct"] = (status_summary["Asset_Count"] / total * 100).round(1)
    order = ["Completed", "In Progress", "Not Started", "Deferred / Exception"]
    status_summary["Sort_Order"] = status_summary["Remediation_Progress_Group"].map({v: i for i, v in enumerate(order)}).fillna(99)
    status_summary = status_summary.sort_values("Sort_Order").drop(columns="Sort_Order")

    summary = pd.DataFrame([
        {"Metric": "Remediation Eligible Assets", "Value": int(len(remediation)), "Display_Value": f"{len(remediation):,}"},
        {"Metric": "Completed Assets", "Value": int((remediation["Remediation_Progress_Group"] == "Completed").sum()), "Display_Value": f"{(remediation['Remediation_Progress_Group'] == 'Completed').sum():,}"},
        {"Metric": "Completed Percent", "Value": float(round((remediation["Remediation_Progress_Group"] == "Completed").mean() * 100, 1)), "Display_Value": f"{round((remediation['Remediation_Progress_Group'] == 'Completed').mean() * 100, 1)}%"},
        {"Metric": "In Progress Percent", "Value": float(round((remediation["Remediation_Progress_Group"] == "In Progress").mean() * 100, 1)), "Display_Value": f"{round((remediation['Remediation_Progress_Group'] == 'In Progress').mean() * 100, 1)}%"},
        {"Metric": "Not Started Percent", "Value": float(round((remediation["Remediation_Progress_Group"] == "Not Started").mean() * 100, 1)), "Display_Value": f"{round((remediation['Remediation_Progress_Group'] == 'Not Started').mean() * 100, 1)}%"},
        {"Metric": "Deferred or Exception Percent", "Value": float(round((remediation["Remediation_Progress_Group"] == "Deferred / Exception").mean() * 100, 1)), "Display_Value": f"{round((remediation['Remediation_Progress_Group'] == 'Deferred / Exception').mean() * 100, 1)}%"},
        {"Metric": "Total Remediation Cost", "Value": float(remediation["Remediation_Cost"].sum()), "Display_Value": f"${remediation['Remediation_Cost'].sum()/1_000_000:.1f}M"},
    ])

    by_bu = remediation.groupby(["Business_Unit_ID", "Business_Unit_Name", "Remediation_Progress_Group"], as_index=False).agg(
        Asset_Count=("Asset_ID", "count"),
        Remediation_Cost=("Remediation_Cost", "sum"),
    )

    status_summary.to_csv(REPORTS / "remediation_progress_by_status.csv", index=False)
    summary.to_csv(REPORTS / "remediation_progress_summary.csv", index=False)
    by_bu.to_csv(REPORTS / "remediation_progress_by_business_unit.csv", index=False)

    for name, df in [
        ("remediation_progress.csv", remediation),
        ("remediation_progress_summary.csv", summary),
        ("remediation_progress_by_status.csv", status_summary),
        ("remediation_progress_by_business_unit.csv", by_bu),
    ]:
        df.to_csv(POWERBI / name, index=False)

    print("Generated remediation progress datasets")
    print(status_summary.to_string(index=False))
    print(f"Total remediation eligible assets: {len(remediation):,}")


if __name__ == "__main__":
    main()
