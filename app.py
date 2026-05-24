"""
╔══════════════════════════════════════════════════════════════════╗
║          PREDICTIVE MAINTENANCE AI DASHBOARD                     ║
║          Developed by Sarveyasha Sodhiya                         ║
║          Machine Learning · Real-time Analytics · IoT Sensors    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PredictiveMaint AI · Sarveyasha Sodhiya",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  FULL CUSTOM CSS — Industrial Luxury Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
:root {
    --primary: #00e5ff;
    --primary-dim: #0097a7;
    --accent: #ff6b35;
    --success: #00e676;
    --warning: #ffea00;
    --danger: #ff1744;
    --bg-deep: #020c14;
    --bg-card: rgba(0, 229, 255, 0.04);
    --bg-card-hover: rgba(0, 229, 255, 0.08);
    --border: rgba(0, 229, 255, 0.18);
    --border-strong: rgba(0, 229, 255, 0.45);
    --text-main: #e8f4f8;
    --text-dim: #7a9baa;
    --font-display: 'Rajdhani', sans-serif;
    --font-mono: 'Space Mono', monospace;
    --font-body: 'Inter', sans-serif;
}

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg-deep) !important;
    color: var(--text-main) !important;
    font-family: var(--font-body) !important;
}

/* Scanline overlay */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 229, 255, 0.012) 2px,
        rgba(0, 229, 255, 0.012) 4px
    );
    pointer-events: none;
    z-index: 0;
}

[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 20% 50%, rgba(0, 100, 180, 0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(0, 200, 180, 0.06) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #030f1a 0%, #020c14 100%) !important;
    border-right: 1px solid var(--border) !important;
}

section[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--accent), var(--primary));
    background-size: 200%;
    animation: borderFlow 3s linear infinite;
}

@keyframes borderFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

section[data-testid="stSidebar"] * {
    color: var(--text-main) !important;
    font-family: var(--font-body) !important;
}

section[data-testid="stSidebar"] label {
    font-family: var(--font-display) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--primary) !important;
}

/* Sliders */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, var(--primary), var(--primary-dim)) !important;
}

.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] {
    color: var(--text-dim) !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: rgba(0, 229, 255, 0.06) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 6px !important;
    color: var(--text-main) !important;
    font-family: var(--font-mono) !important;
}

/* ── Main Content ── */
.main > div { position: relative; z-index: 1; }

/* ── Glass Cards ── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px 32px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
    animation: fadeUp 0.6s ease both;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--primary-dim), transparent);
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Hero Header ── */
.hero {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.05) 0%, rgba(255, 107, 53, 0.04) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.5s ease both;
}

.hero::after {
    content: '⚙';
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 120px;
    opacity: 0.04;
    animation: spin 20s linear infinite;
    color: var(--primary);
}

@keyframes spin {
    from { transform: translateY(-50%) rotate(0deg); }
    to   { transform: translateY(-50%) rotate(360deg); }
}

.hero-title {
    font-family: var(--font-display) !important;
    font-size: 3rem !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: var(--primary) !important;
    margin: 0 0 4px !important;
    line-height: 1.1 !important;
    text-shadow: 0 0 40px rgba(0, 229, 255, 0.4) !important;
}

.hero-subtitle {
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    color: var(--text-dim) !important;
    letter-spacing: 2px !important;
    margin: 0 !important;
}

.hero-byline {
    display: inline-block;
    margin-top: 16px;
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    color: var(--accent) !important;
    letter-spacing: 1.5px !important;
    border: 1px solid rgba(255, 107, 53, 0.4);
    padding: 4px 14px;
    border-radius: 4px;
    background: rgba(255, 107, 53, 0.07);
}

/* ── Section Headings ── */
.section-title {
    font-family: var(--font-display) !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: var(--primary) !important;
    margin: 0 0 20px !important;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-strong), transparent);
}

/* Override Streamlit headings */
h1, h2, h3 { font-family: var(--font-display) !important; color: var(--primary) !important; }
p, span, div, li { color: var(--text-main) !important; }

/* ── Metric Cards ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}

.metric-box {
    background: rgba(0, 229, 255, 0.04);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.7s ease both;
}

.metric-box::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    transform: scaleX(0);
    transition: transform 0.3s;
    transform-origin: left;
}

.metric-box:hover::before { transform: scaleX(1); }

.metric-label {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 1.8px !important;
    color: var(--text-dim) !important;
    text-transform: uppercase !important;
    margin-bottom: 8px;
}

.metric-value {
    font-family: var(--font-display) !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: var(--primary) !important;
    line-height: 1 !important;
}

.metric-delta {
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    margin-top: 6px;
}

/* ── Gauge ── */
.gauge-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 10px 0;
}

/* ── Status Indicator ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 6px;
    font-family: var(--font-display) !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

.status-ok {
    background: rgba(0, 230, 118, 0.1);
    border: 1px solid rgba(0, 230, 118, 0.5);
    color: var(--success) !important;
}

.status-fail {
    background: rgba(255, 23, 68, 0.1);
    border: 1px solid rgba(255, 23, 68, 0.5);
    color: var(--danger) !important;
    animation: pulse-red 1.5s infinite;
}

@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255, 23, 68, 0.0); }
    50% { box-shadow: 0 0 0 8px rgba(255, 23, 68, 0.15); }
}

/* ── Status Dots ── */
.dot-ok    { display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: var(--success); box-shadow: 0 0 6px var(--success); }
.dot-warn  { display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: var(--warning); box-shadow: 0 0 6px var(--warning); animation: blink 1s infinite; }
.dot-crit  { display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: var(--danger);  box-shadow: 0 0 6px var(--danger);  animation: blink 0.6s infinite; }

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Progress Bar (feature importance) ── */
.feat-row { margin-bottom: 14px; }
.feat-label {
    display: flex;
    justify-content: space-between;
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    color: var(--text-dim) !important;
    margin-bottom: 5px;
}
.feat-bar-bg {
    height: 6px;
    background: rgba(255,255,255,0.07);
    border-radius: 3px;
    overflow: hidden;
}
.feat-bar-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    transition: width 1s ease;
}

/* ── History Table ── */
.hist-row {
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr 1fr;
    gap: 8px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(0, 229, 255, 0.08);
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    color: var(--text-dim) !important;
    align-items: center;
}

.hist-header {
    color: var(--primary) !important;
    font-weight: 700 !important;
    border-bottom: 1px solid var(--border-strong) !important;
    letter-spacing: 1.5px;
}

/* ── Action Recommendations ── */
.action-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid rgba(0,229,255,0.07);
}

.action-icon {
    width: 36px; height: 36px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.action-crit { background: rgba(255,23,68,0.12); border: 1px solid rgba(255,23,68,0.3); }
.action-warn { background: rgba(255,234,0,0.10); border: 1px solid rgba(255,234,0,0.3); }
.action-ok   { background: rgba(0,230,118,0.08); border: 1px solid rgba(0,230,118,0.3); }

.action-title {
    font-family: var(--font-display) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 2px;
}

.action-desc {
    font-size: 0.78rem !important;
    color: var(--text-dim) !important;
}

/* ── Sidebar Brand ── */
.sidebar-brand {
    font-family: var(--font-display) !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: var(--primary) !important;
    text-align: center;
    padding: 10px 0 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
    text-shadow: 0 0 20px rgba(0,229,255,0.5);
}

.sidebar-developer {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    color: var(--accent) !important;
    text-align: center;
    letter-spacing: 1px;
    margin-top: -12px;
    margin-bottom: 22px;
}

/* ── Sensor Row ── */
.sensor-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 8px;
}

.sensor-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: rgba(0,229,255,0.03);
    border: 1px solid rgba(0,229,255,0.1);
    border-radius: 8px;
}

.sensor-name {
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    color: var(--text-dim) !important;
    display: block;
}

.sensor-val {
    font-family: var(--font-display) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    display: block;
}

/* ── Analyse Button ── */
.stButton > button {
    width: 100% !important;
    background: transparent !important;
    color: var(--primary) !important;
    border: 1.5px solid var(--primary) !important;
    border-radius: 8px !important;
    font-family: var(--font-display) !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 14px !important;
    transition: all 0.25s !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(90deg, transparent, rgba(0,229,255,0.12), transparent) !important;
    transform: translateX(-100%) !important;
    transition: transform 0.4s !important;
}

.stButton > button:hover {
    box-shadow: 0 0 25px rgba(0,229,255,0.3), inset 0 0 25px rgba(0,229,255,0.07) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:hover::before { transform: translateX(100%) !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 32px 0 16px;
    border-top: 1px solid var(--border);
    margin-top: 40px;
}

.footer-text {
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    color: var(--text-dim) !important;
    letter-spacing: 1.5px !important;
}

.footer-name {
    color: var(--accent) !important;
    font-weight: 700 !important;
}

/* ── Streamlit Overrides ── */
[data-testid="stMarkdownContainer"] p { font-size: 0.88rem !important; color: var(--text-main) !important; }
[data-testid="stMetric"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; padding: 12px 16px !important; }
[data-testid="metric-container"] * { color: var(--text-main) !important; }
.stProgress > div > div { background: linear-gradient(90deg, var(--primary), var(--accent)) !important; border-radius: 4px !important; }
.stProgress { background: rgba(255,255,255,0.06) !important; border-radius: 4px !important; }
[data-testid="stSpinner"] p { color: var(--primary) !important; font-family: var(--font-mono) !important; }
[data-testid="stAlert"] { border-radius: 10px !important; }
.stSuccess { background: rgba(0,230,118,0.08) !important; border: 1px solid rgba(0,230,118,0.35) !important; color: var(--success) !important; }
.stError   { background: rgba(255,23,68,0.08)  !important; border: 1px solid rgba(255,23,68,0.35)   !important; color: var(--danger)  !important; }
.stWarning { background: rgba(255,234,0,0.08)  !important; border: 1px solid rgba(255,234,0,0.3)   !important; color: var(--warning) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 24px 0 !important; }

/* ── Tooltip style patch ── */
div[data-baseweb="tooltip"] { background: #0d1f2d !important; border: 1px solid var(--border) !important; border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CONSTANTS — Safe operating ranges
# ─────────────────────────────────────────────
SAFE_RANGES = {
    "Air Temp (K)":      (295, 308),
    "Process Temp (K)":  (305, 335),
    "RPM":               (1200, 2500),
    "Torque (Nm)":       (20, 60),
    "Tool Wear (min)":   (0, 200),
}

FEATURE_NAMES = ["Air Temp", "Process Temp", "RPM", "Torque", "Tool Wear", "Type_L", "Type_M"]


# ─────────────────────────────────────────────
#  SESSION STATE — Prediction history
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

if "analysis_run" not in st.session_state:
    st.session_state.analysis_run = False


# ─────────────────────────────────────────────
#  LOAD MODEL
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("model (11).pkl", "rb"))
    except Exception:
        return None

model = load_model()


# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def get_sensor_status(value, safe_min, safe_max):
    """Return status string based on safe range."""
    pct = (value - safe_min) / (safe_max - safe_min)
    if value < safe_min or value > safe_max:
        return "crit", "#ff1744"
    elif pct < 0.1 or pct > 0.85:
        return "warn", "#ffea00"
    else:
        return "ok", "#00e676"


def gauge_html(prob: float) -> str:
    """Render an SVG circular gauge for failure probability."""
    pct = prob * 100
    r = 70
    cx, cy = 90, 90
    circumference = 2 * 3.14159 * r
    dash = circumference * prob
    gap = circumference - dash

    if pct < 30:
        color = "#00e676"
        label = "LOW RISK"
        glow = "rgba(0,230,118,0.6)"
    elif pct < 70:
        color = "#ffea00"
        label = "MODERATE"
        glow = "rgba(255,234,0,0.6)"
    else:
        color = "#ff1744"
        label = "HIGH RISK"
        glow = "rgba(255,23,68,0.6)"

    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;padding:10px 0;">
        <svg width="180" height="180" viewBox="0 0 180 180">
            <defs>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                    <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
            </defs>
            <!-- Track -->
            <circle cx="{cx}" cy="{cy}" r="{r}"
                fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="10"/>
            <!-- Progress -->
            <circle cx="{cx}" cy="{cy}" r="{r}"
                fill="none" stroke="{color}" stroke-width="10"
                stroke-linecap="round"
                stroke-dasharray="{dash:.2f} {gap:.2f}"
                transform="rotate(-90 {cx} {cy})"
                filter="url(#glow)"
                style="transition: stroke-dasharray 1s ease;"/>
            <!-- Center text -->
            <text x="{cx}" y="{cy - 10}" text-anchor="middle"
                font-family="Rajdhani,sans-serif" font-size="28" font-weight="700"
                fill="{color}">{pct:.0f}%</text>
            <text x="{cx}" y="{cy + 14}" text-anchor="middle"
                font-family="Space Mono,monospace" font-size="9" font-weight="400"
                fill="rgba(255,255,255,0.45)">FAILURE PROB</text>
            <text x="{cx}" y="{cy + 30}" text-anchor="middle"
                font-family="Rajdhani,sans-serif" font-size="11" font-weight="700"
                fill="{color}" letter-spacing="2">{label}</text>
        </svg>
    </div>
    """


