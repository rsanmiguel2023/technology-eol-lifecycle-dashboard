from pathlib import Path
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data'/'raw'; REF=ROOT/'data'/'reference'; PROCESSED=ROOT/'data'/'processed'; REPORTS=ROOT/'outputs'/'reports'; FIGURES=ROOT/'outputs'/'figures'; PBI=ROOT/'outputs'/'powerbi'
ANALYSIS_DATE=pd.Timestamp('2026-06-02')
for p in [PROCESSED,REPORTS,FIGURES,PBI]: p.mkdir(parents=True,exist_ok=True)

hw=pd.read_csv(RAW/'hardware_assets_raw.csv',parse_dates=['Purchase_Date','Install_Date','Warranty_End_Date'])
href=pd.read_csv(REF/'hardware_model_reference.csv',parse_dates=['Model_Release_Date','Vendor_Support_End_Date'])
vuln=pd.read_csv(RAW/'vulnerabilities_raw.csv')
inc=pd.read_csv(RAW/'incidents_raw.csv',parse_dates=['Opened_DateTime','Closed_DateTime'])
sw=pd.read_csv(RAW/'software_installations_raw.csv')
sref=pd.read_csv(REF/'software_lifecycle_reference.csv',parse_dates=['Vendor_Support_End_Date'])
asset=hw.merge(href,on=['Asset_Type','Manufacturer','Model'],how='left')
asset['Asset_Age_Years']=((ANALYSIS_DATE-asset['Install_Date']).dt.days/365.25).round(2)
asset['Warranty_Status']=np.where(asset['Warranty_End_Date']<ANALYSIS_DATE,'Warranty Expired','Under Warranty')
asset['Months_To_EOL']=((asset['Vendor_Support_End_Date']-ANALYSIS_DATE).dt.days/30.44).round(1)
asset['Lifecycle_Status']=np.select([asset['Vendor_Support_End_Date']<ANALYSIS_DATE,asset['Vendor_Support_End_Date']<=ANALYSIS_DATE+pd.DateOffset(months=12),asset['Vendor_Support_End_Date']<=ANALYSIS_DATE+pd.DateOffset(months=24)],['Past EOL','Expiring in 12 Months','Expiring in 24 Months'],default='Supported')
asset['Past_EOL_Flag']=(asset['Lifecycle_Status']=='Past EOL').astype(int); asset['Expiring_12M_Flag']=(asset['Lifecycle_Status']=='Expiring in 12 Months').astype(int)
asset['Replacement_Cost']=asset['Standard_Replacement_Cost'].fillna(asset['Purchase_Cost']*1.15)
vagg=vuln.groupby('Asset_ID').agg(Open_Vulnerability_Count=('Finding_ID','count'),Critical_Vulnerability_Count=('Severity',lambda x:int((x=='Critical').sum())),High_Vulnerability_Count=('Severity',lambda x:int((x=='High').sum()))).reset_index()
asset=asset.merge(vagg,on='Asset_ID',how='left')
for c in ['Open_Vulnerability_Count','Critical_Vulnerability_Count','High_Vulnerability_Count']: asset[c]=asset[c].fillna(0).astype(int)
inc['Downtime_Hours']=(inc['Closed_DateTime']-inc['Opened_DateTime']).dt.total_seconds()/3600
incagg=inc.groupby('Asset_ID').agg(Incident_Count=('Incident_ID','count'),Downtime_Hours=('Downtime_Hours','sum')).reset_index()
asset=asset.merge(incagg,on='Asset_ID',how='left'); asset['Incident_Count']=asset['Incident_Count'].fillna(0).astype(int); asset['Downtime_Hours']=asset['Downtime_Hours'].fillna(0).round(2)
asset['Lifecycle_Risk_Score']=(asset['Past_EOL_Flag']*40+asset['Expiring_12M_Flag']*20+np.minimum(asset['Critical_Vulnerability_Count'],5)*8+np.minimum(asset['Incident_Count'],10)*2).clip(0,100)
asset['Refresh_Priority']=pd.cut(asset['Lifecycle_Risk_Score'],[-1,30,55,75,100],labels=['Low','Medium','High','Critical'])
asset.to_csv(PROCESSED/'asset_lifecycle_analysis.csv',index=False)
sw_eng=sw.merge(sref,left_on=['Publisher','Software_Name','Software_Version'],right_on=['Publisher','Software_Name','Version'],how='left')
sw_eng['Software_EOL_Status']=np.select([sw_eng['Vendor_Support_End_Date']<ANALYSIS_DATE,sw_eng['Vendor_Support_End_Date']<=ANALYSIS_DATE+pd.DateOffset(months=12)],['Unsupported','Support Ending in 12 Months'],default='Supported')
sw_eng['Software_Compliance_Risk']=np.select([sw_eng['Software_EOL_Status']=='Unsupported',sw_eng['Software_EOL_Status']=='Support Ending in 12 Months'],['High','Medium'],default='Low')
sw_eng.to_csv(PROCESSED/'software_lifecycle_analysis.csv',index=False)
print('Feature engineering completed')
