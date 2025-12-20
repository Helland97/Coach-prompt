from fastapi import FastAPI
from pydantic import BaseModel

from backend.langchain_pipeline import get_coaching_output
from backend.models.coaching_output import CoachingOutput

app = FastAPI(
    title="Coach-Prompt API",
    description="AI-powered strength coaching assistant",
    version="0.1.0"
)


class CoachingRequest(BaseModel):
    exercise: str
    description: str


@app.post("/coach", response_model=CoachingOutput)
def coach(request: CoachingRequest):
    prompt = f"""
You are an experienced strength and conditioning coach.
You give conservative, evidence-based advice.
You prioritize safety and simple cues.
You never over-coach.

Exercise:
{request.exercise}

Athlete description:
{request.description}

Rules:
- Return ONLY valid JSON
- Follow the exact schema below
- Do NOT include explanations
- Do NOT include markdown

Schema:
{{
  "exercise": string,
  "assessment": {{
    "overall_quality": "good | acceptable | poor",
    "confidence": number between 0 and 1
  }},
  "primary_issue": string,
  "secondary_issues": array of strings,
  "primary_cue": string,
  "accessory_exercises": array of strings,
  "safety_notes": array of strings
}}
"""
    return get_coaching_output(prompt)
