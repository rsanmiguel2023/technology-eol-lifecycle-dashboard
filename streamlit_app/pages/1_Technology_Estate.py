from streamlit_app.business_page import *
content = page_header("technology_estate", "🏢")
df = _read_report("technology_estate_summary.csv")
assets = load_assets()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Assets in Scope", _num(df["assets"].sum()), help=content["tooltip"])
c2.metric("Production Assets", _num(df["production_assets"].sum()), help="Assets marked as production in the model.")
c3.metric("Critical Assets", _num(df["critical_assets"].sum()), help="Assets tagged as critical to business or technology operations.")
c4.metric("Replacement Exposure", _money(df["replacement_cost"].sum()), help="Estimated replacement value of the estate in scope.")

st.divider()
col1, col2 = st.columns(2)
with col1:
    estate = df.groupby("Asset_Type").agg(assets=("assets", "sum")).reset_index().sort_values("assets", ascending=True)
    plot_bar(estate, "assets", "Asset_Type", "Technology estate composition", orientation="h")
with col2:
    env = assets.groupby("Environment").size().reset_index(name="assets").sort_values("assets", ascending=False)
    plot_bar(env, "Environment", "assets", "Assets by environment")

show_standard_tabs(content, df, content["file"], "Technology estate summary")
