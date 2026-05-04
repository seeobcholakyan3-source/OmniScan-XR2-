import os
import requests

NASA_API_KEY = os.getenv("5CJUyYN64yan5HgMDGqvZ1TNwzl9SbyOhZ8rlhs2")

BASE_URL = "https://api.nasa.gov/planetary/earth/imagery"

def fetch_nasa_imagery(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "dim": 0.1,
        "api_key": NASA_API_KEY
    }

    response = requests.get(BASE_URL, params=params, timeout=15)

    if response.status_code != 200:
        return {
            "error": "NASA request failed",
            "status_code": response.status_code
        }

    # NASA returns image URL metadata
    return {
        "image_url": response.url,
        "source": "NASA_EARTH_IMAGERY"
    }
