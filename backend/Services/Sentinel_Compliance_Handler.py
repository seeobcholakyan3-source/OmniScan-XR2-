class SentinelHandler:
    """
    Handles OB.DAAC Sentinel-1 GRD Data requests and EULA compliance.
    """
    def __init__(self, api_key: str):
        self.api_url = "https://services.sentinel-hub.com/api/v1/process"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    async def request_s1_grd(self, bbox: list, timerange: str):
        """
        Sends compliant POST request to the Sentinel-1 Process API.
       
        """
        payload = {
            "input": {
                "bounds": {"bbox": bbox},
                "data": [{"type": "sentinel-1-grd", "dataFilter": {"mosaickingOrder": "mostRecent"}}]
            },
            "output": {"responses": [{"identifier": "default", "format": {"type": "image/tiff"}}]}
        }
        async with httpx.AsyncClient() as client:
            return await client.post(self.api_url, json=payload, headers=self.headers)
