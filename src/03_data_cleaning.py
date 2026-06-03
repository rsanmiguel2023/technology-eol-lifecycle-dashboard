
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "outputs" / "reports"
PROCESSED.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

date_columns = {
    "hardware_assets_raw.csv": ["Purchase_Date", "Install_Date", "Warranty_End_Date", "Last_Discovered_Date"],
    "software_installations_raw.csv": ["Install_Date", "Last_Seen_Date"],
    "vulnerabilities_raw.csv": ["First_Detected_Date", "Last_Detected_Date"],
    "incidents_raw.csv": ["Opened_DateTime", "Closed_DateTime"],
    "refresh_projects_raw.csv": ["Planned_Refresh_Date", "Actual_Refresh_Date"],
    "cloud_resources_raw.csv": ["Creation_Date"],
    "budget_allocations_raw.csv": []
}

log = []
for file_name, dates in date_columns.items():
    path = RAW / file_name
    df = pd.read_csv(path)
    before = len(df)
    df = df.drop_duplicates()
    for col in dates:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    out_name = file_name.replace("_raw", "")
    df.to_csv(PROCESSED / out_name, index=False)
    log.append({"source_file": file_name, "processed_file": out_name, "rows_before": before, "rows_after": len(df), "duplicates_removed": before-len(df), "missing_values_after": int(df.isna().sum().sum())})

pd.DataFrame(log).to_csv(REPORTS / "data_cleaning_summary.csv", index=False)
print("Processed clean source tables exported to data/processed")
