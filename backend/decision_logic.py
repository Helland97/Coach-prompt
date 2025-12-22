from backend.models.analysis_output import AnalysisOutput
from backend.models.coaching_output import CoachingOutput


def derive_constraints(analysis: AnalysisOutput) -> dict:
    """
    Converts analysis into rules the LLM must obey.
    """
    constraints = {
        "allow_load_increase": True,
        "tone": "normal",
        "max_confidence": 1.0,
        "safety_override": False,
    }

    if analysis.injury_risk > 0.7 or analysis.severity == "high":
        constraints["allow_load_increase"] = False
        constraints["tone"] = "conservative"
        constraints["max_confidence"] = 0.6
        constraints["safety_override"] = True

    if analysis.uncertainty > 0.5:
        constraints["max_confidence"] = 0.5

    return constraints
