# Senior Analyst Technology EOL Dashboard Project Guide

## 1. Project Background
This project simulates a large Canadian bank managing hardware, software, cloud, developer tooling, vulnerabilities, incidents, and refresh programs. The purpose is to build an executive-ready Technology End-of-Life dashboard that supports lifecycle governance, cybersecurity prioritization, compliance reporting, and budget planning.

## 2. Business Problem
Banks operate thousands of endpoints, network devices, servers, applications, cloud services, and development tools. When technologies pass vendor support dates, the organization faces higher security exposure, operational instability, audit findings, and unplanned refresh costs. The Senior Analyst role is expected to consolidate fragmented inventory data, clean lifecycle information, quantify EOL exposure, and convert the results into actionable dashboards.

## 3. Research Questions
RQ1. Which hardware and software assets are already past EOL or will reach EOL within the next 12 and 24 months?
RQ2. Which regions, business units, and asset classes have the highest EOL exposure?
RQ3. Are EOL assets associated with higher vulnerability burden and incident frequency?
RQ4. What refresh budget is required by year, category, and priority level?
RQ5. Which development tools and runtimes create the highest technology-risk concentration?

## 4. Dataset Overview
Use the CSV files as a star-schema style model. hardware_assets.csv is the main physical asset inventory. software_installations.csv links installed software to assets. software_catalog.csv contains real software products, versions, vendors, support dates, and lifecycle status. vulnerabilities.csv and incidents.csv link operational risk to assets. refresh_projects.csv provides planned remediation work. budget_costs.csv supports financial forecasting. cloud_resources.csv and application_portfolio.csv extend the dashboard into cloud and application governance.

## 5. Data Cleaning Plan
1. Standardize dates into datetime fields.
2. Validate primary keys: Asset_ID, Software_ID, Location_ID, Cloud_Resource_ID, Application_ID.
3. Check duplicate assets using Asset_ID and Serial_Number.
4. Recalculate Lifecycle_Status using EOL_Date and the analysis date of 2026-06-01.
5. Normalize categorical fields such as Business_Unit, Criticality, Region, and Environment.
6. Validate cost fields as numeric and non-negative.
7. Identify missing owners, missing refresh plans, and exception-approved non-compliant software.

## 6. ETL Workflow in Python

```python
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import date

DATA = Path('data')
hardware = pd.read_csv(DATA / 'hardware_assets.csv', parse_dates=['Purchase_Date','Install_Date','Warranty_End','Expected_EOL'])
software = pd.read_csv(DATA / 'software_catalog.csv', parse_dates=['GA_Date','Support_End_Date','EOL_Date'])
installs = pd.read_csv(DATA / 'software_installations.csv', parse_dates=['Install_Date','Software_EOL_Date'])
locations = pd.read_csv(DATA / 'locations.csv')
vulns = pd.read_csv(DATA / 'vulnerabilities.csv', parse_dates=['Discovery_Date','Remediation_Due_Date'])
incidents = pd.read_csv(DATA / 'incidents.csv', parse_dates=['Incident_Date'])
refresh = pd.read_csv(DATA / 'refresh_projects.csv', parse_dates=['Planned_Refresh_Date','Actual_Refresh_Date'])
budget = pd.read_csv(DATA / 'budget_costs.csv')
cloud = pd.read_csv(DATA / 'cloud_resources.csv', parse_dates=['Deployment_Date','Support_End_Date'])
apps = pd.read_csv(DATA / 'application_portfolio.csv', parse_dates=['Technology_EOL_Date'])

analysis_date = pd.Timestamp('2026-06-01')

def lifecycle_bucket(eol_date):
    if pd.isna(eol_date):
        return 'Unknown'
    days = (eol_date - analysis_date).days
    if days < 0:
        return 'Past EOL'
    elif days <= 365:
        return 'EOL within 12 months'
    elif days <= 730:
        return 'EOL within 24 months'
    return 'Supported'

hardware['Calculated_Lifecycle_Status'] = hardware['Expected_EOL'].apply(lifecycle_bucket)
software['Calculated_Lifecycle_Status'] = software['EOL_Date'].apply(lifecycle_bucket)
installs['Calculated_Lifecycle_Status'] = installs['Software_EOL_Date'].apply(lifecycle_bucket)
cloud['Calculated_Lifecycle_Status'] = cloud['Support_End_Date'].apply(lifecycle_bucket)
```

