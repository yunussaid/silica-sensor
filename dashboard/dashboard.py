# Run 'streamlit run dashboard.py' after activating .venv to start the dashboard
# This URL: https://www.phdata.io/blog/how-to-use-the-gauge-chart-template/ has guage pointer
import streamlit as st
import plotly.graph_objects as go
import time
import pandas as pd
import numpy as np

# 1. Setup Streamlit Page
st.set_page_config(page_title="Silica Soft Sensor", layout="wide")
st.title("🏭 % Silica Concentrate - Soft Sensor Dashboard")
st.write("Simulating real-time model inference on test data.")

# 2 Simulate or Load your Test Data
if 'step' not in st.session_state:
    st.session_state.step = 0

# 2.1 Load prediction and actual data from CSV files
pred_path = "dashboard/y_pred.csv"
actual_path = "dashboard/y_true.csv"
pred_df = pd.read_csv(pred_path)
actual_df = pd.read_csv(actual_path)
pred_col = pred_df.columns[-1]
actual_col = actual_df.columns[-1]
pred = pred_df[pred_col].to_numpy()
actual = actual_df[actual_col].to_numpy()

if len(actual) != len(pred):
    min_len = min(len(actual), len(pred))
    pred = pred[:min_len]
    actual = actual[:min_len]

# 2.2 Mocking some predictions and actual values between 0.6% and 5.53%
np.random.seed(42)
mock_pred = np.random.uniform(0.6, 5.53, 100)
mock_actual = np.clip(mock_pred + np.random.uniform(0.0, 1.0, len(mock_pred)), 0, 6)
current_val = mock_pred[st.session_state.step]

# 3. Simulation settings and helper functions
SIMULATION_DURATION = 0.25  # seconds between temporally adjacent readings
INTERPOLATION_FRAMES = 1  # number of subframes for each transition
if 'playing' not in st.session_state:
    st.session_state.playing = False

plot_col, gauge_col = st.columns([2, 1], gap="large")
with plot_col:
    plot_placeholder = st.empty()
with gauge_col:
    placeholder = st.empty()

def draw_gauge(value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        number = {'suffix': '%', 'font': {'size': 80}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "% Silica Gauge", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [0, 6], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "white"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0.0, 0.75],  'color': '#008a7b'},
                {'range': [0.75, 1.5],  'color': '#00a86b'},
                {'range': [1.5, 2.25],  'color': '#4cd137'},
                {'range': [2.25, 3.0],  'color': '#a4e433'},
                {'range': [3.0, 3.75],  'color': '#fcd116'},
                {'range': [3.75, 4.5],  'color': '#ff9f2a'},
                {'range': [4.5, 5.25],  'color': '#ff6f28'},
                {'range': [5.25, 6.0],  'color': '#ff3b30'},
            ]
        }
    ))
    fig.update_layout(paper_bgcolor = "#0E1117", font = {'color': "white", 'family': "Arial"})
    placeholder.plotly_chart(fig, use_container_width=True)

def draw_prediction_plot(step):
    x = np.arange(1, step + 2)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=mock_pred[:step + 1],
        mode='lines+markers',
        name='Predicted',
        line={'color': '#1f77b4'},
        marker={'size': 6}
    ))
    fig.add_trace(go.Scatter(
        x=x,
        y=mock_actual[:step + 1],
        mode='lines+markers',
        name='Actual',
        line={'color': '#ff7f0e'},
        marker={'size': 6}
    ))
    fig.update_layout(
        title='Predicted vs Actual % Silica',
        xaxis_title='Sample Index',
        yaxis_title='% Silica',
        xaxis=dict(range=[1, len(mock_pred)], dtick=10),
        yaxis=dict(range=[0, 6]),
        legend=dict(yanchor='top', y=0.95, xanchor='left', x=0.02),
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        font={'color': 'white', 'family': 'Arial'}
    )
    plot_placeholder.plotly_chart(fig, use_container_width=True)

# 4. Display the Gauge and Prediction Plot in Streamlit
current_val = mock_pred[st.session_state.step]
draw_gauge(current_val)
draw_prediction_plot(st.session_state.step)

# 5. Playback Controls
_, controls_col, _ = st.columns([1, 1, 1], gap="small")
with controls_col:
    button_col1, button_col2, button_col3 = st.columns([1, 1, 1], gap="medium")
    with button_col1:
        if st.button("Next ➡️", disabled=st.session_state.playing, use_container_width=True):
            if st.session_state.step < len(mock_pred) - 1:
                st.session_state.step += 1
                st.rerun()
    with button_col2:
        if st.button("Reset 🔄", use_container_width=True):
            st.session_state.step = 0
            st.session_state.playing = False
            st.rerun()
    with button_col3:
        if st.button("Play ▶️", disabled=st.session_state.playing, use_container_width=True):
            st.session_state.step = 0
            st.session_state.playing = True
            st.rerun()

if st.session_state.playing:
    for next_step in range(st.session_state.step + 1, len(mock_pred)):
        start_val = mock_pred[st.session_state.step]
        end_val = mock_pred[next_step]
        for frame in range(1, INTERPOLATION_FRAMES + 1):
            interp_value = start_val + (end_val - start_val) * (frame / INTERPOLATION_FRAMES)
            draw_gauge(interp_value)
            time.sleep(SIMULATION_DURATION / INTERPOLATION_FRAMES)
        st.session_state.step = next_step
        draw_prediction_plot(st.session_state.step)
    st.session_state.playing = False

st.caption(f"Current Sample Index: {st.session_state.step + 1} / {len(mock_pred)}")