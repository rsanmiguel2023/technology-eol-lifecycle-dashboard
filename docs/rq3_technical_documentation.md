# RQ3: Unsupported Assets with Critical Vulnerabilities

## Research Question
Which unsupported assets also have critical vulnerabilities?

## Hypotheses
**H0:** Unsupported assets are not associated with increased critical vulnerability exposure.

**H1:** Unsupported assets are associated with higher critical vulnerability exposure and should be prioritized for remediation.

## Executive Summary
The highest-risk lifecycle scenario is the overlap between unsupported technology and critical vulnerabilities. These assets create security and audit exposure and should be prioritized ahead of ordinary refresh items.

## Methodology
Filter assets where Lifecycle_Status is Past EOL and Critical_Vuln_Count is greater than zero. Rank by Risk_Score, Criticality, Max_CVSS, and business ownership.

## Interpretation Guide
An unsupported asset with critical vulnerabilities is harder to protect because standard vendor patching or support paths may be limited. These items should be presented to Risk, Security, and Infrastructure leadership.

## Recommended Actions
Create an emergency remediation track for Past EOL plus critical vulnerability assets. Options include patch, isolate, replace, decommission, or formally accept risk.

## Tooltip Definition
This view isolates the most urgent risk overlap: unsupported technology plus critical vulnerabilities.

## Dashboard Mapping
This documentation is loaded by the corresponding Streamlit RQ page. The page uses this file to display the research question, hypothesis framing, interpretation, tooltip language, and recommendations.
