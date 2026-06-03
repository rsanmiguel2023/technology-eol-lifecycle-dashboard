from pathlib import Path
import sys
import pandas as pd
import streamlit as st
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eol_ui import *
setup_page('Operational Impact')
hero('Operational Impact','Incident and downtime view showing how lifecycle status relates to operational disruption.')
op = read_csv_any(ROOT, ['operational_impact_by_lifecycle_status.csv','operational_risk_analysis.csv'])
inc = op['Incident_Count'].sum() if not op.empty and 'Incident_Count' in op.columns else None
down = op['Downtime_Hours'].sum() if not op.empty and 'Downtime_Hours' in op.columns else None
past_down = None
if not op.empty and {'Lifecycle_Status','Downtime_Hours'}.issubset(op.columns):
    m=op[op['Lifecycle_Status'].astype(str).str.contains('Past',case=False,na=False)]
    past_down=m['Downtime_Hours'].sum() if not m.empty else None
max_status = op.sort_values('Operational_Disruption_Index', ascending=False).iloc[0]['Lifecycle_Status'] if not op.empty and 'Operational_Disruption_Index' in op.columns else '—'
cols=st.columns(4)
for col,args in zip(cols,[('TOTAL INCIDENTS',fmt_int(inc),'Events linked to technology estate','blue','!'),('TOTAL DOWNTIME',fmt_int(down),'Hours of operational disruption','orange','◴'),('PAST-EOL DOWNTIME',fmt_int(past_down),'Downtime tied to unsupported assets','red','⚠'),('HIGHEST IMPACT STATUS',max_status,'Lifecycle group with highest disruption index','purple','◎')]):
    with col: kpi_card(*args)
insight_box('Executive Interpretation','Operational impact connects lifecycle exposure to service disruption. Unsupported and near-EOL assets increase support complexity and may require more frequent intervention, creating a measurable operational risk signal for governance and refresh prioritization.')

st.markdown('### Operational Disruption by Lifecycle Status')
chart_note('Compares incident and downtime impact across lifecycle groups. This helps executives understand whether older assets are creating a measurable operational burden.')
if not op.empty and {'Lifecycle_Status','Operational_Disruption_Index'}.issubset(op.columns):
    d=op.sort_values('Operational_Disruption_Index', ascending=True)
    plot_bar(d,'Operational_Disruption_Index','Lifecycle_Status',labels={'Operational_Disruption_Index':'Disruption index','Lifecycle_Status':'Lifecycle status'}, height=390)
