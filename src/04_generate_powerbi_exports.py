import pandas as pd
from utils import PROCESSED, RAW, OUTPUTS

assets = pd.read_csv(PROCESSED / 'asset_risk_model.csv', low_memory=False)
software = pd.read_csv(PROCESSED / 'software_installations_model.csv', low_memory=False)
cloud = pd.read_csv(PROCESSED / 'cloud_resources_model.csv', low_memory=False)
budget = pd.read_csv(RAW / 'budget_costs.csv')
refresh = pd.read_csv(RAW / 'refresh_projects.csv')

exports = OUTPUTS / 'powerbi_exports'
exports.mkdir(parents=True, exist_ok=True)

# Executive summaries for faster Power BI visuals
assets.groupby(['Lifecycle_Status','Asset_Type']).agg(
    Asset_Count=('Asset_ID','count'),
    Replacement_Cost=('Replacement_Cost_CAD','sum'),
    Avg_Risk_Score=('Risk_Score','mean')
).reset_index().to_csv(exports / 'pbi_asset_eol_summary.csv', index=False)

assets.groupby(['Region','Lifecycle_Status']).agg(
    Asset_Count=('Asset_ID','count'),
    Critical_Assets=('Criticality', lambda x: (x == 'Critical').sum()),
    Replacement_Cost=('Replacement_Cost_CAD','sum')
).reset_index().to_csv(exports / 'pbi_regional_eol_summary.csv', index=False)

software.groupby(['Software_Name','Version','Software_Lifecycle_Status']).agg(
    Installation_Count=('Install_ID','count'),
    Distinct_Assets=('Asset_ID','nunique')
).reset_index().sort_values('Installation_Count', ascending=False).to_csv(exports / 'pbi_software_eol_summary.csv', index=False)

cloud.groupby(['Cloud_Provider','Service_Name','Cloud_Lifecycle_Status']).agg(
    Resource_Count=('Cloud_Resource_ID','count'),
    Monthly_Cost=('Monthly_Run_Cost_CAD','sum')
).reset_index().to_csv(exports / 'pbi_cloud_eol_summary.csv', index=False)

budget.to_csv(exports / 'pbi_budget_costs.csv', index=False)
refresh.to_csv(exports / 'pbi_refresh_projects.csv', index=False)
print(f'Power BI export files created at {exports}')
