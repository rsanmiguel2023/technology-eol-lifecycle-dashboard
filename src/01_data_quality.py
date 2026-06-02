import pandas as pd
from utils import RAW, REPORTS, read_csv

files = [
    'hardware_assets.csv', 'software_catalog.csv', 'software_installations.csv',
    'technology_lifecycle_catalog.csv', 'cloud_resources.csv', 'application_portfolio.csv',
    'vulnerabilities.csv', 'incidents.csv', 'refresh_projects.csv', 'budget_costs.csv', 'locations.csv'
]

summary = []
for f in files:
    df = read_csv(f)
    summary.append({
        'table': f,
        'rows': len(df),
        'columns': df.shape[1],
        'duplicate_rows': int(df.duplicated().sum()),
        'missing_cells': int(df.isna().sum().sum()),
        'missing_pct': round(float(df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2)
    })

quality = pd.DataFrame(summary).sort_values('rows', ascending=False)
quality.to_csv(REPORTS / 'data_quality_summary.csv', index=False)
print(quality.to_string(index=False))
