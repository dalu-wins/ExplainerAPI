"""
providers/openai.py
-------------------
LLM provider implementation using the OpenAI Responses API via the
official openai Python SDK.

Relevant .env keys:
    OPENAI_API_KEY   - required
    OPENAI_MODEL     - default: gpt-5.4
    LLM_MAX_TOKENS   - default: 1200
    LLM_TIMEOUT      - default: 60
    LLM_TEMPERATURE  - default: 0.2
"""

from __future__ import annotations

import logging

from openai import AsyncOpenAI
from openai import APIStatusError

from fastapi import HTTPException

import config
from providers.base import LLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    name = "openai"

    def __init__(self) -> None:
        if not config.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set.")
        self._client = AsyncOpenAI(
            api_key=config.OPENAI_API_KEY,
            timeout=config.LLM_TIMEOUT,
        )

    async def complete(
        self,
        *,
        system: str,
        one_shot_user: str,
        one_shot_assistant: str,
        user_message: str,
    ) -> str:
        try:
            response = await self._client.responses.create(
                model=config.OPENAI_MODEL,
                max_output_tokens=config.LLM_MAX_TOKENS,
                temperature=config.LLM_TEMPERATURE,
                instructions=system,
                input=[
                    {"role": "user",      "content": one_shot_user},
                    {"role": "assistant", "content": one_shot_assistant},
                    {"role": "user",      "content": user_message},
                ],
            )
        except APIStatusError as e:
            logger.error("OpenAI API error %s: %s", e.status_code, e.message)
            raise HTTPException(
                status_code=502,
                detail=f"OpenAI API error {e.status_code}: {e.message}",
            )

        return response.output_text.strip()