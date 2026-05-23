# app.py
# Romania Energy Platform — single Streamlit app, three tabs:
#   Tab 1: Energy Dashboard  (your original dashboard.py)
#   Tab 2: Site Map          (interactive map of scored locations)
#   Tab 3: Rankings & Stats  (bar chart, scatter, tables)
#
# Run with:  streamlit run app.py

import time
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

from extract import extract_energy_data
from transform import transform_energy_data
from locations import LOCATIONS
from score import score_location

# ── Config ────────────────────────────────────────────────────────────────────
DB_URL     = "postgresql://postgres:dnd@localhost:5432/energy_pipeline"
START_DATE = "2023-01-01"
END_DATE   = "2023-12-31"
SLEEP_S    = 1

METRIC_LABELS = {
    "composite_score": "Composite Score",
    "wind_score":      "Wind Score",
    "solar_score":     "Solar Score",
    "mean_wind_ms":    "Mean Wind Speed (m/s)",
    "capacity_factor": "Capacity Factor",
}

REGION_COLORS = {
    "Dobrogea":    "#e63946",
    "Moldova":     "#457b9d",
    "Muntenia":    "#2a9d8f",
    "Transilvania":"#e9c46a",
    "Carpathians": "#f4a261",
}

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]


# ── Data loaders ──────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_dashboard_data() -> pd.DataFrame:
    engine = create_engine(DB_URL)
    df = pd.read_sql("SELECT * FROM energy_readings", engine)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


@st.cache_data(show_spinner=False)
def run_recommender_pipeline() -> pd.DataFrame:
    results  = []
    progress = st.progress(0, text="Starting pipeline…")
    for i, loc in enumerate(LOCATIONS):
        try:
            raw    = extract_energy_data(loc["lat"], loc["lon"], START_DATE, END_DATE)
            df     = transform_energy_data(raw)
            scored = score_location(df, loc)
            results.append(scored)
        except Exception as e:
            st.warning(f"⚠️ Skipped {loc['name']}: {e}")
        progress.progress(
            (i + 1) / len(LOCATIONS),
            text=f"Fetched {loc['name']} ({i + 1}/{len(LOCATIONS)})",
        )
        time.sleep(SLEEP_S)
    progress.empty()
    return pd.DataFrame(results)


# ── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Romania Energy Platform",
    layout="wide",
    page_icon="⚡",
)

st.title("⚡ Romania Energy Platform")

