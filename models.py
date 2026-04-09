"""
models.py
---------
Pydantic schemas for the /explain endpoint.
These are provider-agnostic and shared across the entire application.
"""

from __future__ import annotations
from typing import Optional

from pydantic import BaseModel, Field


class ViolationRequest(BaseModel):
    """
    Violation payload sent from the xDECAF frontend.

    Fields
    ------
    constraint        : The DSL constraint expression that was violated.
    violated_vertex   : Name of the vertex at which the violation is observed.
    inducing_vertex   : Name of the vertex whose property causes the violation.
    tfg               : Names of all vertices in the affected Transpose Flow Graph.
    """

    constraint: str = Field(..., description="DSL constraint expression")
    violated_vertex: list[str] = Field(...,
                                 description="Vertex where the violation occurs")
    inducing_vertex: list[str] = Field(
        ..., description="Vertex whose property induces the violation"
    )
    tfg: list[str] = Field(..., description="Vertex names in the affected TFG")


class ExplanationResponse(BaseModel):
    """Structured explanation returned to the frontend."""

    constraint_explanation: str = Field(
        description="Plain-English explanation of what the DSL constraint means."
    )
    violation_explanation: str = Field(
        description="What the violation means concretely in this graph."
    )
    provider: str = Field(
        description="LLM provider that generated this explanation.")
    raw_model_output: Optional[str] = Field(
        default=None,
        description="Raw LLM output for debugging (only set when DEBUG_RAW_OUTPUT=true).",
    )
