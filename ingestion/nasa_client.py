import requests
from core.config import Config
from core.logger import get_logger

logger = get_logger("NASAClient")

class NASAClient:
    def __init__(self):
        self.api_key = Config.NASA_API_KEY
        self.base_url = Config.NASA_BASE_URL

    def fetch_earth_data(self, lat, lon):
        """
        Uses NASA Earth API (placeholder endpoint structure)
        Replace endpoint depending on dataset (MODIS / EMIT / etc.)
        """
        try:
            url = f"{self.base_url}/planetary/earth/imagery"
            params = {
                "lat": lat,
                "lon": lon,
                "api_key": self.api_key
            }

            logger.info(f"Fetching NASA data for {lat},{lon}")
            response = requests.get(url, params=params, timeout=10)

            return response.json()

        except Exception as e:
            logger.error(f"NASA fetch error: {e}")
            return {"error": "NASA data unavailable"}
