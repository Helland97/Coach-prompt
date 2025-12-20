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



---

## 3️⃣ Why this schema is well-designed (you should understand this)

This isn’t random — it’s **engineering**.

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

---

## 4️⃣ Define what the system does NOT do (important)

Add this section to README:

```md
## Non-goals

This system does NOT:
- Diagnose injuries
- Replace a certified coach
- Analyze video or biomechanics (yet)
- Provide medical advice
