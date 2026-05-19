from sqlalchemy import create_engine, text
from sqlalchemy import create_engine

def load_energy_data(df):
    engine = create_engine("postgresql://postgres:dnd@localhost:5432/energy_pipeline")
    
    with engine.connect() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO energy_readings (timestamp, windspeed_kmh, solar_radiation_wm2, temperature_c)
                VALUES (:timestamp, :windspeed, :solar, :temp)
                ON CONFLICT (timestamp) DO NOTHING
            """), {
                "timestamp": row["timestamp"],
                "windspeed": row["windspeed_kmh"],
                "solar": row["solar_radiation_wm2"],
                "temp": row["temperature_c"]
            })
        conn.commit()
    
    print(f"Loaded {len(df)} rows into the database")

if __name__ == "__main__":
    from extract import extract_energy_data
    from transform import transform_energy_data
    
    raw = extract_energy_data(45.75, 21.23, "2024-01-01", "2024-01-07")
    clean = transform_energy_data(raw)
    load_energy_data(clean)