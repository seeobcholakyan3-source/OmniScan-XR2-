import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT = int(os.getenv("PORT", 5001))
    NASA_API_KEY = os.getenv("NASA_API_KEY")
    NASA_API_URL = os.getenv("NASA_API_URL", "")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
