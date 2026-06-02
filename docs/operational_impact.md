# Operational Impact

## Management Question
How does lifecycle status relate to incidents, downtime, and operational reliability?

## Executive Summary
The operational model includes **104,634 incidents** and **298,911 downtime hours** across the technology estate. Past-EOL assets account for **79,128 downtime hours**, with **17.1 downtime hours per asset** compared with **11.4** for assets supported beyond 24 months.

## Business Interpretation
The pattern supports treating EOL as an operational resilience concern, not only an asset management issue. Past-EOL assets show higher disruption per asset in the synthetic model, which strengthens the business case for prioritizing refresh where unsupported technology affects customer-facing or production operations.

## Methodology
Incidents are aggregated at the asset level and joined to lifecycle status. Metrics include incident count, downtime hours, incident rate per asset, and downtime per asset. Additional synthetic operational impact events were applied to past-EOL assets to reflect the greater supportability and reliability burden expected in aging technology environments.

## Recommended Actions
Add lifecycle status to incident review, root cause analysis, major incident review, and change governance. Past-EOL status should trigger additional review during incident escalation and risk exception approval.

## Tooltip Definition
Downtime per asset shows the average operational disruption associated with each lifecycle status group.

## Dashboard Notes
This page is designed for operational risk discussion. It does not replace root-cause investigation, but it provides a management signal for prioritizing remediation.
