import requests
from config import Config

class NASAClient:
    """
    Safe wrapper for NASA APIs.
    NOTE: Requires valid API key + approved usage.
    """

    def get_metadata(self, lat, lon):
        if not Config.NASA_API_KEY:
            return {
                "error": "NASA_API_KEY missing",
                "fallback": True
            }

        try:
            # Example placeholder endpoint (not mineral detection!)
            url = f"{Config.NASA_API_URL}/planetary/apod"
            response = requests.get(url, params={
                "api_key": Config.NASA_API_KEY
            }, timeout=10)

            return response.json()

        except Exception as e:
            return {
                "error": str(e),
                "fallback": True
            }
