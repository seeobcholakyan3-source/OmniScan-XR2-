import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Internal imports
from scan_engine import scan_location

# ==========================================================
# LOAD ENV VARIABLES
# ==========================================================
load_dotenv()

# ==========================================================
# CONFIGURATION
# ==========================================================
PORT = int(os.getenv("PORT", 5000))
ENV = os.getenv("ENV", "development")

# ==========================================================
# LOGGING SETUP
# ==========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("OmniScan-XR2-Backend")

# ==========================================================
# CREATE FLASK APP
# ==========================================================
app = Flask(__name__)
CORS(app)

# ==========================================================
# ROUTES
# ==========================================================

@app.route("/")
def root():
    return jsonify({
        "service": "OmniScan-XR2 Backend",
        "status": "running",
        "environment": ENV
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "OmniScan-XR2"
    })


@app.route("/scan/<float:lat>/<float:lon>")
def scan(lat, lon):
    try:
        logger.info(f"Scan requested for lat={lat}, lon={lon}")

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
        logger.error(f"Scan failed: {str(e)}", exc_info=True)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==========================================================
# ERROR HANDLERS
# ==========================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal server error"
    }), 500


# ==========================================================
# START SERVER
# ==========================================================

def start():
    logger.info(f"Starting OmniScan-XR2 Backend on port {PORT}...")

    try:
        app.run(
            host="0.0.0.0",
            port=PORT,
            debug=(ENV == "development")
        )
    except Exception as e:
        logger.critical(f"Server failed to start: {e}", exc_info=True)


if __name__ == "__main__":
    start()
