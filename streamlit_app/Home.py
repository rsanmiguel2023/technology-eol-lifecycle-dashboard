import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

import pandas as pd
import plotly.express as px
import streamlit as st
from utils import PROCESSED

st.set_page_config(page_title='Technology EOL Dashboard', layout='wide')
st.title('Technology EOL Lifecycle Dashboard')
st.caption('Synthetic banking dataset for Senior Analyst Technology EOL portfolio project')

@st.cache_data
def load_assets():
    return pd.read_csv(PROCESSED / 'asset_risk_model.csv', low_memory=False)

assets = load_assets()

c1, c2, c3, c4 = st.columns(4)
c1.metric('Total assets', f'{len(assets):,}')
c2.metric('Past EOL assets', f"{(assets['Lifecycle_Status']=='Past EOL').sum():,}")
c3.metric('Critical risk assets', f"{(assets['Risk_Band']=='Critical').sum():,}")
c4.metric('Replacement cost', f"${assets['Replacement_Cost_CAD'].sum()/1_000_000:.1f}M")

left, right = st.columns(2)
with left:
    eol = assets.groupby('Lifecycle_Status', as_index=False)['Asset_ID'].count().rename(columns={'Asset_ID':'Asset Count'})
    st.plotly_chart(px.bar(eol, x='Lifecycle_Status', y='Asset Count', title='Assets by lifecycle status'), use_container_width=True)
with right:
    risk = assets.groupby('Risk_Band', as_index=False)['Asset_ID'].count().rename(columns={'Asset_ID':'Asset Count'})
    st.plotly_chart(px.pie(risk, names='Risk_Band', values='Asset Count', title='Risk band distribution'), use_container_width=True)

st.subheader('Highest risk assets')
st.dataframe(
    assets.sort_values('Risk_Score', ascending=False)[['Asset_ID','Asset_Name','Asset_Type','Manufacturer','Model','Region','Criticality','Lifecycle_Status','Risk_Score','Replacement_Cost_CAD']].head(50),
    use_container_width=True,
    hide_index=True
)
