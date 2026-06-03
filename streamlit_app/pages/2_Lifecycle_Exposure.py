from pathlib import Path
import sys
import pandas as pd
import streamlit as st
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eol_ui import *
setup_page('Lifecycle Exposure')
hero('Lifecycle Exposure','Executive view of unsupported and near-end-of-life technology across business units and asset categories.')
bu = read_csv_any(ROOT, ['business_unit_eol_exposure.csv','business_unit_risk.csv'])
by_type = read_csv_any(ROOT, ['asset_lifecycle_by_type.csv','lifecycle_exposure_by_asset_type.csv'])

past = bu['Past_EOL_Assets'].sum() if not bu.empty and 'Past_EOL_Assets' in bu.columns else None
exp12 = bu['Expiring_12M_Assets'].sum() if not bu.empty and 'Expiring_12M_Assets' in bu.columns else None
cost = bu['Total_Replacement_Cost'].sum() if not bu.empty and 'Total_Replacement_Cost' in bu.columns else None
largest = bu.sort_values('Past_EOL_Assets', ascending=False).iloc[0]['Business_Unit_Name'] if not bu.empty and {'Past_EOL_Assets','Business_Unit_Name'}.issubset(bu.columns) else '—'
cols=st.columns(4)
for col,args in zip(cols,[('PAST VENDOR SUPPORT',fmt_int(past),'Assets already unsupported','red','⚠'),('12-MONTH EXPOSURE',fmt_int(exp12),'Assets entering near-term refresh','orange','↻'),('LIFECYCLE COST',fmt_money(cost),'Replacement cost in exposed estate','green','$'),('LARGEST EXPOSURE',largest,'Business unit with highest unsupported volume','purple','◎')]):
    with col: kpi_card(*args)
insight_box('Executive Interpretation','Lifecycle exposure should be managed as a portfolio risk. Unsupported assets create vendor support gaps, audit exposure, operational instability, and increased remediation complexity. The priority is to sequence refresh activity by business criticality and risk concentration rather than by device age alone.')

st.markdown('### Unsupported Assets by Business Unit')
chart_note('Ranks business units by assets already past vendor support. This helps leaders decide where refresh funding and remediation work should start.')
if not bu.empty and {'Business_Unit_Name','Past_EOL_Assets'}.issubset(bu.columns):
    d=bu.sort_values('Past_EOL_Assets', ascending=True)
    plot_bar(d,'Past_EOL_Assets','Business_Unit_Name', color='Risk_Band', labels={'Past_EOL_Assets':'Past vendor support assets','Business_Unit_Name':'Business unit'})

st.markdown('### Lifecycle Exposure by Asset Type')
chart_note('Shows which technology categories carry the largest unsupported or near-EOL footprint.')
if not by_type.empty and {'Asset_Type','Lifecycle_Status','Asset_Count'}.issubset(by_type.columns):
    d = by_type[by_type['Lifecycle_Status'].astype(str).str.contains('Past|12', case=False, na=False)].groupby('Asset_Type', as_index=False)['Asset_Count'].sum().sort_values('Asset_Count', ascending=True)
    plot_bar(d,'Asset_Count','Asset_Type',labels={'Asset_Count':'Exposed assets','Asset_Type':'Asset type'}, height=380)
