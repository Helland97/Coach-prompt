from typing import List, Literal
from pydantic import BaseModel, Field


class AnalysisOutput(BaseModel):
    detected_issues: List[str]

    severity: Literal["low", "medium", "high"]

    movement_quality: Literal["good", "acceptable", "poor"]

    injury_risk: float = Field(ge=0.0, le=1.0)

    uncertainty: float = Field(ge=0.0, le=1.0)
