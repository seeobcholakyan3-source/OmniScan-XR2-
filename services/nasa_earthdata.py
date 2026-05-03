import os
import requests


class NasaEarthData:

    def __init__(self):
        self.api_key = os.getenv("NASA_API_KEY")
        self.base_url = "https://api.nasa.gov/planetary/earth/assets"

        if not self.api_key:
            raise ValueError("NASA_API_KEY not set in environment")

    def get_asset_metadata(self, lat, lon):
        """
        Fetch metadata about available satellite imagery at a location.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "api_key": self.api_key
        }

        response = requests.get(self.base_url, params=params, timeout=10)

        if response.status_code != 200:
            return {
                "error": "Failed to fetch NASA data",
                "status": response.status_code
            }

        return response.json()
