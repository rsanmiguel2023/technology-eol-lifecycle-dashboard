import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / 'src'))

import pandas as pd
import plotly.express as px
import streamlit as st
from utils import PROCESSED

st.set_page_config(page_title='Software EOL', layout='wide')
st.title('Software EOL Dashboard')

@st.cache_data
def load():
    return pd.read_csv(PROCESSED / 'software_installations_model.csv', low_memory=False)

software = load()
status = st.multiselect('Lifecycle Status', sorted(software['Software_Lifecycle_Status'].dropna().unique()), default=sorted(software['Software_Lifecycle_Status'].dropna().unique()))
filtered = software[software['Software_Lifecycle_Status'].isin(status)]

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric('Installations', f'{len(filtered):,}')
kpi2.metric('Past EOL installs', f"{(filtered['Software_Lifecycle_Status']=='Past EOL').sum():,}")
kpi3.metric('Unique software titles', f"{filtered['Software_Name'].nunique():,}")

top = filtered.groupby(['Software_Name','Software_Lifecycle_Status'], as_index=False).agg(Installations=('Install_ID','count'))
top10 = top.groupby('Software_Name')['Installations'].sum().sort_values(ascending=False).head(15).index
top = top[top['Software_Name'].isin(top10)]
st.plotly_chart(px.bar(top, x='Installations', y='Software_Name', color='Software_Lifecycle_Status', orientation='h', title='Top software exposure by installation count'), use_container_width=True)

st.dataframe(filtered[['Install_ID','Asset_ID','Software_Name','Version','Vendor','Software_EOL_Date','Software_Lifecycle_Status','Risk_Rating']].head(500), use_container_width=True, hide_index=True)
