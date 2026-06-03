# Raw Data Model — Enterprise Technology Lifecycle Governance

This version uses realistic source-system extracts. Raw files do **not** contain analysis-ready fields such as `Lifecycle_Status`, `Expected_EOL`, `Replacement_Cost`, `Risk_Score`, `Refresh_Priority`, `Compliance_Risk`, or `Budget_Gap`.

## Raw Sources
- `hardware_assets_raw.csv`: CMDB / SCCM / Intune / network discovery inventory.
- `software_installations_raw.csv`: SCCM / Intune / Tanium software evidence.
- `vulnerabilities_raw.csv`: Tenable / Qualys / Defender vulnerability scanner findings.
- `incidents_raw.csv`: ServiceNow-style incident records.
- `cloud_resources_raw.csv`: Azure/AWS inventory.
- `refresh_projects_raw.csv`: project portfolio management extract.
- `budget_allocations_raw.csv`: finance planning extract.

## Reference Sources
- `hardware_model_reference.csv`: model support and refresh assumptions.
- `software_lifecycle_reference.csv`: software support dates.
- `replacement_cost_reference.csv`: cost lookup used to engineer replacement cost.
- `business_units.csv`, `locations.csv`, `employees.csv`: dimensional reference data.
