# Compliance Risk

## Management Question
Which software versions create the highest compliance exposure?

## Executive Summary
There are **104,497 non-compliant or past-EOL software installations** requiring lifecycle review. The largest exposure is concentrated in common enterprise productivity, browser, collaboration, operating system, and developer/runtime software.

Top exposure drivers:
- **Adobe Acrobat Pro 2020:** 11,213 installations
- **Mozilla Firefox ESR 115 ESR:** 11,213 installations
- **Microsoft Teams Classic/2.x:** 4,544 installations
- **Microsoft OneDrive 24.x:** 4,526 installations
- **Google Chrome Current:** 4,510 installations

## Business Interpretation
Software lifecycle risk is driven by both scale and criticality. Thousands of outdated endpoint installations can create broad audit exposure, while fewer unsupported server, database, or runtime installations can create concentrated production risk. This page helps separate high-volume remediation from high-criticality remediation.

## Methodology
Software installations are grouped by software name, version, category, and lifecycle status. Non-compliant and past-EOL installations are counted and ranked to identify the largest exposure areas.

## Recommended Actions
Prioritize unsupported software with high installation counts and software running in production or privileged environments. Establish application-owner remediation plans for outdated browsers, collaboration tools, operating systems, database platforms, Java/.NET/Python runtimes, and developer tools.

## Tooltip Definition
Software compliance risk means the software installation is either not compliant with the lifecycle standard or is already past its software EOL date.

## Dashboard Notes
Use the top-version table to prepare application-owner follow-up. The dashboard should avoid overly technical tooltips and focus on business risk, remediation ownership, and audit exposure.
