from pathlib import Path
import sys
import pandas as pd
import streamlit as st
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eol_ui import *
setup_page('Cybersecurity Risk')
hero('Cybersecurity Risk','View of unsupported and near-EOL assets with critical or high vulnerability exposure.')
cyber = read_csv_any(ROOT, ['cybersecurity_unsupported_critical_summary.csv','cyber_risk_analysis.csv'])
asset_detail = read_csv_any(ROOT, 'cyber_risk_analysis.csv')
if 'Asset_Count' in cyber.columns:
    exposed = cyber['Asset_Count'].sum(); crit = cyber.get('Critical_Vulnerabilities', pd.Series(dtype=float)).sum(); high = cyber.get('High_Vulnerabilities', pd.Series(dtype=float)).sum()
else:
    exposed = len(cyber); crit = cyber.get('Critical_Vulnerability_Count', pd.Series(dtype=float)).sum(); high = cyber.get('High_Vulnerability_Count', pd.Series(dtype=float)).sum()
cost = asset_detail['Replacement_Cost'].sum() if not asset_detail.empty and 'Replacement_Cost' in asset_detail.columns else None
cols=st.columns(4)
for col,args in zip(cols,[('EXPOSED ASSETS',fmt_int(exposed),'Unsupported assets with cyber exposure','red','△'),('CRITICAL FINDINGS',fmt_int(crit),'Critical vulnerability count','red','!'),('HIGH FINDINGS',fmt_int(high),'High severity vulnerability count','orange','▲'),('REPLACEMENT EXPOSURE',fmt_money(cost),'Cost tied to exposed assets','green','$')]):
    with col: kpi_card(*args)
insight_box('Executive Interpretation','Cybersecurity exposure is most urgent when unsupported assets also carry critical or high vulnerabilities. These systems have a smaller remediation window, weaker vendor support options, and higher operational risk if compensating controls are not in place.')

st.markdown('### Unsupported Vulnerable Assets by Asset Type')
chart_note('Shows which technology platforms combine lifecycle risk with vulnerability exposure. This helps teams focus patching, compensating controls, and accelerated replacement work.')
if not cyber.empty:
    if {'Asset_Type','Asset_Count'}.issubset(cyber.columns):
        d=cyber.groupby('Asset_Type', as_index=False)['Asset_Count'].sum().sort_values('Asset_Count', ascending=True)
        plot_bar(d,'Asset_Count','Asset_Type',labels={'Asset_Count':'Exposed assets','Asset_Type':'Asset type'})
    elif {'Asset_Type','Asset_ID'}.issubset(cyber.columns):
        d=cyber.groupby('Asset_Type', as_index=False)['Asset_ID'].count().rename(columns={'Asset_ID':'Asset_Count'}).sort_values('Asset_Count')
        plot_bar(d,'Asset_Count','Asset_Type',labels={'Asset_Count':'Exposed assets','Asset_Type':'Asset type'})

if not asset_detail.empty and 'Business_Unit_ID' in asset_detail.columns:
    st.markdown('### Cyber Exposure by Business Unit ID')
    chart_note('Groups exposed assets by business unit identifier when the business unit name is not present in the vulnerability export.')
    d=asset_detail.groupby('Business_Unit_ID', as_index=False).agg(Asset_Count=('Asset_ID','count'), Critical=('Critical_Vulnerability_Count','sum')).sort_values('Asset_Count', ascending=True)
    plot_bar(d,'Asset_Count','Business_Unit_ID',labels={'Asset_Count':'Exposed assets','Business_Unit_ID':'Business unit ID'}, height=360)
