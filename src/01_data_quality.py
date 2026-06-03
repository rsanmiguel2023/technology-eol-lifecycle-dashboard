
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIRS = [ROOT / "data" / "raw", ROOT / "data" / "reference", ROOT / "data" / "processed", ROOT / "data" / "engineered"]
REPORTS = ROOT / "outputs" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

rows = []
for folder in DATA_DIRS:
    if not folder.exists():
        continue
    for path in sorted(folder.glob("*.csv")):
        try:
            df = pd.read_csv(path)
            rows.append({
                "data_layer": folder.name,
                "table_name": path.name,
                "row_count": len(df),
                "column_count": len(df.columns),
                "duplicate_rows": int(df.duplicated().sum()),
                "missing_values": int(df.isna().sum().sum()),
                "columns": ", ".join(df.columns)
            })
        except Exception as exc:
            rows.append({"data_layer": folder.name, "table_name": path.name, "error": str(exc)})

out = pd.DataFrame(rows)
out.to_csv(REPORTS / "data_quality_summary.csv", index=False)
print(out[["data_layer", "table_name", "row_count", "column_count", "duplicate_rows", "missing_values"]].to_string(index=False))
