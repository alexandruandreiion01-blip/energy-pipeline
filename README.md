# ⚡ Romania Energy Platform

A data engineering portfolio project built for renewable energy site analysis in Romania. Combines a live ETL pipeline with an interactive multi-location wind farm site recommender.

---

## What It Does

Two tools in one Streamlit app, three tabs, one browser tab:

**📈 Energy Dashboard** — pulls hourly wind speed, solar radiation, and temperature data for a single location via the Open-Meteo Archive API, loads it into PostgreSQL, and visualizes monthly and hourly trends.

**🗺️ Site Map** — runs the same ETL pipeline across 18 candidate locations across Romania, scores each one using industry-standard wind energy metrics, and plots them on an interactive map color-coded by score.

**📊 Rankings & Stats** — full site rankings table, composite score bar chart by region, and a wind vs solar scatter plot.

---

## Scoring Model

Each site is scored on three signals derived from a full year of hourly data:

| Signal | Weight | Why |
|---|---|---|
| Capacity Factor Proxy | 40% | % of hours in turbine operating range (3–25 m/s) — the primary KPI operators report |
| Mean Wind Speed | 35% | Raw energy potential; wind power scales with the cube of speed |
| P90 Wind Speed | 25% | Speed exceeded 90% of the time — the conservative estimate lenders use |

Wind score (70%) and solar score (30%) are combined into a composite 0–100 score. Weights are transparent and adjustable in `score.py`.

Dobrogea (SE Romania) is expected to dominate rankings, consistent with where Romania's actual installed wind capacity is concentrated.

---

## Project Structure

```
energy-pipeline/
├── app.py           # Main Streamlit app — all 3 tabs
├── extract.py       # Open-Meteo API fetcher
├── transform.py     # Cleans and normalizes raw API response
├── load.py          # Loads data into PostgreSQL
├── pipeline.py      # Runs the single-location ETL end to end
├── locations.py     # 18 Romanian candidate sites with coordinates
├── score.py         # Scoring logic (capacity factor, P90, composite)
├── requirements.txt
└── run_all.bat      # Windows launcher — double-click to start
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/alexandruandreiion01-blip/energy-pipeline
cd energy-pipeline
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up PostgreSQL**

Create a database called `energy_pipeline` and run the original pipeline once to populate it:
```bash
python pipeline.py
```

The default connection string is `postgresql://postgres:dnd@localhost:5432/energy_pipeline`. Update it in `app.py` and `load.py` if yours differs.

**4. Run the app**
```bash
streamlit run app.py
```
Or on Windows, double-click `run_all.bat`.

The Site Map tab fetches 18 locations on first load (~2 minutes). Results are cached for the session — instant after that.

---

## Data Source

[Open-Meteo Archive API](https://open-meteo.com/) — free, no API key required. Variables used: `windspeed_10m`, `shortwave_radiation`, `temperature_2m`.

---

## Tech Stack

`Python` · `Streamlit` · `PostgreSQL` · `SQLAlchemy` · `Plotly` · `Pandas` · `Open-Meteo API`
