import math

class GeoAnalyzer:

    def analyze(self, lat, lon):
        """
        Deterministic geospatial feature extraction.
        (No fake minerals, no randomness)
        """

        # Simple geospatial heuristics (placeholder logic)
        elevation_factor = abs(math.sin(lat * 0.1)) * abs(math.cos(lon * 0.1))
        terrain_variance = (lat % 10) * (lon % 10)

        vegetation_index = max(0, min(1, elevation_factor))

        return {
            "vegetation_index": round(vegetation_index, 3),
            "terrain_complexity": round(terrain_variance / 100, 3),
            "stability_score": round(1 - vegetation_index * 0.5, 3)
        }
