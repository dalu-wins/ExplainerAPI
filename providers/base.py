"""
providers/base.py
-----------------
Abstract base class that every LLM provider must implement.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from models import ViolationRequest


class LLMProvider(ABC):
    name: str = "unknown"

    @abstractmethod
    async def complete(self, *, req: ViolationRequest) -> str:
        """
        Send a request to the LLM backend and return the raw text response.

        Parameters
        ----------
        req : ViolationRequest
            The violation payload from the frontend. Providers are responsible
            for building their own prompt from this.

        Returns
        -------
        Raw string content from the model (expected to be a JSON object).
        """
