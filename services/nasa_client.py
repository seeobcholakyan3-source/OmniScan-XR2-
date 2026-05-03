import requests
from config import Config

class NASAClient:
    """
    Real Earth observation data client.
    """

    def get_earth_imagery(self, lat, lon):
        url = "https://api.nasa.gov/planetary/earth/imagery"

        params = {
            "lat": lat,
            "lon": lon,
            "dim": 0.1,
            "api_key": Config.NASA_API_KEY
        }

        r = requests.get(url, params=params, timeout=15)

        return {
            "status": r.status_code,
            "data": r.json() if r.headers.get("content-type") == "application/json" else None
        }
