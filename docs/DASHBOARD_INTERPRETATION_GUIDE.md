
# Executive Dashboard Interpretation Guide

This Streamlit dashboard is designed for a Senior Analyst, Technology EOL presentation to upper management. It is not only a technical inventory dashboard. Each page answers a specific management question and includes an executive summary, visual interpretation, and recommended action.

## Primary Questions Answered

1. **Which assets are already past EOL?**
   - Use the Executive EOL page.
   - Focus on the Past EOL count, high/critical assets, and past-EOL assets with critical vulnerabilities.

2. **Which business units have the highest EOL exposure?**
   - Use the Business Unit View tab in Executive EOL.
   - This converts technical risk into accountable ownership.

3. **Which unsupported assets also have critical vulnerabilities?**
   - Use the Risk & Vulnerabilities page.
   - This is the highest-priority remediation population.

4. **How much budget is needed for refresh planning?**
   - Use the Budget & Refresh Planning page.
   - The dashboard estimates replacement need by EOL year, region, and asset type.

5. **Which software versions create the largest compliance risk?**
   - Use the Software & Compliance page.
   - This includes development software, runtimes, IDEs, CI/CD tools, databases, operating systems, and productivity software.

6. **How does EOL status relate to incidents and downtime?**
   - Use the Incidents & Downtime page.
   - This connects lifecycle risk to operational reliability.

## Figure Export

Run:

```bash
python src/05_export_figures_and_reports.py
```

The script exports:

- PNG figures to `outputs/figures/`
- Executive-ready CSV summaries to `outputs/reports/`

These exported figures can be used in PowerPoint, project documentation, GitHub README screenshots, or LinkedIn portfolio posts.

## Executive Storyline

The recommended presentation flow is:

1. Establish total technology estate size.
2. Show current EOL exposure.
3. Show the highest-risk overlap: Past EOL + Critical Vulnerability.
4. Show which business units own the exposure.
5. Show software/version compliance risk.
6. Convert the exposure into a funded refresh roadmap.
7. Close with recommendations and governance cadence.

## Management Recommendations

- Remediate past-EOL production assets with critical vulnerabilities first.
- Require risk acceptance for unsupported assets that cannot be replaced immediately.
- Fund refresh work in waves: immediate, 12-month, and 24-month.
- Add lifecycle KPIs to monthly technology risk governance.
- Standardize supported developer tools and runtimes to reduce hidden risk.
- Track software version EOL separately from hardware EOL.
