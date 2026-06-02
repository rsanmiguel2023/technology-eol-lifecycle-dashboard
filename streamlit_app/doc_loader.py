from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PAGE_DOCS = {
    "technology_estate": "technology_estate.md",
    "lifecycle_exposure": "lifecycle_exposure.md",
    "cybersecurity_risk": "cybersecurity_risk.md",
    "compliance_risk": "compliance_risk.md",
    "refresh_planning": "refresh_planning.md",
    "operational_impact": "operational_impact.md",
    "recommendations": "recommendations.md",
}

def load_doc(filename: str) -> str:
    path = DOCS / filename
    if not path.exists():
        return f"Documentation file not found: {filename}"
    return path.read_text(encoding="utf-8")

def section(filename: str, heading: str) -> str:
    text = load_doc(filename)
    pattern = rf"## {re.escape(heading)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, flags=re.S)
    return match.group(1).strip() if match else ""

def page_content(page_key: str) -> dict:
    fname = PAGE_DOCS[page_key]
    first_line = load_doc(fname).splitlines()[0].replace("#", "").strip()
    return {
        "file": fname,
        "title": first_line,
        "management_question": section(fname, "Management Question"),
        "executive_summary": section(fname, "Executive Summary"),
        "business_interpretation": section(fname, "Business Interpretation"),
        "methodology": section(fname, "Methodology"),
        "recommended_actions": section(fname, "Recommended Actions"),
        "tooltip": section(fname, "Tooltip Definition"),
        "dashboard_notes": section(fname, "Dashboard Notes"),
    }
