from flask import Flask, jsonify
import requests

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------
NASA_API_KEY = "DEMO_KEY"  # replace later if you get real key

# -----------------------------
# STEP 3: TERRAIN DATA (DEM)
# -----------------------------
def get_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    try:
        r = requests.get(url, timeout=10).json()
        return r["results"][0]["elevation"]
    except:
        return None


# -----------------------------
# STEP 2: NASA SATELLITE DATA
# -----------------------------
def get_nasa_imagery(lat, lon):
    url = (
        "https://api.nasa.gov/planetary/earth/assets"
        f"?lon={lon}&lat={lat}&dim=0.10&api_key={NASA_API_KEY}"
    )
    try:
        r = requests.get(url, timeout=10).json()
        return r
    except:
        return {"error": "NASA fetch failed"}


# -----------------------------
# STEP 4 + STEP 1: SCAN ENGINE
# -----------------------------
@app.route("/scan/<lat>/<lon>")
def scan(lat, lon):
    lat = float(lat)
    lon = float(lon)

    # TERRAIN
    elevation = get_elevation(lat, lon)

    # SATELLITE
    satellite = get_nasa_imagery(lat, lon)

    # SIMPLE DERIVED INTELLIGENCE (REALISTIC)
    terrain_type = "unknown"
    if elevation is not None:
        if elevation < 50:
            terrain_type = "lowland / basin"
        elif elevation < 300:
            terrain_type = "plain / urban zone"
        else:
            terrain_type = "high elevation terrain"

    # STEP 4: FINAL STRUCTURED RESPONSE
    return jsonify({
        "query": {
            "lat": lat,
            "lon": lon
        },
        "terrain": {
            "elevation_m": elevation,
            "classification": terrain_type
        },
        "satellite": satellite,
        "scan": {
            "status": "complete",
            "mode": "geo-intelligence-v1"
        },
        "sources": [
            "NASA Earth API",
            "Open-Elevation DEM"
        ]
    })


# -----------------------------
# STEP 5: SIMPLE WEB VIEW
# -----------------------------
@app.route("/")
def home():
    return """
    <html>
        <head><title>OmniGeo Scanner</title></head>
        <body style="font-family: Arial;">
            <h2>🌍 OmniGeo Intelligence System</h2>
            <p>Use:</p>
            <code>/scan/lat/lon</code>
            <p>Example:</p>
            <code>/scan/34.05/-118.24</code>
        </body>
    </html>
    """


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
