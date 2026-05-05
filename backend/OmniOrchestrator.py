from flask import Flask, jsonify
import requests
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OmniScan-XR2-Backend")

NASA_API_KEY = "DEMO_KEY"  # replace with your key if you have one

# Root endpoint
@app.route("/")
def home():
    return jsonify({
        "service": "OmniScan-XR2",
        "status": "running"
    })

# Health check
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# Scan endpoint
@app.route("/scan/<lat>/<lon>")
def scan(lat, lon):
    logger.info(f"Pinging NASA for coordinates: {lat}, {lon}")

    url = "https://api.nasa.gov/planetary/earth/assets"

    params = {
        "lon": lon,
        "lat": lat,
        "api_key": NASA_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        return jsonify({
            "input": {"lat": lat, "lon": lon},
            "nasa_response": data
        })

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting OmniScan-XR2 Backend on port {port}...")
    app.run(host="0.0.0.0", port=port)
