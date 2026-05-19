import requests

def extract_energy_data(latitude, longitude, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "windspeed_10m,shortwave_radiation,temperature_2m"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return data

if __name__ == "__main__":
    raw_data = extract_energy_data(
        latitude=45.75,
        longitude=21.23,
        start_date="2024-01-01",
        end_date="2024-01-07"
    )
    print(raw_data)