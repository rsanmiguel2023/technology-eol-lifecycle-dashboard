# Data Cleaning

Cleaning steps include date parsing, lifecycle status normalization, duplicate checks, missing value review, asset-location validation, software installation validation, and risk field standardization.

## Cleaning Rules
- Convert all date columns to datetime.
- Validate Expected_EOL and Software_EOL_Date.
- Standardize Lifecycle_Status values.
- Replace missing vulnerability counts with zero.
- Validate cost fields as non-negative.
