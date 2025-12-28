import json
import os

from langchain_ollama import OllamaLLM
from pydantic import ValidationError

from models.coaching_output import CoachingOutput

MAX_RETRIES = 3
MIN_CONFIDENCE = 0.6

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"  # default for local dev
)

llm = OllamaLLM(
    model="llama3.2:3b",
    base_url=OLLAMA_BASE_URL,
    temperature=0.2,
    num_predict=256
)


def get_coaching_output(prompt: str) -> CoachingOutput:
    for _ in range(MAX_RETRIES):
        try:
            raw = llm.invoke(prompt)
            parsed = json.loads(raw)
            output = CoachingOutput.model_validate(parsed)

            if output.assessment.confidence < MIN_CONFIDENCE:
                raise ValueError("Low confidence")

            return output

        except (json.JSONDecodeError, ValidationError, ValueError):
            continue

    return fallback_response()


def fallback_response() -> CoachingOutput:
    return CoachingOutput(
        exercise="unknown",
        assessment={
            "overall_quality": "acceptable",
            "confidence": 0.0
        },
        primary_issue="Insufficient information for detailed analysis",
        secondary_issues=[],
        primary_cue="Focus on controlled technique and reduce load",
        accessory_exercises=[],
        safety_notes=["Consult a qualified coach if unsure"]
    )


def warmup_llm():
    llm.invoke("Say ready.")
