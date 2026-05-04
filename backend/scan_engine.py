import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from services.spectral_processor import extract_features
from models.mineral_model import predict_minerals


def scan_location(lat, lon):
    """
    Core scan pipeline:
    satellite data → spectral features → AI prediction
    """

    # --------------------------------------------------
    # MOCK / NASA INTEGRATION POINT (replace later)
    # --------------------------------------------------
    spectral_data = [0.12, 0.33, 0.55, 0.78, 0.91]

    features = extract_features(spectral_data)

    prediction = predict_minerals(features)

    return {
        "input": {
            "lat": lat,
            "lon": lon
        },
        "features": features,
        "prediction": prediction
    }
