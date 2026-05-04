import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NASA_API_KEY = os.getenv("NASA_API_KEY")
    NASA_BASE_URL = os.getenv("NASA_BASE_URL", "https://api.nasa.gov")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