## 7. Analytical Mart Creation

```python
hw_enriched = hardware.merge(locations, on='Location_ID', how='left')

vuln_summary = vulns.groupby('Asset_ID').agg(
    Open_Vulnerabilities=('Remediation_Status', lambda x: (x == 'Open').sum()),
    Critical_Vulnerabilities=('Severity', lambda x: (x == 'Critical').sum()),
    Avg_CVSS=('CVSS_Score', 'mean')
).reset_index()

incident_summary = incidents.groupby('Asset_ID').agg(
    Incident_Count=('Incident_ID','count'),
    Total_Downtime_Hours=('Downtime_Hours','sum'),
    Critical_Incidents=('Severity', lambda x: (x == 'Critical').sum())
).reset_index()

asset_risk = hw_enriched.merge(vuln_summary, on='Asset_ID', how='left').merge(incident_summary, on='Asset_ID', how='left')
asset_risk[['Open_Vulnerabilities','Critical_Vulnerabilities','Incident_Count','Total_Downtime_Hours','Critical_Incidents']] = asset_risk[['Open_Vulnerabilities','Critical_Vulnerabilities','Incident_Count','Total_Downtime_Hours','Critical_Incidents']].fillna(0)
```

## 8. Risk Scoring Method

```python
criticality_points = {'Low':1, 'Medium':2, 'High':3, 'Critical':4}
lifecycle_points = {'Supported':0, 'EOL within 24 months':1, 'EOL within 12 months':2, 'Past EOL':3}

asset_risk['Criticality_Points'] = asset_risk['Criticality'].map(criticality_points)
asset_risk['Lifecycle_Points'] = asset_risk['Calculated_Lifecycle_Status'].map(lifecycle_points)
asset_risk['Risk_Score'] = (
    asset_risk['Lifecycle_Points'] * 30 +
    asset_risk['Criticality_Points'] * 15 +
    np.log1p(asset_risk['Open_Vulnerabilities']) * 20 +
    np.log1p(asset_risk['Incident_Count']) * 10
)
asset_risk['Risk_Band'] = pd.cut(asset_risk['Risk_Score'], bins=[-1,40,70,100,999], labels=['Low','Medium','High','Critical'])
```

## 9. Statistical Analysis for EOL

### Test 1: Are EOL assets associated with more incidents?
- H0: Mean incident count is the same for supported and EOL assets.
- H1: EOL assets have higher incident counts.
- Recommended test: Mann-Whitney U test.

```python
from scipy.stats import mannwhitneyu, kruskal, spearmanr

eol_group = asset_risk[asset_risk['Calculated_Lifecycle_Status'].isin(['Past EOL','EOL within 12 months'])]['Incident_Count']
supported_group = asset_risk[asset_risk['Calculated_Lifecycle_Status'] == 'Supported']['Incident_Count']
stat, p = mannwhitneyu(eol_group, supported_group, alternative='greater')
print(stat, p)
```

### Test 2: Does vulnerability burden differ by lifecycle status?

```python
groups = [g['Open_Vulnerabilities'].values for _, g in asset_risk.groupby('Calculated_Lifecycle_Status')]
stat, p = kruskal(*groups)
print(stat, p)
```

### Test 3: Is risk score correlated with downtime?

```python
corr, p = spearmanr(asset_risk['Risk_Score'], asset_risk['Total_Downtime_Hours'])
print(corr, p)
```