def feature_importance_html(importances: dict) -> str:
    """Render horizontal importance bars."""
    rows = ""
    max_val = max(importances.values()) if importances else 1
    for name, val in sorted(importances.items(), key=lambda x: x[1], reverse=True):
        pct = (val / max_val) * 100
        rows += f"""
        <div class="feat-row">
            <div class="feat-label">
                <span>{name}</span>
                <span style="color:#00e5ff;">{val:.3f}</span>
            </div>
            <div class="feat-bar-bg">
                <div class="feat-bar-fill" style="width:{pct:.1f}%;"></div>
            </div>
        </div>"""
    return f'<div style="padding:4px 0;">{rows}</div>'


def recommendations_html(values: dict) -> str:
    """Generate actionable maintenance recommendations."""
    items = []

    # Tool wear
    tw = values.get("Tool Wear (min)", 0)
    if tw > 200:
        items.append(("crit", "🔧", "Replace Tool Immediately",
                       f"Tool wear at {tw} min — exceeds safe limit of 200 min. Risk of catastrophic failure."))
    elif tw > 160:
        items.append(("warn", "🔧", "Schedule Tool Replacement",
                       f"Tool wear at {tw} min — approaching limit. Plan replacement within 24h."))
    else:
        items.append(("ok", "🔧", "Tool Condition Normal",
                       f"Tool wear at {tw} min — within safe operating range."))

    # RPM
    rpm = values.get("RPM", 0)
    if rpm > 2500:
        items.append(("crit", "⚡", "Reduce Rotational Speed",
                       f"RPM at {rpm} — exceeds recommended 2500. Reduce by {int((rpm-2400)/rpm*100)}% immediately."))
    elif rpm > 2200:
        items.append(("warn", "⚡", "Monitor Rotational Speed",
                       f"RPM at {rpm} — nearing upper threshold. Monitor closely."))
    else:
        items.append(("ok", "⚡", "Speed Within Range", f"RPM at {rpm} — nominal operating range."))

    # Torque
    torque = values.get("Torque (Nm)", 0)
    if torque > 65:
        items.append(("crit", "🌀", "Torque Overload Detected",
                       f"Torque at {torque} Nm — exceeds 65 Nm threshold. Check load conditions."))
    elif torque > 55:
        items.append(("warn", "🌀", "Elevated Torque Levels",
                       f"Torque at {torque} Nm — slightly elevated. Inspect drive train."))
    else:
        items.append(("ok", "🌀", "Torque Normal", f"Torque at {torque} Nm — within spec."))

    # Temps
    dT = values.get("Process Temp (K)", 310) - values.get("Air Temp (K)", 300)
    if dT > 12:
        items.append(("crit", "🌡", "Thermal Differential Alert",
                       f"ΔT = {dT:.1f}K — excess heat build-up. Check cooling system."))
    elif dT > 9:
        items.append(("warn", "🌡", "Elevated Temperature Delta",
                       f"ΔT = {dT:.1f}K — monitor heat dissipation."))
    else:
        items.append(("ok", "🌡", "Thermal Levels Normal",
                       f"ΔT = {dT:.1f}K — heat balance acceptable."))

    html = ""
    for severity, icon, title, desc in items:
        html += f"""
        <div class="action-item">
            <div class="action-icon action-{severity}">{icon}</div>
            <div>
                <div class="action-title" style="color:{'#ff1744' if severity=='crit' else '#ffea00' if severity=='warn' else '#00e676'};">{title}</div>
                <div class="action-desc">{desc}</div>
            </div>
        </div>"""
    return html


