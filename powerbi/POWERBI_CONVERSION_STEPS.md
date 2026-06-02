# Power BI Conversion Steps

## 1. Load data
Use **Get Data > Text/CSV** and load:

- `data/processed/asset_risk_model.csv`
- `data/processed/software_installations_model.csv`
- `data/processed/cloud_resources_model.csv`
- `data/raw/refresh_projects.csv`
- `data/raw/budget_costs.csv`
- `data/raw/locations.csv`
- `outputs/powerbi_exports/*.csv`

## 2. Recommended model
Create a star-like model:

- FactAssetRisk → DimLocation using `Location_ID`
- FactSoftwareInstallations → FactAssetRisk using `Asset_ID`
- FactRefreshProjects → FactAssetRisk using `Asset_ID`
- FactCloudResources as its own fact table
- FactBudgetCosts as a planning table by Year and Asset_Category

## 3. Core DAX measures

```DAX
Total Assets = DISTINCTCOUNT(asset_risk_model[Asset_ID])

Past EOL Assets =
CALCULATE(
    [Total Assets],
    asset_risk_model[Lifecycle_Status] = "Past EOL"
)

EOL Within 12 Months =
CALCULATE(
    [Total Assets],
    asset_risk_model[Lifecycle_Status] IN {"0-6 Months", "6-12 Months"}
)

Replacement Cost = SUM(asset_risk_model[Replacement_Cost])

Average Risk Score = AVERAGE(asset_risk_model[Risk_Score])

Critical Risk Assets =
CALCULATE(
    [Total Assets],
    asset_risk_model[Risk_Band] = "Critical"
)

Critical Vulnerabilities = SUM(asset_risk_model[Critical_Vuln_Count])
```

## 4. Dashboard pages

### Page 1: Executive EOL Overview
- KPI cards: Total Assets, Past EOL Assets, EOL Within 12 Months, Replacement Cost
- Stacked bar: Lifecycle Status by Asset Type
- Map or bar: EOL exposure by Region
- Table: Top 50 highest-risk assets

### Page 2: Software EOL and Compliance
- KPI cards: Software Installations, Past EOL Software, High-Risk Software
- Bar: Top Software Names by Past EOL Installations
- Matrix: Software Name, Version, Lifecycle Status, Installation Count

### Page 3: Vulnerability and Risk
- Scatter: Age Years vs Risk Score
- Bar: Critical vulnerabilities by Asset Type
- Table: Critical assets with critical CVEs

### Page 4: Budget and Refresh Planning
- Line: Budget Allocated vs Replacement Cost by Year
- Bar: Refresh Budget by Status
- Table: Refresh candidates sorted by Risk Score

### Page 5: Infrastructure and Cloud
- Bar: Server and Network EOL by Platform
- Bar: Cloud lifecycle status by Service
- KPI cards: Cloud Monthly Cost, Cloud Past EOL Resources
