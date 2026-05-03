import math

class ScanEngine:
    """
    Simulated geospatial signal analysis engine.
    (NO REAL MINERAL DETECTION CLAIMS)
    """

    def analyze(self, lat, lon):
        lat = float(lat)
        lon = float(lon)

        # deterministic pseudo-science model (safe simulation)
        seed = abs(math.sin(lat * lon))

        return {
            "coordinates": {"lat": lat, "lon": lon},
            "signals": {
                "density_index": round(seed * 100, 2),
                "anomaly_score": round((1 - seed) * 50, 2)
            },
            "classification": "simulated_scan"
        }