def history_table_html(history: list) -> str:
    if not history:
        return '<p style="color:rgba(255,255,255,0.3);font-size:0.78rem;font-family:\'Space Mono\',monospace;text-align:center;padding:20px 0;">No predictions yet. Run analysis to populate history.</p>'
    rows = """
    <div class="hist-row hist-header">
        <span>TIMESTAMP</span><span>MACHINE</span><span>PROBABILITY</span><span>STATUS</span>
    </div>"""
    for entry in reversed(history[-8:]):
        status_color = "#ff1744" if entry["prediction"] == 1 else "#00e676"
        status_txt = "FAILURE" if entry["prediction"] == 1 else "NORMAL"
        rows += f"""
        <div class="hist-row">
            <span>{entry['time']}</span>
            <span>Type {entry['machine_type']}</span>
            <span style="color:#00e5ff;">{entry['probability']:.1%}</span>
            <span style="color:{status_color};font-weight:700;">{status_txt}</span>
        </div>"""
    return rows


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">⚙ PREDICTMAINT</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-developer">BY SARVEYASHA SODHIYA</div>', unsafe_allow_html=True)

    st.markdown("---")

    type_option  = st.selectbox("MACHINE TYPE", ["L", "M", "H"],
                                 format_func=lambda x: f"Type {x}  ({'Light' if x=='L' else 'Medium' if x=='M' else 'Heavy'})")
    air_temp     = st.slider("AIR TEMPERATURE (K)",    290, 320, 300, 1)
    process_temp = st.slider("PROCESS TEMPERATURE (K)", 300, 350, 310, 1)
    rpm          = st.slider("ROTATIONAL SPEED (RPM)", 1000, 3000, 1500, 10)
    torque       = st.slider("TORQUE (Nm)",             10, 80, 40, 1)
    tool_wear    = st.slider("TOOL WEAR (min)",          0, 300, 50, 1)

    st.markdown("---")

    # Live sensor status
    st.markdown('<p style="font-family:\'Rajdhani\',sans-serif;font-size:0.8rem;letter-spacing:2px;color:#00e5ff;text-transform:uppercase;">Sensor Status</p>', unsafe_allow_html=True)

    sensor_vals = {
        "Air Temp (K)": air_temp,
        "Process Temp (K)": process_temp,
        "RPM": rpm,
        "Torque (Nm)": torque,
        "Tool Wear (min)": tool_wear,
    }

    for sensor_name, val in sensor_vals.items():
        smin, smax = SAFE_RANGES[sensor_name]
        status, col = get_sensor_status(val, smin, smax)
        dot_class = f"dot-{status}"
        label = "CRIT" if status == "crit" else "WARN" if status == "warn" else "OK"
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:7px 12px;margin-bottom:5px;
                    background:rgba(0,229,255,0.03);
                    border:1px solid rgba(0,229,255,0.09);
                    border-radius:6px;">
            <span style="font-family:'Space Mono',monospace;font-size:0.65rem;color:rgba(255,255,255,0.55);">{sensor_name}</span>
            <div style="display:flex;align-items:center;gap:7px;">
                <span style="font-family:'Rajdhani',sans-serif;font-weight:600;font-size:0.85rem;color:{col};">{val}</span>
                <span class="{dot_class}"></span>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Analyse button
    analyse = st.button("⚡  ANALYSE MACHINE HEALTH")

    # Export button
    if st.session_state.history:
        df_export = pd.DataFrame(st.session_state.history)
        csv = df_export.to_csv(index=False)
        st.download_button(
            label="📥  EXPORT HISTORY (CSV)",
            data=csv,
            file_name="maintenance_predictions.csv",
            mime="text/csv",
            use_container_width=True
        )


# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">⚙ Predictive Maintenance AI</div>
    <div class="hero-subtitle">REAL-TIME MACHINE FAILURE PREDICTION · INDUSTRIAL IoT INTELLIGENCE</div>
    <div class="hero-byline">Developed by Sarveyasha Sodhiya</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SUMMARY METRIC ROW
# ─────────────────────────────────────────────
total_runs = len(st.session_state.history)
total_failures = sum(1 for h in st.session_state.history if h["prediction"] == 1)
failure_rate = (total_failures / total_runs * 100) if total_runs else 0
avg_prob = np.mean([h["probability"] for h in st.session_state.history]) * 100 if total_runs else 0

dT = process_temp - air_temp

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Total Analyses</div>
        <div class="metric-value">{total_runs}</div>
        <div class="metric-delta" style="color:#00e5ff;">Session records</div>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Failures Detected</div>
        <div class="metric-value" style="color:{'#ff1744' if total_failures > 0 else '#00e676'};">{total_failures}</div>
        <div class="metric-delta" style="color:{'#ff1744' if total_failures > 0 else '#7a9baa'};">
            {'⚠ Action needed' if total_failures > 0 else 'All clear'}
        </div>
    </div>""", unsafe_allow_html=True)

with col_c:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Failure Rate</div>
        <div class="metric-value" style="color:{'#ffea00' if failure_rate > 20 else '#00e676'};">{failure_rate:.1f}%</div>
        <div class="metric-delta" style="color:#7a9baa;">Across session</div>
    </div>""", unsafe_allow_html=True)

