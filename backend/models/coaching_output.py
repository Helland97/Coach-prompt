from typing import List, Literal
from pydantic import BaseModel, Field


class Assessment(BaseModel):
    overall_quality: Literal["good", "acceptable", "poor"]
    confidence: float = Field(ge=0.0, le=1.0)


class CoachingOutput(BaseModel):
    exercise: str

    assessment: Assessment

    primary_issue: str
    secondary_issues: List[str]

    primary_cue: str
    accessory_exercises: List[str]

    safety_notes: List[str]
