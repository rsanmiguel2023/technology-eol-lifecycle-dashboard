import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / 'src'))

import pandas as pd
import plotly.express as px
import streamlit as st
from utils import PROCESSED

st.set_page_config(page_title='Risk and Vulnerabilities', layout='wide')
st.title('Risk and Vulnerability Dashboard')

@st.cache_data
def load():
    return pd.read_csv(PROCESSED / 'asset_risk_model.csv', low_memory=False)

assets = load()

scatter = assets.sample(min(5000, len(assets)), random_state=42)
st.plotly_chart(px.scatter(scatter, x='Age_Years', y='Risk_Score', color='Lifecycle_Status', size='Vulnerability_Count', hover_data=['Asset_ID','Asset_Type','Criticality'], title='Asset age vs risk score'), use_container_width=True)

risk_region = assets.groupby(['Region','Risk_Band'], as_index=False).agg(Asset_Count=('Asset_ID','count'))
st.plotly_chart(px.bar(risk_region, x='Region', y='Asset_Count', color='Risk_Band', title='Risk band by region'), use_container_width=True)

st.subheader('Critical vulnerability exposure')
st.dataframe(assets.sort_values(['Critical_Vuln_Count','Risk_Score'], ascending=False)[['Asset_ID','Asset_Type','Manufacturer','Model','Region','Criticality','Lifecycle_Status','Critical_Vuln_Count','High_Vuln_Count','Risk_Score']].head(100), use_container_width=True, hide_index=True)
