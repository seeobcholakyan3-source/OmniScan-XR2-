"""
Mineral Classification Model (Lightweight AI)

- No heavy ML dependencies (Termux-safe)
- Uses statistical + spectral heuristics
- Designed to be replaced later with real ML model
"""

import numpy as np
import logging

logger = logging.getLogger("MineralModel")


class MineralClassifier:
    def __init__(self):
        logger.info("MineralClassifier initialized")

    def extract_features(self, spectral_data: np.ndarray) -> dict:
        """
        Extract meaningful features from spectral data
        """
        return {
            "mean": float(np.mean(spectral_data)),
            "std": float(np.std(spectral_data)),
            "max": float(np.max(spectral_data)),
            "min": float(np.min(spectral_data)),
        }

    def classify(self, spectral_data: np.ndarray) -> dict:
        """
        Classify mineral likelihood based on spectral characteristics
        """

        if spectral_data is None or len(spectral_data) == 0:
            logger.warning("Empty spectral data received")
            return {
                "label": "no_data",
                "confidence": 0.0
            }

        features = self.extract_features(spectral_data)

        mean_val = features["mean"]
        std_val = features["std"]

        # Heuristic classification (replace later with ML model)
        if mean_val > 0.75 and std_val > 0.2:
            label = "high_confidence_mineral"
            confidence = 0.9
        elif mean_val > 0.5:
            label = "possible_mineral"
            confidence = 0.65
        else:
            label = "low_probability"
            confidence = 0.3

        logger.info(f"Classification result: {label} ({confidence})")

        return {
            "label": label,
            "confidence": confidence,
            "features": features
        }


# Singleton instance (shared across app)
classifier = MineralClassifier()
