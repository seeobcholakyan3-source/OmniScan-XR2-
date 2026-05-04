import requests
from requests.auth import HTTPBasicAuth
from config import Config

class NASAClient:

    @staticmethod
    def get_earth_imagery(lat, lon):
        url = f"{Config.NASA_API_BASE}/planetary/earth/assets"
        params = {
            "lat": lat,
            "lon": lon,
            "api_key": Config.NASA_API_KEY
        }

        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()

    @staticmethod
    def get_emit_data():
        # Example Earthdata protected endpoint
        url = "https://data.lpdaac.earthdatacloud.nasa.gov/s3credentials"

        res = requests.get(
            url,
            auth=HTTPBasicAuth(
                Config.EARTHDATA_USERNAME,
                Config.EARTHDATA_PASSWORD
            ),
            timeout=10
        )

        res.raise_for_status()
        return res.json()
