# Run Dashboard Pipeline

Run these commands from the project root.

## 1. Create and activate environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Run the full analytics pipeline

```bash
python src/01_data_quality.py
python src/02_data_profiling_eda.py
python src/03_data_cleaning.py
python src/04_feature_engineering_lifecycle.py
python src/05_statistical_analysis.py
python src/06_executive_reporting.py
python src/07_export_powerbi_datasets.py
python src/08_export_figures.py
```

## 3. Launch Streamlit dashboard

```bash
streamlit run streamlit_app/Home.py
```

## 4. Key outputs to review

```text
outputs/reports/executive_questions_summary.csv
outputs/reports/business_unit_eol_exposure.csv
outputs/reports/risk_heatmap_business_unit.csv
outputs/reports/past_eol_critical_vulnerability_assets.csv
outputs/reports/software_compliance_risk_summary.csv
outputs/reports/refresh_budget_planning_summary.csv
outputs/reports/operational_impact_by_lifecycle_status.csv
outputs/reports/recommendation_actions.csv
```

## 5. Key engineered datasets

```text
data/engineered/asset_lifecycle_analysis.csv
data/engineered/software_lifecycle_analysis.csv
data/engineered/business_unit_risk.csv
data/engineered/cyber_risk_analysis.csv
data/engineered/refresh_forecast.csv
data/engineered/operational_risk_analysis.csv
```
