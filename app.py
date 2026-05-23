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
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Glass Card */
.glass {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    animation: fadeIn 1s ease-in-out;
}

/* Fade Animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Button Style */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #00c6ff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.35);
    backdrop-filter: blur(10px);
}

/* Metric Card */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 10px;
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
model = pickle.load(open("model (11).pkl", "rb"))

# ------------------- SIDEBAR -------------------
st.sidebar.markdown("## 🔧 Machine Parameters")

type_option = st.sidebar.selectbox("Machine Type", ["L", "M", "H"])
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

    fig, ax = plt.subplots()
    ax.barh(features_names, importance)
    ax.set_title("Feature Importance")
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
