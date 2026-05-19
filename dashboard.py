import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

def load_data():
    engine = create_engine("postgresql://postgres:dnd@localhost:5432/energy_pipeline")
    df = pd.read_sql("SELECT * FROM energy_readings", engine)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

df = load_data()

st.set_page_config(page_title="Romania Energy Dashboard", layout="wide")
st.title("🌬️ Romania Energy Dashboard")
st.caption("Hourly wind & solar data — Timișoara region, 2024")

col1, col2, col3 = st.columns(3)
col1.metric("Total Hours Tracked", f"{len(df):,}")
col2.metric("Avg Wind Speed", f"{df['windspeed_kmh'].mean():.1f} km/h")
col3.metric("Avg Solar Radiation", f"{df['solar_radiation_wm2'].mean():.1f} W/m²")

st.subheader("☀️ Monthly Solar Radiation")
monthly_solar = df.groupby(df["timestamp"].dt.month)["solar_radiation_wm2"].mean().round(2)
monthly_solar.index = pd.CategoricalIndex(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    categories=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    ordered=True
)
st.line_chart(monthly_solar)

st.subheader("💨 Monthly Wind Speed")
monthly_wind = df.groupby(df["timestamp"].dt.month)["windspeed_kmh"].mean().round(2)
monthly_wind.index = pd.CategoricalIndex(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    categories=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    ordered=True
)
st.line_chart(monthly_wind)

st.subheader("⏰ Average Output by Hour of Day")
hourly = df.groupby(df["timestamp"].dt.hour).agg(
    avg_wind=("windspeed_kmh", "mean"),
    avg_solar=("solar_radiation_wm2", "mean")
).round(2)
st.line_chart(hourly)

st.subheader("📋 Raw Data")
st.dataframe(df.sort_values("timestamp", ascending=False).head(100), use_container_width=True)