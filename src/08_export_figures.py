
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "outputs" / "reports"
FIGURES = ROOT / "outputs" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

def save_bar(csv_name, x_col, y_col, title, file_name, top_n=10):
    path = REPORTS / csv_name
    if not path.exists(): return
    df = pd.read_csv(path).sort_values(y_col, ascending=False).head(top_n)
    plt.figure(figsize=(10, 6))
    plt.barh(df[x_col].astype(str), df[y_col])
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.xlabel(y_col.replace('_', ' '))
    plt.tight_layout()
    plt.savefig(FIGURES / file_name, dpi=160)
    plt.close()

save_bar('business_unit_eol_exposure.csv', 'Business_Unit_Name', 'Past_EOL_Assets', 'Past EOL Assets by Business Unit', 'business_unit_eol_exposure.png')
save_bar('refresh_budget_planning_summary.csv', 'Refresh_Year', 'Estimated_Refresh_Cost', 'Refresh Investment Roadmap', 'refresh_budget_planning_summary.png', 5)
save_bar('operational_impact_by_lifecycle_status.csv', 'Lifecycle_Status', 'Downtime_Hours', 'Downtime by Lifecycle Status', 'operational_impact_by_lifecycle_status.png', 10)
print('Figures exported')
