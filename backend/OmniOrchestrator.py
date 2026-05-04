import os
import sys
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# ==========================================================
# SAFE PATH RESOLUTION (CRITICAL FIX)
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from scan_engine import scan_location

# ==========================================================
# ENV + CONFIG
# ==========================================================
load_dotenv()

PORT = int(os.getenv("PORT", 5000))
ENV = os.getenv("ENV", "development")

# ==========================================================
# LOGGING
# ==========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("OmniScan-XR2")

# ==========================================================
# APP
# ==========================================================
app = Flask(__name__)
CORS(app)

# ==========================================================
# ROUTES
# ==========================================================

@app.route("/")
def root():
    return jsonify({
        "service": "OmniScan-XR2",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.route("/scan/<float:lat>/<float:lon>")
def scan(lat, lon):
    try:
        logger.info(f"Scan request: {lat}, {lon}")

        result = scan_location(lat, lon)

        return jsonify({
            "status": "active",
            "coordinates": {
                "lat": lat,
                "lon": lon
            },
            "result": result
        })

    except Exception as e:
        logger.error(str(e), exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==========================================================
# STARTUP
# ==========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
