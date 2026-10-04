"""
Agent 1 – Health Guidance Agent
Provides educational health information in English and Gujarati.
Does NOT diagnose diseases or prescribe medicines.
"""

from .granite_client import generate_text

SYSTEM_CONTEXT = """You are SwasthyaSetu, a friendly rural healthcare education assistant in India.
Your role is to provide simple, safe, and accurate health education.
Rules you must always follow:
1. Never diagnose diseases.
2. Never prescribe medicines or dosages.
3. Always recommend consulting a qualified doctor for medical decisions.
4. Use simple language appropriate for rural communities.
5. When responding in Gujarati, use clear and simple Gujarati script.
6. End every response with a disclaimer that this is educational information only.
"""


def get_health_guidance(question: str, language: str = "english") -> dict:
    """
    Generate health education response for the given question.
    language: 'english', 'gujarati', or 'hindi'
    """
    lang_map = {
        "gujarati": "Respond in simple, clear Gujarati script (Gujarati language). ",
        "hindi":    "Respond in simple, clear Hindi (Devanagari script). ",
    }
    lang_instruction = lang_map.get(language.lower(), "Respond in simple, clear English. ")

    prompt = f"""{SYSTEM_CONTEXT}

{lang_instruction}

User question: {question}

Provide a helpful, educational response. Structure your answer with:
- Simple explanation
- General health tips related to the topic
- When to seek professional help
- Educational disclaimer

Response:"""

    raw = generate_text(prompt, max_new_tokens=400, temperature=0.3)

    disclaimers = {
        "gujarati": "આ માહિતી શૈક્ષણિક હેતુ માટે છે. ડૉક્ટરની સલાહ લો.",
        "hindi":    "यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है। कृपया चिकित्सीय सलाह के लिए डॉक्टर से परामर्श करें।",
    }
    return {
        "agent": "Health Guidance Agent",
        "question": question,
        "language": language,
        "response": raw,
        "disclaimer": disclaimers.get(
            language.lower(),
            "This information is for educational purposes only. Please consult a qualified doctor for medical advice."
        ),
    }
