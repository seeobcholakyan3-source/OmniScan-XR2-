from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic_settings import BaseSettings
import earthaccess
import uvicorn
import os

# 1. Load Credentials
class Settings(BaseSettings):
    EARTHDATA_USERNAME: str
    EARTHDATA_PASSWORD: str
    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI(title="OmniScan-XR2: NASA Mobile Engine")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. Authenticate with NASA
# This uses your .env file to log into the Earthdata Cloud
auth = earthaccess.login(
    username=settings.EARTHDATA_USERNAME, 
    password=settings.EARTHDATA_PASSWORD
)

@app.get("/")
async def serve_home():
    return FileResponse("static/index.html")

@app.get("/api/satellite-data")
async def get_nasa_data():
    try:
        # Search for the latest Sentinel-2 data (Granules)
        # We'll search for data in a broad bounding box for testing
        results = earthaccess.search_data(
            short_name="MSI_L2A", # Sentinel-2
            cloud_hosted=True,
            count=5
        )
        
        # Extract coordinates and info for our VR pins
        granules = []
        for g in results:
            # Simplify coordinates for the 3D globe (Lat/Long)
            point = g.get_coordinates() 
            granules.append({
                "id": g.get_name(),
                "coords": point, # Format: [lat, lon] or similar
                "cloud_cover": g.get_cloud_cover()
            })
            
        return {"status": "Live", "data": granules}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
