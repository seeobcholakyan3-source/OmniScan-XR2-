import math
from database import SessionLocal, ScanRecord


class ScanEngine:
    """
    Deterministic geospatial analysis engine.
    Stores scan results into database for persistence + retrieval.
    """

    def analyze(self, lat, lon):
        lat = float(lat)
        lon = float(lon)

        # -----------------------------
        # Core deterministic signal model
        # -----------------------------
        seed = abs(math.sin(lat * 12.9898 + lon * 78.233))

        density_index = round(seed * 100, 2)
        anomaly_score = round((1 - seed) * 50, 2)

        result = {
            "coordinates": {
                "lat": lat,
                "lon": lon
            },
            "signals": {
                "density_index": density_index,
                "anomaly_score": anomaly_score
            },
            "classification": self._classify(density_index, anomaly_score)
        }

        # -----------------------------
        # Persist to database safely
        # -----------------------------
        self._save_to_db(lat, lon, density_index, anomaly_score, result["classification"])

        return result

    def _classify(self, density, anomaly):
        if density > 70:
            return "high_density_zone"
        elif anomaly > 30:
            return "high_variance_zone"
        return "stable_region"

    def _save_to_db(self, lat, lon, density, anomaly, classification):
        db = SessionLocal()
        try:
            record = ScanRecord(
                lat=lat,
                lon=lon,
                density_index=density,
                anomaly_score=anomaly,
                classification=classification
            )
            db.add(record)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[DB ERROR] {e}")
        finally:
            db.close()
