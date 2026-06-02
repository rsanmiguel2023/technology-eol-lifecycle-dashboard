from streamlit_app.business_page import *
content = page_header("refresh_planning", "💰")
df = _read_report("refresh_budget_planning_summary.csv")
gap = _read_report("refresh_budget_gap_summary.csv")

assets = int(df["assets"].sum())
need = float(df["estimated_replacement_cost"].sum())
allocated = float(gap["budget_allocated"].sum()) if "budget_allocated" in gap.columns else 0
gap_total = float(gap["funding_gap"].sum()) if "funding_gap" in gap.columns else need

c1,c2,c3,c4 = st.columns(4)
c1.metric("Assets in Refresh Scope", f"{assets:,}", help="Assets past EOL or due within 24 months.")
c2.metric("Estimated Refresh Need", _money(need), help=content["tooltip"])
c3.metric("Budget Allocated", _money(allocated), help="Available budget from the synthetic budget planning table.")
c4.metric("Funding Gap", _money(gap_total), help="Estimated refresh need minus allocated budget.")

st.divider()
col1, col2 = st.columns(2)
with col1:
    win = df.groupby("Refresh_Window").agg(estimated_replacement_cost=("estimated_replacement_cost", "sum")).reset_index()
    plot_bar(win, "Refresh_Window", "estimated_replacement_cost", "Refresh need by planning window")
with col2:
    year = gap.sort_values("EOL_Year")
    plot_bar(year, "EOL_Year", "estimated_replacement_cost", "Estimated refresh cost by year")

show_standard_tabs(content, df, content["file"], "Refresh budget planning summary")