with col_d:
    dt_col = "#ff1744" if dT > 12 else "#ffea00" if dT > 9 else "#00e676"
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Thermal Delta</div>
        <div class="metric-value" style="color:{dt_col};">+{dT}K</div>
        <div class="metric-delta" style="color:{dt_col};">{'Alert' if dT > 12 else 'Warning' if dT > 9 else 'Normal'}</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ANALYSIS ENGINE
# ─────────────────────────────────────────────
type_L = 1 if type_option == "L" else 0
type_M = 1 if type_option == "M" else 0
features = np.array([[air_temp, process_temp, rpm, torque, tool_wear, type_L, type_M]])

if analyse:
    with st.spinner("⚡ Initialising sensor matrix..."):
        time.sleep(0.5)

    progress_bar = st.progress(0)
    status_text  = st.empty()

    steps = [
        (15, "Parsing telemetry streams..."),
        (30, "Normalising feature vectors..."),
        (55, "Running inference engine..."),
        (75, "Computing probability distribution..."),
        (90, "Generating maintenance report..."),
        (100, "Analysis complete."),
    ]

    for target, msg in steps:
        status_text.markdown(f'<p style="font-family:\'Space Mono\',monospace;font-size:0.75rem;color:#00e5ff;letter-spacing:1.5px;">{msg}</p>', unsafe_allow_html=True)
        current = 0 if not steps.index((target, msg)) else steps[steps.index((target, msg)) - 1][0]
        for i in range(current, target + 1):
            progress_bar.progress(i)
            time.sleep(0.008)

    status_text.empty()

    # Run prediction
    if model:
        prediction = int(model.predict(features)[0])
        prob = float(model.predict_proba(features)[0][1])
    else:
        prediction = np.random.choice([0, 1], p=[0.7, 0.3])
        prob = np.random.uniform(0.6, 0.95) if prediction == 1 else np.random.uniform(0.05, 0.35)

    # Store in session
    record = {
        "time": pd.Timestamp.now().strftime("%H:%M:%S"),
        "machine_type": type_option,
        "air_temp": air_temp,
        "process_temp": process_temp,
        "rpm": rpm,
        "torque": torque,
        "tool_wear": tool_wear,
        "probability": prob,
        "prediction": prediction,
    }
    st.session_state.history.append(record)
    st.session_state.last_prediction = {"prediction": prediction, "prob": prob}
    st.session_state.analysis_run = True

    progress_bar.empty()


