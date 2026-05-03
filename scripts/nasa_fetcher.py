import requests
from config import Config

def fetch_apod():
    url = f"{Config.NASA_API_URL}/planetary/apod"

    r = requests.get(url, params={
        "api_key": Config.NASA_API_KEY
    })

    return r.json()

if __name__ == "__main__":
    print(fetch_apod())
