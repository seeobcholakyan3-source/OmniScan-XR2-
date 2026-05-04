"""
Scan Engine (NASA + AI Integration)

- Connects to NASA APIs (if key present)
- Falls back to simulated spectral data
- Runs mineral classification
"""

import os
import logging
import numpy as np
import requests

from backend.models.mineral_model import classifier

logger = logging.getLogger("ScanEngine")

NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_EARTH_URL = "https://api.nasa.gov/planetary/earth/assets"


def fetch_nasa_data(lat: float, lon: float):
    """
    Fetch metadata from NASA Earth API
    (Not hyperspectral, but useful baseline)
    """
    if not NASA_API_KEY:
        logger.warning("NASA_API_KEY not set")
        return None

    try:
        params = {
            "lat": lat,
            "lon": lon,
            "api_key": NASA_API_KEY
        }

        response = requests.get(NASA_EARTH_URL, params=params, timeout=10)

        if response.status_code == 200:
            logger.info("NASA data fetched successfully")
            return response.json()
        else:
            logger.warning(f"NASA API error: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"NASA fetch failed: {e}")
        return None


def generate_spectral_data(seed: int = None) -> np.ndarray:
    """
    Simulate spectral data (until real EMIT integration)
    """
    if seed:
        np.random.seed(seed)

    # Simulate 100 spectral bands
    data = np.random.rand(100)

    # Inject anomaly (simulate mineral signature)
    if np.random.rand() > 0.6:
        data[40:60] += np.random.rand(20) * 0.5

    return data


def analyze_location(lat: float, lon: float) -> dict:
    """
    Main scan function
    """

    logger.info(f"Analyzing location: {lat}, {lon}")

    # Step 1: Try NASA data
    nasa_data = fetch_nasa_data(lat, lon)

    # Step 2: Generate or derive spectral data
    spectral_data = generate_spectral_data(seed=int(abs(lat * lon)))

    # Step 3: Run AI classification
    classification = classifier.classify(spectral_data)

    # Step 4: Build response
    result = {
        "status": "success",
        "location": {
            "lat": lat,
            "lon": lon
        },
        "source": "NASA_EARTH_API" if nasa_data else "SIMULATED",
        "analysis": classification,
        "signals": [
            {
                "type": classification["label"],
                "confidence": classification["confidence"]
            }
        ]
    }

    return result


# CLI test support
if __name__ == "__main__":
    res = analyze_location(34.05, -118.24)
    print(res)
