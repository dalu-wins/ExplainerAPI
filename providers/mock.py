"""
providers/mock.py
-------------------
Mock provider implementation.
"""

import json

from providers.base import LLMProvider

class MockProvider(LLMProvider):
    name = "mock"

    async def complete(
        self,
        *,
        system: str,
        one_shot_user: str,
        one_shot_assistant: str,
        user_message: str,
    ) -> str:
        raw_text = (
            f"system {system}."
            f"one_shot_user {one_shot_user}."
            f"one_shot_assistant {one_shot_assistant}."
            f"user_message {user_message}"
        )
        response_data = {
            "constraint_explanation": "Mock constraint violation.",
            "violation_explanation": "Mock violation explanation.",
            "tfg_context": "Mock tfg context.",
            "provider": "mock",
            "raw_model_output": raw_text
        }

        return json.dumps(response_data)