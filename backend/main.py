from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_pipeline import get_coaching_output, warmup_llm
from models.coaching_output import CoachingOutput

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        warmup_llm()
        print("✅ LLM warmed up")
    except Exception as e:
        print("⚠️ LLM warmup failed:", e)

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # IMPORTANT: allows OPTIONS
    allow_headers=["*"],
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


@app.get("/health")
def health():
    return {
        "status": "ok",
        "llm": "ollama",
        "model": "llama3.2:3b"
    }

@app.post("/coach", response_model=CoachingOutput)
def coach(request: CoachingRequest):
    print("RAW REQUEST:", request)