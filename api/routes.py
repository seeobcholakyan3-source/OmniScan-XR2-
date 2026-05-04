from flask import Blueprint, jsonify
from processing.scan_engine import ScanEngine

scan_engine = ScanEngine()
routes = Blueprint("routes", __name__)

@routes.route("/scan/<lat>/<lon>")
def scan(lat, lon):
    result = scan_engine.scan(float(lat), float(lon))
    return jsonify(result)
