from streamlit_app.business_page import *
content = page_header("compliance_risk", "⚖️")
df = _read_report("compliance_software_versions_summary.csv")

installs = int(df["non_compliant_installs"].sum())
assets = int(df["distinct_assets"].sum()) if "distinct_assets" in df.columns else 0
products = df["Software_Name"].nunique()
versions = len(df)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Non-Compliant Installs", f"{installs:,}", help=content["tooltip"])
c2.metric("Affected Asset Count", f"{assets:,}", help="Distinct asset count summed across software/version groups.")
c3.metric("Software Products", f"{products:,}", help="Number of software products represented in non-compliant inventory.")
c4.metric("Versions in Scope", f"{versions:,}", help="Software-version combinations in scope.")

st.divider()
col1, col2 = st.columns(2)
with col1:
    top = df.sort_values("non_compliant_installs", ascending=True).tail(15)
    plot_bar(top, "non_compliant_installs", "Software_Name", "Top software products creating compliance exposure", orientation="h")
with col2:
    cat = df.groupby("Category").agg(non_compliant_installs=("non_compliant_installs", "sum")).reset_index().sort_values("non_compliant_installs", ascending=False)
    plot_bar(cat, "Category", "non_compliant_installs", "Compliance exposure by software category")

show_standard_tabs(content, df, content["file"], "Software compliance risk summary")
