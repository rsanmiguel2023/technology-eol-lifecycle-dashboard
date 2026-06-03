# Data Quality

## Purpose

The data quality layer validates that raw source extracts are suitable for lifecycle analytics before feature engineering is applied.

## Checks Performed

- Row counts by source table
- Column counts by source table
- Duplicate record checks
- Missing value checks
- Date field validation
- Asset-to-software and asset-to-vulnerability relationship checks

## Interpretation

This step demonstrates that the dashboard is not built directly from raw files. Source extracts are profiled and cleaned before analytical features such as lifecycle status, replacement cost, and risk scores are created.
