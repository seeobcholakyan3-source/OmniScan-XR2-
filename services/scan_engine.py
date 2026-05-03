import math

from database import SessionLocal, ScanRecord
from services.satellite_ingestion import SatelliteIngestion
from services.ai_model import AnomalyModel


class ScanEngine:

    def __init__(self):
        self.satellite = SatelliteIngestion()
        self.ai = AnomalyModel()

    def analyze(self, lat, lon):
        lat = float(lat)
        lon = float(lon)

        # -----------------------------
        # SATELLITE LAYER
        # -----------------------------
        sat_data = self.satellite.process_location(lat, lon)
        spectral = sat_data["satellite_features"]

        density_index = spectral["mean_reflectance"] * 100
        anomaly_score = spectral["variance"] * 100

        # -----------------------------
        # AI LAYER (NEW)
        # -----------------------------
        ai_result = self.ai.predict(density_index, anomaly_score)

        classification = self._classify(
            density_index,
            anomaly_score,
            ai_result["is_anomaly"]
        )

        result = {
            "coordinates": {"lat": lat, "lon": lon},
            "satellite": sat_data,
            "signals": {
                "density_index": round(density_index, 2),
                "anomaly_score": round(anomaly_score, 2)
            },
            "ai": ai_result,
            "classification": classification
        }

        self._save(lat, lon, density_index, anomaly_score, classification)

        return result

    def _classify(self, density, anomaly, ai_flag):
        if ai_flag:
            return "ai_detected_anomaly_zone"
        if density > 65:
            return "high_density_region"
        return "normal_region"

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
