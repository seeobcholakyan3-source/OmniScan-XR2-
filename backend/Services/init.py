"""
Service layer package for OmniScan‑XR2.

This package contains reusable service classes responsible for
external communication, business logic, and integration with
third‑party systems such as Sentinel.
"""

from .Sentinel_Compliance_Handler import SentinelComplianceHandler

__all__ = [
    "SentinelComplianceHandler",
]