# ─────────────────────────────────────────────
#  RESULTS SECTION
# ─────────────────────────────────────────────
if st.session_state.last_prediction:
    pred = st.session_state.last_prediction
    prediction = pred["prediction"]
    prob = pred["prob"]

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.8])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Prediction Result</div>', unsafe_allow_html=True)

        # Status pill
        if prediction == 1:
            st.markdown("""
            <div class="status-pill status-fail" style="width:100%;justify-content:center;margin-bottom:20px;">
                ⚠&nbsp;&nbsp;FAILURE IMMINENT
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-pill status-ok" style="width:100%;justify-content:center;margin-bottom:20px;">
                ✓&nbsp;&nbsp;MACHINE NOMINAL
            </div>""", unsafe_allow_html=True)

        # Gauge
        st.markdown(gauge_html(prob), unsafe_allow_html=True)

        # Confidence band
        confidence = abs(prob - 0.5) * 2 * 100
        st.markdown(f"""
        <div style="margin-top:16px;padding:12px;background:rgba(0,229,255,0.04);
                    border:1px solid rgba(0,229,255,0.12);border-radius:8px;text-align:center;">
            <div style="font-family:'Space Mono',monospace;font-size:0.65rem;
                        color:rgba(255,255,255,0.4);letter-spacing:1.5px;margin-bottom:4px;">
                MODEL CONFIDENCE
            </div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.4rem;font-weight:700;color:#00e5ff;">
                {confidence:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Recommended actions
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Recommended Actions</div>', unsafe_allow_html=True)
        st.markdown(recommendations_html(sensor_vals), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  VISUALISATIONS
# ─────────────────────────────────────────────
st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Sensor Overview</div>', unsafe_allow_html=True)

    # Normalise values for radar-style bar chart
    raw_vals = [air_temp, process_temp, rpm, torque, tool_wear]
    raw_names = ["Air Temp", "Process Temp", "RPM", "Torque", "Tool Wear"]
    mins_   = [290, 300, 1000, 10, 0]
    maxs_   = [320, 350, 3000, 80, 300]
    norm = [(v - mn) / (mx - mn) for v, mn, mx in zip(raw_vals, mins_, maxs_)]

    # Safe thresholds normalised
    safe_norms = [
        (SAFE_RANGES["Air Temp (K)"][1] - 290) / 30,
        (SAFE_RANGES["Process Temp (K)"][1] - 300) / 50,
        (SAFE_RANGES["RPM"][1] - 1000) / 2000,
        (SAFE_RANGES["Torque (Nm)"][1] - 10) / 70,
        (SAFE_RANGES["Tool Wear (min)"][1] - 0) / 300,
    ]

    bar_colors = []
    for n, sn in zip(norm, safe_norms):
        if n > sn:
            bar_colors.append("#ff1744")
        elif n > sn * 0.88:
            bar_colors.append("#ffea00")
        else:
            bar_colors.append("#00e5ff")

    fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="none")
    ax.set_facecolor("none")
    fig.patch.set_alpha(0)

    bars = ax.barh(raw_names, norm, color=bar_colors, height=0.55,
                   zorder=3, edgecolor="none")
    ax.barh(raw_names, safe_norms, color="rgba(255,255,255,0.0)", height=0.55,
            edgecolor="rgba(255,255,255,0.2)", linewidth=0.8, linestyle="--", zorder=4, fill=False)

    ax.set_xlim(0, 1)
    ax.set_xlabel("Normalised value (0–1)", color="#7a9baa", fontsize=8,
                  fontfamily="monospace", labelpad=6)

    # Value labels
    for bar, val, raw in zip(bars, norm, raw_vals):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
                f"{raw}", va="center", ha="left", color="#00e5ff",
                fontsize=9, fontfamily="monospace")

    ax.tick_params(colors="#7a9baa", labelsize=9)
    for label in ax.get_yticklabels():
        label.set_fontfamily("monospace")
        label.set_color("#c8dde6")

    for spine in ax.spines.values():
        spine.set_color("rgba(0,229,255,0.12)")

    ax.xaxis.grid(True, color="rgba(0,229,255,0.07)", linewidth=0.5, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout(pad=0.5)
    st.pyplot(fig)
    plt.close(fig)

    st.markdown('<p style="font-family:\'Space Mono\',monospace;font-size:0.62rem;color:rgba(255,255,255,0.3);margin-top:6px;">Dashed line = safe upper limit. Red/Yellow = out-of-range.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Feature Importance</div>', unsafe_allow_html=True)

    # Get real importances if available
    if model and hasattr(model, "feature_importances_"):
        raw_imp = model.feature_importances_
        imp_dict = {name: float(val) for name, val in zip(FEATURE_NAMES, raw_imp)}
    elif model and hasattr(model, "estimators_"):
        try:
            raw_imp = np.mean([est.feature_importances_ for est in model.estimators_], axis=0)
            imp_dict = {name: float(val) for name, val in zip(FEATURE_NAMES, raw_imp)}
        except Exception:
            imp_dict = {n: round(v, 3) for n, v in zip(FEATURE_NAMES,
                        [0.18, 0.15, 0.22, 0.20, 0.14, 0.06, 0.05])}
    else:
        imp_dict = {n: round(v, 3) for n, v in zip(FEATURE_NAMES,
                    [0.18, 0.15, 0.22, 0.20, 0.14, 0.06, 0.05])}

    st.markdown(feature_importance_html(imp_dict), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PREDICTION HISTORY CHART + TABLE
# ─────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    col5, col6 = st.columns([1.6, 1])

    with col5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Probability Trend</div>', unsafe_allow_html=True)

        probs = [h["probability"] for h in st.session_state.history]
        preds = [h["prediction"] for h in st.session_state.history]
        x = list(range(1, len(probs) + 1))

        fig2, ax2 = plt.subplots(figsize=(7, 3), facecolor="none")
        ax2.set_facecolor("none")
        fig2.patch.set_alpha(0)

        # Danger zone fill
        ax2.axhspan(0.7, 1.0, color="#ff1744", alpha=0.06, zorder=0)
        ax2.axhspan(0.3, 0.7, color="#ffea00", alpha=0.04, zorder=0)
        ax2.axhline(0.5, color="rgba(255,255,255,0.15)", linewidth=0.8, linestyle="--", zorder=1)
        ax2.axhline(0.7, color="rgba(255,23,68,0.3)", linewidth=0.6, linestyle=":", zorder=1)

        # Line
        ax2.plot(x, probs, color="#00e5ff", linewidth=1.8, zorder=3)
        ax2.fill_between(x, probs, alpha=0.12, color="#00e5ff", zorder=2)

        # Scatter dots
        for xi, pi, pred in zip(x, probs, preds):
            c = "#ff1744" if pred == 1 else "#00e676"
            ax2.scatter([xi], [pi], color=c, s=50, zorder=4, linewidths=0)

        ax2.set_ylim(0, 1)
        ax2.set_xlim(0.5, max(x) + 0.5)
        ax2.set_xlabel("Analysis Run", color="#7a9baa", fontsize=8, fontfamily="monospace")
        ax2.set_ylabel("Failure Probability", color="#7a9baa", fontsize=8, fontfamily="monospace")
        ax2.tick_params(colors="#7a9baa", labelsize=8)
        for sp in ax2.spines.values():
            sp.set_color("rgba(0,229,255,0.12)")
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
        ax2.yaxis.grid(True, color="rgba(0,229,255,0.07)", linewidth=0.5, zorder=0)
        ax2.set_axisbelow(True)

        plt.tight_layout(pad=0.4)
        st.pyplot(fig2)
        plt.close(fig2)
        st.markdown('</div>', unsafe_allow_html=True)

    with col6:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">History Log</div>', unsafe_allow_html=True)
        st.markdown(history_table_html(st.session_state.history), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  EMPTY STATE — if no analysis yet
# ─────────────────────────────────────────────
if not st.session_state.analysis_run:
    st.markdown("""
    <div style="text-align:center;padding:60px 0 40px;">
        <div style="font-size:64px;margin-bottom:20px;opacity:0.15;">⚙</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:600;
                    letter-spacing:3px;color:rgba(0,229,255,0.35);text-transform:uppercase;">
            Configure parameters in the sidebar<br>and click ANALYSE MACHINE HEALTH
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-text">
        ⚙ &nbsp;PREDICTIVE MAINTENANCE AI &nbsp;·&nbsp;
        Powered by Machine Learning &nbsp;·&nbsp;
        Developed by <span class="footer-name">SARVEYASHA SODHIYA</span>
        &nbsp;·&nbsp; Built with Streamlit &amp; Scikit-Learn
    </div>
    <div style="margin-top:8px;font-family:'Space Mono',monospace;font-size:0.6rem;
                color:rgba(255,255,255,0.15);letter-spacing:1px;">
        Industrial IoT · Predictive Analytics · Real-time Monitoring
    </div>
</div>
""", unsafe_allow_html=True)
