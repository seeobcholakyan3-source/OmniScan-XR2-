"""
Sentinel Compliance Handler.

Provides an asynchronous client for communicating with the Sentinel
compliance service.
"""

import logging
from typing import Any, Dict, Optional

import httpx

LOGGER = logging.getLogger(__name__)


class SentinelComplianceHandler:
    """Asynchronous client for Sentinel compliance checks."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout_seconds: float = 10.0,
    ) -> None:
        self.base_url: str = base_url.rstrip("/")
        self.api_key: Optional[str] = api_key
        self.timeout: httpx.Timeout = httpx.Timeout(timeout_seconds)

    async def check_compliance(
        self,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Send a compliance request to the Sentinel service.

        Args:
            payload: JSON‑serializable request body.

        Returns:
            Parsed JSON response from the Sentinel service.

        Raises:
            httpx.HTTPError: If the request fails.
            ValueError: If the response body is not valid JSON.
        """

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }

        if self.api_key is not None:
            headers["Authorization"] = f"Bearer {self.api_key}"

        url: str = f"{self.base_url}/compliance/check"

        LOGGER.debug("Sending compliance request to %s", url)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response: httpx.Response = await client.post(
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

            try:
                data: Dict[str, Any] = response.json()
            except ValueError as exc:
                LOGGER.error("Invalid JSON response from Sentinel")
                raise ValueError(
                    "Invalid JSON response from Sentinel"
                ) from exc

        LOGGER.debug("Compliance response received successfully")
        return data
