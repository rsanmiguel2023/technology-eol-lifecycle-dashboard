# RQ5: Software Compliance Risk

## Research Question
Which software versions create the largest compliance risk?

## Hypotheses
**H0:** Software lifecycle status has no material impact on compliance exposure.

**H1:** Unsupported software versions materially increase compliance exposure and should be remediated.

## Executive Summary
Unsupported software versions can trigger audit findings and security exceptions. This page identifies software versions with the largest unsupported installation footprint.

## Methodology
Aggregate software installations by Software_Name, Version, Category, Software_Lifecycle_Status, and Compliance_Status. Count non-compliant installations.

## Interpretation Guide
High-volume unsupported software creates enterprise compliance risk even when each installation seems small. Developer tools, browsers, runtimes, databases, and server platforms require active lifecycle governance.

## Recommended Actions
Create a software remediation backlog. Prioritize unsupported operating systems, databases, Java, Python, Node.js, browsers, and security tools.

## Tooltip Definition
Software compliance risk shows unsupported versions that may create audit, security, and operational issues.

## Dashboard Mapping
This documentation is loaded by the corresponding Streamlit RQ page. The page uses this file to display the research question, hypothesis framing, interpretation, tooltip language, and recommendations.
