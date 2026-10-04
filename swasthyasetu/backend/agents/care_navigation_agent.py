"""
Agent 3 – Care Navigation Agent
Recommends the appropriate healthcare pathway based on risk and context.
"""

from .granite_client import generate_text

SYSTEM_CONTEXT = """You are a healthcare navigation assistant for rural India.
Your job is to recommend the most appropriate healthcare pathway for the user.

Available pathways (choose ONE):
1. LOCAL_HEALTH_WORKER – ASHA/ANM worker for basic care, home visits, health education
2. PHC – Primary Health Centre for basic outpatient care, vaccinations, minor illnesses
3. DOCTOR_CONSULTATION – GP or specialist consultation for diagnosed or complex conditions
4. HOSPITAL – District or sub-district hospital for moderate to serious conditions
5. EMERGENCY_SERVICES – Call 108 / go to emergency room immediately for life-threatening situations

Rules:
1. Always recommend the LEAST intensive appropriate pathway first.
2. Provide a clear reason for your recommendation.
3. Include practical guidance on how to access the recommended service.
4. Never recommend specific prescription medicines.
5. Always include a disclaimer that this is navigational guidance, not a medical referral.
"""

PATHWAY_DETAILS = {
    "LOCAL_HEALTH_WORKER": {
        "title": "Local Health Worker (ASHA/ANM)",
        "icon": "👩‍⚕️",
        "color": "#22c55e",
        "description": "Contact your local ASHA or ANM worker for basic care and guidance.",
        "access": "Contact through village panchayat or community health board.",
    },
    "PHC": {
        "title": "Primary Health Centre (PHC)",
        "icon": "🏥",
        "color": "#3b82f6",
        "description": "Visit your nearest Primary Health Centre for basic outpatient care.",
        "access": "PHCs are usually open 8am-2pm on weekdays. Emergency care 24/7.",
    },
    "DOCTOR_CONSULTATION": {
        "title": "Doctor Consultation",
        "icon": "👨‍⚕️",
        "color": "#8b5cf6",
        "description": "Schedule an appointment with a general physician or specialist.",
        "access": "Contact your nearest CHC or district hospital for referral.",
    },
    "HOSPITAL": {
        "title": "Hospital",
        "icon": "🏨",
        "color": "#f59e0b",
        "description": "Visit the nearest district or sub-district hospital for further evaluation.",
        "access": "District hospitals have OPD, lab, and specialist services.",
    },
    "EMERGENCY_SERVICES": {
        "title": "Emergency Services – Call 108",
        "icon": "🚨",
        "color": "#ef4444",
        "description": "Call 108 (Free Ambulance) or go to the nearest emergency room immediately.",
        "access": "Dial 108 for free ambulance service anywhere in India.",
    },
}


def navigate_care(symptoms: str, risk_level: str = "MODERATE", location: str = "") -> dict:
    """
    Recommend appropriate healthcare pathway.
    """
    # Direct routing for urgent cases
    if risk_level.upper() == "URGENT":
        pathway = PATHWAY_DETAILS["EMERGENCY_SERVICES"].copy()
        pathway["key"] = "EMERGENCY_SERVICES"
        return {
            "agent": "Care Navigation Agent",
            "symptoms": symptoms,
            "risk_level": risk_level,
            "recommended_pathway": pathway,
            "reason": (
                "Based on the urgency level identified, immediate emergency medical care is required. "
                "Please do not delay — call 108 or go to the nearest hospital emergency department now."
            ),
            "disclaimer": (
                "This is navigational guidance only, not a medical referral. "
                "In emergencies, always call 108 or proceed to the nearest emergency department."
            ),
        }

    location_context = f"Patient location/district: {location}. " if location else ""

    prompt = f"""{SYSTEM_CONTEXT}

{location_context}
Reported symptoms: {symptoms}
Preliminary risk level: {risk_level}

Based on this information, recommend the most appropriate healthcare pathway.
Respond EXACTLY in this format:
PATHWAY: [ONE OF: LOCAL_HEALTH_WORKER / PHC / DOCTOR_CONSULTATION / HOSPITAL / EMERGENCY_SERVICES]
REASON: [2-3 sentences explaining why this pathway is recommended]
NEXT_STEPS: [Practical steps the person should take]
DISCLAIMER: [Navigation guidance disclaimer]

Response:"""

    raw = generate_text(prompt, max_new_tokens=350, temperature=0.2)

    pathway_key = _extract_pathway(raw, risk_level)
    pathway = PATHWAY_DETAILS.get(pathway_key, PATHWAY_DETAILS["PHC"]).copy()
    pathway["key"] = pathway_key

    reason = _extract_field(raw, "REASON")
    next_steps = _extract_field(raw, "NEXT_STEPS")

    return {
        "agent": "Care Navigation Agent",
        "symptoms": symptoms,
        "risk_level": risk_level,
        "recommended_pathway": pathway,
        "reason": reason or f"Based on your symptoms and risk level ({risk_level}), this pathway is most appropriate.",
        "next_steps": next_steps or pathway["access"],
        "raw_response": raw,
        "disclaimer": (
            "This is navigational guidance only and does not constitute a medical referral or prescription. "
            "Please consult a qualified healthcare professional for medical decisions."
        ),
    }


def _extract_pathway(text: str, risk_level: str) -> str:
    """Parse recommended pathway from model output."""
    import re
    text_upper = text.upper()
    for key in PATHWAY_DETAILS.keys():
        if key in text_upper:
            return key
    # Fallback based on risk level
    return {
        "LOW": "LOCAL_HEALTH_WORKER",
        "MODERATE": "PHC",
        "URGENT": "EMERGENCY_SERVICES",
    }.get(risk_level.upper(), "PHC")


def _extract_field(text: str, field: str) -> str:
    """Extract a field value from structured model output."""
    import re
    pattern = rf"{field}:\s*(.+?)(?=\n[A-Z_]+:|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""
