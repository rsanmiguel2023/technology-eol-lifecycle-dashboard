from pathlib import Path
import sys
import pandas as pd
import streamlit as st
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eol_ui import *
setup_page('Technology Estate')
hero('Technology Estate', "Baseline view of the bank's managed technology footprint across device types, environments, and business areas.")
assets = read_csv_any(ROOT, 'asset_lifecycle_analysis.csv')
by_type = read_csv_any(ROOT, ['asset_lifecycle_by_type.csv','lifecycle_exposure_by_asset_type.csv'])

managed = len(assets) if not assets.empty else None
prod = assets[assets.get('Environment','').astype(str).str.contains('Production', case=False, na=False)].shape[0] if not assets.empty and 'Environment' in assets.columns else None
critical = assets[assets.get('Business_Unit_ID','').notna()].shape[0] if not assets.empty and 'Business_Unit_ID' in assets.columns else None
replace = assets['Replacement_Cost'].sum() if not assets.empty and 'Replacement_Cost' in assets.columns else None
cols=st.columns(4)
for col,args in zip(cols,[('MANAGED ASSETS',fmt_int(managed),'All hardware and infrastructure assets','blue','▣'),('PRODUCTION ASSETS',fmt_int(prod),'Assets supporting live environments','green','●'),('CRITICAL ASSETS',fmt_int(critical),'Assets mapped to business services','red','⚠'),('REPLACEMENT BASELINE',fmt_money(replace),'Estimated current replacement value','purple','$')]):
    with col: kpi_card(*args)
insight_box('Executive Interpretation','The estate baseline establishes the size and business dependency of the managed technology footprint before lifecycle, cyber, compliance, and refresh risk are calculated. This view helps leaders understand whether exposure is concentrated in end-user computing, infrastructure, or specific business areas.')

st.markdown('### Technology Estate by Asset Type')
chart_note('Shows how the managed estate is distributed across device and infrastructure types. This helps leaders see whether exposure is concentrated in end-user devices, servers, network infrastructure, or storage platforms.')
if not by_type.empty:
    if {'Asset_Type','Asset_Count'}.issubset(by_type.columns):
        d = by_type.groupby('Asset_Type', as_index=False)['Asset_Count'].sum().sort_values('Asset_Count', ascending=True)
        plot_bar(d, 'Asset_Count', 'Asset_Type', labels={'Asset_Count':'Assets','Asset_Type':'Asset type'})
    elif not assets.empty and 'Asset_Type' in assets.columns:
        d = assets['Asset_Type'].value_counts().rename_axis('Asset_Type').reset_index(name='Asset_Count').sort_values('Asset_Count')
        plot_bar(d, 'Asset_Count', 'Asset_Type', labels={'Asset_Count':'Assets','Asset_Type':'Asset type'})
else:
    if not assets.empty and 'Asset_Type' in assets.columns:
        d = assets['Asset_Type'].value_counts().rename_axis('Asset_Type').reset_index(name='Asset_Count').sort_values('Asset_Count')
        plot_bar(d, 'Asset_Count', 'Asset_Type', labels={'Asset_Count':'Assets','Asset_Type':'Asset type'})
    else: st.info('Asset type data is not available.')
