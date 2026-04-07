"""
providers/mock.py
-----------------
Mock provider — returns static lorem ipsum without calling any LLM.
"""
import json
from models import ViolationRequest
from providers.base import LLMProvider


class MockProvider(LLMProvider):
    name = "mock"

    async def complete(self, *, req: ViolationRequest) -> str:
        return json.dumps({
            "constraint_explanation": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
            "violation_explanation": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.",
            "provider": "mock",
            "raw_model_output": None,
        })