from flask import Flask, jsonify
from flask_cors import CORS

import logging

from core.logging import setup_logging
from services.scan_engine import ScanEngine
from database import init_db, SessionLocal, ScanRecord

# -----------------------------
# INIT SYSTEM
# -----------------------------
setup_logging()
logger = logging.getLogger("OmniScan-XR2")

app = Flask(__name__)
CORS(app)

engine = ScanEngine()

# Initialize DB on startup
init_db()


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "database": "active"
    })


# -----------------------------
# GEO SCAN ENDPOINT
# -----------------------------
@app.route("/scan/<lat>/<lon>")
def scan(lat, lon):
    logger.info(f"Scan request received: {lat}, {lon}")

    result = engine.analyze(lat, lon)

    return jsonify({
        "status": "success",
        "data": result
    })


# -----------------------------
# HISTORY ENDPOINT (LATEST SCANS)
# -----------------------------
@app.route("/history")
def history():
    db = SessionLocal()

    try:
        records = db.query(ScanRecord)\
                    .order_by(ScanRecord.id.desc())\
                    .limit(50)\
                    .all()

        return jsonify({
            "count": len(records),
            "results": [
                {
                    "lat": r.lat,
                    "lon": r.lon,
                    "density_index": r.density_index,
                    "anomaly_score": r.anomaly_score,
                    "classification": r.classification
                }
                for r in records
            ]
        })

    except Exception as e:
        logger.error(f"History fetch error: {e}")
        return jsonify({"error": "failed_to_fetch_history"}), 500

    finally:
        db.close()


# -----------------------------
# START SERVER
# -----------------------------
if __name__ == "__main__":
    logger.info("Starting OmniScan-XR2 Backend on port 5001...")
    app.run(host="0.0.0.0", port=5001)
