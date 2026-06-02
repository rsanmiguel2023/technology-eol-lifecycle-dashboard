# Technology EOL Lifecycle Management Dashboard

Executive-ready portfolio project for a Senior Analyst, Technology End-of-Life role.

## What changed in this version
- Each business question is now a formal research question.
- Streamlit reads executive summaries, hypotheses, interpretations, tooltips, and recommendations from `docs/`.
- The dashboard follows a capstone-style structure with EDA, RQ pages, technical documentation, presentation notes, and recommendation logic.
- Figure exports and Power BI export CSVs are included.

## Run
```bash
pip install -r requirements.txt
python src/05_export_figures_and_reports.py
streamlit run streamlit_app/Home.py
```

## Research Questions
1. Which assets are already past EOL?
2. Which business units have the highest EOL exposure?
3. Which unsupported assets also have critical vulnerabilities?
4. How much budget is needed for refresh planning?
5. Which software versions create the largest compliance risk?
6. How does EOL status relate to incidents and downtime?
