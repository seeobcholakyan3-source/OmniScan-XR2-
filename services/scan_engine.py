import logging
import math
from datetime import datetime

import numpy as np
from sklearn.ensemble import IsolationForest

from services.satellite_ingestion import SatelliteIngestion


logger = logging.getLogger(__name__)


class ScanEngine:
    """
    Core orchestration engine for:
    - Satellite ingestion
    - Feature engineering
    - AI anomaly detection
    - Mineral classification (heuristic + ML hybrid)
    """

    def __init__(self):
        self.satellite = SatelliteIngestion()

        # Isolation Forest for anomaly detection
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.15,
            random_state=42
        )

        # Pre-fit with baseline synthetic distribution
        self._train_baseline_model()

    # ---------------------------------------------------------
    # MODEL INITIALIZATION
    # ---------------------------------------------------------
    def _train_baseline_model(self):
        """
        Train model on baseline "normal Earth surface" distributions.
        This avoids uninitialized predictions.
        """
        try:
            baseline_data = np.array([
                [0.3, 0.1],
                [0.5, 0.2],
                [0.4, 0.15],
                [0.6, 0.25],
                [0.45, 0.18],
                [0.35, 0.12],
                [0.55, 0.22]
            ])
            self.model.fit(baseline_data)
            logger.info("IsolationForest baseline model trained")
        except Exception as e:
            logger.error(f"Model training failed: {e}")

    # ---------------------------------------------------------
    # MAIN ENTRY
    # ---------------------------------------------------------
    def scan_location(self, lat: float, lon: float) -> dict:
        """
        Main scan pipeline:
        1. Fetch satellite data
        2. Extract features
        3. Run anomaly detection
        4. Classify mineral likelihood
        """

        try:
            self._validate_coordinates(lat, lon)

            sat_data = self.satellite.process_location(lat, lon)

            if "error" in sat_data:
                return self._error_response("Satellite ingestion failed", sat_data)

            features = sat_data.get("satellite_features", {})
            metadata = sat_data.get("metadata", {})

            vector = self._build_feature_vector(features)

            anomaly_score, anomaly_flag = self._run_anomaly_detection(vector)

            classification = self._classify(features, anomaly_score)

            confidence = self._compute_confidence(features, anomaly_score)

            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),

                "location": {
                    "lat": lat,
                    "lon": lon
                },

                "satellite": {
                    "source": sat_data.get("source"),
                    "metadata": metadata,
                    "features": features
                },

                "analysis": {
                    "feature_vector": vector.tolist(),
                    "anomaly_score": float(anomaly_score),
                    "is_anomalous": bool(anomaly_flag),
                    "confidence": confidence
                },

                "classification": classification
            }

        except Exception as e:
            logger.exception("Scan failed")
            return self._error_response("Scan execution failed", str(e))

    # ---------------------------------------------------------
    # FEATURE ENGINEERING
    # ---------------------------------------------------------
    def _build_feature_vector(self, features: dict) -> np.ndarray:
        """
        Convert satellite features into ML vector.
        """

        mean_reflectance = features.get("mean_reflectance", 0.0)
        variance = features.get("variance", 0.0)
        ndvi = features.get("ndvi_proxy", 0.0)

        # Normalize + stabilize
        vector = np.array([
            float(mean_reflectance),
            float(variance + abs(ndvi) * 0.5)
        ])

        return vector

    # ---------------------------------------------------------
    # AI DETECTION
    # ---------------------------------------------------------
    def _run_anomaly_detection(self, vector: np.ndarray):
        """
        Run Isolation Forest inference.
        """

        score = self.model.decision_function([vector])[0]
        prediction = self.model.predict([vector])[0]

        is_anomaly = prediction == -1

        return score, is_anomaly

    # ---------------------------------------------------------
    # CLASSIFICATION LOGIC
    # ---------------------------------------------------------
    def _classify(self, features: dict, anomaly_score: float) -> dict:
        """
        Hybrid classification (heuristics + anomaly weighting)
        """

        reflectance = features.get("mean_reflectance", 0)
        variance = features.get("variance", 0)

        # Gold tends to correlate with:
        # - moderate reflectance
        # - high anomaly zones
        gold_score = (
            (1 - abs(reflectance - 0.6)) * 0.5 +
            variance * 0.3 +
            max(0, -anomaly_score) * 0.2
        )

        # Diamonds:
        # - low variance
        # - stable reflectance zones
        diamond_score = (
            (1 - variance) * 0.6 +
            reflectance * 0.2 +
            (1 - abs(anomaly_score)) * 0.2
        )

        gold_score = float(self._clamp(gold_score))
        diamond_score = float(self._clamp(diamond_score))

        return {
            "gold_probability": round(gold_score, 3),
            "diamond_indicator": round(diamond_score, 3)
        }

    # ---------------------------------------------------------
    # CONFIDENCE
    # ---------------------------------------------------------
    def _compute_confidence(self, features, anomaly_score):
        """
        Confidence based on signal strength + anomaly clarity
        """

        variance = features.get("variance", 0)
        reflectance = features.get("mean_reflectance", 0)

        base = (variance + reflectance) / 2
        anomaly_factor = abs(anomaly_score)

        confidence = (base * 0.6) + (anomaly_factor * 0.4)

        return round(self._clamp(confidence), 3)

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------
    def _validate_coordinates(self, lat, lon):
        if not (-90 <= lat <= 90):
            raise ValueError("Invalid latitude")

        if not (-180 <= lon <= 180):
            raise ValueError("Invalid longitude")

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def _clamp(self, value, min_v=0.0, max_v=1.0):
        return max(min_v, min(max_v, value))

    def _error_response(self, message, details):
        return {
            "status": "error",
            "message": message,
            "details": details
        }
