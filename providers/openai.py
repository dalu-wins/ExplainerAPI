"""
providers/openai.py
-------------------
LLM provider implementation using the OpenAI Responses API.
"""
from __future__ import annotations
import logging
from openai import AsyncOpenAI, APIStatusError
from fastapi import HTTPException
import config
from models import ViolationRequest
from providers.base import LLMProvider
from prompt import ONE_SHOT_ASSISTANT, ONE_SHOT_USER, SYSTEM_PROMPT, build_user_message

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

    async def complete(self, *, req: ViolationRequest) -> str:
        try:
            response = await self._client.responses.create(
                model=config.OPENAI_MODEL,
                max_output_tokens=config.LLM_MAX_TOKENS,
                temperature=config.LLM_TEMPERATURE,
                instructions=SYSTEM_PROMPT,
                input=[
                    {"role": "user",      "content": ONE_SHOT_USER},
                    {"role": "assistant", "content": ONE_SHOT_ASSISTANT},
                    {"role": "user",      "content": build_user_message(req)},
                ],
            )
        except APIStatusError as e:
            logger.error("OpenAI API error %s: %s", e.status_code, e.message)
            raise HTTPException(
                status_code=502,
                detail=f"OpenAI API error {e.status_code}: {e.message}",
            )
        return response.output_text.strip()