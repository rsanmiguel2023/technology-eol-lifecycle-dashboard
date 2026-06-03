from pathlib import Path
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data'/'raw'; REF=ROOT/'data'/'reference'; PROCESSED=ROOT/'data'/'processed'; REPORTS=ROOT/'outputs'/'reports'; FIGURES=ROOT/'outputs'/'figures'; PBI=ROOT/'outputs'/'powerbi'
ANALYSIS_DATE=pd.Timestamp('2026-06-02')
for p in [PROCESSED,REPORTS,FIGURES,PBI]: p.mkdir(parents=True,exist_ok=True)

import matplotlib.pyplot as plt
items=[('business_unit_eol_exposure','Past_EOL_Assets','Business_Unit_Name','Top Business Units by Past-EOL Assets'),('refresh_budget_planning_summary','Estimated_Refresh_Cost','Refresh_Year','Refresh Investment Roadmap'),('operational_impact_by_lifecycle_status','Downtime_Hours','Lifecycle_Status','Downtime by Lifecycle Status')]
for name,y,x,title in items:
 df=pd.read_csv(REPORTS/f'{name}.csv')
 plt.figure(figsize=(10,5)); plt.barh(df[x].astype(str),df[y]); plt.title(title); plt.tight_layout(); plt.savefig(FIGURES/f'{name}.png',dpi=160); plt.close()
print('Figures exported')
