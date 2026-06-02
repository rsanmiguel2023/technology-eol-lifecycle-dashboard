
import streamlit as st

EXECUTIVE_CSS = """
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
.exec-banner {
    background: linear-gradient(135deg, #0f2440 0%, #1a3660 100%);
    border-left: 5px solid #f0c040;
    border-radius: 12px;
    padding: 22px 28px;
    margin: 12px 0 22px 0;
}
.exec-label {color:#f0c040; font-size:0.78rem; font-weight:800; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:10px;}
.exec-text {color:#e8eaf0; font-size:1.02rem; line-height:1.75; margin:0;}
.question-card {
    border:1px solid rgba(49,51,63,.16); border-radius:12px; padding:16px 18px; margin-bottom:12px;
    background: rgba(250,250,252,.65);
}
.question-title {font-weight:800; font-size:1.05rem; margin-bottom:6px; color:#0f2440;}
.question-text {font-size:.98rem; line-height:1.55; color:#30343b; margin:0;}
.recommendation-card {
    border-left:5px solid #2e7d32; background:#f3fbf5; border-radius:10px; padding:16px 18px; margin:10px 0;
}
.risk-card {
    border-left:5px solid #c62828; background:#fff5f5; border-radius:10px; padding:16px 18px; margin:10px 0;
}
.note-card {
    border-left:5px solid #1565c0; background:#f4f8ff; border-radius:10px; padding:16px 18px; margin:10px 0;
}
.tip-title {display:flex; align-items:center; margin-bottom:0.4rem;}
.tip-title h2 {margin:0; padding:0; font-size:1.5rem; font-weight:750; letter-spacing:-0.01em;}
.tip-title h3 {margin:0; padding:0; font-size:1.25rem; font-weight:700; letter-spacing:-0.01em;}
.tip {position:relative; display:inline-flex; align-items:center; cursor:help; margin-left:10px; flex-shrink:0;}
.tip-icon {font-size:.9rem; color:#777; user-select:none;}
.tip-box {
    visibility:hidden; opacity:0; width:420px; background-color:rgba(28,28,44,.98); color:#e4e4f0;
    text-align:left; border-radius:8px; padding:14px 18px; font-size:.92rem; line-height:1.6;
    position:absolute; z-index:9999; bottom:calc(100% + 10px); left:50%; transform:translateX(-50%);
    transition:opacity .2s ease; box-shadow:0 6px 24px rgba(0,0,0,.45); pointer-events:none; white-space:normal;
}
.tip-box::after {content:""; position:absolute; top:100%; left:50%; margin-left:-6px; border:6px solid transparent; border-top-color:rgba(28,28,44,.98);}
.tip:hover .tip-box {visibility:visible; opacity:1;}
.step-badge {background:#f0f4ff; border-radius:6px; padding:8px 14px; margin-bottom:8px; font-size:.75rem; font-weight:800; color:#2c5282; letter-spacing:.08em; display:inline-block;}
.small-muted {font-size:.86rem; color:#5f6368; line-height:1.5;}
</style>
"""

def inject_css():
    st.markdown(EXECUTIVE_CSS, unsafe_allow_html=True)

def tip_header(label: str, tooltip: str, level: int = 3):
    safe = tooltip.replace('**','<strong>',1) if False else tooltip
    parts = tooltip.split('**')
    html = ''.join(f'<strong>{p}</strong>' if i % 2 == 1 else p for i,p in enumerate(parts))
    st.markdown(f'<div class="tip-title"><h{level}>{label}</h{level}><span class="tip"><span class="tip-icon">ℹ️</span><span class="tip-box">{html}</span></span></div>', unsafe_allow_html=True)

def executive_banner(label: str, text: str):
    st.markdown(f'<div class="exec-banner"><div class="exec-label">{label}</div><p class="exec-text">{text}</p></div>', unsafe_allow_html=True)

def question_card(title: str, text: str):
    st.markdown(f'<div class="question-card"><div class="question-title">{title}</div><p class="question-text">{text}</p></div>', unsafe_allow_html=True)

def recommendation_card(text: str):
    st.markdown(f'<div class="recommendation-card"><strong>Recommended management action:</strong> {text}</div>', unsafe_allow_html=True)

def risk_card(text: str):
    st.markdown(f'<div class="risk-card"><strong>Risk interpretation:</strong> {text}</div>', unsafe_allow_html=True)

def note_card(text: str):
    st.markdown(f'<div class="note-card"><strong>How to read this:</strong> {text}</div>', unsafe_allow_html=True)
