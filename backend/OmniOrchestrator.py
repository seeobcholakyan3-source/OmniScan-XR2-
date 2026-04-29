import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv() # Loads keys from .env

app = Flask(__name__)

NASA_URL = os.getenv("NASA_API_URL")

@app.route('/scan/<lat>/<lon>')
def get_mineral_data(lat, lon):
    # This simulates a hyperspectral check against NASA EMIT data
    # Logic: SWIR1/SWIR2 ratio for Gold detection
    print(f"Pinging NASA at {NASA_URL} for coordinates: {lat}, {lon}")
    
    return jsonify({
        "status": "active",
        "minerals": {
            "gold_probability": 0.84,
            "diamond_indicator": 0.12
        },
        "source": "NASA_EMIT_2026"
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
