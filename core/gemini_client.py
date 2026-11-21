"""Shared HTTP options for Gemini clients."""

import os

from google.genai import types


def gemini_client_options() -> dict:
    """Use the configured Gemini gateway, or the SDK default endpoint."""
    base_url = os.getenv("GOOGLE_GEMINI_BASE_URL", "").strip()
    if not base_url:
        return {}
    return {"http_options": types.HttpOptions(base_url=base_url.rstrip("/"), api_version="v1beta")}