## 10. Visualization Plan
1. EOL assets by lifecycle status.
2. Top 10 business units by Past EOL count.
3. EOL exposure by region and criticality heatmap.
4. Open vulnerabilities by lifecycle status.
5. Incident count by lifecycle status.
6. Refresh budget forecast by year.
7. Developer tooling EOL exposure by software category.
8. Cloud resources by lifecycle status and provider.
9. Risk score distribution.
10. Top 25 critical assets by risk score.

## 11. Streamlit Dashboard Structure
Create five tabs:

### Tab 1: Executive Overview
KPI cards: Total Assets, Past EOL Assets, EOL Next 12 Months, Critical Risk Assets, Forecast Refresh Cost.
Charts: lifecycle status distribution, region exposure, risk band distribution.

### Tab 2: Hardware & Network Lifecycle
Filters: region, asset type, business unit, criticality.
Charts: asset age, EOL timeline, network devices by EOL status, server exposure.

### Tab 3: Software & Developer Tooling
Filters: software category, vendor, business unit.
Charts: top EOL software, runtimes at risk, IDE and CI/CD lifecycle exposure.

### Tab 4: Cybersecurity & Operational Risk
Charts: vulnerabilities on EOL assets, incident frequency by lifecycle status, risk score ranking.

### Tab 5: Budget & Refresh Planning
Charts: refresh projects by year, budget versus forecast, deferred assets, blockers by category.

## 12. Power BI Conversion
Recommended relationships:
- hardware_assets[Location_ID] to locations[Location_ID]
- hardware_assets[Asset_ID] to software_installations[Asset_ID]
- hardware_assets[Asset_ID] to vulnerabilities[Asset_ID]
- hardware_assets[Asset_ID] to incidents[Asset_ID]
- hardware_assets[Asset_ID] to refresh_projects[Asset_ID]
- software_installations[Software_ID] to software_catalog[Software_ID]

Recommended pages:
1. Executive EOL Overview
2. Hardware Lifecycle
3. Software and Developer Tooling
4. Cybersecurity Risk
5. Refresh Budget Forecast
6. Cloud and Application Portfolio

Recommended DAX:

```DAX
Total Assets = COUNTROWS(hardware_assets)
Past EOL Assets = CALCULATE([Total Assets], hardware_assets[Lifecycle_Status] = "Past EOL")
EOL Next 12 Months = CALCULATE([Total Assets], hardware_assets[Lifecycle_Status] = "EOL within 12 months")
Past EOL % = DIVIDE([Past EOL Assets], [Total Assets])
Total Replacement Cost = SUM(hardware_assets[Replacement_Cost_CAD])
Open Vulnerabilities = CALCULATE(COUNTROWS(vulnerabilities), vulnerabilities[Remediation_Status] = "Open")
Critical Vulnerabilities = CALCULATE(COUNTROWS(vulnerabilities), vulnerabilities[Severity] = "Critical")
Total Downtime Hours = SUM(incidents[Downtime_Hours])
Refresh Budget = SUM(refresh_projects[Budget_Estimate_CAD])
```

## 13. Final Presentation Structure
1. Business context and objective.
2. Dataset design and banking technology estate.
3. Data model and ETL workflow.
4. EOL exposure summary.
5. Hardware and network lifecycle findings.
6. Software and developer tooling findings.
7. Cybersecurity and incident analysis.
8. Statistical analysis results.
9. Refresh budget forecast.
10. Recommendations and roadmap.

## 14. Recommended Actions
1. Prioritize Past EOL critical assets supporting Production and Tier 1 applications.
2. Create a 12-month refresh wave for endpoint and network assets nearing EOL.
3. Establish developer-tooling lifecycle standards for Python, Java, Node.js, .NET, Jenkins, Kubernetes, and IDE versions.
4. Link EOL governance with vulnerability management and incident problem records.
5. Build quarterly EOL steering committee reporting for budget and compliance tracking.
