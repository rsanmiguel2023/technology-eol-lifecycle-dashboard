import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / 'src'))

import pandas as pd
import plotly.express as px
import streamlit as st
from utils import RAW, PROCESSED

st.set_page_config(page_title='Budget and Refresh', layout='wide')
st.title('Budget and Refresh Planning')

@st.cache_data
def load():
    assets = pd.read_csv(PROCESSED / 'asset_risk_model.csv', low_memory=False)
    budget = pd.read_csv(RAW / 'budget_costs.csv')
    refresh = pd.read_csv(RAW / 'refresh_projects.csv')
    return assets, budget, refresh

assets, budget, refresh = load()

st.plotly_chart(px.line(budget, x='Year', y=['Maintenance_Cost','Support_Cost','Replacement_Cost_CAD','Budget_Allocated'], color='Asset_Category', title='Technology budget forecast by category'), use_container_width=True)

refresh_summary = refresh.groupby(['Refresh_Year','Status'], as_index=False).agg(Project_Count=('Project_ID','count'), Budget=('Budget','sum'))
st.plotly_chart(px.bar(refresh_summary, x='Refresh_Year', y='Budget', color='Status', title='Refresh project budget by year and status'), use_container_width=True)

past_eol = assets[assets['Lifecycle_Status'].isin(['Past EOL','0-6 Months','6-12 Months'])]
st.subheader('Replacement candidates')
st.dataframe(past_eol.sort_values('Risk_Score', ascending=False)[['Asset_ID','Asset_Type','Manufacturer','Model','Region','Business_Unit','Lifecycle_Status','Risk_Score','Replacement_Cost_CAD']].head(200), use_container_width=True, hide_index=True)
