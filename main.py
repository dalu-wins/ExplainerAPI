"""
main.py
-------
FastAPI application entry point.

This file is intentionally thin: it only wires together the modules.
Business logic lives in prompt.py, parsing.py, auth.py, and providers/.
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

import config
from auth import require_api_key
from models import ExplanationResponse, ViolationRequest
from parsing import parse_llm_json
from prompt import ONE_SHOT_ASSISTANT, ONE_SHOT_USER, SYSTEM_PROMPT, build_user_message
from providers import get_provider

logger = logging.getLogger(__name__)

_provider = get_provider(config.LLM_PROVIDER)

# Rate limiter  (in-memory, per API key, sliding window)
# { api_key: [timestamp, timestamp, ...] }
_request_log: dict[str, list[float]] = defaultdict(list)


def _check_rate_limit(key: str) -> None:
    """
    Sliding-window rate limiter keyed on the API key.
    Raises 429 if the key has exceeded RATE_LIMIT_PER_MINUTE requests
    in the last 60 seconds.
    """
    now = time.monotonic()
    window = 60.0
    limit = config.RATE_LIMIT_PER_MINUTE

    # Drop timestamps older than the window
    _request_log[key] = [t for t in _request_log[key] if now - t < window]

    if len(_request_log[key]) >= limit:
        logger.warning("Rate limit exceeded for key ...%s", key[-6:])
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: max {limit} requests per minute.",
            headers={"Retry-After": "60"},
        )

    _request_log[key].append(now)


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not config.VALID_API_KEYS:
        logger.error(
            "API_KEYS is not configured – all protected endpoints will return 503. "
            "Set API_KEYS=<key1>,<key2> in .env."
        )
    else:
        logger.info(
            "API key auth enabled (%d key(s)). Provider: %s. Rate limit: %d req/min.",
            len(config.VALID_API_KEYS),
            _provider.name,
            config.RATE_LIMIT_PER_MINUTE,
        )
    yield


# App
app = FastAPI(
    title="xDECAF Violation Explainer",
    description=(
        "Receives an xDECAF violation and returns a structured, "
        "academically-phrased natural-language explanation via an LLM backend. "
        f"Active provider: **{_provider.name}**."
    ),
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO In production, set this to the frontend URL(s)
    allow_methods=["POST", "GET"],
    allow_headers=["*", "X-API-Key"],
)


# Routes
@app.get("/health")
async def health() -> dict:
    """Public health-check – no auth required."""
    return {
        "status": "ok",
        "provider": _provider.name,
        "auth_enabled": bool(config.VALID_API_KEYS),
        "rate_limit_per_minute": config.RATE_LIMIT_PER_MINUTE,
    }


@app.post("/explain", response_model=ExplanationResponse)
async def explain_violation(
    req: ViolationRequest,
    key: str = Depends(require_api_key),
) -> ExplanationResponse:
    """
    Accept a violation from the xDECAF frontend and return a structured
    explanation: constraint semantics, violation explaination, TFG context.
    """
    _check_rate_limit(key)

    logger.info(
        "Explain request | provider=%s constraint=%r violated=%r inducing=%r",
        _provider.name, req.constraint, req.violated_vertex, req.inducing_vertex,
    )

    user_message = build_user_message(req)

    raw = await _provider.complete(
        system=SYSTEM_PROMPT,
        one_shot_user=ONE_SHOT_USER,
        one_shot_assistant=ONE_SHOT_ASSISTANT,
        user_message=user_message,
    )

    parsed = parse_llm_json(raw)

    return ExplanationResponse(
        constraint_explanation=parsed.get("constraint_explanation", ""),
        violation_explanation=parsed.get("violation_explanation", ""),
        tfg_context=parsed.get("tfg_context", ""),
        provider=_provider.name,
        raw_model_output=raw if config.DEBUG_RAW_OUTPUT else None,
    )
