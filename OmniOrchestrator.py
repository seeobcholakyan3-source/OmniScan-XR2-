from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from core.geo_analyzer import GeoAnalyzer
from core.dataset_builder import DatasetBuilder
from services.nasa_client import NASAClient
from services.storage import GeoStorage
from utils.validators import validate_coordinates

app = Flask(__name__)
CORS(app)

geo = GeoAnalyzer()
nasa = NASAClient()
db = GeoStorage()
builder = DatasetBuilder()


@app.route("/health")
def health():
    return jsonify({"status": "online"})


@app.route("/scan/<lat>/<lon>")
def scan(lat, lon):

    valid, result = validate_coordinates(lat, lon)
    if not valid:
        return jsonify({"error": result}), 400

    lat, lon = result

    geo_data = geo.compute(lat, lon)
    nasa_data = nasa.get_earth_imagery(lat, lon)

    # ML-ready feature vector
    feature_vector = builder.build_features(geo_data, nasa_data)

    # persist scan
    db.save_scan(lat, lon, geo_data, nasa_data)

    return jsonify({
        "location": {"lat": lat, "lon": lon},
        "geo_analysis": geo_data,
        "nasa_data": nasa_data,
        "feature_vector": feature_vector.tolist(),
        "system": "OmniScan-XR2 Research Pipeline"
    })


@app.route("/dataset")
def dataset():
    return jsonify(db.fetch_all())


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
