"""
providers/__init__.py
---------------------
Provider registry: maps the LLM_PROVIDER env string to the right class and
returns a ready-to-use singleton.

Adding a new provider
---------------------
1. Create providers/yourprovider.py, subclass LLMProvider, implement complete().
2. Add one line to _REGISTRY below.
3. Set LLM_PROVIDER=yourprovider in .env.

That's it – no other file needs to change.
"""

from __future__ import annotations

import logging

from providers.base import LLMProvider

logger = logging.getLogger(__name__)


# Registry  –  name -> class
def _build_registry() -> dict[str, type[LLMProvider]]:
    from providers.openai import OpenAIProvider
    from providers.mock import MockProvider

    return {
        "openai":   OpenAIProvider,
        "mock":     MockProvider,
    }


# Factory
def get_provider(name: str) -> LLMProvider:
    """
    Return an instantiated LLMProvider for the given name.
    Raises ValueError with a helpful message if the name is unknown.
    """
    registry = _build_registry()
    provider_cls = registry.get(name.lower())

    if provider_cls is None:
        available = ", ".join(sorted(registry))
        raise ValueError(
            f"Unknown LLM provider '{name}'. "
            f"Available providers: {available}. "
            f"Check LLM_PROVIDER in your .env file."
        )

    logger.info("Using LLM provider: %s", name)
    return provider_cls()
