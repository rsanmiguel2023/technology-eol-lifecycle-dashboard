# Technology EOL Lifecycle Dashboard

Synthetic banking dataset and analytics project for a Senior Analyst, Technology End-of-Life role.

## Project goal
Analyze hardware, software, cloud, network, vulnerability, incident, refresh, and cost data to identify lifecycle risk, unsupported technology exposure, budget requirements, and regulatory/compliance risk.

## Folder structure

```text
technology-eol-lifecycle-dashboard/
├── data/
│   ├── raw/                 # Synthetic source CSV files
│   └── processed/           # Cleaned/model-ready outputs
├── docs/                    # Data dictionary and project guide
├── outputs/
│   ├── figures/
│   ├── reports/
│   └── powerbi_exports/
├── powerbi/                 # Power BI notes and model instructions
├── src/                     # Python ETL and analysis scripts
├── streamlit_app/           # Streamlit dashboard app
├── requirements.txt
├── config.yaml
└── README.md
```

## Setup in VS Code

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

For Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the pipeline

```bash
python src/01_data_quality.py
python src/02_etl_prepare_model.py
python src/03_statistical_analysis.py
python src/04_generate_powerbi_exports.py
```

## Run Streamlit dashboard

```bash
streamlit run streamlit_app/Home.py
```

## Power BI workflow

1. Run the Python ETL scripts first.
2. Open Power BI Desktop.
3. Import CSVs from `data/processed` and `outputs/powerbi_exports`.
4. Build relationships using `Asset_ID`, `Location_ID`, `Application_ID`, and lifecycle dimensions.
5. Create executive, compliance, infrastructure, software, and budget dashboards.

## Main analysis questions

- Which assets are already past EOL?
- Which business units have the highest EOL exposure?
- Which unsupported assets also have critical vulnerabilities?
- How much budget is needed for refresh planning?
- Which software versions create the largest compliance risk?
- How does EOL status relate to incidents and downtime?

