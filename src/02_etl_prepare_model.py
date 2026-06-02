import pandas as pd
from utils import read_csv, save_csv, lifecycle_status, criticality_score, eol_score, severity_score, AS_OF_DATE, safe_date

assets = read_csv('hardware_assets.csv')
locations = read_csv('locations.csv')
software = read_csv('software_installations.csv')
vulns = read_csv('vulnerabilities.csv')
incidents = read_csv('incidents.csv')
refresh = read_csv('refresh_projects.csv')
cloud = read_csv('cloud_resources.csv')

# Date standardization
for col in ['Purchase_Date', 'Install_Date', 'Warranty_End', 'Expected_EOL']:
    if col in assets.columns:
        assets[col] = safe_date(assets[col])

assets['Lifecycle_Status'] = assets['Expected_EOL'].apply(lifecycle_status)
assets['Days_To_EOL'] = (assets['Expected_EOL'] - AS_OF_DATE).dt.days
assets['Age_Years'] = ((AS_OF_DATE - assets['Purchase_Date']).dt.days / 365.25).round(1)
assets['Criticality_Score'] = assets['Criticality'].apply(criticality_score)
assets['EOL_Score'] = assets['Lifecycle_Status'].apply(eol_score)

# Vulnerability aggregation
vulns['Severity_Score'] = vulns['Severity'].apply(severity_score)
vuln_agg = vulns.groupby('Asset_ID').agg(
    Vulnerability_Count=('Vulnerability_Record_ID', 'count'),
    Critical_Vuln_Count=('Severity', lambda x: (x == 'Critical').sum()),
    High_Vuln_Count=('Severity', lambda x: (x == 'High').sum()),
    Avg_CVSS=('CVSS_Score', 'mean'),
    Max_CVSS=('CVSS_Score', 'max')
).reset_index()

# Incident aggregation
incidents['Incident_Date'] = safe_date(incidents['Incident_Date'])
incident_agg = incidents.groupby('Asset_ID').agg(
    Incident_Count=('Incident_ID', 'count'),
    Total_Downtime_Hours=('Downtime_Hours', 'sum'),
    Avg_Downtime_Hours=('Downtime_Hours', 'mean')
).reset_index()

# Refresh aggregation
refresh_agg = refresh.groupby('Asset_ID').agg(
    Refresh_Project_Count=('Project_ID', 'count'),
    Latest_Refresh_Status=('Project_Status', 'last'),
    Planned_Refresh_Budget=('Budget_Estimate_CAD', 'sum')
).reset_index()

asset_risk = assets.merge(vuln_agg, on='Asset_ID', how='left')
asset_risk = asset_risk.merge(incident_agg, on='Asset_ID', how='left')
asset_risk = asset_risk.merge(refresh_agg, on='Asset_ID', how='left')
asset_risk = asset_risk.merge(locations, on='Location_ID', how='left')

fill_zero = ['Vulnerability_Count','Critical_Vuln_Count','High_Vuln_Count','Incident_Count','Total_Downtime_Hours','Avg_Downtime_Hours','Refresh_Project_Count','Planned_Refresh_Budget']
for c in fill_zero:
    if c in asset_risk.columns:
        asset_risk[c] = asset_risk[c].fillna(0)

asset_risk['Risk_Score'] = (
    asset_risk['EOL_Score'] * 20 +
    asset_risk['Criticality_Score'] * 15 +
    asset_risk['Critical_Vuln_Count'].clip(0, 10) * 4 +
    asset_risk['High_Vuln_Count'].clip(0, 10) * 2 +
    asset_risk['Incident_Count'].clip(0, 10) * 1.5
).round(1)
asset_risk['Risk_Band'] = pd.cut(asset_risk['Risk_Score'], bins=[-1, 50, 80, 110, 999], labels=['Low','Medium','High','Critical'])

# Software lifecycle model
software['Software_EOL_Date'] = safe_date(software['Software_EOL_Date'])
software['Software_Lifecycle_Status'] = software['Software_EOL_Date'].apply(lifecycle_status)
software['Days_To_Software_EOL'] = (software['Software_EOL_Date'] - AS_OF_DATE).dt.days

# Cloud lifecycle model
cloud['Support_End_Date'] = safe_date(cloud['Support_End_Date'])
cloud['Cloud_Lifecycle_Status'] = cloud['Support_End_Date'].apply(lifecycle_status)
cloud['Days_To_EOL'] = (cloud['Support_End_Date'] - AS_OF_DATE).dt.days

save_csv(asset_risk, 'asset_risk_model.csv')
save_csv(software, 'software_installations_model.csv')
save_csv(cloud, 'cloud_resources_model.csv')
print('Created processed model files in data/processed/')
