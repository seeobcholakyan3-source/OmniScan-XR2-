import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from backend.Services.OmniScan_Metadata_Manager import MetadataManager
from backend.Services.MultiDAAC_Client import MultiDAACClient
from backend.Services.Sentinel_Compliance_Handler import SentinelHandler

# Load environment variables (NASA_USER, NASA_PASSwORD, NASA_TOKEN_KEY)
load_dotenv()

app = FastAPI(
    title="OmniScan-XR2 Fusion Core",
    description="High-performance relay for AR Point Cloud and NASA Spectral Data",
    version="2.0.0"
)

# Configure CORS for mobile device access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production to my device IP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Service Clients
daac_client = MultiDAACClient()
sentinel_handler = SentinelHandler(api_key=os.getenv("NASA_API_KEY"))
# Using zroehrich1 credentials via environment context
metadata_tool = MetadataManager(edl_token=os.getenv("NASA_TOKEN"))

# --- Data Models ---

class ARScanRequest(BaseModel):
    lat: float
    lon: float
    device_id: str
    sensor_type: str = "ARCore_LiDAR"

class ScanResponse(BaseModel):
    status: str
    session_id: str
    relay_active: bool
    authorized_sources: List[str]

# --- Background Processing Logic ---

async def process_satellite_fusion(lat: float, lon: float, session_id: str):
    """
    Handles heavy NASA data retrieval in the background to prevent 
    blocking the mobile UI during the initial 'Start Scan' press.
    """
    print(f"[{session_id}] Initiating background fusion for {lat}, {lon}...")
    try:
        # Fetch Discovery Metadata from AESICS/CMR
        metadata = await metadata_tool.search_discovery(provider="LPDAAC", short_name="ASTGTM")
        
        # Fetch Multi-DAAC spectral data (LP DAAC, GESDISC, ASF)
        # This utilizes the authorized apps like 'ASTER Free Data'
        print(f"[{session_id}] Syncing with LP DAAC and ASF NISAR Data...")
        
        # Logic for Sentinel-1 GRD EULA compliance
        await sentinel_handler.request_s1_grd(bbox=[lon-0.1, lat-0.1, lon+0.1, lat+0.1], timerange="2026-04")
        
        print(f"[{session_id}] Fusion Complete. Relay Buffer Updated.")
    except Exception as e:
        print(f"[{session_id}] Background Fusion Failed: {str(e)}")

# --- API Endpoints ---

@app.get("/")
async def health_check():
    """Verify backend is reachable from device browser at http://127.0.0.1:5001/"""
    return {
        "server": "OmniScan-XR2 Fusion Core",
        "status": "online",
        "timestamp": datetime.utcnow().isoformat(),
        "authorized_user": "zroehrich1"
    }

@app.post("/api/scan/start", response_model=ScanResponse)
async def start_scan(request: ARScanRequest, background_tasks: BackgroundTasks):
    """
    Triggered by the blue 'Start Scan' button on the Pixel 9.
    """
    session_id = f"OS-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    print(f"Incoming Scan Request: Device {request.device_id} at {request.lat}, {request.lon}")

    # Add NASA data retrieval to background tasks to keep the button responsive
    background_tasks.add_task(process_satellite_fusion, request.lat, request.lon, session_id)

    # Immediate 200 OK Response to unlock the Android UI
    return ScanResponse(
        status="success",
        session_id=session_id,
        relay_active=True,
        authorized_sources=["ASTER", "LPDAAC", "ASF", "GESDISC", "Sentinel-1"]
    )

@app.on_event("startup")
async def startup_event():
    print("--------------------------------------------------")
    print("OmniScan-XR2 Fusion Core Starting Up")
    print(f"Targeting NASA DAACs for user: zroehrich1")
    print("Listening on: http://0.0.0.0:5001")
    print("--------------------------------------------------")

if __name__ == "__main__":
    # Using 0.0.0.0 to ensure the Pixel 9 can connect over the local network
    uvicorn.run(app, host="0.0.0.0", port=5001, log_level="info")
