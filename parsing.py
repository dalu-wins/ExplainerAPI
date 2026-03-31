"""
parsing.py
----------
Utility for parsing JSON out of raw LLM output.

Models sometimes wrap their response in markdown code fences (```json … ```)
despite being instructed not to. This module strips those fences before
attempting to parse, making the pipeline robust to such deviations.
"""

from __future__ import annotations

import json
import logging

from fastapi import HTTPException

logger = logging.getLogger(__name__)


def parse_llm_json(raw: str) -> dict:
    """
    Strip optional markdown fences from *raw* and return the parsed dict.

    Raises HTTPException(502) if the content cannot be parsed as JSON so that
    the error surfaces cleanly to the frontend.
    """
    cleaned = raw.strip()

    if cleaned.startswith("```"):
        # Remove opening fence (```json or ```)
        cleaned = cleaned.split("```", maxsplit=2)[1]
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
        # Remove closing fence if present
        cleaned = cleaned.rsplit("```", maxsplit=1)[0]

    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse LLM JSON: %s\nRaw output:\n%s", exc, raw)
        raise HTTPException(
            status_code=502,
            detail="The language model returned malformed JSON.",
        )
