import random

from services.nasa_earthdata import NasaEarthData


class SatelliteIngestion:

    def __init__(self):
        self.nasa = NasaEarthData()

    def process_location(self, lat, lon):
        """
        Combines real NASA metadata with simulated spectral extraction.
        (Full real spectral extraction requires GeoTIFF processing — next phase)
        """

        nasa_data = self.nasa.get_asset_metadata(lat, lon)

        if "error" in nasa_data:
            return {
                "source": "nasa",
                "error": nasa_data
            }

        # -------------------------------------------------
        # TEMPORARY FEATURE EXTRACTION (REALISTIC HYBRID)
        # -------------------------------------------------
        # We don't yet download raster images (next upgrade),
        # so we simulate spectral features but BASED on real availability.

        date = nasa_data.get("date", "unknown")

        spectral_features = {
            "mean_reflectance": random.uniform(0.2, 0.9),
            "variance": random.uniform(0.05, 0.4),
            "ndvi_proxy": random.uniform(-0.2, 0.8)
        }

        return {
            "source": "nasa",
            "metadata": {
                "date": date,
                "id": nasa_data.get("id")
            },
            "satellite_features": spectral_features
        }
