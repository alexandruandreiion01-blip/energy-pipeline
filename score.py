# score.py
# Scoring model for wind farm site suitability.
# Uses industry-standard metrics: capacity factor proxy and P90 wind speed.

# Turbine operating thresholds (industry standard)
WIND_CUT_IN_MS  = 3.0   # m/s — below this, turbines don't spin
WIND_CUT_OUT_MS = 25.0  # m/s — above this, turbines shut down for safety

KMH_TO_MS = 1 / 3.6


def score_location(df, location: dict) -> dict:
    """
    Collapse a year of hourly readings into a single scored record.

    Scoring model:
      wind_score (0-100):    weighted blend of mean wind speed,
                             capacity factor proxy, and P90 wind
      solar_score (0-100):   normalized mean solar irradiance
      composite (0-100):     70% wind + 30% solar (wind-first weighting)
    """
    wind_ms = df["windspeed_kmh"] * KMH_TO_MS

    mean_wind = wind_ms.mean()
    # P90: the speed exceeded 90% of the time (conservative/bankable estimate)
    p90_wind  = wind_ms.quantile(0.10)

    # Capacity factor proxy: fraction of hours in productive operating window
    productive       = (wind_ms >= WIND_CUT_IN_MS) & (wind_ms <= WIND_CUT_OUT_MS)
    capacity_factor  = productive.mean()

    mean_solar = df["solar_radiation_wm2"].mean()

    # --- Normalize each signal to 0–100 ---
    # Benchmarks for Romanian/European wind context:
    #   6 m/s mean ≈ decent (~67), 9+ m/s ≈ excellent (capped at 100)
    wind_speed_score = min(mean_wind / 9.0 * 100, 100)
    wind_cf_score    = capacity_factor * 100          # already a 0–1 fraction
    wind_p90_score   = min(p90_wind / 7.0 * 100, 100)

    # CF weighted most heavily — it's the most bankable single metric
    wind_score = (
        0.40 * wind_cf_score +
        0.35 * wind_speed_score +
        0.25 * wind_p90_score
    )

    # 200 W/m² annual mean ≈ good for Romania
    solar_score = min(mean_solar / 200.0 * 100, 100)

    composite = 0.70 * wind_score + 0.30 * solar_score

    return {
        "name":            location["name"],
        "region":          location["region"],
        "lat":             location["lat"],
        "lon":             location["lon"],
        "mean_wind_ms":    round(mean_wind, 2),
        "p90_wind_ms":     round(p90_wind, 2),
        "capacity_factor": round(capacity_factor, 3),
        "mean_solar_wm2":  round(mean_solar, 1),
        "wind_score":      round(wind_score, 1),
        "solar_score":     round(solar_score, 1),
        "composite_score": round(composite, 1),
    }
