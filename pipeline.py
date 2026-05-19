from extract import extract_energy_data
from transform import transform_energy_data
from load import load_energy_data

def run_pipeline(latitude, longitude, start_date, end_date):
    print("Starting pipeline...")
    
    print("Extracting data...")
    raw = extract_energy_data(latitude, longitude, start_date, end_date)
    
    print("Transforming data...")
    clean = transform_energy_data(raw)
    
    print("Loading data...")
    load_energy_data(clean)
    
    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline(
        latitude=45.75,
        longitude=21.23,
        start_date="2024-01-01",
        end_date="2024-12-31"
    )