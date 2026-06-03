from pathlib import Path
import sys
import pandas as pd
import streamlit as st
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eol_ui import *
setup_page('Compliance Risk')
hero('Compliance Risk','Software lifecycle compliance view for unsupported and high-risk software versions.')
soft = read_csv_any(ROOT, ['software_compliance_risk_summary.csv','software_lifecycle_analysis.csv'])
unsupported = None; high = None
if not soft.empty:
    if 'Installation_Count' in soft.columns: unsupported = soft['Installation_Count'].sum()
    else: unsupported = len(soft[soft.get('Software_EOL_Status','').astype(str).str.contains('Unsupported', case=False, na=False)]) if 'Software_EOL_Status' in soft.columns else len(soft)
    high = soft[soft.get('Software_Compliance_Risk','').astype(str).str.contains('High', case=False, na=False)].shape[0] if 'Software_Compliance_Risk' in soft.columns else None
cols=st.columns(4)
for col,args in zip(cols,[('UNSUPPORTED INSTALLS',fmt_int(unsupported),'Software installs requiring review','orange','▣'),('HIGH-RISK VERSIONS',fmt_int(high),'Version-level compliance exposure','red','!'),('PRIMARY DRIVER','Adobe Acrobat Pro 2020','Largest unsupported deployment group','blue','◎'),('ACTION TYPE','Version Retirement','Standardize supported software versions','green','✓')]):
    with col: kpi_card(*args)
insight_box('Executive Interpretation','Software compliance risk is driven by version-level support timelines. The same product can have supported and unsupported versions, so remediation should focus on high-volume unsupported versions and applications with business-critical usage.')

st.markdown('### Unsupported Software Versions')
chart_note('Breaks down compliance exposure at the version level. This matters because different versions of the same product can have very different support timelines and remediation plans.')
if not soft.empty:
    if {'Software_Name','Software_Version','Installation_Count'}.issubset(soft.columns):
        d=soft.copy(); d['Software Version']=d['Software_Name'].astype(str)+' '+d['Software_Version'].astype(str); d=d.groupby('Software Version', as_index=False)['Installation_Count'].sum().sort_values('Installation_Count', ascending=True).tail(15)
        plot_bar(d,'Installation_Count','Software Version',labels={'Installation_Count':'Installations','Software Version':'Software version'}, height=520)
    elif {'Software_Name','Software_Version'}.issubset(soft.columns):
        d=soft.copy(); d['Software Version']=d['Software_Name'].astype(str)+' '+d['Software_Version'].astype(str); d=d['Software Version'].value_counts().rename_axis('Software Version').reset_index(name='Installation_Count').sort_values('Installation_Count', ascending=True).tail(15)
        plot_bar(d,'Installation_Count','Software Version',labels={'Installation_Count':'Installations','Software Version':'Software version'}, height=520)
