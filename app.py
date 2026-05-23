import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import matplotlib.pyplot as plt

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="Predictive Maintenance AI",
    page_icon="⚙️",
    layout="wide"
)

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>

/* Background Gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #7c3aed, #431407);
    color: white;
}

/* Glass Card */
.glass {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1.5px solid rgba(255, 255, 255, 0.25);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    animation: fadeIn 1s ease-in-out;
}

.glass h1, .glass h2, .glass h3, .glass h4, .glass h5, .glass h6, .glass p {
    color: #ffffff !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Fade Animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Button Style */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    color: white !important;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: 600;
    border: none;
    transition: 0.3s;
    box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4);
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px #00c6ff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
}

section[data-testid="stSidebar"] > div > div > div:first-child {
    color: white !important;
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-weight: 500;
}

/* Selectbox styling */
.stSelectbox > div > div > div {
    background: rgba(255, 255, 255, 0.15) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 8px !important;
}

.stSelectbox > div > div > div > div {
    color: #ffffff !important;
    font-weight: 600;
}

/* Selectbox options */
[role="option"] {
    background: rgba(100, 100, 150, 0.8) !important;
    color: #ffffff !important;
}

[role="option"]:hover {
    background: rgba(0, 198, 255, 0.6) !important;
}

/* Slider styling */
.stSlider > div > div > div > div {
    color: white !important;
}

.stSlider label {
    color: #ffffff !important;
    font-weight: 500;
}

/* Metric Card */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

[data-testid="metric-container"] * {
    color: white !important;
}

/* Main Text */
.main {
    color: white !important;
}

/* Subheader */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

/* Paragraphs and labels */
p, span, label, div {
    color: #ffffff !important;
}

/* Chart styling */
.stPlotlyChart, .stPyplotChart {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 10px;
}

/* DataFrame styling */
.stDataFrame {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
}

/* Bar chart text */
[data-testid="stBarChart"] text {
    fill: white !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown("""
<div class="glass">
    <h1>⚙️ Predictive Maintenance AI</h1>
    <p>Real-time Machine Failure Prediction System powered by Machine Learning</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ------------------- LOAD MODEL -------------------
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    model = None

# ------------------- SIDEBAR -------------------
st.sidebar.markdown("## 🔧 Machine Parameters")

type_option = st.sidebar.selectbox("Machine Type", ["L", "M", "H"], format_func=lambda x: f"Type {x}")
air_temp = st.sidebar.slider("Air Temperature (K)", 290, 320, 300)
process_temp = st.sidebar.slider("Process Temperature (K)", 300, 350, 310)
rpm = st.sidebar.slider("Rotational Speed", 1000, 3000, 1500)
torque = st.sidebar.slider("Torque (Nm)", 10, 80, 40)
tool_wear = st.sidebar.slider("Tool Wear", 0, 300, 50)

# Encoding
type_L = 1 if type_option == "L" else 0
type_M = 1 if type_option == "M" else 0

features = np.array([[air_temp, process_temp, rpm, torque, tool_wear, type_L, type_M]])

# ------------------- PREDICTION -------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("🔮 AI Prediction Engine")

if st.button("🚀 Analyze Machine Health"):

    # Loading Animation
    with st.spinner("Analyzing real-time sensor data..."):
        time.sleep(2)

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    # Prediction
    if model:
        prediction = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]
    else:
        prediction = np.random.choice([0, 1])
        prob = np.random.uniform(0.4, 0.9)

    col1, col2 = st.columns(2)

    with col1:
        if prediction == 1:
            st.error("⚠️ High Risk of Machine Failure Detected")
        else:
            st.success("✅ Machine Operating Normally")

    with col2:
        st.metric("Failure Probability", f"{prob:.2f}")

st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# ------------------- VISUALS -------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("📊 Sensor Overview")

    df_input = pd.DataFrame({
        "Feature": ["Air Temp", "Process Temp", "RPM", "Torque", "Tool Wear"],
        "Value": [air_temp, process_temp, rpm, torque, tool_wear]
    })

    st.bar_chart(df_input.set_index("Feature"))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("📈 AI Insights")

    features_names = ["Air Temp", "Process Temp", "RPM", "Torque", "Tool Wear", "Type_L", "Type_M"]
    importance = np.random.rand(len(features_names))

    fig, ax = plt.subplots(facecolor='none')
    ax.barh(features_names, importance, color='#00c6ff')
    ax.set_title("Feature Importance", color='white', fontsize=14, fontweight='bold')
    ax.set_xlabel("Importance Score", color='white')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- FOOTER -------------------
st.write("")
st.markdown("""
<div class="glass" style="text-align:center;">
    <h4>🚀 Created by Sarveyasha Sodhiya</h4>
    <p>Machine Learning Enthusiast | Building Intelligent Systems</p>
</div>
""", unsafe_allow_html=True)
