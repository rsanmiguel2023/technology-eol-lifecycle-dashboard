import streamlit as st

CSS = """
<style>
.exec-banner{background:linear-gradient(135deg,#0f2440 0%,#1a3660 100%);border-left:5px solid #f0c040;border-radius:10px;padding:22px 28px;margin:10px 0 18px 0;color:#e8eaf0;line-height:1.7}.exec-banner .label{color:#f0c040;font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px}.rq-card{border:1px solid rgba(49,51,63,.18);border-radius:10px;padding:18px 20px;margin-bottom:16px;background:rgba(250,250,252,.7)}.insight-box{background:#f7f9fc;border-left:4px solid #2c5282;border-radius:8px;padding:14px 18px;margin:12px 0}.recommend-box{background:#fff8e1;border-left:4px solid #f0a500;border-radius:8px;padding:14px 18px;margin:12px 0}.tip-title{display:flex;align-items:center;margin-bottom:.4rem}.tip-title h3{margin:0;padding:0;font-size:1.28rem;font-weight:700}.tip{position:relative;display:inline-flex;align-items:center;cursor:help;margin-left:10px}.tip-icon{font-size:.9rem;color:#888}.tip-box{visibility:hidden;opacity:0;width:390px;background-color:rgba(28,28,44,.97);color:#e4e4f0;text-align:left;border-radius:8px;padding:14px 18px;font-size:.95rem;line-height:1.65;position:absolute;z-index:9999;bottom:calc(100% + 10px);left:50%;transform:translateX(-50%);transition:opacity .2s ease;box-shadow:0 6px 24px rgba(0,0,0,.45);pointer-events:none;white-space:normal}.tip-box::after{content:"";position:absolute;top:100%;left:50%;margin-left:-6px;border:6px solid transparent;border-top-color:rgba(28,28,44,.97)}.tip:hover .tip-box{visibility:visible;opacity:1}.small-muted{color:#666;font-size:.9rem}
</style>
"""

def inject_css(): st.markdown(CSS, unsafe_allow_html=True)

def tip_header(label, tooltip, level=3):
    label = str(label).replace('<','&lt;').replace('>','&gt;')
    tooltip = str(tooltip).replace('<','&lt;').replace('>','&gt;')
    st.markdown(f'<div class="tip-title"><h{level}>{label}</h{level}><span class="tip"><span class="tip-icon">ℹ️</span><span class="tip-box">{tooltip}</span></span></div>', unsafe_allow_html=True)

def exec_banner(text):
    st.markdown(f'<div class="exec-banner"><div class="label">Executive Summary — Key Finding and Implication</div>{text}</div>', unsafe_allow_html=True)

def insight(text): st.markdown(f'<div class="insight-box"><strong>Interpretation:</strong><br>{text}</div>', unsafe_allow_html=True)

def recommendation(text): st.markdown(f'<div class="recommend-box"><strong>Recommended Action:</strong><br>{text}</div>', unsafe_allow_html=True)
