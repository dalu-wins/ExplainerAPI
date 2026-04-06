"""
models.py
---------
Pydantic schemas for the /explain endpoint.
These are provider-agnostic and shared across the entire application.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class VertexWithProperties(BaseModel):
    """Enriched vertex representation for the optional TFG extension."""

    name: str
    incoming_properties: list[str] = Field(default_factory=list)
    outgoing_properties: list[str] = Field(default_factory=list)


class ViolationRequest(BaseModel):
    """
    Violation payload sent from the xDECAF frontend.

    Fields
    ------
    constraint        : The DSL constraint expression that was violated.
    violated_vertex   : Name of the vertex at which the violation is observed.
    inducing_vertex   : Name of the vertex whose property causes the violation.
    tfg               : Names of all vertices in the affected Transpose Flow Graph.
    tfg_enriched      : Optional enriched TFG (vertex name + in/out properties).
                        Extend the frontend to send this once property data is
                        available per vertex.
    """

    constraint: str = Field(..., description="DSL constraint expression")
    violated_vertex: str = Field(...,
                                 description="Vertex where the violation occurs")
    inducing_vertex: str = Field(
        ..., description="Vertex whose property induces the violation"
    )
    tfg: list[str] = Field(..., description="Vertex names in the affected TFG")
    tfg_enriched: Optional[list[VertexWithProperties]] = Field(
        default=None,
        description="Enriched TFG with per-vertex data properties (optional extension)",
    )


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
