from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
PROCESSED = ROOT / 'data' / 'processed'
OUTPUTS = ROOT / 'outputs'
FIGURES = OUTPUTS / 'figures'
REPORTS = OUTPUTS / 'reports'

for p in [PROCESSED, FIGURES, REPORTS]:
    p.mkdir(parents=True, exist_ok=True)

AS_OF_DATE = pd.Timestamp('2026-06-01')


def read_csv(name: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(RAW / name, low_memory=False, **kwargs)


def save_csv(df: pd.DataFrame, name: str) -> None:
    df.to_csv(PROCESSED / name, index=False)


def lifecycle_status(eol_date) -> str:
    if pd.isna(eol_date):
        return 'Unknown'
    eol = pd.to_datetime(eol_date, errors='coerce')
    if pd.isna(eol):
        return 'Unknown'
    days = (eol - AS_OF_DATE).days
    if days < 0:
        return 'Past EOL'
    if days <= 180:
        return '0-6 Months'
    if days <= 365:
        return '6-12 Months'
    if days <= 730:
        return '12-24 Months'
    return 'Supported >24 Months'


def criticality_score(value: str) -> int:
    return {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}.get(str(value), 1)


def eol_score(status: str) -> int:
    return {'Past EOL': 5, '0-6 Months': 4, '6-12 Months': 3, '12-24 Months': 2, 'Supported >24 Months': 1, 'Unknown': 2}.get(str(status), 2)


def severity_score(value: str) -> int:
    return {'Low': 1, 'Medium': 2, 'High': 4, 'Critical': 5}.get(str(value), 0)


def safe_date(series):
    return pd.to_datetime(series, errors='coerce')
