import math

from database import SessionLocal, ScanRecord
from services.satellite_ingestion import SatelliteIngestion


class ScanEngine:

    def __init__(self):
        self.satellite = SatelliteIngestion()

    def analyze(self, lat, lon):
        lat = float(lat)
        lon = float(lon)

        # -----------------------------
        # SATELLITE LAYER (NEW)
        # -----------------------------
        sat_data = self.satellite.process_location(lat, lon)

        spectral = sat_data["satellite_features"]

        # -----------------------------
        # COMBINED SIGNAL MODEL
        # -----------------------------
        density_index = round(spectral["mean_reflectance"] * 100, 2)
        anomaly_score = round(spectral["variance"] * 100, 2)

        classification = self._classify(density_index, anomaly_score)

        result = {
            "coordinates": {"lat": lat, "lon": lon},
            "satellite": sat_data,
            "signals": {
                "density_index": density_index,
                "anomaly_score": anomaly_score
            },
            "classification": classification
        }

        self._save(lat, lon, density_index, anomaly_score, classification)

        return result

    def _classify(self, density, anomaly):
        if density > 65 and anomaly > 20:
            return "geo_anomaly_zone"
        elif density > 50:
            return "high_reflectance_region"
        return "normal_terrain"

    def _save(self, lat, lon, density, anomaly, classification):
        db = SessionLocal()
        try:
            db.add(ScanRecord(
                lat=lat,
                lon=lon,
                density_index=density,
                anomaly_score=anomaly,
                classification=classification
            ))
            db.commit()
        finally:
            db.close()
