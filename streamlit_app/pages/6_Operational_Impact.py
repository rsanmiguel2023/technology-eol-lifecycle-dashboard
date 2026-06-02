from streamlit_app.business_page import *
content = page_header("operational_impact", "⏱️")
df = _read_report("operational_impact_by_lifecycle_status.csv")

incidents = int(df["incidents"].sum())
downtime = float(df["downtime_hours"].sum())
max_rate = df.sort_values("downtime_per_asset", ascending=False).iloc[0]
assets = int(df["assets"].sum())

c1,c2,c3,c4 = st.columns(4)
c1.metric("Incidents", f"{incidents:,}", help="Total incident count attached to assets.")
c2.metric("Downtime Hours", f"{downtime:,.0f}", help="Total downtime hours attached to assets.")
c3.metric("Highest Downtime Group", str(max_rate["Lifecycle_Status"]), help="Lifecycle group with the highest downtime per asset.")
c4.metric("Assets in Analysis", f"{assets:,}", help="Assets included in operational impact analysis.")

st.divider()
col1, col2 = st.columns(2)
with col1:
    plot_bar(df.sort_values("downtime_per_asset", ascending=False), "Lifecycle_Status", "downtime_per_asset", "Downtime per asset by lifecycle status")
with col2:
    plot_bar(df.sort_values("incident_rate_per_asset", ascending=False), "Lifecycle_Status", "incident_rate_per_asset", "Incident rate per asset by lifecycle status")

show_standard_tabs(content, df, content["file"], "Operational impact by lifecycle status")
