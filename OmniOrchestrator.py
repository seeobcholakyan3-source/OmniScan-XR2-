from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from core.logging import setup_logging
from services.scan_engine import ScanEngine
from services.nasa_client import NASAClient

import logging

setup_logging()
logger = logging.getLogger("OmniScan-XR2")

app = Flask(__name__)
CORS(app)

engine = ScanEngine()
nasa = NASAClient()


@app.route("/health")
def health():
    return jsonify({"status": "online"})


@app.route("/scan/<lat>/<lon>")
def scan(lat, lon):
    logger.info(f"Scan request: {lat}, {lon}")

    geo_result = engine.analyze(lat, lon)
    nasa_data = nasa.get_metadata(lat, lon)

    return jsonify({
        "geo": geo_result,
        "external": nasa_data,
        "system": "OmniScan-XR2-Core"
    })


@app.errorhandler(500)
def error(e):
    return jsonify({"error": "internal_error"}), 500


if __name__ == "__main__":
    logger.info(f"Starting server on port {Config.PORT}")
    app.run(host="0.0.0.0", port=Config.PORT)
