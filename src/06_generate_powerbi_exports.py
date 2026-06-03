from pathlib import Path
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data'/'raw'; REF=ROOT/'data'/'reference'; PROCESSED=ROOT/'data'/'processed'; REPORTS=ROOT/'outputs'/'reports'; FIGURES=ROOT/'outputs'/'figures'; PBI=ROOT/'outputs'/'powerbi'
ANALYSIS_DATE=pd.Timestamp('2026-06-02')
for p in [PROCESSED,REPORTS,FIGURES,PBI]: p.mkdir(parents=True,exist_ok=True)

for src in list(PROCESSED.glob('*.csv'))+list(REPORTS.glob('*.csv')):
 pd.read_csv(src).to_csv(PBI/src.name,index=False)
print('Power BI exports generated')
