class MineralModel:
    """
    Placeholder for future ML upgrade (LightGBM / CNN)
    """

    def predict(self, features):
        # deterministic fallback model
        return {
            "gold_probability": 0.5,
            "diamond_indicator": 0.5
        }
