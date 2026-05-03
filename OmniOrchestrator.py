from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from core.scanner import GeoAnalyzer
from services.nasa_client import NASAClient

app = Flask(__name__)
CORS(app)

geo = GeoAnalyzer()
nasa = NASAClient()


@app.route("/health")
def health():
    return jsonify({"status": "online"})


@app.route("/scan/<lat>/<lon>")
def scan(lat, lon):
    lat, lon = float(lat), float(lon)

    geo_data = geo.analyze(lat, lon)
    nasa_data = nasa.get_earth_imagery(lat, lon)

    return jsonify({
        "location": {"lat": lat, "lon": lon},
        "geo_analysis": geo_data,
        "nasa_imagery": nasa_data,
        "system": "OmniScan-XR2 Earth Observation Engine"
    })


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT)
