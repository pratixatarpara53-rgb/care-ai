"""
IBM Granite / Watsonx.ai client wrapper.
Credentials are read exclusively from environment variables — no secrets in code.
"""

import os
import requests

WATSONX_API_URL = os.environ.get("WATSONX_API_URL", "https://us-south.ml.cloud.ibm.com")
WATSONX_PROJECT_ID = os.environ.get("WATSONX_PROJECT_ID", "")
WATSONX_API_KEY = os.environ.get("WATSONX_API_KEY", "")
GRANITE_MODEL_ID = os.environ.get("GRANITE_MODEL_ID", "ibm/granite-13b-instruct-v2")

IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"

_iam_token_cache: dict = {}


def _get_iam_token() -> str:
    """Exchange IBM Cloud API key for a short-lived IAM bearer token (cached)."""
    import time
    now = time.time()
    if _iam_token_cache.get("token") and now < _iam_token_cache.get("expires", 0) - 60:
        return _iam_token_cache["token"]

    if not WATSONX_API_KEY:
        raise EnvironmentError(
            "WATSONX_API_KEY is not set. "
            "Add it to your .env file and restart the server."
        )

    resp = requests.post(
        IAM_TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": WATSONX_API_KEY,
        },
        timeout=20,
    )
    resp.raise_for_status()
    payload = resp.json()
    _iam_token_cache["token"] = payload["access_token"]
    _iam_token_cache["expires"] = now + payload.get("expires_in", 3600)
    return _iam_token_cache["token"]


def generate_text(prompt: str, max_new_tokens: int = 512, temperature: float = 0.3) -> str:
    """
    Call IBM Granite on Watsonx.ai and return the generated text.
    Falls back to a safe stub response when credentials are not configured
    (demo / offline mode).
    """
    if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
        return _demo_fallback(prompt)

    try:
        token = _get_iam_token()
        endpoint = f"{WATSONX_API_URL}/ml/v1/text/generation?version=2023-05-29"
        payload = {
            "model_id": GRANITE_MODEL_ID,
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "repetition_penalty": 1.1,
            },
            "project_id": WATSONX_PROJECT_ID,
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return results[0].get("generated_text", "").strip() if results else ""
    except Exception as exc:  # pylint: disable=broad-except
        # Graceful degradation: return demo content so UI never crashes
        return f"[Offline Demo Mode] {_demo_fallback(prompt)}"


def _demo_fallback(prompt: str) -> str:
    """Return a context-aware placeholder when Watsonx.ai is unavailable."""
    prompt_lower = prompt.lower()
    if "risk" in prompt_lower or "urgent" in prompt_lower:
        return (
            "RISK_LEVEL: Low\n"
            "EXPLANATION: Based on the symptoms described, this appears to be a low-risk situation. "
            "Please monitor the symptoms. If they worsen, contact a healthcare worker.\n"
            "DISCLAIMER: This is preliminary screening only, not a medical diagnosis."
        )
    if "navigate" in prompt_lower or "navigation" in prompt_lower:
        return (
            "RECOMMENDATION: Visit your nearest Primary Health Centre (PHC)\n"
            "REASON: Your symptoms and situation indicate that a visit to the PHC "
            "would be the most appropriate first step for further evaluation.\n"
            "DISCLAIMER: This is a general guidance suggestion, not a medical referral."
        )
    return (
        "Thank you for your question. Based on the information provided, "
        "I recommend consulting a qualified healthcare professional for personalised advice. "
        "For general health information, maintaining a balanced diet, regular exercise, "
        "adequate sleep, and staying hydrated are foundational to good health.\n"
        "DISCLAIMER: This information is for educational purposes only."
    )
