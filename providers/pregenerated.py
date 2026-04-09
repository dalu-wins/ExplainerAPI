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
            "violated_vertex": ["Third-Party Partner (2)"],
            "inducing_vertex": ["AI Speaker Core Process"],
        },
        "response": {
            "constraint_explanation": "The DSL constraint `data Purpose.Storage neverFlows vertex ComponentCategory.ThirdPartyPartner` defines a prohibition on data flow based on processing purpose and destination category. Any data that has acquired the characteristic `Purpose.Storage` must not flow to any vertex annotated with `ComponentCategory.ThirdPartyPartner`. In other words, data intended or classified for storage purposes is not allowed to be transmitted to third-party partner components.",
            "violation_explanation": "The violation occurs at `Third-Party Partner (2)`, which is a vertex in the forbidden category `ComponentCategory.ThirdPartyPartner`. The relevant data characteristic, `Purpose.Storage`, is induced at `AI Speaker Core Process`, meaning this vertex is where the data becomes classified as storage-related for the purposes of the constraint. From there, the data flows along the TFG path through `Third-Party Exposed Service` and ultimately reaches `Third-Party Partner (2)`. Because the flow carries data marked with `Purpose.Storage` into a third-party partner vertex, the `neverFlows` prohibition is violated at `Third-Party Partner (2)`.",
        },
    },
    {
        "match": {
            "constraint": "- StorageConstraint: data Purpose.Storage neverFlows vertex ComponentCategory.ThirdPartyPartner",
            "violated_vertex": ["Third-Party Partner (1)"],
            "inducing_vertex": ["AI Voice Service"],
        },
        "response": {
            "constraint_explanation": "The constraint `data Purpose.Storage neverFlows vertex ComponentCategory.ThirdPartyPartner` defines a prohibited data-flow pattern: any data that has the characteristic `Purpose.Storage` must not reach any vertex classified as `ComponentCategory.ThirdPartyPartner`. In other words, data intended or marked for storage purposes is not allowed to flow into third-party partner components.",
            "violation_explanation": "The violation occurs at `Third-Party Partner (1)`, which is one of the forbidden destination vertices because it is categorized as `ComponentCategory.ThirdPartyPartner`. The relevant data characteristic, `Purpose.Storage`, is induced by `AI Voice Service`. According to the TFG, the flow proceeds from `AI Voice Service` through `Rules storage` and `Third-Party Exposed Service` before reaching `Third-Party Partner (1)`. Intuitively, data that has become marked as storage-related at `AI Voice Service` is propagated along this path and ultimately disclosed to a third-party partner, which the constraint explicitly forbids. Therefore, the policy is violated at `Third-Party Partner (1)`.",
        },
    },
    {
        "match": {
            "constraint": "- PermissionConstraint: data Purpose.NoPermission neverFlows vertex ComponentCategory.UserHomeDevice",
            "violated_vertex": ['Keyword Listener and Signal Processor', 'Send Interpreted Command', 'Communication Handler'],
            "inducing_vertex": ["Household User (Guest/Family)"],
        },
        "response": {
            "constraint_explanation": "The constraint `data Purpose.NoPermission neverFlows vertex ComponentCategory.UserHomeDevice` is a prohibition on data flow. It states that any data marked with the characteristic `Purpose.NoPermission` must not reach any vertex classified as `ComponentCategory.UserHomeDevice`. In other words, data for which no valid permission exists is not allowed to be processed, transmitted, or stored by home-device components.",
            "violation_explanation": "The violating data characteristic `Purpose.NoPermission` is induced by `Household User (Guest/Family)`, meaning the flow contains data associated with a guest or family member for whom the required permission is absent. This prohibited data then propagates through the graph and reaches multiple vertices that are violation sites because they belong to `ComponentCategory.UserHomeDevice`: `Keyword Listener and Signal Processor`, `Send Interpreted Command`, and `Communication Handler`. Intuitively, unpermitted user data enters the home-device processing path and is handled by device-side components. The listed TFG vertices show the relevant propagation context: the data starts from `Household User (Guest/Family)`, flows into device logic such as `Keyword Listener and Signal Processor`, continues through `Send Interpreted Command` and `Communication Handler`, and is connected with further processing and service interaction including `Authenticate Client`, `AI Voice Service`, and `Rules storage`. The constraint is violated because data lacking permission is present at each of the listed home-device vertices, whereas the policy requires that such data never flow to any user-home-device component.",
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