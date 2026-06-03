
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
PBI = ROOT / "outputs" / "powerbi"
PBI.mkdir(parents=True, exist_ok=True)
for folder in [ROOT / "outputs" / "reports", ROOT / "data" / "engineered"]:
    for path in folder.glob("*.csv"):
        shutil.copy2(path, PBI / path.name)
print("Power BI datasets exported to outputs/powerbi")
