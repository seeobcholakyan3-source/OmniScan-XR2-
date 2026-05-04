import math
import logging
from providers.nasa_client import fetch_nasa_imagery
from providers.mock_provider import mock_scan

logger = logging.getLogger("ScanEngine")


class ScanEngine:
    """
    Core geospatial analysis engine.

    Responsibilities:
    - Fetch raw satellite/imagery data (NASA or fallback)
    - Normalize data into analyzable structure
    - Apply scoring logic (placeholder ML-ready system)
    - Return structured scan result
    """

    def __init__(self, use_real_data: bool = False):
        self.use_real_data = use_real_data

    # -----------------------------
    # PUBLIC API
    # -----------------------------
    def scan(self, lat: float, lon: float) -> dict:
        """
        Main entry point for geospatial scan.
        """

        logger.info(f"Scanning coordinates: {lat}, {lon}")

        # 1. Fetch data
        raw_data = self._fetch_data(lat, lon)

        # 2. Normalize input
        normalized = self._normalize(raw_data, lat, lon)

        # 3. Compute analysis scores
        scores = self._compute_scores(normalized)

        # 4. Build response
        return {
            "lat": lat,
            "lon": lon,
            "gold_probability": scores["gold_probability"],
            "diamond_indicator": scores["diamond_indicator"],
            "confidence": scores["confidence"],
            "source": raw_data.get("source", "UNKNOWN")
        }

    # -----------------------------
    # DATA LAYER
    # -----------------------------
    def _fetch_data(self, lat, lon) -> dict:
        """
        Switch between real NASA data and mock fallback.
        """

        try:
            if self.use_real_data:
                return fetch_nasa_imagery(lat, lon)

            return mock_scan(lat, lon)

        except Exception as e:
            logger.error(f"Data fetch failed: {str(e)}")

            return {
                "source": "FALLBACK_ERROR",
                "error": str(e)
            }

    # -----------------------------
    # NORMALIZATION LAYER
    # -----------------------------
    def _normalize(self, data: dict, lat: float, lon: float) -> dict:
        """
        Converts raw API response into consistent internal format.
        """

        return {
            "lat": lat,
            "lon": lon,
            "raw": data
        }

    # -----------------------------
    # ANALYTICS LAYER (CORE LOGIC)
    # -----------------------------
    def _compute_scores(self, data: dict) -> dict:
        """
        Placeholder geospatial scoring engine.

        This is where real ML / spectral analysis will plug in later.
        """

        raw = data.get("raw", {})

        # If NASA imagery exists, derive pseudo-features
        image_signal = self._extract_signal(raw)

        # Simple deterministic scoring model (replace later with ML)
        gold_score = self._sigmoid(image_signal * 0.8)
        diamond_score = self._sigmoid(image_signal * 0.3)

        confidence = min(1.0, max(0.2, image_signal / 10))

        return {
            "gold_probability": round(gold_score, 4),
            "diamond_indicator": round(diamond_score, 4),
            "confidence": round(confidence, 4)
        }

    # -----------------------------
    # FEATURE EXTRACTION
    # -----------------------------
    def _extract_signal(self, raw: dict) -> float:
        """
        Converts NASA response into a numeric signal proxy.

        Right now:
        - Uses metadata presence as weak signal
        Future:
        - Will process satellite imagery pixels / spectral bands
        """

        if not raw:
            return 0.1

        # If NASA returned valid imagery URL or data
        if "image_url" in raw:
            return 7.5

        if "error" in raw:
            return 0.5

        return 3.0

    # -----------------------------
    # MATH UTIL
    # -----------------------------
    def _sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-x))
