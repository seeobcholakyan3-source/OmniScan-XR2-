import os
import logging
import requests
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_ASSETS_URL = "https://api.nasa.gov/planetary/earth/assets"

# ------------------------------------------------------------------------------
# Validate coordinates
# ------------------------------------------------------------------------------
def validate_coordinates(lat, lon):
    lat = float(lat)
    lon = float(lon)

    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError("Invalid lat/lon range")

    return lat, lon

# ------------------------------------------------------------------------------
# Fetch image URL from NASA
# ------------------------------------------------------------------------------
def fetch_satellite_image_url(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "dim": 0.15,
        "api_key": NASA_API_KEY
    }

    response = requests.get(NASA_ASSETS_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data.get("url"), data.get("date")

# ------------------------------------------------------------------------------
# Download image
# ------------------------------------------------------------------------------
def download_image(url):
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    return Image.open(BytesIO(response.content)).convert("RGB")

# ------------------------------------------------------------------------------
# Extract spectral-like features from RGB
# ------------------------------------------------------------------------------
def extract_spectral_features(image):
    """
    Approximate spectral analysis using RGB channels
    (REALISTIC constraint: NASA public imagery is not hyperspectral)
    """

    img = np.array(image)

    red = img[:, :, 0].astype(float)
    green = img[:, :, 1].astype(float)
    blue = img[:, :, 2].astype(float)

    # Normalize
    red /= 255.0
    green /= 255.0
    blue /= 255.0

    # Spectral indices (approximations)
    iron_index = red / (green + 1e-5)
    brightness = (red + green + blue) / 3

    features = {
        "mean_red": float(np.mean(red)),
        "mean_green": float(np.mean(green)),
        "mean_blue": float(np.mean(blue)),
        "iron_index": float(np.mean(iron_index)),
        "brightness": float(np.mean(brightness)),
    }

    return features

# ------------------------------------------------------------------------------
# ML-style classifier (lightweight, no sklearn needed)
# ------------------------------------------------------------------------------
def mineral_classifier(features):
    """
    Lightweight deterministic model (Termux safe)
    """

    iron = features["iron_index"]
    brightness = features["brightness"]

    # Gold heuristic (iron-rich + reflective)
    gold_probability = np.clip((iron * 0.6 + brightness * 0.4), 0, 1)

    # Diamond heuristic (low iron, high brightness contrast)
    diamond_indicator = np.clip((brightness * (1 - iron)), 0, 1)

    confidence = np.clip((gold_probability + diamond_indicator) / 2, 0, 1)

    return {
        "gold_probability": round(float(gold_probability), 3),
        "diamond_indicator": round(float(diamond_indicator), 3),
        "confidence": round(float(confidence), 3)
    }

# ------------------------------------------------------------------------------
# MAIN PIPELINE
# ------------------------------------------------------------------------------
def run_scan(lat, lon):
    logger.info(f"Scan start: {lat}, {lon}")

    if not NASA_API_KEY:
        raise RuntimeError("NASA_API_KEY missing")

    lat, lon = validate_coordinates(lat, lon)

    # Step 1: Get image URL
    image_url, date = fetch_satellite_image_url(lat, lon)

    if not image_url:
        return {"status": "error", "message": "No image available"}

    # Step 2: Download image
    image = download_image(image_url)

    # Step 3: Extract features
    features = extract_spectral_features(image)

    # Step 4: Run classifier
    minerals = mineral_classifier(features)

    result = {
        "status": "active",
        "coordinates": {"lat": lat, "lon": lon},
        "timestamp": datetime.utcnow().isoformat(),
        "image_source": image_url,
        "date": date,
        "features": features,
        "minerals": minerals,
        "source": "NASA_EARTH_RGB_ANALYSIS_V2",
        "note": "RGB-derived spectral approximation (not true hyperspectral)"
    }

    logger.info("Scan complete")

    return result
