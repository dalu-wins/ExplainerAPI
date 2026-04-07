"""
providers/pregenerated.py
-------------------------
Returns pre-generated explanations for known violations, lorem ipsum otherwise.
"""
import json
from models import ViolationRequest
from providers.base import LLMProvider


PREGENERATED: list[dict] = [
    {
        "match": {
            "constraint": "- StorageConstraint: data Purpose.Storage neverFlows vertex ComponentCategory.ThirdPartyPartner",
            "violated_vertex": "Third-Party Partner (1)",
            "inducing_vertex": "AI Voice Service",
        },
        "response": {
            "constraint_explanation": "Your constraint explanation here. 1",
            "violation_explanation": "Your violation explanation here. 1",
        },
    },
    {
        "match": {
            "constraint": "- StorageConstraint: data Purpose.Storage neverFlows vertex ComponentCategory.ThirdPartyPartner",
            "violated_vertex": "Third-Party Partner (2)",
            "inducing_vertex": "AI Speaker Core Process",
        },
        "response": {
            "constraint_explanation": "Your constraint explanation here. 2",
            "violation_explanation": "Your violation explanation here. 2",
        },
    },
    {
        "match": {
            "constraint": "- PermissionConstraint: data Purpose.NoPermission neverFlows vertex ComponentCategory.UserHomeDevice",
            "violated_vertex": "Keyword Listener and Signal Processor",
            "inducing_vertex": "Household User (Guest/Family)",
        },
        "response": {
            "constraint_explanation": "Your constraint explanation here. 3",
            "violation_explanation": "Your violation explanation here. 3",
        },
    }
]

LOREM_IPSUM = {
    "constraint_explanation": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.",
    "violation_explanation": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.",
}


def _matches(entry: dict, req: ViolationRequest) -> bool:
    m = entry["match"]
    return (
        m["constraint"] == req.constraint
        and m["violated_vertex"] == req.violated_vertex
        and m["inducing_vertex"] == req.inducing_vertex
    )


class PregeneratedProvider(LLMProvider):
    name = "pregenerated"

    async def complete(self, *, req: ViolationRequest) -> str:
        result = next(
            (entry["response"] for entry in PREGENERATED if _matches(entry, req)),
            LOREM_IPSUM,
        )
        return json.dumps({
            **result,
            "provider": "pregenerated",
            "raw_model_output": None,
        })