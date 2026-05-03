import math

class GeoAnalyzer:

    def compute(self, lat, lon):

        lat_r = math.radians(lat)
        lon_r = math.radians(lon)

        curvature = abs(math.sin(lat_r) * math.cos(lon_r))
        stability = 1 - (curvature * 0.6)
        complexity = (abs(lat % 7) + abs(lon % 5)) / 10

        return {
            "terrain_curvature": round(curvature, 4),
            "stability_index": round(stability, 4),
            "surface_complexity": round(complexity, 4)
        }
