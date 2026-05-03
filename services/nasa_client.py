import requests
from config import Config

class NASAClient:

    def get_earth_imagery(self, lat, lon):

        url = f"{Config.NASA_API_URL}/planetary/earth/imagery"

        params = {
            "lat": lat,
            "lon": lon,
            "dim": 0.1,
            "api_key": Config.NASA_API_KEY
        }

        try:
            r = requests.get(url, params=params, timeout=15)

            return {
                "status_code": r.status_code,
                "content_type": r.headers.get("content-type"),
                "ok": r.status_code == 200
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}
