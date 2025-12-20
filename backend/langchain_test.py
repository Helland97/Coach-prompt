import json

from langchain_ollama import OllamaLLM
from pydantic import ValidationError

from models.coaching_output import CoachingOutput

MAX_RETRIES = 3
MIN_CONFIDENCE = 0.6


llm = OllamaLLM(
    model="llama3.2:3b",
    temperature=0.2
)


prompt = """
You are an experienced strength and conditioning coach.
You give conservative, evidence-based advice.
You prioritize safety and simple cues.
You never over-coach.

Exercise:
Back squat

Athlete description:
I feel my knees cave in at the bottom and I lose tightness.

Rules:
- Return ONLY valid JSON
- Follow the exact schema below
- Do NOT include explanations
- Do NOT include markdown

Schema:
{
  "exercise": string,
  "assessment": {
    "overall_quality": "good | acceptable | poor",
    "confidence": number between 0 and 1
  },
  "primary_issue": string,
  "secondary_issues": array of strings,
  "primary_cue": string,
  "accessory_exercises": array of strings,
  "safety_notes": array of strings
}
"""


def get_coaching_output(llm, prompt: str) -> CoachingOutput | None:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw_response = llm.invoke(prompt)
            parsed_json = json.loads(raw_response)
            output = CoachingOutput.model_validate(parsed_json)

            if output.assessment.confidence < MIN_CONFIDENCE:
                raise ValueError("Low confidence output")

            return output

        except (json.JSONDecodeError, ValidationError, ValueError) as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")

    return None


def fallback_response(exercise: str) -> CoachingOutput:
    return CoachingOutput(
        exercise=exercise,
        assessment={
            "overall_quality": "acceptable",
            "confidence": 0.0
        },
        primary_issue="Insufficient information for detailed analysis",
        secondary_issues=[],
        primary_cue="Focus on controlled technique and reduce load if needed",
        accessory_exercises=[],
        safety_notes=["Consult a qualified coach if unsure"]
    )


# 🔹 ORCHESTRATION LAYER (THIS WAS MISSING)
if __name__ == "__main__":
    result = get_coaching_output(llm, prompt)

    if result is None:
        print("⚠️ Falling back to safe default response")
        result = fallback_response(exercise="Back squat")

    print("\n✅ Final coaching output:")
    print(result.model_dump_json(indent=2))
