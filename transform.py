import pandas as pd

def transform_energy_data(raw_data):
    hourly = raw_data["hourly"]
    
    df = pd.DataFrame({
        "timestamp": hourly["time"],
        "windspeed_kmh": hourly["windspeed_10m"],
        "solar_radiation_wm2": hourly["shortwave_radiation"],
        "temperature_c": hourly["temperature_2m"]
    })
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.dropna()
    
    return df

if __name__ == "__main__":
    from extract import extract_energy_data
    raw = extract_energy_data(45.75, 21.23, "2024-01-01", "2024-01-07")
    clean = transform_energy_data(raw)
    print(clean)
    print(f"\nRows: {len(clean)}")