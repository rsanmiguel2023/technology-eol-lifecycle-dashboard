import html
import streamlit as st

CSS = """
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2.5rem; max-width: 1500px;}
[data-testid="stSidebarNav"] ul {padding-top: .5rem;}
.exec-banner{background:linear-gradient(135deg,#0f2440 0%,#1a3660 100%);border-left:6px solid #f0c040;border-radius:12px;padding:22px 28px;margin:12px 0 22px 0;color:#e8eaf0;line-height:1.75}.exec-banner .label{color:#f0c040;font-size:.78rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px}.question-strip{background:#f7f9fc;border:1px solid rgba(49,51,63,.12);border-radius:12px;padding:16px 20px;margin:10px 0 18px 0}.question-strip .label{font-size:.74rem;font-weight:800;color:#4b5563;letter-spacing:.10em;text-transform:uppercase;margin-bottom:5px}.question-strip .text{font-size:1.05rem;font-weight:650;color:#111827;line-height:1.55}.insight-box{background:#f4f8ff;border-left:5px solid #1565c0;border-radius:10px;padding:15px 18px;margin:12px 0;line-height:1.65}.recommend-box{background:#fff8e1;border-left:5px solid #f0a500;border-radius:10px;padding:15px 18px;margin:12px 0;line-height:1.65}.risk-box{background:#fff5f5;border-left:5px solid #c62828;border-radius:10px;padding:15px 18px;margin:12px 0;line-height:1.65}.tip-title{display:flex;align-items:center;margin-bottom:.4rem}.tip-title h2{margin:0;padding:0;font-size:1.45rem;font-weight:750}.tip-title h3{margin:0;padding:0;font-size:1.24rem;font-weight:700}.tip{position:relative;display:inline-flex;align-items:center;cursor:help;margin-left:10px}.tip-icon{font-size:.9rem;color:#777}.tip-box{visibility:hidden;opacity:0;width:430px;background-color:rgba(28,28,44,.98);color:#e4e4f0;text-align:left;border-radius:8px;padding:14px 18px;font-size:.93rem;line-height:1.6;position:absolute;z-index:9999;bottom:calc(100% + 10px);left:50%;transform:translateX(-50%);transition:opacity .2s ease;box-shadow:0 6px 24px rgba(0,0,0,.45);pointer-events:none;white-space:normal}.tip-box::after{content:"";position:absolute;top:100%;left:50%;margin-left:-6px;border:6px solid transparent;border-top-color:rgba(28,28,44,.98)}.tip:hover .tip-box{visibility:visible;opacity:1}.small-muted{color:#5f6368;font-size:.9rem;line-height:1.5}.priority-card{border:1px solid rgba(49,51,63,.14);border-radius:12px;padding:15px 18px;margin:10px 0;background:#ffffff}.priority-title{font-weight:800;color:#0f2440;margin-bottom:6px}.footer-note{font-size:.86rem;color:#5f6368;margin-top:8px;}
</style>
"""

def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)

def _clean(text):
    return html.escape(str(text or ""))

def tip_header(label, tooltip, level=3):
    st.markdown(
        f'<div class="tip-title"><h{level}>{_clean(label)}</h{level}><span class="tip"><span class="tip-icon">ℹ️</span><span class="tip-box">{_clean(tooltip)}</span></span></div>',
        unsafe_allow_html=True,
    )

def exec_banner(text, label="Executive Summary — Management View"):
    st.markdown(f'<div class="exec-banner"><div class="label">{_clean(label)}</div>{text}</div>', unsafe_allow_html=True)

def management_question(text):
    st.markdown(f'<div class="question-strip"><div class="label">Management Question</div><div class="text">{_clean(text)}</div></div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box"><strong>Business interpretation:</strong><br>{text}</div>', unsafe_allow_html=True)

def recommendation(text):
    st.markdown(f'<div class="recommend-box"><strong>Recommended action:</strong><br>{text}</div>', unsafe_allow_html=True)

def risk_note(text):
    st.markdown(f'<div class="risk-box"><strong>Risk note:</strong><br>{text}</div>', unsafe_allow_html=True)
