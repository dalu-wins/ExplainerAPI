"""
config.py
---------
Single source of truth for all environment-based configuration.
Load a .env file with python-dotenv before importing this module, or set
the variables in your shell / Docker environment.
"""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)

# LLM provider selection
LLM_PROVIDER: str = os.environ.get("LLM_PROVIDER", "mock")

# OpenAI
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-4o")

# Shared
LLM_MAX_TOKENS: int = int(os.environ.get("LLM_MAX_TOKENS", "1200"))
LLM_TIMEOUT: float = float(os.environ.get("LLM_TIMEOUT", "60"))
LLM_TEMPERATURE: float = float(os.environ.get("LLM_TEMPERATURE", "0.2"))

# API key auth (for protecting this server's own endpoints)
_raw_keys: str = os.environ.get("API_KEYS", "")
VALID_API_KEYS: set[str] = {k.strip() for k in _raw_keys.split(",") if k.strip()}

# Debug
DEBUG_RAW_OUTPUT: bool = os.environ.get("DEBUG_RAW_OUTPUT", "false").lower() == "true"

# Maximum requests per API key per minute for the /explain endpoint
RATE_LIMIT_PER_MINUTE: int = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "2"))