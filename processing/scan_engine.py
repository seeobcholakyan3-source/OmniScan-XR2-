import numpy as np
from ingestion.nasa_client import NASAClient
from core.logger import get_logger

logger = get_logger("ScanEngine")

class ScanEngine:
    def __init__(self):
        self.nasa = NASAClient()

    def compute_mineral_signature(self, spectral_data):
        """
        Lightweight analytical model (replaces scikit-learn)
        """
        try:
            if not spectral_data:
                return self._fallback()

            # simulate spectral extraction logic
            swir1 = spectral_data.get("swir1", 0.5)
            swir2 = spectral_data.get("swir2", 0.5)

            gold_score = float(np.clip((swir1 / (swir2 + 1e-6)), 0, 1))
            diamond_score = float(np.clip((swir2 / (swir1 + 1e-6)), 0, 1))

            return {
                "gold_probability": round(gold_score, 3),
                "diamond_indicator": round(diamond_score, 3)
            }

        except Exception as e:
            logger.error(f"Scan error: {e}")
            return self._fallback()

    def _fallback(self):
        return {
            "gold_probability": 0.0,
            "diamond_indicator": 0.0
        }

    def scan(self, lat, lon):
        nasa_data = self.nasa.fetch_earth_data(lat, lon)

        spectral = {
            "swir1": nasa_data.get("swir1", 0.5),
            "swir2": nasa_data.get("swir2", 0.5)
        }

        result = self.compute_mineral_signature(spectral)

        return {
            "status": "active",
            "coordinates": {"lat": lat, "lon": lon},
            "minerals": result,
            "source": "NASA_EARTH_PIPELINE_V2"
        }
