from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eol_ui import *

setup_page('Recommendations')
hero('Recommendations', 'Prioritized actions for reducing lifecycle, cyber, compliance, refresh, and operational exposure.')

rec = read_csv_any(ROOT, 'recommendation_actions.csv')
rem_status = read_csv_any(ROOT, 'remediation_progress_by_status.csv')
rem_summary = read_csv_any(ROOT, 'remediation_progress_summary.csv')

completed = '—'
in_progress = '—'
not_started = '—'
if not rem_summary.empty and {'Metric','Display_Value'}.issubset(rem_summary.columns):
    def mval(label):
        m = rem_summary[rem_summary['Metric'].astype(str).str.contains(label, case=False, na=False)]
        return str(m.iloc[0]['Display_Value']) if not m.empty else '—'
    completed = mval('Completed Percent')
    in_progress = mval('In Progress Percent')
    not_started = mval('Not Started Percent')

cols = st.columns(3)
for col, args in zip(cols, [
    ('COMPLETED', completed, 'Exposure already remediated', 'green', '✓'),
    ('IN PROGRESS', in_progress, 'Work moving through delivery teams', 'blue', '↻'),
    ('NOT STARTED', not_started, 'Exposure requiring delivery start', 'orange', '!'),
]):
    with col:
        kpi_card(*args)

insight_box('Executive Interpretation', 'Recommendations should be sequenced by risk reduction and delivery progress. The dashboard should not only identify exposure; it should show whether exposure is actively being reduced through funded remediation work.')

if not rem_status.empty and {'Remediation_Progress_Group','Asset_Count'}.issubset(rem_status.columns):
    st.markdown('### Remediation Progress')
    chart_note('Shows whether the lifecycle remediation program is reducing exposure or whether too much work remains not started or deferred.')
    fig = px.bar(rem_status, x='Remediation_Progress_Group', y='Asset_Count', text='Progress_Pct', labels={'Remediation_Progress_Group':'Status','Asset_Count':'Assets'})
    fig = clean_fig(fig, height=360)
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
else:
    st.info('Run `python src/09_generate_remediation_progress.py` to generate remediation progress reporting.')

st.markdown('### Recommended Actions')
if not rec.empty:
    for i, row in rec.iterrows():
        title = row.get('Recommendation', row.get('Action', row.get('Recommended_Action', f'Action {i+1}')))
        owner = row.get('Owner', row.get('Accountable_Owner', 'Technology Governance'))
        timeline = row.get('Timeframe', row.get('Timeline', 'Near term'))
        priority = row.get('Priority', f'Priority {i+1}')
        rationale = row.get('Rationale', row.get('Business_Rationale', 'Reduces lifecycle risk exposure and improves governance visibility.'))
        st.markdown(f"""
<div class="insight-card">
  <h3>{priority}: {title}</h3>
  <div class="accent-line"></div>
  <p><b>Owner:</b> {owner}<br><b>Timeframe:</b> {timeline}</p>
  <p>{rationale}</p>
</div>
""", unsafe_allow_html=True)
else:
    st.info('Recommendation action data is not available.')
