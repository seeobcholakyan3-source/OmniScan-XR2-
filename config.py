import os

class Config:
    NASA_API_KEY = os.getenv("NASA_API_KEY")
    NASA_API_BASE = os.getenv("NASA_API_BASE", "https://api.nasa.gov")

    EARTHDATA_USERNAME = os.getenv("EARTHDATA_USERNAME")
    EARTHDATA_PASSWORD = os.getenv("EARTHDATA_PASSWORD")
