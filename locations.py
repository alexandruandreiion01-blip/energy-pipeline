# locations.py
# 18 Romanian candidate sites for wind farm siting analysis.
# Dobrogea (SE) dominates Romania's real installed wind capacity.
# We also include Moldavia and the Wallachian plain for comparison.

LOCATIONS = [
    # Dobrogea — Romania's primary wind belt
    {"name": "Constanța",       "lat": 44.18, "lon": 28.65, "region": "Dobrogea"},
    {"name": "Tulcea",          "lat": 45.18, "lon": 28.80, "region": "Dobrogea"},
    {"name": "Cernavodă",       "lat": 44.33, "lon": 28.03, "region": "Dobrogea"},
    {"name": "Mangalia",        "lat": 43.82, "lon": 28.58, "region": "Dobrogea"},
    {"name": "Fântânele",       "lat": 44.60, "lon": 28.50, "region": "Dobrogea"},

    # Moldavian Plateau — good secondary wind corridor
    {"name": "Iași",            "lat": 47.16, "lon": 27.59, "region": "Moldova"},
    {"name": "Vaslui",          "lat": 46.64, "lon": 27.73, "region": "Moldova"},
    {"name": "Bârlad",          "lat": 46.23, "lon": 27.67, "region": "Moldova"},
    {"name": "Suceava",         "lat": 47.65, "lon": 26.25, "region": "Moldova"},

    # Wallachian Plain — flat, consistent wind
    {"name": "Buzău",           "lat": 45.15, "lon": 26.82, "region": "Muntenia"},
    {"name": "Brăila",          "lat": 45.27, "lon": 27.96, "region": "Muntenia"},
    {"name": "Călărași",        "lat": 44.20, "lon": 27.33, "region": "Muntenia"},
    {"name": "Giurgiu",         "lat": 43.90, "lon": 25.97, "region": "Muntenia"},

    # Transylvania — lower wind, high solar, hybrid interest
    {"name": "Cluj-Napoca",     "lat": 46.77, "lon": 23.59, "region": "Transilvania"},
    {"name": "Sibiu",           "lat": 45.80, "lon": 24.15, "region": "Transilvania"},
    {"name": "Brașov",          "lat": 45.65, "lon": 25.61, "region": "Transilvania"},

    # Carpathian passes — high-elevation wind
    {"name": "Predeal Pass",    "lat": 45.51, "lon": 25.58, "region": "Carpathians"},
    {"name": "Vrancea Ridge",   "lat": 45.80, "lon": 26.80, "region": "Carpathians"},
]
