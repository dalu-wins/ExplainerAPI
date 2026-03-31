"""
auth.py
-------
FastAPI dependency for X-API-Key header authentication.

Usage:
    @app.post("/some-route")
    async def route(_key: str = Depends(require_api_key)):
        ...
"""

from __future__ import annotations

import logging
import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

import config

logger = logging.getLogger(__name__)

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(key: str | None = Security(_api_key_header)) -> str:
    """
    Validate the X-API-Key request header.

    - If API_KEYS is not set in the environment, ALL requests are rejected.
      The server will not serve any protected endpoint without at least one
      configured key — regardless of how it is started.
    - Uses secrets.compare_digest for all comparisons to prevent timing attacks.
    """
    if not config.VALID_API_KEYS:
        logger.error(
            "Request blocked: API_KEYS is not configured. "
            "Set API_KEYS=<key> in .env to enable access."
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="This server is not configured correctly. Contact the administrator.",
        )

    if key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header.",
        )

    if not any(secrets.compare_digest(key, valid) for valid in config.VALID_API_KEYS):
        logger.warning("Rejected request with invalid API key.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )

    return key