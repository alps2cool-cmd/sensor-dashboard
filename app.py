import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Sensor Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Real-Time Sensor Monitoring Dashboard")
st.markdown("---")

# Sidebar controls
st.sidebar.header("Controls")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 10, 3)
sensor_id = st.sidebar.selectbox("Select Sensor", ["All", "Sensor-A", "Sensor-B", "Sensor-C"])

# Generate mock sensor data
def generate_sensor_data():
    data = []
    for i in range(100):
        timestamp = datetime.now() - timedelta(minutes=i)
        for sensor in ["Sensor-A", "Sensor-B", "Sensor-C"]:
            temperature = 20 + random.uniform(-5, 15)
            humidity = 50 + random.uniform(-20, 20)
            data.append({
                "timestamp": timestamp,
                "sensor": sensor,
                "temperature": round(temperature, 1),
                "humidity": round(humidity, 1)
            })
    return pd.DataFrame(data)

# Load data
df = generate_sensor_data()

# Filter data
if sensor_id != "All":
    df = df[df["sensor"] == sensor_id]

# Create metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Average Temperature", f"{df['temperature'].mean():.1f}°C", 
              f"{df['temperature'].iloc[-1] - df['temperature'].iloc[0]:.1f}°C")

with col2:
    st.metric("Average Humidity", f"{df['humidity'].mean():.1f}%",
              f"{df['humidity'].iloc[-1] - df['humidity'].iloc[0]:.1f}%")

with col3:
    st.metric("Max Temperature", f"{df['temperature'].max():.1f}°C")

with col4:
    st.metric("Min Temperature", f"{df['temperature'].min():.1f}°C")

# Temperature Chart
st.subheader("🌡️ Temperature Trends")
fig_temp = px.line(df, x="timestamp", y="temperature", color="sensor",
                   title="Temperature Over Time")
st.plotly_chart(fig_temp, use_container_width=True)

# Humidity Chart
st.subheader("💧 Humidity Trends")
fig_hum = px.line(df, x="timestamp", y="humidity", color="sensor",
                  title="Humidity Over Time")
st.plotly_chart(fig_hum, use_container_width=True)

# Data table
with st.expander("📋 View Raw Data"):
    st.dataframe(df.sort_values("timestamp", ascending=False))

# Auto-refresh
if st.button("Refresh Data"):
    st.rerun()

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")