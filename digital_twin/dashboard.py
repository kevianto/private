import streamlit as st
import pandas as pd
import os
from twin_engine import TwinEngine
from full_viz import integrated_digital_twin_viz

# Page Config
st.set_page_config(page_title="Vestas V52 Digital Twin", page_icon="🌪️", layout="wide")

# Premium CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0f172a; }
    .stApp { background: #0f172a; }
    .main-title { font-size: 2.5rem; font-weight: 800; background: linear-gradient(to right, #38bdf8, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; }
    div[data-testid="stMetric"] { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title" style="font-size: 1.8rem;">Prototype 3D Digital Twin Model for Wind Turbine Performance Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #94a3b8; margin-top: -1.5rem; font-weight: 600;">Case Study: Lake Turkana Wind Power (LTWP) Farm</p>', unsafe_allow_html=True)

# Initialize Session State
if 'engine' not in st.session_state:
    st.session_state.engine = TwinEngine()
if 'running' not in st.session_state:
    st.session_state.running = False

# Sidebar
st.sidebar.markdown("### 🌪️ VESTAS V52")
st.sidebar.markdown("---")
st.sidebar.header("🛠️ CORE CONTROLS")
base_wind = st.sidebar.slider("Ambient Wind (m/s)", 0.0, 30.0, 12.0)

if st.sidebar.button("🚀 INITIATE SYSTEM / SHUTDOWN", use_container_width=True):
    st.session_state.running = not st.session_state.running
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("**Researcher:** Christine Njoki Kiongore")
st.sidebar.markdown("**Reg No:** SRT/B/01-57933/2023")
st.sidebar.markdown("**Supervisor:** Dr. Osore")
st.sidebar.markdown("**Institution:** MMUST")

if st.sidebar.button("🔄 HARD RESET", use_container_width=True):
    st.session_state.engine.reset_history()
    st.session_state.running = False
    st.rerun()

# --- Main Layout ---
# Top Section: Smooth Integrated Viz
integrated_digital_twin_viz(base_wind, st.session_state.running)

# Bottom Section: Diagnostics
st.markdown("### 📋 System Health & Analytics")
col1, col2, col3, col4 = st.columns(4)

# Static metrics that update on slider/button change
if st.session_state.running:
    # Use the model to show predicted values in the Streamlit UI
    pwr, state = st.session_state.engine.model.calculate_power(base_wind)
    rpm = st.session_state.engine.model.calculate_rpm(base_wind)
    with col1: st.metric("Target Wind", f"{base_wind:.1f} m/s")
    with col2: st.metric("Energy Output", f"{pwr/1000:.1f} kW")
    with col3: st.metric("Rotor Speed", f"{rpm:.1f} RPM")
    with col4: st.metric("Health Score", "98%" if state != "SHUTDOWN" else "OFFLINE")

    if state == "SHUTDOWN":
        st.error("⚠️ CRITICAL: Wind speed exceeding safety limits (25 m/s).")
else:
    with col1: st.metric("Target Wind", "0.0 m/s")
    with col2: st.metric("Energy Output", "0.0 kW")
    with col3: st.metric("Rotor Speed", "0.0 RPM")
    with col4: st.metric("Health Score", "STANDBY")
    st.info("System in STANDBY mode. Visualizer is idling.")

# History is available via expander
with st.expander("📝 View Telemetry History"):
    st.dataframe(st.session_state.engine.history.iloc[::-1], use_container_width=True)
