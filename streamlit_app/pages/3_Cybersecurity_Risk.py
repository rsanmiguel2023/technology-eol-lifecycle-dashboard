from streamlit_app.business_page import *
content = page_header("cybersecurity_risk", "🛡️")
df = _read_report("cybersecurity_unsupported_critical_summary.csv")
detail = _read_report("past_eol_critical_vulnerability_assets.csv")

assets_count = len(detail)
critical_vulns = int(detail["Critical_Vuln_Count"].sum()) if "Critical_Vuln_Count" in detail.columns else 0
high_vulns = int(detail["High_Vuln_Count"].sum()) if "High_Vuln_Count" in detail.columns else 0
replacement = float(detail["Replacement_Cost_CAD"].sum()) if "Replacement_Cost_CAD" in detail.columns else 0

c1,c2,c3,c4 = st.columns(4)
c1.metric("Unsupported + Critical Vuln Assets", f"{assets_count:,}", help=content["tooltip"])
c2.metric("Critical Vulnerabilities", f"{critical_vulns:,}", help="Critical vulnerabilities on past-EOL assets.")
c3.metric("High Vulnerabilities", f"{high_vulns:,}", help="High vulnerabilities on past-EOL assets.")
c4.metric("Replacement Exposure", _money(replacement), help="Estimated replacement cost for affected unsupported assets.")

st.divider()
col1, col2 = st.columns(2)
with col1:
    by_bu = detail.groupby("Business_Unit").agg(assets=("Asset_ID", "count"), critical_vulns=("Critical_Vuln_Count", "sum")).reset_index().sort_values("critical_vulns", ascending=True).tail(10)
    plot_bar(by_bu, "critical_vulns", "Business_Unit", "Critical vulnerabilities on unsupported assets", orientation="h")
with col2:
    by_type = detail.groupby("Asset_Type").size().reset_index(name="assets").sort_values("assets", ascending=True)
    plot_bar(by_type, "assets", "Asset_Type", "Unsupported vulnerable assets by type", orientation="h")

show_standard_tabs(content, df, content["file"], "Unsupported assets with critical vulnerability summary")
