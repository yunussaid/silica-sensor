# Run 'streamlit run dashboard.py' after activating .venv to start the dashboard
# This URL: https://www.phdata.io/blog/how-to-use-the-gauge-chart-template/ has guage pointer
import streamlit as st
import plotly.graph_objects as go
import time
import pandas as pd
import numpy as np

# 1. Setup Streamlit Page
st.set_page_config(page_title="Silica Soft Sensor", layout="centered")
st.title("🏭 % Silica Concentrate - Soft Sensor Dashboard")
st.write("Simulating real-time model inference on test data.")

# 2. Simulate or Load your Test Data
# (Replacing this with your actual X_test / predictions later)
if 'step' not in st.session_state:
    st.session_state.step = 0

# Mocking some predictions between 0.6% and 5.53%
np.random.seed(42)
mock_predictions = np.random.uniform(0.6, 5.53, 100)
current_val = mock_predictions[st.session_state.step]

# 3. Create the Custom Gauge Chart
fig = go.Figure(go.Indicator(
    # mode = "gauge+number+delta",
    mode = "gauge+number",
    value = current_val,
    number = {'suffix': '%', 'font': {'size': 80}},
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "% Silica Gauge", 'font': {'size': 24}},
    # delta = {'reference': 3.0, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
    gauge = {
        'axis': {'range': [0, 6], 'tickwidth': 1, 'tickcolor': "white"},
        'bar': {'color': "white"}, # The needle/pointer bar color
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0.0, 0.75],  'color': '#008a7b'},  # 1. Teal / Dark Green
            {'range': [0.75, 1.5],  'color': '#00a86b'},  # 2. Medium Green
            {'range': [1.5, 2.25],  'color': '#4cd137'},  # 3. Light Green
            {'range': [2.25, 3.0],  'color': '#a4e433'},  # 4. Lime Green
            {'range': [3.0, 3.75],  'color': '#fcd116'},  # 5. Yellow
            {'range': [3.75, 4.5],  'color': '#ff9f2a'},  # 6. Light Orange
            {'range': [4.5, 5.25],  'color': '#ff6f28'},  # 7. Dark Orange
            {'range': [5.25, 6.0],  'color': '#ff3b30'},  # 8. Red
        ]
    }
))

fig.update_layout(paper_bgcolor = "#0E1117", font = {'color': "white", 'family': "Arial"})

# 4. Display the Gauge in Streamlit
st.plotly_chart(fig, use_container_width=True)

# 5. Playback Controls
col1, col2 = st.columns(2)
with col1:
    if st.button("Next Sample ➡️"):
        if st.session_state.step < len(mock_predictions) - 1:
            st.session_state.step += 1
            st.rerun()
with col2:
    if st.button("🔄 Reset"):
        st.session_state.step = 0
        st.rerun()

st.caption(f"Current Sample Index: {st.session_state.step} / {len(mock_predictions)}")