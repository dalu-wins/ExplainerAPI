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
a tool for detecting data-flow violations in annotated graphs using a \
domain-specific language (DSL) for flow constraints.

Your task is to produce a clear and precise explanation of a given constraint \
violation. Use formal terminology where appropriate, but ensure each step of the \
violation's flow is also explained intuitively.

CRITICAL FORMATTING RULE: 
You MUST enclose all technical identifiers in backticks (`). This includes:
1. All DSL keywords, types, and properties (e.g., `neverFlows`, `Type.Sensitive`, `Purpose.Storage`).
2. All vertex names/components from the graph (e.g., `ExternalStorage`, `UserProfile`).
3. All data characteristics or annotations mentioned in the analysis.

Think step by step before writing the final answer. Structure your response \
EXACTLY as a JSON object with these two string fields:
  - constraint_explanation
  - violation_explanation

Output ONLY the JSON object. No preamble, no markdown fences. Use our previous \
one-shot example as a style guide. Multiple vertices may induce a data characteristic \
that causes the violation, and multiple vertices may be listed as the violation site. \
Make sure to address all of them in your explanation.\
"""

# One-shot example  (user turn -> assistant turn)
ONE_SHOT_USER = """\
Constraint (DSL): data Type.Sensitive neverFlows vertex Location.nonEU
Violated vertices: [ExternalStorage]
Inducing vertices: [UserProfile]
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
    sent to the LLM.
    """
    
    tfg_section = f"TFG vertices: [{', '.join(req.tfg)}]"

    return (
        f"Constraint (DSL): {req.constraint}\n"
        f"Violated vertices: {req.violated_vertex}\n"
        f"Inducing vertices: {req.inducing_vertex}\n"
        f"TFG vertices: {tfg_section}"
    )
