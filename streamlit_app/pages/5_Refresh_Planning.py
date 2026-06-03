from pathlib import Path
import sys
import pandas as pd
import streamlit as st
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eol_ui import *
setup_page('Refresh Planning')
hero('Refresh Planning','Funding roadmap for past-support and near-end-of-life technology refresh demand.')
ref = read_csv_any(ROOT, ['refresh_budget_planning_summary.csv','refresh_forecast.csv'])
assets = ref['Assets'].sum() if not ref.empty and 'Assets' in ref.columns else None
cost = ref['Estimated_Refresh_Cost'].sum() if not ref.empty and 'Estimated_Refresh_Cost' in ref.columns else None
peak_year = ref.sort_values('Estimated_Refresh_Cost', ascending=False).iloc[0]['Refresh_Year'] if not ref.empty and {'Refresh_Year','Estimated_Refresh_Cost'}.issubset(ref.columns) else '—'
peak_cost = ref['Estimated_Refresh_Cost'].max() if not ref.empty and 'Estimated_Refresh_Cost' in ref.columns else None
cols=st.columns(4)
for col,args in zip(cols,[('REFRESH ASSETS',fmt_int(assets),'Assets in planning horizon','blue','↻'),('TOTAL INVESTMENT',fmt_money(cost),'Estimated refresh funding need','green','$'),('PEAK YEAR',str(peak_year),'Largest annual refresh demand','orange','◎'),('PEAK-YEAR COST',fmt_money(peak_cost),'Largest annual funding requirement','purple','$')]):
    with col: kpi_card(*args)
insight_box('Executive Interpretation','Refresh planning converts lifecycle exposure into a funding roadmap. This helps leaders move from reactive replacement to sequenced investment based on asset support timelines, risk concentration, and operational dependency.')

st.markdown('### Refresh Investment Roadmap')
chart_note('Shows estimated annual investment required to remediate past-support and near-end-of-life technology. This supports budget planning and funding approval discussions.')
if not ref.empty and {'Refresh_Year','Estimated_Refresh_Cost'}.issubset(ref.columns):
    d=ref.sort_values('Refresh_Year')
    fig = px.bar(d, x='Refresh_Year', y='Estimated_Refresh_Cost', text=d['Estimated_Refresh_Cost'].apply(fmt_money), labels={'Refresh_Year':'Refresh year','Estimated_Refresh_Cost':'Estimated cost'})
    fig=clean_fig(fig, height=430); fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
