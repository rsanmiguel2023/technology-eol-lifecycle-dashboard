from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

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

def rq_content(n: int) -> dict:
    fname = f"rq{n}_technical_documentation.md"
    return {
        "file": fname,
        "title": load_doc(fname).splitlines()[0].replace("#", "").strip(),
        "question": section(fname, "Research Question"),
        "hypotheses": section(fname, "Hypotheses"),
        "executive_summary": section(fname, "Executive Summary"),
        "methodology": section(fname, "Methodology"),
        "interpretation": section(fname, "Interpretation Guide"),
        "recommendations": section(fname, "Recommended Actions"),
        "tooltip": section(fname, "Tooltip Definition"),
    }
