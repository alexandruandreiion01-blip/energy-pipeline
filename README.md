
# 🌬️ Romania Energy Pipeline

An end-to-end ETL pipeline that extracts, transforms, and loads hourly renewable energy data for Romania, with an interactive analytics dashboard.

## What it does
- Extracts hourly wind speed, solar radiation, and temperature data from the [Open-Meteo Archive API](https://open-meteo.com/)
- Transforms raw API responses into clean, structured rows — dropping null values and validating data integrity
- Loads data into a PostgreSQL database with idempotent inserts (no duplicates on re-runs)
- Visualizes 8,784 hourly readings via a Streamlit dashboard

## Tech Stack
- Python (requests, pandas, sqlalchemy)
- PostgreSQL
- Streamlit

## Pipeline Structure