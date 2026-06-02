"""Rebalance synthetic EOL and critical vulnerability exposure for executive realism.

This script keeps the total technology estate size the same, but distributes Past-EOL
and critical-vulnerability overlap across endpoints, servers, and network assets.
Run before the main ETL pipeline when rebuilding the synthetic dataset.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
AS_OF_DATE = pd.Timestamp("2026-06-01")
SEED = 42
rng = np.random.default_rng(SEED)

hardware_path = RAW / "hardware_assets.csv"
vuln_path = RAW / "vulnerabilities.csv"

hardware = pd.read_csv(hardware_path, low_memory=False)
vulns = pd.read_csv(vuln_path, low_memory=False)

# Total Past-EOL exposure is preserved from the first generated dataset.
# Distribution is adjusted to look like a realistic bank estate instead of 100% laptops.
past_eol_targets = {
    "Laptop": 2085,
    "Desktop": 695,
    "Server": 927,
    "Firewall": 150,
    "Router": 185,
    "Access Switch": 185,
    "Distribution Switch": 139,
    "Storage": 40,
    "Wireless Access Point": 228,
}

# Critical vulnerability overlap target is preserved at 3,661 assets.
critical_overlap_targets = {
    "Laptop": 1648,
    "Desktop": 549,
    "Server": 732,
    "Firewall": 150,
    "Router": 146,
    "Access Switch": 146,
    "Distribution Switch": 110,
    "Storage": 40,
    "Wireless Access Point": 140,
}

assert sum(past_eol_targets.values()) == 4634, "Past-EOL target must stay at 4,634 assets."
assert sum(critical_overlap_targets.values()) == 3661, "Critical overlap target must stay at 3,661 assets."

# Pick deterministic assets by type.
past_eol_ids = []
critical_overlap_ids = []
for asset_type, count in past_eol_targets.items():
    ids = hardware.loc[hardware["Asset_Type"].eq(asset_type), "Asset_ID"].tolist()
    if len(ids) < count:
        raise ValueError(f"Not enough {asset_type} assets for target {count}; available {len(ids)}")
    chosen = rng.choice(ids, size=count, replace=False).tolist()
    past_eol_ids.extend(chosen)

    crit_count = critical_overlap_targets.get(asset_type, 0)
    if crit_count:
        critical_overlap_ids.extend(rng.choice(chosen, size=crit_count, replace=False).tolist())

past_eol_ids = set(past_eol_ids)
critical_overlap_ids = set(critical_overlap_ids)

# Assign lifecycle dates. Dates remain synthetic but are internally consistent.
def random_dates(start: str, end: str, n: int) -> pd.Series:
    start_ts = pd.Timestamp(start).value // 10**9
    end_ts = pd.Timestamp(end).value // 10**9
    vals = rng.integers(start_ts, end_ts, size=n)
    return pd.to_datetime(vals, unit="s").normalize()

hardware["Expected_EOL"] = pd.to_datetime(hardware["Expected_EOL"], errors="coerce")

past_mask = hardware["Asset_ID"].isin(past_eol_ids)
hardware.loc[past_mask, "Expected_EOL"] = random_dates("2023-01-01", "2026-05-15", int(past_mask.sum())).values

# Move non-selected assets that were previously Past EOL into realistic planning windows.
not_past = ~past_mask
# Preserve future variety by asset class with deterministic buckets.
idx = hardware.loc[not_past].index.to_numpy()
rng.shuffle(idx)
n = len(idx)
b1 = idx[: int(n * 0.38)]      # 0-12 months
b2 = idx[int(n * 0.38): int(n * 0.72)]  # 12-24 months
b3 = idx[int(n * 0.72):]       # Supported >24 months
hardware.loc[b1, "Expected_EOL"] = random_dates("2026-06-15", "2027-05-31", len(b1)).values
hardware.loc[b2, "Expected_EOL"] = random_dates("2027-06-01", "2028-05-31", len(b2)).values
hardware.loc[b3, "Expected_EOL"] = random_dates("2028-06-01", "2031-12-31", len(b3)).values

# Keep raw lifecycle label readable for users browsing the raw CSV.
def status(eol):
    days = (pd.Timestamp(eol) - AS_OF_DATE).days
    if days < 0:
        return "Past EOL"
    if days <= 365:
        return "EOL within 12 months"
    if days <= 730:
        return "EOL within 24 months"
    return "Supported"

hardware["Lifecycle_Status"] = hardware["Expected_EOL"].apply(status)
hardware["Expected_EOL"] = pd.to_datetime(hardware["Expected_EOL"]).dt.date.astype(str)
hardware.to_csv(hardware_path, index=False)

# Rebalance critical vulnerability overlap for Past-EOL assets.
# 1) Downgrade existing critical vulnerabilities on Past-EOL assets outside the target overlap.
past_noncritical_ids = past_eol_ids - critical_overlap_ids
mask_downgrade = vulns["Asset_ID"].isin(past_noncritical_ids) & vulns["Severity"].eq("Critical")
vulns.loc[mask_downgrade, "Severity"] = "High"
vulns.loc[mask_downgrade, "CVSS_Score"] = vulns.loc[mask_downgrade, "CVSS_Score"].clip(upper=8.8)

# 2) Ensure each target overlap asset has at least one critical vulnerability.
existing_critical = set(vulns.loc[vulns["Severity"].eq("Critical"), "Asset_ID"])
missing = sorted(critical_overlap_ids - existing_critical)

if missing:
    start_num = len(vulns) + 1
    cves = [
        "CVE-2024-20674", "CVE-2024-30078", "CVE-2023-36884", "CVE-2024-3400",
        "CVE-2023-20198", "CVE-2024-21762", "CVE-2023-4966", "CVE-2024-3094",
        "CVE-2023-34362", "CVE-2024-6387",
    ]
    products = [
        "Microsoft Windows", "Microsoft Defender", "Cisco IOS XE", "Palo Alto PAN-OS",
        "Fortinet FortiOS", "OpenSSH", "Citrix NetScaler ADC", "Apache HTTP Server",
        "Google Chrome", "Adobe Acrobat",
    ]
    new_rows = []
    for i, asset_id in enumerate(missing, start=start_num):
        new_rows.append({
            "Vulnerability_Record_ID": f"VUL-{i:08d}",
            "Asset_ID": asset_id,
            "CVE": cves[i % len(cves)],
            "Affected_Product": products[i % len(products)],
            "Severity": "Critical",
            "CVSS_Score": round(float(rng.uniform(9.0, 10.0)), 1),
            "Discovery_Date": str(pd.Timestamp("2026-01-01") + pd.Timedelta(days=int(rng.integers(0, 140)))),
            "Remediation_Due_Date": str(pd.Timestamp("2026-06-01") + pd.Timedelta(days=int(rng.integers(7, 45)))),
            "Remediation_Status": rng.choice(["Open", "In Progress", "Exception Requested"], p=[0.50, 0.35, 0.15]),
            "Patch_Available": rng.choice(["Yes", "No"], p=[0.70, 0.30]),
            "Recommended_Action": rng.choice(["Patch", "Upgrade", "Compensating Control", "Vendor Fix Pending"], p=[0.45, 0.30, 0.15, 0.10]),
        })
    vulns = pd.concat([vulns, pd.DataFrame(new_rows)], ignore_index=True)

vulns.to_csv(vuln_path, index=False)

summary = hardware[hardware["Lifecycle_Status"].eq("Past EOL")]["Asset_Type"].value_counts().sort_index()
print("Rebalanced Past-EOL assets by type:")
print(summary.to_string())
print(f"Past-EOL total: {int(summary.sum()):,}")
print(f"Target critical vulnerability overlap assets: {len(critical_overlap_ids):,}")
print("Updated raw hardware and vulnerability files.")
