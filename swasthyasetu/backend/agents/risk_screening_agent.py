"""
Agent 2 – Risk Screening Agent
Categorizes user-reported symptoms as Low / Moderate / Urgent.
Explicitly does NOT provide medical diagnosis.
"""

import re
from .granite_client import generate_text

SYSTEM_CONTEXT = """You are a preliminary health risk screening assistant for rural India.
Your ONLY job is to categorize the urgency level based on user-described symptoms.

CRITICAL RULES:
1. You do NOT diagnose diseases.
2. You do NOT prescribe medicines.
3. You classify urgency as: LOW, MODERATE, or URGENT only.
4. For URGENT cases, always recommend immediate emergency medical care.
5. Always state clearly this is NOT a medical diagnosis.

URGENCY DEFINITIONS:
- LOW: Minor symptoms, no immediate threat (e.g., mild cold, minor cuts, slight fatigue)
- MODERATE: Symptoms need attention within 24-48 hours (e.g., fever >101F, persistent vomiting)
- URGENT: Requires immediate medical attention (e.g., chest pain, difficulty breathing, unconsciousness, severe bleeding, signs of stroke)
"""

URGENT_KEYWORDS = [
    "chest pain", "can't breathe", "cannot breathe", "difficulty breathing",
    "unconscious", "fainted", "severe bleeding", "stroke", "paralysis",
    "heart attack", "seizure", "fits", "poisoning", "high fever child",
    "not responding", "severe head injury", "saans", "chhati dard",
]


def screen_risk(symptoms: str, age: str = "", gender: str = "") -> dict:
    """
    Screen symptoms and return risk level with explanation.
    """
    # Quick safety check for obvious emergencies
    symptoms_lower = symptoms.lower()
    for keyword in URGENT_KEYWORDS:
        if keyword in symptoms_lower:
            return _urgent_response(symptoms)

    patient_context = ""
    if age:
        patient_context += f"Patient age: {age}. "
    if gender:
        patient_context += f"Patient gender: {gender}. "

    prompt = f"""{SYSTEM_CONTEXT}

{patient_context}
Reported symptoms/concerns: {symptoms}

Analyze these symptoms and provide:
RISK_LEVEL: [LOW / MODERATE / URGENT]
EXPLANATION: [1-2 sentence explanation of why this level was chosen]
RECOMMENDED_ACTION: [What the person should do next]
DISCLAIMER: [State this is preliminary screening, not a diagnosis]

Response:"""

    raw = generate_text(prompt, max_new_tokens=300, temperature=0.2)

    risk_level = _extract_risk_level(raw)

    return {
        "agent": "Risk Screening Agent",
        "symptoms": symptoms,
        "risk_level": risk_level,
        "raw_response": raw,
        "is_emergency": risk_level == "URGENT",
        "disclaimer": (
            "⚠️ IMPORTANT: This is a preliminary screening tool only — it does NOT provide "
            "medical diagnosis. Please consult a qualified healthcare professional for any "
            "health concerns. In case of emergency, contact 108 (Ambulance) or visit the "
            "nearest hospital immediately."
        ),
    }


def _extract_risk_level(text: str) -> str:
    """Parse risk level from model output."""
    text_upper = text.upper()
    for pattern in [r"RISK_LEVEL:\s*(URGENT|MODERATE|LOW)", r"\b(URGENT|MODERATE|LOW)\b"]:
        match = re.search(pattern, text_upper)
        if match:
            return match.group(1)
    # Conservative default
    return "MODERATE"


def _urgent_response(symptoms: str) -> dict:
    return {
        "agent": "Risk Screening Agent",
        "symptoms": symptoms,
        "risk_level": "URGENT",
        "raw_response": (
            "RISK_LEVEL: URGENT\n"
            "EXPLANATION: The symptoms described may indicate a serious or life-threatening condition.\n"
            "RECOMMENDED_ACTION: Call 108 (Emergency Ambulance) or go to the nearest hospital emergency department IMMEDIATELY. "
            "Do not wait.\n"
            "DISCLAIMER: This is preliminary screening only, not a medical diagnosis."
        ),
        "is_emergency": True,
        "disclaimer": (
            "🚨 EMERGENCY: Please call 108 (Ambulance) or go to your nearest hospital IMMEDIATELY. "
            "This screening tool does NOT replace emergency medical care."
        ),
    }
