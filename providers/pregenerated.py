"""
providers/pregenerated.py
-------------------------
Static provider implementation that returns pre-generated LLM explanations for research purposes.
"""

import json

from providers.base import LLMProvider

class PregeneratedProvider(LLMProvider):
    name = "pregenerated"

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
            "constraint_explanation": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
            "violation_explanation": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
            "provider": "pregenerated",
            "raw_model_output": raw_text
        }

        return json.dumps(response_data)