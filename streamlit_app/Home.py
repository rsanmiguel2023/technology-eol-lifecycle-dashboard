from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from eol_ui import *

setup_page('Executive Summary')
hero('Technology Lifecycle Governance Dashboard', 'Executive technology risk and refresh planning overview for Maple Financial Bank. This view summarizes lifecycle exposure, cybersecurity concentration, software compliance risk, funding requirements, operational impact, and remediation progress.')

q = read_csv_any(ROOT, 'executive_questions_summary.csv')
bu = read_csv_any(ROOT, ['risk_heatmap_business_unit.csv', 'business_unit_eol_exposure.csv', 'business_unit_risk.csv'])
op = read_csv_any(ROOT, ['operational_impact_by_lifecycle_status.csv', 'operational_risk_analysis.csv'])
rem_summary = read_csv_any(ROOT, 'remediation_progress_summary.csv')
rem_status = read_csv_any(ROOT, 'remediation_progress_by_status.csv')
rem_bu = read_csv_any(ROOT, 'remediation_progress_by_business_unit.csv')


def qval(contains, default='—'):
    if not q.empty:
        cols = list(q.columns)
        text_col = cols[0]
        val_col = cols[-1]
        m = q[q[text_col].astype(str).str.contains(contains, case=False, na=False)]
        if not m.empty:
            return str(m.iloc[0][val_col])
    return default


def summary_value(metric_name, default='—'):
    if rem_summary.empty:
        return default
    if {'Metric', 'Display_Value'}.issubset(rem_summary.columns):
        m = rem_summary[rem_summary['Metric'].astype(str).str.contains(metric_name, case=False, na=False)]
        if not m.empty:
            return str(m.iloc[0]['Display_Value'])
    return default


managed = qval('managed|total', '23,770')
past = qval('past vendor|past eol|already past', '4,682')
exp12 = qval('12', '8,337')
refresh_cost_raw = qval('refresh cost|investment', '70816400')

try:
    refresh_cost_num = float(
        str(refresh_cost_raw)
        .replace('CAD', '')
        .replace('$', '')
        .replace(',', '')
        .replace('M', '')
        .strip()
    )

    # if already in millions
    if refresh_cost_num < 1000:
        refresh_cost = f"CAD ${refresh_cost_num:.1f}M"
    else:
        refresh_cost = f"CAD ${refresh_cost_num/1_000_000:.1f}M"

except:
    refresh_cost = "CAD $70.8M"
cyber = qval('critical|vulnerab', '1,391')
software = qval('software', '91,618')
rem_completed = summary_value('Completed Percent', '—')
rem_in_progress = summary_value('In Progress Percent', '—')

past_down = '129,119'
if not op.empty and 'Lifecycle_Status' in op.columns and 'Downtime_Hours' in op.columns:
    m = op[op['Lifecycle_Status'].astype(str).str.contains('Past', case=False, na=False)]
    if not m.empty:
        past_down = fmt_int(m['Downtime_Hours'].sum())

high_area = 'Retail Banking'
if not bu.empty and 'Executive_Risk_Index' in bu.columns and 'Business_Unit_Name' in bu.columns:
    high_area = str(bu.sort_values('Executive_Risk_Index', ascending=False).iloc[0]['Business_Unit_Name'])

rows = [
    [
        ('MANAGED ASSETS', managed, 'Scope of the technology estate', 'blue', '▣'),
        ('PAST VENDOR SUPPORT', past, 'Unsupported assets requiring governance', 'red', '⚠'),
        ('12-MONTH REFRESH DEMAND', exp12, 'Assets entering near-term refresh window', 'orange', '↻'),
        ('ESTIMATED REFRESH COST', refresh_cost, 'Past and near-EOL investment need', 'green', '$'),
    ],
    [
        ('CYBER EXPOSURE', cyber, 'Unsupported assets with critical or high findings', 'red', '△'),
        ('UNSUPPORTED SOFTWARE', software, 'Installations requiring compliance review', 'blue', '▣'),
        ('PAST-EOL DOWNTIME', past_down, 'Operational disruption linked to unsupported assets', 'orange', '◴'),
        ('HIGHEST-RISK AREA', high_area, 'Business unit requiring first executive focus', 'purple', '◎'),
    ],
    [
        ('REMEDIATION COMPLETE', rem_completed, 'Share of eligible exposure already remediated', 'green', '✓'),
        ('REMEDIATION IN PROGRESS', rem_in_progress, 'Work actively moving through delivery teams', 'blue', '↻'),
    ],
]

