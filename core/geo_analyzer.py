import math

class GeoAnalyzer:
    """
    Deterministic geospatial feature extraction engine.
    Ready for ML upgrade later.
    """

    def compute(self, lat, lon):

        lat_r = math.radians(lat)
        lon_r = math.radians(lon)

        # Terrain curvature approximation
        curvature = abs(math.sin(lat_r) * math.cos(lon_r))

        # Stability heuristic
        stability = 1 - (curvature * 0.6)

        # Surface complexity estimate
        complexity = (abs(lat % 7) + abs(lon % 5)) / 10

        return {
            "terrain_curvature": round(curvature, 4),
            "stability_index": round(stability, 4),
            "surface_complexity": round(complexity, 4)
        }
