import numpy as np

class DatasetBuilder:

    def build_features(self, geo_data, nasa_data):
        """
        Converts raw geospatial + NASA data into ML-ready vector.
        """

        features = []

        # deterministic geo features
        features.append(geo_data["terrain_curvature"])
        features.append(geo_data["stability_index"])
        features.append(geo_data["surface_complexity"])

        # NASA placeholder extraction (safe parsing layer)
        try:
            img_score = 0.0
            if nasa_data and nasa_data.get("status_code") == 200:
                img_score = 1.0
        except:
            img_score = 0.0

        features.append(img_score)

        return np.array(features, dtype=float)
