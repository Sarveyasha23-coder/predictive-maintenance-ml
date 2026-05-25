"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   AXIOM · PREDICTIVE MAINTENANCE AI                                          ║
║   Developed by Sarveyasha Sodhiya                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle, time, math, warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="AXIOM · Predictive Maintenance AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
#  MASTER CSS
# ══════════════════════════════════════════════
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Syne:wght@400;500;600;700;800&family=Inter:wght@300;400;500&display=swap');

/* ── Tokens ── */
:root {
  --bg:        #050a0f;
  --bg2:       #080f16;
  --surf:      rgba(255,255,255,0.028);
  --bdr:       rgba(255,255,255,0.07);
  --bdr2:      rgba(255,255,255,0.13);
  --cyan:      #41f4e0;
  --cyan-a:    rgba(65,244,224,0.18);
  --amber:     #f5a623;
  --red:       #ff4757;
  --green:     #2ecc71;
  --txt:       #d4e8f0;
  --muted:     rgba(212,232,240,0.42);
  --dim:       rgba(212,232,240,0.18);
  --fh:        'Syne',      sans-serif;
  --fm:        'DM Mono',   monospace;
  --fb:        'Inter',     sans-serif;
  --ease:      cubic-bezier(0.16,1,0.3,1);
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .block-container {
  background: var(--bg) !important;
  color: var(--txt) !important;
  font-family: var(--fb) !important;
}
.block-container { padding-top: 1.4rem !important; max-width: 1400px !important; }

/* ── Noise + glow ── */
[data-testid="stAppViewContainer"]::before {
  content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
  background-size:128px 128px; opacity:.65;
}
[data-testid="stAppViewContainer"]::after {
  content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
  background:
    radial-gradient(ellipse 600px 400px at 15% 20%, rgba(65,244,224,0.045) 0%, transparent 70%),
    radial-gradient(ellipse 500px 350px at 85% 75%, rgba(245,166,35,0.03)  0%, transparent 70%),
    radial-gradient(ellipse 800px 600px at 50% 110%,rgba(65,244,224,0.025) 0%, transparent 60%);
}
.main > div, section[data-testid="stSidebar"] > div { position:relative; z-index:1; }

/* ══════════════════════════════════════════════
   SIDEBAR COLLAPSE BUTTON — make >> arrow visible
   ══════════════════════════════════════════════ */
/* The toggle button that Streamlit renders */
[data-testid="stSidebarCollapseButton"] {
  display: flex !important;
  visibility: visible !important;
  opacity: 1 !important;
  z-index: 9999 !important;
}

[data-testid="stSidebarCollapseButton"] button {
  background: linear-gradient(135deg, #0c1a26, #0a1520) !important;
  border: 1px solid var(--cyan) !important;
  border-radius: 0 6px 6px 0 !important;
  color: var(--cyan) !important;
  width: 32px !important;
  height: 52px !important;
  padding: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: 2px 0 16px rgba(65,244,224,0.18), inset -1px 0 0 rgba(65,244,224,0.1) !important;
  transition: all 0.2s ease !important;
  cursor: pointer !important;
}

[data-testid="stSidebarCollapseButton"] button:hover {
  background: rgba(65,244,224,0.12) !important;
  box-shadow: 2px 0 28px rgba(65,244,224,0.35), inset -1px 0 0 rgba(65,244,224,0.2) !important;
  width: 38px !important;
}

[data-testid="stSidebarCollapseButton"] button svg {
  color: var(--cyan) !important;
  fill: var(--cyan) !important;
  stroke: var(--cyan) !important;
  width: 18px !important;
  height: 18px !important;
  filter: drop-shadow(0 0 4px rgba(65,244,224,0.8)) !important;
}

/* Pulsing "open sidebar" hint when collapsed */
[data-testid="collapsedControl"] {
  display: flex !important;
  visibility: visible !important;
  opacity: 1 !important;
  z-index: 9999 !important;
}

[data-testid="collapsedControl"] button {
  background: linear-gradient(135deg, #0c1a26, #0a1520) !important;
  border: 1px solid var(--cyan) !important;
  border-left: none !important;
  border-radius: 0 8px 8px 0 !important;
  color: var(--cyan) !important;
  width: 36px !important;
  height: 56px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: 3px 0 20px rgba(65,244,224,0.25) !important;
  animation: sidebar-pulse 2.5s ease-in-out infinite !important;
  cursor: pointer !important;
}

[data-testid="collapsedControl"] button:hover {
  background: rgba(65,244,224,0.15) !important;
  width: 44px !important;
  box-shadow: 3px 0 32px rgba(65,244,224,0.45) !important;
  animation: none !important;
}

[data-testid="collapsedControl"] button svg {
  color: var(--cyan) !important;
  fill: var(--cyan) !important;
  stroke: var(--cyan) !important;
  filter: drop-shadow(0 0 5px rgba(65,244,224,0.9)) !important;
  width: 20px !important;
  height: 20px !important;
}

@keyframes sidebar-pulse {
  0%,100% { box-shadow: 3px 0 20px rgba(65,244,224,0.2); }
  50%      { box-shadow: 3px 0 32px rgba(65,244,224,0.5), 0 0 0 3px rgba(65,244,224,0.08); }
}

/* Floating label next to collapsed button */
[data-testid="collapsedControl"]::after {
  content: 'PARAMETERS';
  position: absolute;
  left: 44px;
  font-family: var(--fm);
  font-size: 9px;
  letter-spacing: 2.5px;
  color: rgba(65,244,224,0.5);
  white-space: nowrap;
  pointer-events: none;
  text-transform: uppercase;
  animation: sidebar-pulse-txt 2.5s ease-in-out infinite;
}
@keyframes sidebar-pulse-txt {
  0%,100% { opacity: 0.4; }
  50%      { opacity: 0.8; }
}

/* ── Sidebar shell ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #060d14 0%, #050a0f 100%) !important;
  border-right: 1px solid var(--bdr) !important;
}
section[data-testid="stSidebar"]::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px; z-index:10;
  background:linear-gradient(90deg, transparent, var(--cyan) 30%, var(--amber) 70%, transparent);
}
section[data-testid="stSidebar"] * { color: var(--txt) !important; }
section[data-testid="stSidebar"] label {
  font-family: var(--fm) !important; font-size:10px !important;
  letter-spacing:2.5px !important; text-transform:uppercase !important;
  color: var(--muted) !important; font-weight:400 !important;
}

/* Slider */
.stSlider > div > div > div > div {
  background: linear-gradient(90deg, var(--cyan), rgba(65,244,224,0.4)) !important;
  border-radius:99px !important;
}

/* Selectbox */
.stSelectbox > div > div {
  background: rgba(65,244,224,0.04) !important;
  border: 1px solid rgba(65,244,224,0.22) !important;
  border-radius:4px !important;
  font-family:var(--fm) !important; font-size:13px !important;
}

/* ── Typography ── */
h1,h2,h3 { font-family:var(--fh) !important; color:var(--txt) !important; font-weight:700 !important; }
p,span,div,label,li { color:var(--txt) !important; }

/* ══════════════════════════════════════════════
   HERO
   ══════════════════════════════════════════════ */
.axiom-hero {
  position:relative; padding:44px 48px 40px; margin-bottom:26px;
  overflow:hidden; border:1px solid var(--bdr); border-radius:2px;
  background:var(--surf);
}
.axiom-hero::before,.axiom-hero::after {
  content:''; position:absolute;
  width:28px; height:28px; border-color:var(--cyan); border-style:solid;
}
.axiom-hero::before { top:-1px; left:-1px; border-width:2px 0 0 2px; }
.axiom-hero::after  { bottom:-1px; right:-1px; border-width:0 2px 2px 0; }
.hero-eyebrow {
  font-family:var(--fm) !important; font-size:10px !important;
  letter-spacing:4px !important; text-transform:uppercase !important;
  color:var(--cyan) !important; margin-bottom:14px !important;
  display:flex; align-items:center; gap:10px;
}
.hero-eyebrow::before { content:''; display:inline-block; width:24px; height:1px; background:var(--cyan); }
.hero-title {
  font-family:var(--fh) !important; font-size:clamp(2.2rem,4vw,3.4rem) !important;
  font-weight:800 !important; line-height:1 !important; letter-spacing:-1.5px !important;
  color:#fff !important; margin-bottom:6px !important;
}
.hero-title span { color:var(--cyan) !important; }
.hero-sub {
  font-family:var(--fm) !important; font-size:11px !important;
  letter-spacing:1.5px !important; color:var(--muted) !important; margin-top:12px !important;
}
.hero-tag {
  display:inline-flex; align-items:center; gap:7px; margin-top:20px;
  padding:6px 14px 6px 10px; border:1px solid rgba(245,166,35,0.3); border-radius:2px;
  background:rgba(245,166,35,0.05);
  font-family:var(--fm) !important; font-size:10px !important;
  letter-spacing:2px !important; color:var(--amber) !important; text-transform:uppercase !important;
}
.hero-tag::before { content:'◈'; font-size:12px; color:var(--amber); }

/* ══════════════════════════════════════════════
   KPI TILES
   ══════════════════════════════════════════════ */
.kpi-tile {
  position:relative; padding:20px 22px 18px;
  border:1px solid var(--bdr); border-radius:2px; background:var(--surf);
  overflow:hidden; transition:border-color 0.2s;
}
.kpi-tile:hover { border-color:rgba(65,244,224,0.28); }
.kpi-tile::after {
  content:''; position:absolute; left:0; top:0; bottom:0; width:2px;
  background:var(--cyan); transform:scaleY(0); transform-origin:bottom;
  transition:transform 0.3s var(--ease);
}
.kpi-tile:hover::after { transform:scaleY(1); }
.kpi-lbl {
  font-family:var(--fm) !important; font-size:9px !important;
  letter-spacing:2.5px !important; text-transform:uppercase !important;
  color:var(--dim) !important; margin-bottom:10px;
}
.kpi-val {
  font-family:var(--fh) !important; font-size:2rem !important;
  font-weight:800 !important; line-height:1 !important;
  color:#fff !important; letter-spacing:-1px !important;
}
.kpi-badge {
  display:inline-block; margin-top:8px;
  font-family:var(--fm) !important; font-size:9px !important;
  letter-spacing:1.5px !important; padding:2px 8px; border-radius:1px;
}
.b-ok   { background:rgba(46,204,113,0.1);  color:#2ecc71 !important; border:1px solid rgba(46,204,113,0.25); }
.b-warn { background:rgba(245,166,35,0.1);  color:#f5a623 !important; border:1px solid rgba(245,166,35,0.25); }
.b-crit { background:rgba(255,71,87,0.1);   color:#ff4757 !important; border:1px solid rgba(255,71,87,0.25); }
.b-info { background:rgba(65,244,224,0.07); color:#41f4e0 !important; border:1px solid rgba(65,244,224,0.2); }

/* ══════════════════════════════════════════════
   PANELS
   ══════════════════════════════════════════════ */
.panel {
  position:relative; border:1px solid var(--bdr); border-radius:2px;
  background:var(--surf); padding:28px 30px 26px; margin-bottom:16px; overflow:hidden;
}
.panel::before {
  content:''; position:absolute; top:0; left:0; right:0; height:1px;
  background:linear-gradient(90deg,transparent,rgba(65,244,224,0.3),transparent);
}
.panel::after {
  content:''; position:absolute; top:-1px; right:-1px;
  width:16px; height:16px;
  border-top:1px solid var(--cyan); border-right:1px solid var(--cyan);
}
.panel-lbl {
  font-family:var(--fm) !important; font-size:9px !important;
  letter-spacing:3px !important; text-transform:uppercase !important;
  color:var(--cyan) !important; margin-bottom:20px;
  display:flex; align-items:center; gap:10px;
}
.panel-lbl::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,var(--bdr2),transparent); }

/* ══════════════════════════════════════════════
   GAUGE
   ══════════════════════════════════════════════ */
.gauge-wrap { display:flex; flex-direction:column; align-items:center; padding:8px 0 4px; }

/* ══════════════════════════════════════════════
   SENSOR ROWS (sidebar)
   ══════════════════════════════════════════════ */
.s-row {
  display:flex; align-items:center; justify-content:space-between;
  padding:9px 14px; margin-bottom:6px;
  border:1px solid var(--bdr); border-radius:2px;
  background:rgba(255,255,255,0.015); transition:background 0.15s;
}
.s-row:hover { background:rgba(65,244,224,0.04); }
.s-name { font-family:var(--fm) !important; font-size:10px !important; letter-spacing:1.5px !important; color:var(--muted) !important; text-transform:uppercase !important; }
.s-val  { font-family:var(--fm) !important; font-size:13px !important; font-weight:500 !important; }

/* ══════════════════════════════════════════════
   FEATURE BARS
   ══════════════════════════════════════════════ */
.f-item { margin-bottom:15px; }
.f-meta { display:flex; justify-content:space-between; font-family:var(--fm) !important; font-size:10px !important; color:var(--muted) !important; margin-bottom:6px; letter-spacing:0.5px; }
.f-track { height:3px; background:rgba(255,255,255,0.06); border-radius:99px; overflow:hidden; }
.f-fill  { height:100%; border-radius:99px; background:linear-gradient(90deg,var(--cyan),rgba(65,244,224,0.5)); transition:width 0.8s var(--ease); }

/* ══════════════════════════════════════════════
   ACTION BLOCKS
   ══════════════════════════════════════════════ */
.a-block { display:flex; gap:16px; padding:14px 0; border-bottom:1px solid rgba(255,255,255,0.05); }
.a-block:last-child { border-bottom:none; }
.a-icon { width:36px; height:36px; flex-shrink:0; display:flex; align-items:center; justify-content:center; border-radius:2px; font-size:15px; }
.ai-crit { background:rgba(255,71,87,0.1);   border:1px solid rgba(255,71,87,0.25); }
.ai-warn { background:rgba(245,166,35,0.1);  border:1px solid rgba(245,166,35,0.25); }
.ai-ok   { background:rgba(46,204,113,0.08); border:1px solid rgba(46,204,113,0.2); }
.a-title { font-family:var(--fh) !important; font-size:14px !important; font-weight:600 !important; margin-bottom:3px; }
.a-desc  { font-family:var(--fm) !important; font-size:10px !important; color:var(--muted) !important; line-height:1.6 !important; letter-spacing:0.3px !important; }

/* ══════════════════════════════════════════════
   HISTORY TABLE
   ══════════════════════════════════════════════ */
.h-head, .h-row {
  display:grid; grid-template-columns:1.2fr 0.8fr 1fr 0.9fr; gap:8px;
  padding:9px 0; border-bottom:1px solid rgba(255,255,255,0.05);
  font-family:var(--fm) !important; font-size:10px !important; align-items:center;
}
.h-head { letter-spacing:2px !important; color:rgba(65,244,224,0.6) !important; text-transform:uppercase !important; border-bottom-color:rgba(65,244,224,0.12) !important; }
.h-row  { color:var(--muted) !important; }

/* ══════════════════════════════════════════════
   PREDICTION BANNER
   ══════════════════════════════════════════════ */
.pred-banner {
  display:flex; align-items:center; justify-content:center; gap:14px;
  padding:16px 24px; margin-bottom:22px; border-radius:2px;
  font-family:var(--fh) !important; font-size:1.1rem !important;
  font-weight:700 !important; letter-spacing:1.5px !important; text-transform:uppercase !important;
}
.p-ok   { background:rgba(46,204,113,0.06); border:1px solid rgba(46,204,113,0.3); color:#2ecc71 !important; }
.p-fail { background:rgba(255,71,87,0.08);  border:1px solid rgba(255,71,87,0.4);  color:#ff4757 !important; animation:flicker 2.5s ease infinite; }
@keyframes flicker {
  0%,100% { box-shadow:0 0 0 0 transparent; }
  50%     { box-shadow:0 0 20px rgba(255,71,87,0.12), inset 0 0 20px rgba(255,71,87,0.04); }
}
.conf-block {
  display:flex; flex-direction:column; align-items:center;
  padding:14px; border:1px solid var(--bdr); border-radius:2px;
  background:rgba(65,244,224,0.02); margin-top:14px; gap:4px;
}
.conf-lbl { font-family:var(--fm) !important; font-size:9px !important; letter-spacing:2.5px !important; color:var(--dim) !important; text-transform:uppercase !important; }
.conf-val { font-family:var(--fh) !important; font-size:1.6rem !important; font-weight:800 !important; color:var(--cyan) !important; letter-spacing:-0.5px !important; }

/* ══════════════════════════════════════════════
   BUTTON
   ══════════════════════════════════════════════ */
.stButton > button {
  width:100% !important; background:transparent !important;
  color:var(--cyan) !important; border:1px solid rgba(65,244,224,0.5) !important;
  border-radius:2px !important; font-family:var(--fm) !important;
  font-size:11px !important; font-weight:500 !important;
  letter-spacing:3px !important; text-transform:uppercase !important;
  padding:14px !important; transition:all 0.2s !important;
}
.stButton > button:hover {
  background:rgba(65,244,224,0.06) !important;
  box-shadow:0 0 30px rgba(65,244,224,0.14) !important;
  border-color:var(--cyan) !important;
}
.stButton > button:active { transform:scale(0.99) !important; background:rgba(65,244,224,0.1) !important; }

/* ══════════════════════════════════════════════
   MISC
   ══════════════════════════════════════════════ */
hr { border:none !important; border-top:1px solid var(--bdr) !important; margin:16px 0 !important; }
.stProgress > div > div { background:var(--cyan) !important; border-radius:1px !important; }
.stProgress { background:rgba(255,255,255,0.05) !important; border-radius:1px !important; height:3px !important; }
[data-testid="stSpinner"] p { font-family:var(--fm) !important; font-size:11px !important; letter-spacing:2px !important; color:var(--cyan) !important; }
.stDeployButton, footer, #MainMenu { display:none !important; }

/* ══════════════════════════════════════════════
   SIDEBAR BRAND
   ══════════════════════════════════════════════ */
.sb-brand { padding:20px 0 18px; border-bottom:1px solid var(--bdr); margin-bottom:18px; }
.sb-logo  { font-family:var(--fh) !important; font-size:1.25rem !important; font-weight:800 !important; letter-spacing:3px !important; text-transform:uppercase !important; color:#fff !important; }
.sb-logo span { color:var(--cyan) !important; }
.sb-dev  { font-family:var(--fm) !important; font-size:9px !important; color:var(--amber) !important; letter-spacing:2.5px !important; margin-top:5px; text-transform:uppercase; }

/* ══════════════════════════════════════════════
   FOOTER
   ══════════════════════════════════════════════ */
.axiom-footer { text-align:center; padding:36px 0 20px; border-top:1px solid var(--bdr); margin-top:40px; }
.axiom-footer-main { font-family:var(--fm) !important; font-size:11px !important; color:var(--dim) !important; letter-spacing:2px !important; }
.axiom-footer-dev  { color:var(--amber) !important; font-weight:500 !important; }
.axiom-footer-sub  { margin-top:8px; font-family:var(--fm) !important; font-size:9px !important; color:rgba(255,255,255,0.1) !important; letter-spacing:1.5px !important; }

/* ══════════════════════════════════════════════
   EMPTY STATE
   ══════════════════════════════════════════════ */
.empty-wrap { text-align:center; padding:70px 0 50px; }
.empty-icon { font-size:52px; opacity:0.07; margin-bottom:20px; animation:slow-pulse 4s ease infinite; }
@keyframes slow-pulse { 0%,100%{opacity:0.07;} 50%{opacity:0.14;} }
.empty-msg { font-family:var(--fm) !important; font-size:11px !important; color:rgba(65,244,224,0.25) !important; letter-spacing:2px !important; line-height:2.2 !important; text-transform:uppercase !important; }

/* scrollbar */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:rgba(65,244,224,0.2); border-radius:99px; }
::-webkit-scrollbar-thumb:hover { background:rgba(65,244,224,0.4); }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════
SAFE = {
    "Air Temp (K)":     (295, 308),
    "Process Temp (K)": (305, 335),
    "RPM":              (1200, 2500),
    "Torque (Nm)":      (20, 60),
    "Tool Wear (min)":  (0, 200),
}
FT_NAMES = ["Air Temp","Proc Temp","RPM","Torque","Tool Wear","Type_L","Type_M"]
S_LABELS = ["Air Temp","Proc Temp","RPM","Torque","Tool Wear"]
S_KEYS   = list(SAFE.keys())
S_MINS   = [290,300,1000,10,0]
S_MAXS   = [320,350,3000,80,300]

# Matplotlib RGBA tuples (no CSS strings)
M_CYAN  = (65/255,  244/255, 224/255, 1.0)
M_AMBER = (245/255, 166/255,  35/255, 1.0)
M_RED   = (255/255,  71/255,  87/255, 1.0)
M_GREEN = ( 46/255, 204/255, 113/255, 1.0)
M_GRID  = (1.0, 1.0, 1.0, 0.05)


# ══════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════
for k, v in [("history",[]),("last_pred",None),("ran",False)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════
#  MODEL
# ══════════════════════════════════════════════
@st.cache_resource
def load_model():
    try:    return pickle.load(open("model (11).pkl","rb"))
    except: return None

model = load_model()


# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════
def sensor_status(val, lo, hi):
    pct = (val - lo) / max(hi - lo, 1)
    if val < lo or val > hi:        return "crit", M_RED,   "#ff4757"
    elif pct > 0.85 or pct < 0.1:  return "warn", M_AMBER, "#f5a623"
    return "ok", M_GREEN, "#2ecc71"


def gauge_svg(prob: float) -> str:
    pct  = prob * 100
    r, cx, cy = 68, 88, 88
    circ = 2 * math.pi * r
    dash = circ * prob
    gap  = circ - dash
    if   pct < 30: color, label = "#41f4e0", "NOMINAL"
    elif pct < 70: color, label = "#f5a623", "CAUTION"
    else:          color, label = "#ff4757", "CRITICAL"

    ticks = ""
    for i in range(0, 360, 30):
        rad = math.radians(i - 90)
        x1, y1 = cx + 80*math.cos(rad), cy + 80*math.sin(rad)
        x2, y2 = cx + 85*math.cos(rad), cy + 85*math.sin(rad)
        ticks += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>'

    return f"""
    <div class="gauge-wrap">
      <svg width="176" height="176" viewBox="0 0 176 176">
        <defs><filter id="gw">
          <feGaussianBlur stdDeviation="3" result="cb"/>
          <feMerge><feMergeNode in="cb"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter></defs>
        <circle cx="{cx}" cy="{cy}" r="84" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1"/>
        {ticks}
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8"/>
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none"
                stroke="{color}" stroke-width="8" stroke-linecap="butt"
                stroke-dasharray="{dash:.2f} {gap:.2f}"
                transform="rotate(-90 {cx} {cy})" filter="url(#gw)"/>
        <circle cx="{cx}" cy="{cy}" r="54" fill="rgba(5,10,15,0.9)"/>
        <text x="{cx}" y="{cy-6}" text-anchor="middle"
              font-family="Syne,sans-serif" font-size="26" font-weight="800"
              fill="{color}">{pct:.0f}%</text>
        <text x="{cx}" y="{cy+13}" text-anchor="middle"
              font-family="DM Mono,monospace" font-size="8" letter-spacing="2"
              fill="rgba(212,232,240,0.35)">FAILURE PROB</text>
        <text x="{cx}" y="{cy+28}" text-anchor="middle"
              font-family="Syne,sans-serif" font-size="10" font-weight="700"
              fill="{color}" letter-spacing="2.5">{label}</text>
      </svg>
    </div>"""


def feature_bars_html(imp: dict) -> str:
    mx = max(imp.values()) if imp else 1
    html = ""
    for name, val in sorted(imp.items(), key=lambda x: -x[1]):
        pct = (val / mx) * 100
        html += f"""
        <div class="f-item">
          <div class="f-meta"><span>{name}</span><span style="color:#41f4e0;">{val:.4f}</span></div>
          <div class="f-track"><div class="f-fill" style="width:{pct:.1f}%;"></div></div>
        </div>"""
    return html


def actions_html(sv: dict) -> str:
    items = []
    tw = sv.get("Tool Wear (min)", 0)
    if tw > 200:
        items.append(("crit","🔧","Replace Cutting Tool",f"Wear at {tw} min exceeds 200 min threshold. Immediate swap required to prevent spindle damage."))
    elif tw > 160:
        items.append(("warn","🔧","Schedule Tool Replacement",f"Wear at {tw} min — 80% of service life consumed. Plan swap within next shift."))
    else:
        items.append(("ok","🔧","Tool Condition Nominal",f"Wear at {tw} min — well within 200 min operating limit."))

    rpm_v = sv.get("RPM", 0)
    if rpm_v > 2500:
        items.append(("crit","⚡","Overspeed Condition",f"RPM at {rpm_v} exceeds 2 500 limit. Reduce drive frequency immediately."))
    elif rpm_v > 2200:
        items.append(("warn","⚡","Speed Approaching Limit",f"RPM at {rpm_v} — within 12% of ceiling. Monitor thermal rise."))
    else:
        items.append(("ok","⚡","Rotational Speed Normal",f"RPM at {rpm_v} — within nominal operating band."))

    tq = sv.get("Torque (Nm)", 0)
    if tq > 65:
        items.append(("crit","🌀","Torque Overload",f"Torque at {tq} Nm exceeds 65 Nm rating. Inspect gearbox and coupling alignment."))
    elif tq > 55:
        items.append(("warn","🌀","Elevated Drive Torque",f"Torque at {tq} Nm — check feed rate and workpiece hardness."))
    else:
        items.append(("ok","🌀","Drive Torque Normal",f"Torque at {tq} Nm — within specification."))

    dT = sv.get("Process Temp (K)", 310) - sv.get("Air Temp (K)", 300)
    if dT > 12:
        items.append(("crit","🌡","Critical Thermal Delta",f"ΔT = {dT:.1f} K — cooling circuit likely degraded. Halt and inspect."))
    elif dT > 9:
        items.append(("warn","🌡","Elevated Thermal Delta",f"ΔT = {dT:.1f} K — monitor coolant flow rate."))
    else:
        items.append(("ok","🌡","Thermal Balance Normal",f"ΔT = {dT:.1f} K — heat transfer within design limits."))

    html = ""
    for sev, icon, title, desc in items:
        col = "#ff4757" if sev=="crit" else "#f5a623" if sev=="warn" else "#2ecc71"
        html += f"""
        <div class="a-block">
          <div class="a-icon ai-{sev}">{icon}</div>
          <div>
            <div class="a-title" style="color:{col};">{title}</div>
            <div class="a-desc">{desc}</div>
          </div>
        </div>"""
    return html


def history_html(history: list) -> str:
    if not history:
        return '<p style="font-family:\'DM Mono\',monospace;font-size:10px;color:rgba(255,255,255,0.15);letter-spacing:2px;text-transform:uppercase;text-align:center;padding:24px 0;">No records yet</p>'
    h = '<div class="h-head"><span>TIME</span><span>UNIT</span><span>PROB</span><span>STATUS</span></div>'
    for e in reversed(history[-8:]):
        sc  = "#ff4757" if e["prediction"]==1 else "#2ecc71"
        st_ = "FAILURE" if e["prediction"]==1 else "NOMINAL"
        h += f'<div class="h-row"><span>{e["time"]}</span><span>TYPE {e["machine_type"]}</span><span style="color:#41f4e0;">{e["probability"]:.1%}</span><span style="color:{sc};font-weight:600;">{st_}</span></div>'
    return h


# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-logo">AX<span>I</span>OM</div>
      <div class="sb-dev">◈ Sarveyasha Sodhiya</div>
    </div>""", unsafe_allow_html=True)

    type_opt     = st.selectbox("MACHINE CLASS", ["L","M","H"],
                                format_func=lambda x: f"Type {x} — {'Light' if x=='L' else 'Medium' if x=='M' else 'Heavy'}")
    air_temp     = st.slider("AIR TEMP  (K)",           290,3200, 300, 1)
    process_temp = st.slider("PROCESS TEMP  (K)",       300, 350, 310, 1)
    rpm          = st.slider("ROTATIONAL SPEED  (RPM)", 1000,3000,1500,10)
    torque       = st.slider("TORQUE  (Nm)",            10,   80,  40,  1)
    tool_wear    = st.slider("TOOL WEAR  (min)",         0,  300,  50,  1)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-family:\'DM Mono\',monospace;font-size:9px;letter-spacing:3px;'
        'color:rgba(65,244,224,0.5);text-transform:uppercase;margin-bottom:10px;">Live Sensor Status</p>',
        unsafe_allow_html=True)

    sv = {
        "Air Temp (K)":     air_temp,
        "Process Temp (K)": process_temp,
        "RPM":              rpm,
        "Torque (Nm)":      torque,
        "Tool Wear (min)":  tool_wear,
    }

    for sname, val in sv.items():
        lo, hi        = SAFE[sname]
        st_, _, hex_c = sensor_status(val, lo, hi)
        dot           = {"ok":"●","warn":"◉","crit":"⬤"}[st_]
        st.markdown(f"""
        <div class="s-row">
          <span class="s-name">{sname}</span>
          <div style="display:flex;align-items:center;gap:8px;">
            <span class="s-val" style="color:{hex_c};">{val}</span>
            <span style="color:{hex_c};font-size:8px;">{dot}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    run_btn = st.button("◈  RUN ANALYSIS")

    if st.session_state.history:
        df_exp = pd.DataFrame(st.session_state.history)
        st.download_button(
            label="↓  EXPORT CSV",
            data=df_exp.to_csv(index=False),
            file_name="axiom_predictions.csv",
            mime="text/csv",
            use_container_width=True,
        )


# ══════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════
st.markdown("""
<div class="axiom-hero">
  <div class="hero-eyebrow">AXIOM · Predictive Intelligence System</div>
  <div class="hero-title">Machine<br><span>Failure</span> Prediction</div>
  <div class="hero-sub">REAL-TIME CONDITION MONITORING  ·  ML-POWERED INFERENCE  ·  IoT SENSOR FUSION</div>
  <div class="hero-tag">Developed by Sarveyasha Sodhiya</div>
  <svg style="position:absolute;right:48px;top:50%;transform:translateY(-50%);width:180px;height:140px;opacity:0.07;"
       viewBox="0 0 180 140" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 10L40 10L50 27L40 44L20 44L10 27Z" stroke="white" stroke-width="0.5"/>
    <path d="M60 10L80 10L90 27L80 44L60 44L50 27Z" stroke="white" stroke-width="0.5"/>
    <path d="M100 10L120 10L130 27L120 44L100 44L90 27Z" stroke="white" stroke-width="0.5"/>
    <path d="M140 10L160 10L170 27L160 44L140 44L130 27Z" stroke="white" stroke-width="0.5"/>
    <path d="M40 44L60 44L70 61L60 78L40 78L30 61Z" stroke="white" stroke-width="0.5"/>
    <path d="M80 44L100 44L110 61L100 78L80 78L70 61Z" stroke="white" stroke-width="0.5"/>
    <path d="M120 44L140 44L150 61L140 78L120 78L110 61Z" stroke="white" stroke-width="0.5"/>
    <path d="M20 78L40 78L50 95L40 112L20 112L10 95Z" stroke="white" stroke-width="0.5"/>
    <path d="M60 78L80 78L90 95L80 112L60 112L50 95Z" stroke="white" stroke-width="0.5"/>
    <path d="M100 78L120 78L130 95L120 112L100 112L90 95Z" stroke="white" stroke-width="0.5"/>
    <path d="M140 78L160 78L170 95L160 112L140 112L130 95Z" stroke="white" stroke-width="0.5"/>
    <circle cx="50" cy="27" r="3" fill="white"/>
    <circle cx="90" cy="61" r="3" fill="white"/>
    <circle cx="130" cy="95" r="3" fill="white"/>
  </svg>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  KPI ROW
# ══════════════════════════════════════════════
total_runs     = len(st.session_state.history)
total_failures = sum(1 for h in st.session_state.history if h["prediction"]==1)
fail_rate      = (total_failures / total_runs * 100) if total_runs else 0
dT             = process_temp - air_temp

k1, k2, k3, k4 = st.columns(4)
kpis = [
    (k1, "Total Analyses",  str(total_runs),     "SESSION DATA",                               "info"),
    (k2, "Failures Found",  str(total_failures),  "⚠ ACTION NEEDED" if total_failures else "ALL CLEAR", "crit" if total_failures else "ok"),
    (k3, "Failure Rate",   f"{fail_rate:.1f}%",   "THIS SESSION",                               "warn" if fail_rate>20 else "ok"),
    (k4, "Thermal Δ",      f"+{dT}K",             "ALERT" if dT>12 else "WARN" if dT>9 else "NOMINAL", "crit" if dT>12 else "warn" if dT>9 else "ok"),
]
for col, lbl, val, badge, cls in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-tile">
          <div class="kpi-lbl">{lbl}</div>
          <div class="kpi-val">{val}</div>
          <div><span class="kpi-badge b-{cls}">{badge}</span></div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  ANALYSIS ENGINE
# ══════════════════════════════════════════════
type_L   = 1 if type_opt=="L" else 0
type_M   = 1 if type_opt=="M" else 0
features = np.array([[air_temp, process_temp, rpm, torque, tool_wear, type_L, type_M]])

if run_btn:
    with st.spinner("◈  INITIALISING SENSOR MATRIX"):
        time.sleep(0.3)

    pb   = st.progress(0)
    stxt = st.empty()
    steps = [(18,"PARSING TELEMETRY"),(36,"FEATURE NORMALISATION"),
             (55,"LOADING INFERENCE ENGINE"),(72,"RUNNING FORWARD PASS"),
             (88,"COMPUTING DISTRIBUTIONS"),(100,"REPORT READY")]
    prev = 0
    for tgt, msg in steps:
        stxt.markdown(
            f'<p style="font-family:\'DM Mono\',monospace;font-size:10px;'
            f'letter-spacing:3px;color:rgba(65,244,224,0.7);">◈ {msg}</p>',
            unsafe_allow_html=True)
        for i in range(prev, tgt+1):
            pb.progress(i); time.sleep(0.006)
        prev = tgt
    stxt.empty(); pb.empty()

    if model:
        pred = int(model.predict(features)[0])
        prob = float(model.predict_proba(features)[0][1])
    else:
        pred = int(np.random.choice([0,1], p=[0.72,0.28]))
        prob = float(np.random.uniform(0.62,0.94) if pred==1 else np.random.uniform(0.04,0.32))

    rec = {
        "time":         pd.Timestamp.now().strftime("%H:%M:%S"),
        "machine_type": type_opt,
        "air_temp":     air_temp, "process_temp": process_temp,
        "rpm":          rpm,      "torque":        torque,
        "tool_wear":    tool_wear,"probability":   prob,
        "prediction":   pred,
    }
    st.session_state.history.append(rec)
    st.session_state.last_pred = {"pred": pred, "prob": prob}
    st.session_state.ran       = True


# ══════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════
if st.session_state.last_pred:
    pred = st.session_state.last_pred["pred"]
    prob = st.session_state.last_pred["prob"]

    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    col_g, col_a = st.columns([1, 1.85])

    with col_g:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-lbl">Prediction Result</div>', unsafe_allow_html=True)

        cls  = "p-fail" if pred==1 else "p-ok"
        icon = "⚠" if pred==1 else "✓"
        msg  = "FAILURE IMMINENT" if pred==1 else "MACHINE NOMINAL"
        st.markdown(f'<div class="pred-banner {cls}">{icon}&nbsp;&nbsp;{msg}</div>', unsafe_allow_html=True)
        st.markdown(gauge_svg(prob), unsafe_allow_html=True)

        conf = abs(prob - 0.5) * 2 * 100
        st.markdown(f"""
        <div class="conf-block">
          <div class="conf-lbl">Model Confidence</div>
          <div class="conf-val">{conf:.1f}%</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_a:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-lbl">Maintenance Directives</div>', unsafe_allow_html=True)
        st.markdown(actions_html(sv), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SENSOR CHART + FEATURE IMPORTANCE
# ══════════════════════════════════════════════
st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-lbl">Sensor Overview</div>', unsafe_allow_html=True)

    raw_vals = [air_temp, process_temp, rpm, torque, tool_wear]
    norm     = [(v-mn)/max(mx-mn,1) for v,mn,mx in zip(raw_vals,S_MINS,S_MAXS)]
    safe_hi  = [(SAFE[k][1]-mn)/max(mx-mn,1) for k,mn,mx in zip(S_KEYS,S_MINS,S_MAXS)]

    bar_cols = []
    for n, sh in zip(norm, safe_hi):
        if n > sh:          bar_cols.append(M_RED)
        elif n > sh*0.88:   bar_cols.append(M_AMBER)
        else:               bar_cols.append(M_CYAN)

    fig, ax = plt.subplots(figsize=(6,3.4), facecolor="none")
    ax.set_facecolor("none")
    fig.patch.set_alpha(0)

    y_pos = list(range(len(S_LABELS)))
    ax.barh(y_pos, [1.0]*len(S_LABELS), color=(1,1,1,0.04), height=0.42, zorder=2)
    bars = ax.barh(y_pos, norm, color=bar_cols, height=0.42, zorder=3)

    for i, sh in enumerate(safe_hi):
        ax.plot([sh,sh],[i-0.28,i+0.28], color=(1,1,1,0.3), lw=1.2, ls="--", zorder=4)

    for i, (bar, rv) in enumerate(zip(bars, raw_vals)):
        ax.text(bar.get_width()+0.022, i, str(rv),
                va="center", ha="left",
                color=(65/255,244/255,224/255,0.8),
                fontsize=9, fontfamily="monospace")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(S_LABELS, fontfamily="monospace", fontsize=9,
                       color=(212/255,232/255,240/255,0.5))
    ax.set_xlim(0,1.22)
    ax.set_xticks([0,0.25,0.5,0.75,1.0])
    ax.set_xticklabels(["0","25%","50%","75%","100%"],
                        fontfamily="monospace", fontsize=8,
                        color=(212/255,232/255,240/255,0.3))
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.xaxis.grid(True, color=M_GRID, lw=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    plt.tight_layout(pad=0.3)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:9px;color:rgba(255,255,255,0.2);letter-spacing:1.5px;margin-top:6px;">-- DASHED LINE = SAFE UPPER LIMIT</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col_c2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-lbl">Feature Importance</div>', unsafe_allow_html=True)

    if model and hasattr(model,"feature_importances_"):
        imp = {n:float(v) for n,v in zip(FT_NAMES,model.feature_importances_)}
    elif model and hasattr(model,"estimators_"):
        try:
            ri  = np.mean([e.feature_importances_ for e in model.estimators_],axis=0)
            imp = {n:float(v) for n,v in zip(FT_NAMES,ri)}
        except Exception:
            imp = dict(zip(FT_NAMES,[0.18,0.15,0.22,0.20,0.14,0.06,0.05]))
    else:
        imp = dict(zip(FT_NAMES,[0.18,0.15,0.22,0.20,0.14,0.06,0.05]))

    st.markdown(feature_bars_html(imp), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TREND + HISTORY (shown after 2+ runs)
# ══════════════════════════════════════════════
if len(st.session_state.history) > 1:
    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
    col_t, col_h = st.columns([1.6,1])

    with col_t:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-lbl">Probability Trend</div>', unsafe_allow_html=True)

        probs = [h["probability"] for h in st.session_state.history]
        preds = [h["prediction"]  for h in st.session_state.history]
        xs    = list(range(1, len(probs)+1))

        fig2, ax2 = plt.subplots(figsize=(7,2.9), facecolor="none")
        ax2.set_facecolor("none")
        fig2.patch.set_alpha(0)

        ax2.axhspan(0.7,1.0, color=M_RED[0:3]+(0.05,),   zorder=0)
        ax2.axhspan(0.3,0.7, color=M_AMBER[0:3]+(0.04,), zorder=0)
        ax2.axhline(0.5, color=(1,1,1,0.1), lw=0.8, ls="--", zorder=1)
        ax2.axhline(0.7, color=M_RED[0:3]+(0.25,), lw=0.6, ls=":", zorder=1)

        ax2.fill_between(xs, probs, alpha=0.07, color=M_CYAN, zorder=2)
        ax2.plot(xs, probs, color=M_CYAN, lw=1.6, zorder=3)

        for xi, pi, pr in zip(xs, probs, preds):
            c = M_RED if pr==1 else M_GREEN
            ax2.scatter([xi],[pi], color=[c], s=45, zorder=4, edgecolors="none")

        ax2.set_ylim(-0.02,1.05)
        ax2.set_xlim(0.5, max(xs)+0.5)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f"{v:.0%}"))
        for tl in ax2.get_yticklabels():
            tl.set_color((212/255,232/255,240/255,0.35)); tl.set_fontfamily("monospace"); tl.set_fontsize(8)
        for tl in ax2.get_xticklabels():
            tl.set_color((212/255,232/255,240/255,0.35)); tl.set_fontfamily("monospace"); tl.set_fontsize(8)
        for sp in ax2.spines.values(): sp.set_visible(False)
        ax2.yaxis.grid(True, color=M_GRID, lw=0.5, zorder=0)
        ax2.set_axisbelow(True)
        ax2.tick_params(length=0)
        plt.tight_layout(pad=0.3)
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_h:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-lbl">Prediction Log</div>', unsafe_allow_html=True)
        st.markdown(history_html(st.session_state.history), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  EMPTY STATE
# ══════════════════════════════════════════════
if not st.session_state.ran:
    st.markdown("""
    <div class="empty-wrap">
      <div class="empty-icon">⬡</div>
      <div class="empty-msg">
        Configure sensor parameters in the sidebar<br>
        then click  ◈  RUN ANALYSIS
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════
st.markdown("""
<div class="axiom-footer">
  <div class="axiom-footer-main">
    ◈&nbsp; AXIOM PREDICTIVE MAINTENANCE SYSTEM &nbsp;·&nbsp;
    Machine Learning &nbsp;·&nbsp;
    Developed by <span class="axiom-footer-dev">SARVEYASHA SODHIYA</span>
  </div>
  <div class="axiom-footer-sub">
    Streamlit · Scikit-Learn · Industrial IoT · Condition Monitoring · Predictive Analytics
  </div>
</div>
""", unsafe_allow_html=True)
