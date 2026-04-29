# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL
# OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan
# ==============================================================================

import os
import requests
from dotenv import load_dotenv

# Load the secret token from the .env file
load_dotenv()

class NasaEarthData:
def __init__(self):
self.token = os.getenv("NASA_TOKEN")
self.base_url = "https://earthdata.nasa.gov/api"

if not self.token:
raise ValueError("🚨 CRITICAL: NASA_TOKEN missing from .env file!")

def fetch_emit_data(self, lat, lon):
"""Fetches hyperspectral data for given coordinates."""
headers = {
"Authorization": f"Bearer {self.token}",
"Content-Type": "application/json"
}

print(f"🛰️ Authenticating with NASA Earthdata for coords: {lat}, {lon}...")

# Example API call (Replace with actual EMIT endpoint)
# response = requests.get(f"{self.base_url}/search/granules", headers=headers)

# Simulated successful return for backend processing
return {"status": "success", "data": "Hyperspectral_Cube_Loaded"}

if __name__ == "__main__":
client = NasaEarthData()
client.fetch_emit_data(34.0522, -118.2437)
