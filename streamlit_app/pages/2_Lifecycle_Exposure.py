from streamlit_app.business_page import *
content = page_header("lifecycle_exposure", "📊")
df = _read_report("lifecycle_exposure_by_asset_type.csv")
bu = _read_report("business_unit_eol_exposure.csv")
lifecycle = _read_report("executive_lifecycle_summary.csv")

past = int(lifecycle.loc[lifecycle["Lifecycle_Status"].eq("Past EOL"), "assets"].sum())
exp12 = int(lifecycle.loc[lifecycle["Lifecycle_Status"].isin(["0-6 Months", "6-12 Months"]), "assets"].sum())
exp24 = int(lifecycle.loc[lifecycle["Lifecycle_Status"].eq("12-24 Months"), "assets"].sum())
replacement = float(lifecycle.loc[lifecycle["Lifecycle_Status"].isin(["Past EOL", "0-6 Months", "6-12 Months", "12-24 Months"]), "replacement_cost"].sum())

c1,c2,c3,c4 = st.columns(4)
c1.metric("Past EOL", f"{past:,}", help="Assets already beyond expected lifecycle date.")
c2.metric("Due <12 Months", f"{exp12:,}", help="Assets due within the next 12 months.")
c3.metric("Due 12-24 Months", f"{exp24:,}", help="Assets due in the second year of the planning window.")
c4.metric("Near-Term Refresh Exposure", _money(replacement), help="Replacement exposure for assets past EOL or due within 24 months.")

st.divider()
col1, col2 = st.columns(2)
with col1:
    mix = lifecycle.sort_values("assets", ascending=False)
    plot_bar(mix, "Lifecycle_Status", "assets", "Lifecycle status mix")
with col2:
    top_bu = bu.sort_values("past_eol", ascending=True).tail(10)
    plot_bar(top_bu, "past_eol", "Business_Unit", "Top business units by past-EOL assets", orientation="h")

show_standard_tabs(content, df, content["file"], "Lifecycle exposure by asset type")
