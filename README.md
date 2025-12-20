# Coach-Prompt

Coach-Prompt is a local AI-powered strength coaching assistant.
It analyzes short text descriptions of lifts and returns
structured, actionable coaching feedback.

The system is designed to:
- Avoid over-coaching
- Prioritize safety
- Return machine-readable output (JSON)
- Run locally using Ollama (no paid APIs)


## Coaching Output Schema (v1)

All model responses MUST follow this schema exactly.

```json
{
  "exercise": "string",
  "assessment": {
    "overall_quality": "good | acceptable | poor",
    "confidence": 0.0
  },
  "primary_issue": "string",
  "secondary_issues": ["string"],
  "primary_cue": "string",
  "accessory_exercises": ["string"],
  "safety_notes": ["string"]
}

```

### Key design decisions

### ✅ One primary cue
Prevents:
- Information overload
- ChatGPT-style rambling

### ✅ Confidence score
Lets you later:
- Filter low-quality responses
- Trigger fallback logic
- Log uncertainty

### ✅ Safety notes
Signals:
- You thought about liability
- You understand real-world use

### ✅ No long explanations
Forces:
- Deterministic output
- Easy API / UI integration

This is *much* better than “free text advice”.


## Non-goals

This system does NOT:
- Diagnose injuries
- Replace a certified coach
- Analyze video or biomechanics (yet)
- Provide medical advice



## Input Format

The system currently accepts:
- Exercise name (string)
- Free-text description of perceived issues

Example input:
"I feel my knees cave in at the bottom and I lose tightness"
