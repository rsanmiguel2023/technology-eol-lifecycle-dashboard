import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / 'src'))

import pandas as pd
import plotly.express as px
import streamlit as st
from utils import PROCESSED

st.set_page_config(page_title='Executive EOL', layout='wide')
st.title('Executive EOL Overview')

@st.cache_data
def load():
    return pd.read_csv(PROCESSED / 'asset_risk_model.csv', low_memory=False)

assets = load()
regions = st.multiselect('Region', sorted(assets['Region'].dropna().unique()), default=sorted(assets['Region'].dropna().unique()))
asset_types = st.multiselect('Asset Type', sorted(assets['Asset_Type'].dropna().unique()), default=sorted(assets['Asset_Type'].dropna().unique()))
filtered = assets[assets['Region'].isin(regions) & assets['Asset_Type'].isin(asset_types)]

c1, c2, c3 = st.columns(3)
c1.metric('Filtered assets', f'{len(filtered):,}')
c2.metric('Past EOL', f"{(filtered['Lifecycle_Status']=='Past EOL').sum():,}")
c3.metric('0-12 months', f"{filtered['Lifecycle_Status'].isin(['0-6 Months','6-12 Months']).sum():,}")

summary = filtered.groupby(['Asset_Type','Lifecycle_Status'], as_index=False).agg(Asset_Count=('Asset_ID','count'))
st.plotly_chart(px.bar(summary, x='Asset_Type', y='Asset_Count', color='Lifecycle_Status', barmode='stack', title='Lifecycle status by asset type'), use_container_width=True)

region = filtered.groupby(['Region','Lifecycle_Status'], as_index=False).agg(Asset_Count=('Asset_ID','count'))
st.plotly_chart(px.bar(region, x='Region', y='Asset_Count', color='Lifecycle_Status', title='Regional EOL exposure'), use_container_width=True)
