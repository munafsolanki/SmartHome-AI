import streamlit as st
import pandas as pd
import time
from sensors import generate_sensor_data, get_manual_data
from agent import SmartHomeAgent
from logger import log_data, get_history_df, archive_logs
from ai_module import GeminiProvider
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sternritter Smart System | Credit-Safe Mode", page_icon="🏚️", layout="wide")

# --- INITIALIZATION ---
if 'agent' not in st.session_state:
    st.session_state.agent = SmartHomeAgent()
if 'brain' not in st.session_state:
    st.session_state.brain = GeminiProvider()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'theme' not in st.session_state:
    st.session_state.theme = "Dark"
if 'last_ai_insight' not in st.session_state:
    st.session_state.last_ai_insight = "No insight requested yet. Click the button below to use 1 AI credit."

agent = st.session_state.agent
brain = st.session_state.brain

# --- STABLE THEME LOGIC ---
selected_theme = st.sidebar.selectbox(
    "UI Theme", ["Dark", "Light"], 
    index=0 if st.session_state.theme == "Dark" else 1,
    key="theme_selector"
)
st.session_state.theme = selected_theme

def load_css(theme):
    if theme == "Dark":
        bg = "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)"
        card_bg = "rgba(255, 255, 255, 0.05)"
        text_color = "#f0f0f0"
        hero_bg = "linear-gradient(90deg, #4facfe 0%, #00f2fe 100%)"
    else:
        bg = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        card_bg = "rgba(0, 0, 0, 0.05)"
        text_color = "#333333"
        hero_bg = "linear-gradient(90deg, #a1c4fd 0%, #c2e9fb 100%)"

    st.markdown(f"""
    <style>
        .stApp {{ background: {bg}; color: {text_color}; transition: all 0.5s ease; }}
        .metric-card {{ background: {card_bg}; backdrop-filter: blur(10px); border-radius: 20px; padding: 15px; border: 1px solid rgba(255,255,255,0.1); text-align: center; }}
        .decision-hero {{ background: {hero_bg}; padding: 30px; border-radius: 24px; color: #1a1a1a; margin-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

load_css(st.session_state.theme)

# --- SIDEBAR ---
with st.sidebar:
    st.title("Sternritter Control")
    st.divider()
    mode = st.radio("Simulation Mode", ["Automatic", "Manual Override"], key="sim_mode")
    st.divider()
    
    if mode == "Manual Override":
        st.subheader("Sensor Overrides")
        m_temp = st.slider("Temperature", 10, 45, 25, key="m_temp")
        m_motion = st.toggle("Motion", True, key="m_motion")
        m_time = st.slider("Hour", 0, 23, 12, key="m_time")
        m_cost = st.slider("Energy Cost ($)", 0.05, 0.8, 0.2, key="m_cost")
        m_light = st.slider("Light Level", 0, 1000, 400, key="m_light")
    
    if st.button("📦 Archive Activity Log"):
        archived_as = archive_logs()
        if archived_as: st.success(f"History archived as {archived_as}")

# --- MAIN DASHBOARD ---
with st.expander("🛠️ Advanced Gemini Brain Settings", expanded=False):
    st.write("Configure your Google Gemini API Key here.")
    new_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""), placeholder="AIzaSy...")
    if st.button("Connect Gemini Brain"):
        if new_key:
            st.session_state.brain = GeminiProvider(api_key=new_key)
            st.success("Successfully connected to Gemini")
            st.rerun()

st.title("Sternritter Smart System")
st.caption("Classical Utility Logic + On-Demand AI Intelligence")

# AI Status Widget
if brain.is_active():
    st.success("🟢 Brain Ready (Credit-Safe Mode: No background usage)")
else:
    st.error("🔴 Brain Offline. Enter an API Key in Advanced Settings to activate.")

# --- DATA FETCHING ---
if mode == "Automatic":
    sensor_data = generate_sensor_data()
else:
    sensor_data = get_manual_data(m_temp, m_motion, m_time, m_cost, m_light)

action, utilities, rule_explanation = agent.get_decision(sensor_data)

# Log to CSV (uses a placeholder if no AI insight triggered yet)
sensor_data["ai_explanation"] = st.session_state.last_ai_insight
log_data(sensor_data, utilities, action, rule_explanation)

# UI Display
st.markdown(f'<div class="decision-hero"><h3>Selected Action:</h3><h1>{action}</h1></div>', unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
with m1: st.markdown(f'<div class="metric-card">Temp<br><b>{sensor_data["temperature"]}°C</b></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card">Motion<br><b>{"YES" if sensor_data["motion"] else "NO"}</b></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card">Time<br><b>{sensor_data["time"]}:00</b></div>', unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-card">Cost<br><b>${sensor_data["energy_cost"]}</b></div>', unsafe_allow_html=True)
with m5: st.markdown(f'<div class="metric-card">Light<br><b>{sensor_data["light_intensity"]}</b></div>', unsafe_allow_html=True)

st.divider()

col_l, col_r = st.columns([1, 1])

# --- AI INSIGHT SECTION ---
with col_l:
    st.subheader("🧠 On-Demand Brain Insight")
    st.info(st.session_state.last_ai_insight)
    
    if st.button("🧠 Explain this decision (Uses 1 Credit)"):
        if brain.is_active():
            with st.spinner("Consulting Sternritter Brain..."):
                insight = brain.generate_explanation(action, sensor_data)
                st.session_state.last_ai_insight = f"AI Insight: {insight}"
                st.rerun()
        else:
            st.error("Please connect Gemini to use this feature.")
    
    st.divider()
    st.subheader("💡 Smart Living Tips")
    recommendations = ["Keep temperature above 24°C.", "Use natural light when intensity is high.", "Motion detection prevents power waste."]
    for tip in recommendations: st.write(f"🔹 {tip}")

    st.divider()
    st.write("**Adaptive Priorities:**")
    st.progress(agent.weights["comfort_w"], text=f"Comfort: {agent.weights['comfort_w']:.2f}")
    st.progress(agent.weights["energy_w"], text=f"Efficiency: {agent.weights['energy_w']:.2f}")

# --- CHATBOT SECTION ---
with col_r:
    st.subheader("💬 Sternritter AI Chatbot")
    chat_container = st.container(height=355)
    for message in st.session_state.chat_history:
        with chat_container.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("Ask about your home..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with chat_container.chat_message("user"): st.markdown(prompt)
        
        system_context = f"Current Action: {action}, Sensors: {sensor_data}"
        response = brain.get_chat_response(prompt, system_context, st.session_state.chat_history[-3:])
        
        with chat_container.chat_message("assistant"): st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

st.divider()

# History
st.subheader("📊 Activity History")
history = get_history_df()
if not history.empty:
    history['Timestamp'] = pd.to_datetime(history['Timestamp'])
    if date_range := st.date_input("Filter History", [], key="date_filter"):
        if len(date_range) == 2:
            s_d, e_d = date_range
            history = history[(history['Timestamp'].dt.date >= s_d) & (history['Timestamp'].dt.date <= e_d)]
    
    st.dataframe(history.iloc[::-1], width='stretch', height=250)
    csv = history.to_csv(index=False).encode('utf-8')
    st.download_button("Export Data", csv, "sternritter_data.csv", "text/csv")

if mode == "Automatic":
    time.sleep(3)
    st.rerun()
