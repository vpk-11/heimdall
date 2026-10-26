from typing import Literal

from pydantic import BaseModel, Field

OUTCOMES = ("immediate_fulfillment", "partial_backorder", "full_production", "rejected")


class TriageOutput(BaseModel):
    """Final structured draft returned by the agent."""

    outcome: Literal[OUTCOMES] = Field(
        description="Triage scenario. Use 'rejected' when the company is unknown or an ID is invalid."
    )
    shortfall: int = Field(ge=0, description="stock_shortfall from compute_shortfall, 0 if rejected.")
    cost: float = Field(ge=0, description="Total production cost from production_estimate, 0 if none.")
    draft_email: str = Field(description="Draft email for human review, clearly marked as a draft.")
