"""
providers/base.py
-----------------
Abstract base class that every LLM provider must implement.

To add a new provider (e.g. Google Gemini):
  1. Create providers/gemini.py
  2. Subclass LLMProvider and implement `complete()`
  3. Register it in providers/__init__.py
  4. Set LLM_PROVIDER=gemini in your .env
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Common interface for all LLM backends.

    Implementations receive the fully-assembled prompt pieces and return
    the raw string content from the model. JSON parsing happens in the
    route handler so it stays provider-agnostic.
    """

    # Human-readable name used in logs and the API response
    name: str = "unknown"

    @abstractmethod
    async def complete(
        self,
        *,
        system: str,
        one_shot_user: str,
        one_shot_assistant: str,
        user_message: str,
    ) -> str:
        """
        Send a prompted request to the LLM and return the raw text response.

        Parameters
        ----------
        system              : System-prompt / persona instruction.
        one_shot_user       : The user turn of the one-shot example.
        one_shot_assistant  : The assistant turn of the one-shot example.
        user_message        : The actual user request for this violation.

        Returns
        -------
        Raw string content from the model (expected to be a JSON object).
        """