for row in rows[:2]:
    cols = st.columns(4)
    for col, (label, value, cap, tone, icon) in zip(cols, row):
        with col:
            kpi_card(label, value, cap, tone, icon)

# Keep the remediation KPIs visually distinct and narrower so the page does not feel overloaded.
rem_cols = st.columns([1, 1, 2])
for col, (label, value, cap, tone, icon) in zip(rem_cols[:2], rows[2]):
    with col:
        kpi_card(label, value, cap, tone, icon)
with rem_cols[2]:
    insight_box('Governance signal', 'Remediation progress shows whether lifecycle exposure is being reduced, not just measured. Mature EOL programs are judged by how quickly exposure moves from not started to in progress to completed.')

insight_box('Executive Summary', 'Maple Financial Bank maintains a managed technology estate across end-user computing, infrastructure, network, cloud, and enterprise application environments. The current lifecycle assessment identifies unsupported assets, near-term refresh demand, cybersecurity exposure, software compliance risk, operational disruption, and remediation execution progress that require coordinated governance rather than one-time hardware replacement.')

col1, col2 = st.columns([1.05, 1])
with col1:
    st.markdown('### Key Decision Points')
    st.markdown('''
- Prioritize unsupported assets with critical and high vulnerabilities.
- Approve a phased refresh roadmap instead of funding replacements reactively.
- Use business-unit risk ranking to sequence remediation and funding.
- Reduce unsupported software in parallel with hardware refresh.
- Track remediation progress monthly so exposure reduction is visible to leadership.
''')

with col2:
    st.markdown('### Remediation Progress')
    chart_note('Shows how much of the lifecycle exposure has already been remediated, how much is actively moving, and how much has not yet started. This helps leadership understand whether risk is decreasing fast enough.')
    if not rem_status.empty and {'Remediation_Progress_Group', 'Asset_Count'}.issubset(rem_status.columns):
        colors = {
            'Completed': '#16A34A',
            'In Progress': '#2563EB',
            'Not Started': '#EA580C',
            'Deferred / Exception': '#64748B',
        }
        fig = px.pie(
            rem_status,
            values='Asset_Count',
            names='Remediation_Progress_Group',
            hole=0.56,
            color='Remediation_Progress_Group',
            color_discrete_map=colors,
        )
        fig = clean_fig(fig, height=330)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info('Run `python src/09_generate_remediation_progress.py` to generate remediation progress reporting.')

st.markdown('### Highest-Risk Business Units')
chart_note('Ranks business units by combined lifecycle exposure, cyber risk, downtime, and replacement cost. This helps prioritize funding and remediation sequencing.')
if not bu.empty and {'Business_Unit_Name', 'Executive_Risk_Index'}.issubset(bu.columns):
    d = bu.sort_values('Executive_Risk_Index', ascending=True).tail(8)
    plot_bar(d, x='Executive_Risk_Index', y='Business_Unit_Name', orientation='h', color='Risk_Band', labels={'Executive_Risk_Index': 'Risk index', 'Business_Unit_Name': 'Business unit'}, height=360)
else:
    st.info('Risk ranking data is not available.')

if not rem_bu.empty and {'Business_Unit_Name', 'Asset_Count', 'Remediation_Progress_Group'}.issubset(rem_bu.columns):
    st.markdown('### Remediation Progress by Business Unit')
    chart_note('Shows whether remediation is moving evenly across business units or whether high-risk areas are falling behind.')
    # Show top business units by remediation population.
    top_units = rem_bu.groupby('Business_Unit_Name', as_index=False)['Asset_Count'].sum().sort_values('Asset_Count', ascending=False).head(8)['Business_Unit_Name']
    d = rem_bu[rem_bu['Business_Unit_Name'].isin(top_units)]
    fig = px.bar(d, x='Asset_Count', y='Business_Unit_Name', color='Remediation_Progress_Group', orientation='h', labels={'Asset_Count': 'Assets', 'Business_Unit_Name': 'Business unit', 'Remediation_Progress_Group': 'Status'})
    fig = clean_fig(fig, height=420)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
