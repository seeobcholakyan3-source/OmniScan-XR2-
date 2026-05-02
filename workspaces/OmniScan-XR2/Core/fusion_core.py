from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI(title="OmniScan-XR2 Core API")

# Mount the 'static' directory so the browser can access your WebXR files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the VR interface when you navigate to the base URL
@app.get("/")
async def serve_vr_dashboard():
    return FileResponse("static/index.html")

# Your existing NASA data endpoints remain exactly the same!
@app.get("/api/satellite-data")
async def get_data():
    return {"status": "success", "data": "NASA Sentinel data here"}

if __name__ == "__main__":
    # Host on 0.0.0.0 so devices on your WiFi can connect
    uvicorn.run(app, host="0.0.0.0", port=5001)
  
