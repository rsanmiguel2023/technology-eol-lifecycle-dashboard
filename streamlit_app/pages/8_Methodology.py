
from pathlib import Path
import pandas as pd
import streamlit as st
ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / 'docs'
REPORTS = ROOT / 'outputs' / 'reports'
st.set_page_config(page_title='Methodology', layout='wide')
st.title('Methodology')
doc = DOCS / 'methodology.md'
if doc.exists(): st.markdown(doc.read_text(encoding='utf-8'))
st.divider()
for file_name in ['data_quality_summary.csv', 'data_cleaning_summary.csv']:
    p = REPORTS / file_name
    if p.exists():
        st.subheader(file_name.replace('_',' ').replace('.csv','').title())
        st.dataframe(pd.read_csv(p), use_container_width=True)
