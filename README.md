# Technology EOL Enterprise Lifecycle Governance Analytics

Synthetic but enterprise-realistic analytics project for a Senior Analyst, Technology End-of-Life / Lifecycle Governance role in a banking environment.

The project is designed to show a realistic workflow:

```text
Raw source extracts
→ Data quality assessment
→ EDA / profiling
→ Data cleaning
→ Feature engineering
→ Lifecycle and risk analysis
→ Executive reporting
→ Streamlit dashboard
→ Power BI export layer
```

## Final data-layer structure

```text
data/raw          Source-system style extracts only
data/processed    Cleaned datasets after standardization and validation
data/engineered   Analytical datasets with lifecycle, risk, cost, and compliance features
outputs/reports   Executive summary outputs and dashboard-ready CSV reports
outputs/figures   Exported visuals
outputs/powerbi   Power BI-ready reporting tables
docs              Dashboard narrative and methodology documentation
src               Pipeline scripts
streamlit_app     Executive Streamlit dashboard
```

## Run order

```bash
python src/01_data_quality.py
python src/02_data_profiling_eda.py
python src/03_data_cleaning.py
python src/04_feature_engineering_lifecycle.py
python src/05_statistical_analysis.py
python src/06_executive_reporting.py
python src/07_export_powerbi_datasets.py
python src/08_export_figures.py
streamlit run streamlit_app/Home.py
```

## Key design decisions

- Raw data intentionally excludes analytical fields such as `Lifecycle_Status`, `Months_To_EOL`, `Replacement_Cost`, `Risk_Band`, and `Refresh_Priority`.
- Lifecycle fields are engineered by joining cleaned inventory to reference lifecycle and replacement cost tables.
- Business-unit risk bands use an executive risk index based on scale, lifecycle exposure, cyber exposure, replacement cost, downtime, and business criticality.
- The lifecycle distribution was adjusted through the reference lifecycle catalog, not by directly editing raw inventory records.
- Cyber-risk reporting now includes infrastructure, network, server, endpoint, and storage assets instead of only laptops.
