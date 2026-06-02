# Git Workflow Used for This Project

This project follows a realistic analytics delivery workflow.

## Branching Model

| Branch | Purpose |
|---|---|
| `main` | Stable released portfolio version |
| `dev` | Integration branch for completed work |
| `feat/*` | Individual feature branches |

## Delivery Flow

```text
feat/data-package              -> dev
feat/data-quality-checks       -> dev
feat/etl-modeling              -> dev
feat/eol-statistical-analysis  -> dev
feat/streamlit-dashboard       -> dev
feat/powerbi-export-layer      -> dev
feat/documentation-polish      -> dev

dev -> main
```

## Why This Looks Believable

A real Technology EOL analytics project is normally built in phases:

1. Data package setup
2. Data quality checks
3. ETL and model-ready table preparation
4. Statistical analysis
5. Streamlit dashboard development
6. Power BI export layer
7. Documentation and final release

This avoids a single unrealistic mega-commit and shows a controlled delivery approach.
