from streamlit_app.business_page import *
content = page_header("recommendations", "🎯")
df = _read_report("recommendation_actions.csv")
questions = _read_report("executive_questions_summary.csv")

c1,c2,c3,c4 = st.columns(4)
c1.metric("Priority Actions", f"{len(df):,}", help=content["tooltip"])
c2.metric("Immediate Actions", f"{(df['timeframe'].str.contains('0-90|30-60', case=False, na=False)).sum():,}", help="Actions with immediate or near-term target windows.")
c3.metric("Executive Questions Answered", f"{len(questions):,}", help="Management questions supported by exported reports.")
c4.metric("Governance Mode", "Quarterly", help="Recommended executive review cadence.")

st.divider()
for _, row in df.sort_values("priority").iterrows():
    st.markdown(f"<div class='priority-card'><div class='priority-title'>Priority {int(row['priority'])}: {row['action']}</div><p>{row['rationale']}</p><p><strong>Owner:</strong> {row['owner']}<br><strong>Timeframe:</strong> {row['timeframe']}<br><strong>Expected outcome:</strong> {row['expected_outcome']}</p></div>", unsafe_allow_html=True)

st.divider()
show_standard_tabs(content, df, content["file"], "Recommendation action plan")