tab_dash, tab_map, tab_stats = st.tabs([
    "📈  Energy Dashboard",
    "🗺️  Site Map",
    "📊  Rankings & Stats",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — ENERGY DASHBOARD (original dashboard.py)
# ════════════════════════════════════════════════════════════════════════════
with tab_dash:
    st.subheader("🌬️ Romania Energy Dashboard")
    st.caption("Hourly wind & solar data — Timișoara region, 2024")

    df_dash = load_dashboard_data()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Hours Tracked",  f"{len(df_dash):,}")
    col2.metric("Avg Wind Speed",        f"{df_dash['windspeed_kmh'].mean():.1f} km/h")
    col3.metric("Avg Solar Radiation",   f"{df_dash['solar_radiation_wm2'].mean():.1f} W/m²")

    st.subheader("☀️ Monthly Solar Radiation")
    monthly_solar = df_dash.groupby(df_dash["timestamp"].dt.month)["solar_radiation_wm2"].mean().round(2)
    monthly_solar.index = pd.CategoricalIndex(MONTHS, categories=MONTHS, ordered=True)
    st.line_chart(monthly_solar)

    st.subheader("💨 Monthly Wind Speed")
    monthly_wind = df_dash.groupby(df_dash["timestamp"].dt.month)["windspeed_kmh"].mean().round(2)
    monthly_wind.index = pd.CategoricalIndex(MONTHS, categories=MONTHS, ordered=True)
    st.line_chart(monthly_wind)

    st.subheader("⏰ Average Output by Hour of Day")
    hourly = df_dash.groupby(df_dash["timestamp"].dt.hour).agg(
        avg_wind=("windspeed_kmh",        "mean"),
        avg_solar=("solar_radiation_wm2", "mean"),
    ).round(2)
    st.line_chart(hourly)

    st.subheader("📋 Raw Data")
    st.dataframe(
        df_dash.sort_values("timestamp", ascending=False).head(100),
        use_container_width=True,
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — SITE MAP
# ════════════════════════════════════════════════════════════════════════════
with tab_map:
    st.subheader("🗺️ Wind Farm Site Recommender — Romania")
    st.caption(f"Scoring {len(LOCATIONS)} candidate sites · {START_DATE} to {END_DATE} · Open-Meteo API")

    with st.spinner("Running ETL pipeline… (~2 min on first run, cached after)"):
        df_rec = run_recommender_pipeline()

    best = df_rec.loc[df_rec["composite_score"].idxmax()]
    st.success(
        f"🏆 **Top recommendation: {best['name']}** ({best['region']})  ·  "
        f"Composite {best['composite_score']:.1f}/100  ·  "
        f"Wind CF {best['capacity_factor']:.1%}  ·  "
        f"Mean wind {best['mean_wind_ms']:.1f} m/s"
    )

    col_ctrl, col_map = st.columns([1, 4])
    with col_ctrl:
        st.markdown("#### Display options")
        metric = st.selectbox(
            "Color by",
            options=list(METRIC_LABELS.keys()),
            format_func=lambda x: METRIC_LABELS[x],
        )
        show_labels = st.toggle("Show site labels", value=True)

    with col_map:
        fig_map = px.scatter_mapbox(
            df_rec,
            lat="lat", lon="lon",
            color=metric,
            size="composite_score",
            hover_name="name",
            text="name" if show_labels else None,
            hover_data={
                "region":          True,
                "composite_score": ":.1f",
                "wind_score":      ":.1f",
                "solar_score":     ":.1f",
                "mean_wind_ms":    ":.2f",
                "capacity_factor": ":.1%",
                "lat":             False,
                "lon":             False,
            },
            color_continuous_scale="RdYlGn",
            size_max=35,
            zoom=5.8,
            center={"lat": 45.9, "lon": 25.0},
            mapbox_style="carto-positron",
        )
        fig_map.update_traces(textposition="top center")
        fig_map.update_layout(
            margin={"r": 0, "t": 10, "l": 0, "b": 0},
            height=560,
            coloraxis_colorbar=dict(title=METRIC_LABELS[metric]),
        )
        st.plotly_chart(fig_map, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — RANKINGS & STATS
# ════════════════════════════════════════════════════════════════════════════
with tab_stats:
    # df_rec is already loaded by tab 2's cache call — no re-fetch
    try:
        df_rec
    except NameError:
        with st.spinner("Loading data…"):
            df_rec = run_recommender_pipeline()

    df_sorted = df_rec.sort_values("composite_score", ascending=False)

    st.markdown("#### Composite Score by Site")
    fig_bar = px.bar(
        df_sorted,
        x="name", y="composite_score",
        color="region",
        color_discrete_map=REGION_COLORS,
        hover_data={"wind_score": True, "solar_score": True, "capacity_factor": True},
        labels={"composite_score": "Composite Score (0–100)", "name": ""},
        height=380,
    )
    fig_bar.update_layout(xaxis_tickangle=-35, margin={"t": 20, "b": 10}, legend_title="Region")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### Wind Score vs Solar Score")
    fig_scatter = px.scatter(
        df_rec,
        x="wind_score", y="solar_score",
        color="region", size="composite_score",
        hover_name="name",
        color_discrete_map=REGION_COLORS,
        labels={"wind_score": "Wind Score (0–100)", "solar_score": "Solar Score (0–100)"},
        height=380,
    )
    fig_scatter.update_layout(margin={"t": 20})
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("#### Full Rankings Table")
    display_cols = [
        "name", "region", "composite_score", "wind_score", "solar_score",
        "mean_wind_ms", "p90_wind_ms", "capacity_factor", "mean_solar_wm2",
    ]
    st.dataframe(
        df_sorted[display_cols]
            .reset_index(drop=True)
            .style
            .background_gradient(subset=["composite_score"], cmap="RdYlGn")
            .format({
                "composite_score": "{:.1f}",
                "wind_score":      "{:.1f}",
                "solar_score":     "{:.1f}",
                "mean_wind_ms":    "{:.2f}",
                "p90_wind_ms":     "{:.2f}",
                "capacity_factor": "{:.1%}",
                "mean_solar_wm2":  "{:.0f}",
            }),
        use_container_width=True,
        height=500,
    )

    st.markdown("#### Average Scores by Region")
    region_summary = (
        df_rec.groupby("region")[["composite_score", "wind_score", "solar_score"]]
              .mean().round(1)
              .sort_values("composite_score", ascending=False)
    )
    st.dataframe(region_summary, use_container_width=True)
