from flask import Flask, jsonify, request
import logging
import os

# Your existing scan engine
from scan_engine import scan_location

app = Flask(__name__)

# ----------------------------
# LOGGING
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OmniScan-XR2-Backend")

# ----------------------------
# ROOT ENDPOINT
# ----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "OmniScan-XR2",
        "status": "running"
    })

# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok"
    })

# ----------------------------
# SCAN ENDPOINT (FIXED)
# IMPORTANT: using string route for Termux stability
# ----------------------------
@app.route("/scan/<lat>/<lon>", methods=["GET"])
def scan(lat, lon):
    try:
        # Convert safely
        lat = float(lat)
        lon = float(lon)

        logger.info(f"Pinging scan engine for coordinates: {lat}, {lon}")

        # Call your scan engine
        result = scan_location(lat, lon)

        return jsonify({
            "input": {
                "lat": lat,
                "lon": lon
            },
            "result": result
        })

    except Exception as e:
        logger.error(f"Scan error: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "failed"
        }), 500


# ----------------------------
# START SERVER
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    logger.info(f"Starting OmniScan-XR2 Backend on port {port}...")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
