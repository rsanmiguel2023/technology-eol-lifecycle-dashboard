from pathlib import Path
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data'/'raw'; REF=ROOT/'data'/'reference'; PROCESSED=ROOT/'data'/'processed'; REPORTS=ROOT/'outputs'/'reports'; FIGURES=ROOT/'outputs'/'figures'; PBI=ROOT/'outputs'/'powerbi'
ANALYSIS_DATE=pd.Timestamp('2026-06-02')
for p in [PROCESSED,REPORTS,FIGURES,PBI]: p.mkdir(parents=True,exist_ok=True)

hw=pd.read_csv(RAW/'hardware_assets_raw.csv')
sw=pd.read_csv(RAW/'software_installations_raw.csv')
v=pd.read_csv(RAW/'vulnerabilities_raw.csv')
inc=pd.read_csv(RAW/'incidents_raw.csv')
hw.groupby('Asset_Type').agg(asset_count=('Asset_ID','count'),avg_purchase_cost=('Purchase_Cost','mean')).reset_index().to_csv(REPORTS/'eda_asset_type_distribution.csv',index=False)
hw.groupby('Business_Unit_ID').agg(asset_count=('Asset_ID','count'),avg_purchase_cost=('Purchase_Cost','mean')).reset_index().to_csv(REPORTS/'eda_business_unit_asset_distribution.csv',index=False)
sw.groupby(['Software_Name','Software_Version']).agg(installation_count=('Installation_ID','count'),asset_count=('Asset_ID','nunique')).reset_index().sort_values('installation_count',ascending=False).to_csv(REPORTS/'eda_software_installation_distribution.csv',index=False)
v.groupby('Severity').agg(finding_count=('Finding_ID','count'),unique_assets=('Asset_ID','nunique')).reset_index().to_csv(REPORTS/'eda_vulnerability_severity_distribution.csv',index=False)
inc.groupby('Priority').agg(incident_count=('Incident_ID','count')).reset_index().to_csv(REPORTS/'eda_incident_priority_distribution.csv',index=False)
print('EDA reports exported')
