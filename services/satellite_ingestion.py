import requests
import numpy as np

from services.earth_data_parser import EarthDataParser


class SatelliteIngestion:
    """
    Real-world pattern:
    - fetch satellite tile
    - decode raster
    - extract spectral features
    """

    def __init__(self):
        self.parser = EarthDataParser()

    def fetch_tile(self, lat, lon):
        """
        NOTE: This is a placeholder endpoint structure.
        Real systems would use:
        - NASA Earthdata
        - Sentinel Hub
        - Google Earth Engine
        """

        # Simulated raster matrix (replace with real API response later)
        np.random.seed(int(float(lat) * 1000) % 9999)

        fake_raster = np.random.rand(64, 64, 4)  # 4 spectral bands

        return fake_raster

    def process_location(self, lat, lon):
        raster = self.fetch_tile(lat, lon)

        features = self.parser.parse_spectral_array(raster)

        return {
            "location": {"lat": float(lat), "lon": float(lon)},
            "satellite_features": features,
            "source": "SIMULATED_SENTINEL_PIPELINE"
        }
