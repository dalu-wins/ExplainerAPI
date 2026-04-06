"""
prompt.py
---------
All prompt content lives here: system message, one-shot example, and the
function that turns a ViolationRequest into the user-turn string.
Keeping prompts separate from provider code means you can iterate on wording
without touching HTTP logic, and both providers always use the same prompts.
"""
from __future__ import annotations
from models import ViolationRequest


# System prompt
SYSTEM_PROMPT = """\
You are an information security expert specializing in data-flow analysis. \
You assist researchers and students working with xDECAF, \
a tool for detecting data-flow violations in annotated program graphs using a \
domain-specific language (DSL) for flow constraints.

Your task is to produce a clear and precise explanation of a given constraint \
violation. Use formal terminology where appropriate, but ensure each step of the \
violation's flow is also explained intuitively.

Think step by step before writing the final answer. Structure your response \
EXACTLY as a JSON object with these two string fields:
  - constraint_explanation
  - violation_explanation

Output ONLY the JSON object. No preamble, no markdown fences. Use our previoous \
one-shot example as a style guide.\
"""

# One-shot example  (user turn -> assistant turn)
ONE_SHOT_USER = """\
Constraint (DSL): data Type.Sensitive neverFlows vertex Location.nonEU
Violated vertex: ExternalStorage (Location.nonEU)
Inducing vertex: UserProfile
TFG vertices: [UserProfile, PaymentProcessor, ExternalStorage, ReportingService]\
"""

ONE_SHOT_ASSISTANT = """\
{
  "constraint_explanation": "The DSL constraint `data Type.Sensitive neverFlows vertex Location.nonEU` specifies that any data carrying the property `Type.Sensitive` must never reach a vertex annotated with `Location.nonEU`. This is a confidentiality rule that prohibits sensitive data from leaving the EU-bounded region of the system.",
  "violation_explanation": "A violation is detected at vertex `ExternalStorage`, which is annotated with `Location.nonEU`. Sensitive data originates at the inducing vertex `UserProfile` — carrying the property `Type.Sensitive` — and flows through `PaymentProcessor` before reaching `ExternalStorage`. Because `ExternalStorage` is the forbidden destination, the constraint is violated at this vertex.",
}\
"""


# Message builder
def build_user_message(req: ViolationRequest) -> str:
    """
    Serialise a ViolationRequest into the plain-text user message that is
    sent to the LLM. Both basic (tfg) and enriched (tfg_enriched) formats
    are supported.
    """
    if req.tfg_enriched:
        lines = [
            f"  - {v.name} "
            f"| in: [{', '.join(v.incoming_properties)}] "
            f"| out: [{', '.join(v.outgoing_properties)}]"
            for v in req.tfg_enriched
        ]
        tfg_section = "TFG vertices (enriched):\n" + "\n".join(lines)
    else:
        tfg_section = f"TFG vertices: [{', '.join(req.tfg)}]"

    return (
        f"Constraint (DSL): {req.constraint}\n"
        f"Violated vertex: {req.violated_vertex}\n"
        f"Inducing vertex: {req.inducing_vertex}\n"
        f"{tfg_section}"
    )
