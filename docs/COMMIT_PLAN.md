# Suggested Commit Plan

Use this as your working checklist when pushing the project to GitHub.

| Step | Branch | Commit Message |
|---:|---|---|
| 1 | `main` | `chore: initialize Technology EOL analytics project` |
| 2 | `feat/data-package` | `feat(data): add synthetic banking technology inventory datasets` |
| 3 | `feat/data-quality-checks` | `feat(quality): add reusable data validation checks` |
| 4 | `feat/etl-modeling` | `feat(etl): prepare model-ready lifecycle risk datasets` |
| 5 | `feat/eol-statistical-analysis` | `feat(analysis): add EOL statistical risk analysis` |
| 6 | `feat/streamlit-dashboard` | `feat(streamlit): add executive Technology EOL dashboard` |
| 7 | `feat/powerbi-export-layer` | `feat(powerbi): add curated export tables for Power BI dashboard` |
| 8 | `feat/documentation-polish` | `docs: add realistic branch workflow and project delivery notes` |
| 9 | `main` | `release: publish Technology EOL lifecycle dashboard v1` |

## Practical Tip

Push each feature branch separately, then merge it into `dev`. Only merge `dev` into `main` once the whole project runs successfully.
