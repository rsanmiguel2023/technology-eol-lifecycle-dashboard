# Feature Engineering

## Purpose

Feature engineering converts raw source-system extracts into lifecycle, risk, and refresh planning indicators.

## Key Engineered Features

| Feature | Logic |
|---|---|
| Asset_Age_Years | Current reporting date minus purchase date |
| Months_To_EOL | Vendor support end date minus reporting date |
| Lifecycle_Status | Derived from months to EOL |
| Past_EOL_Flag | 1 when vendor support has already ended |
| Expiring_12M_Flag | 1 when support ends within 12 months |
| Warranty_Status | Derived from warranty end date |
| Replacement_Cost | Standard replacement cost from reference table |
| Lifecycle_Risk_Score | Weighted score using lifecycle, vulnerability, incident, and business factors |
| Refresh_Priority | Derived from risk score and lifecycle status |

## Current Engineered Results

- Past-EOL assets: **4,682**
- Assets expiring within 12 months: **8,337**
- Unsupported software installations: **91,618**
- Assets with critical/high cyber exposure: **1,391**

## Interpretation

These features are not stored in the raw data. They are derived through the analytics pipeline, which makes the project more realistic and defensible for a Technology Lifecycle Governance use case.
