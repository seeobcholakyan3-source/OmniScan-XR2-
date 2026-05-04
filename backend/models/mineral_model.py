import numpy as np


def predict_minerals(features):
    """
    Simple baseline model (placeholder for real ML model)
    """

    score = (
        features["mean"] * 0.4 +
        features["std"] * 0.3 +
        features["max"] * 0.2
    )

    gold_probability = float(min(max(score, 0), 1))
    diamond_indicator = float(features["max"] * 0.5)

    return {
        "gold_probability": round(gold_probability, 3),
        "diamond_indicator": round(diamond_indicator, 3),
        "model": "baseline_v1"
    }
