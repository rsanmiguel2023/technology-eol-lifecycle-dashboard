# Cybersecurity Risk

## Management Question
Which unsupported assets represent the greatest cyber exposure?

## Executive Summary
The dashboard identifies **3,661 past-EOL assets with at least one critical vulnerability**. These assets carry **9,412 critical vulnerabilities** and **2,949 high vulnerabilities**, with an estimated replacement exposure of **CAD $22.8M**. The exposure now spans multiple technology classes rather than appearing as an endpoint-only issue.

## Business Interpretation
An unsupported asset is a lifecycle risk. An unsupported asset with a critical vulnerability is a cybersecurity governance issue. These assets should receive immediate attention because patch options, vendor support, and audit defensibility may be reduced.

Current critical-overlap asset mix:
- **Laptop:** 1,648 assets
- **Server:** 732 assets
- **Desktop:** 549 assets
- **Firewall:** 150 assets
- **Access Switch:** 146 assets
- **Router:** 146 assets
- **Wireless Access Point:** 140 assets
- **Distribution Switch:** 110 assets
- **Storage:** 40 assets

## Methodology
The processed asset risk model aggregates vulnerability counts by asset. This page filters for assets that are Past EOL and have at least one critical vulnerability, then groups the exposure by business unit, asset type, and business criticality.

## Recommended Actions
Create a 30-60-90 day remediation plan for unsupported assets with critical vulnerabilities. Where replacement cannot be completed immediately, document compensating controls such as network isolation, patch exception approval, enhanced monitoring, and business-owner risk acceptance.

## Tooltip Definition
Critical vulnerability overlap means an asset is already past EOL and has one or more critical vulnerabilities assigned to it.

## Dashboard Notes
The executive story should focus on the overlap count, the top business units, and the mix of affected infrastructure. The asset-level table is for remediation tracking, not for executive presentation.
