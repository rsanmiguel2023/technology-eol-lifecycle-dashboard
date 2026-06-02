# Technology Lifecycle Risk Dashboard — Executive Banking EOL Analytics

This project is a synthetic but realistic Technology End-of-Life (EOL) analytics project for a banking environment. It supports executive reporting across technology lifecycle exposure, cybersecurity risk, software compliance, refresh funding, operational impact, and management recommendations.

The project is designed for a Senior Analyst / Technology EOL portfolio scenario and can be analyzed using Python, Streamlit, Power BI, or Tableau.

## Executive Dashboard Pages

- Executive Summary
- Technology Estate
- Lifecycle Exposure
- Cybersecurity Risk
- Compliance Risk
- Refresh Planning
- Operational Impact
- Recommendations

## Key Management Questions

1. Which assets are already past EOL?
2. Which business units have the highest EOL exposure?
3. Which unsupported assets also have critical vulnerabilities?
4. How much budget is needed for refresh planning?
5. Which software versions create the largest compliance risk?
6. How does EOL status relate to incidents and downtime?

## Run Order

Run from the project root:

```bash
python src/00_rebalance_synthetic_eol_risk.py
python src/01_data_quality.py
python src/02_etl_prepare_model.py
python src/03_statistical_analysis.py
python src/04_generate_powerbi_exports.py
python src/05_export_figures_and_reports.py
streamlit run streamlit_app/Home.py
```

## Main Outputs

- `outputs/reports/executive_questions_summary.csv`
- `outputs/reports/business_unit_eol_exposure.csv`
- `outputs/reports/past_eol_critical_vulnerability_assets.csv`
- `outputs/reports/software_compliance_risk_summary.csv`
- `outputs/reports/refresh_budget_gap_summary.csv`
- `outputs/reports/operational_impact_by_lifecycle_status.csv`
- `outputs/reports/recommendation_actions.csv`
- `outputs/figures/*.png`
- `outputs/powerbi_exports/*.csv`

## Important Synthetic Data Note

Vendor, hardware, and software product names are real. Asset records, costs, incidents, vulnerabilities, lifecycle dates, locations, ownership, and business unit assignments are synthetic and created for portfolio demonstration purposes.
