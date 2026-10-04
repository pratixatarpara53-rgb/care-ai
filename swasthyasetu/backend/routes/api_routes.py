"""
API routes for all four agents and dashboard.
"""

from flask import Blueprint, request, jsonify
from ..agents.health_guidance_agent import get_health_guidance
from ..agents.risk_screening_agent import screen_risk
from ..agents.care_navigation_agent import navigate_care
from ..agents.followup_agent import (
    create_followup, get_all_followups, complete_followup,
    add_medicine_reminder, get_medicine_reminders,
    create_hw_task, get_hw_tasks,
)
from ..data.demo_data import interaction_history, followup_store

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _log_interaction(patient_name, agent_used, query_summary, risk_level=None, language="English"):
    """Append an interaction to in-memory history."""
    from datetime import datetime
    import uuid
    interaction_history.insert(0, {
        "id": str(uuid.uuid4())[:8].upper(),
        "timestamp": datetime.now().isoformat(),
        "patient_name": patient_name or "Anonymous",
        "agent_used": agent_used,
        "query_summary": query_summary[:120],
        "risk_level": risk_level,
        "language": language,
    })


# ─── Health Guidance Agent ───────────────────────────────────────────────────

@api_bp.route("/health-guidance", methods=["POST"])
def health_guidance():
    data = request.get_json(force=True)
    question = (data.get("question") or "").strip()
    language = data.get("language", "english")
    patient_name = data.get("patient_name", "Anonymous")

    if not question:
        return jsonify({"error": "Question is required."}), 400

    result = get_health_guidance(question, language)
    _log_interaction(patient_name, "Health Guidance Agent", question, language=language)
    return jsonify(result)


# ─── Risk Screening Agent ─────────────────────────────────────────────────────

@api_bp.route("/risk-screening", methods=["POST"])
def risk_screening():
    data = request.get_json(force=True)
    symptoms = (data.get("symptoms") or "").strip()
    age = data.get("age", "")
    gender = data.get("gender", "")
    patient_name = data.get("patient_name", "Anonymous")

    if not symptoms:
        return jsonify({"error": "Symptoms description is required."}), 400

    result = screen_risk(symptoms, age, gender)
    _log_interaction(
        patient_name, "Risk Screening Agent",
        symptoms[:80], risk_level=result.get("risk_level"),
    )
    return jsonify(result)


# ─── Care Navigation Agent ────────────────────────────────────────────────────

@api_bp.route("/care-navigation", methods=["POST"])
def care_navigation():
    data = request.get_json(force=True)
    symptoms = (data.get("symptoms") or "").strip()
    risk_level = data.get("risk_level", "MODERATE")
    location = data.get("location", "")
    patient_name = data.get("patient_name", "Anonymous")

    if not symptoms:
        return jsonify({"error": "Symptoms description is required."}), 400

    result = navigate_care(symptoms, risk_level, location)
    _log_interaction(
        patient_name, "Care Navigation Agent",
        f"Navigation for: {symptoms[:60]}",
        risk_level=risk_level,
    )
    return jsonify(result)


# ─── Follow-up Agent ──────────────────────────────────────────────────────────

@api_bp.route("/followup", methods=["GET"])
def get_followups():
    status = request.args.get("status")
    return jsonify(get_all_followups(status))


@api_bp.route("/followup", methods=["POST"])
def post_followup():
    data = request.get_json(force=True)
    patient_name = (data.get("patient_name") or "").strip()
    concern = (data.get("concern") or "").strip()
    if not patient_name or not concern:
        return jsonify({"error": "patient_name and concern are required."}), 400

    result = create_followup(
        patient_name=patient_name,
        concern=concern,
        recommended_date=data.get("recommended_date"),
        notes=data.get("notes", ""),
        pathway=data.get("pathway", "PHC"),
        contact=data.get("contact", ""),
    )
    return jsonify(result), 201


@api_bp.route("/followup/<followup_id>/complete", methods=["PATCH"])
def mark_followup_complete(followup_id):
    return jsonify(complete_followup(followup_id))


@api_bp.route("/medicine-reminder", methods=["GET"])
def get_reminders():
    patient_name = request.args.get("patient_name")
    return jsonify(get_medicine_reminders(patient_name))


@api_bp.route("/medicine-reminder", methods=["POST"])
def post_reminder():
    data = request.get_json(force=True)
    patient_name = (data.get("patient_name") or "").strip()
    medicine_name = (data.get("medicine_name") or "").strip()
    reminder_time = (data.get("reminder_time") or "").strip()

    if not patient_name or not medicine_name or not reminder_time:
        return jsonify({"error": "patient_name, medicine_name, and reminder_time are required."}), 400

    return jsonify(add_medicine_reminder(
        patient_name=patient_name,
        medicine_name=medicine_name,
        reminder_time=reminder_time,
        frequency=data.get("frequency", "Once daily"),
        notes=data.get("notes", ""),
    )), 201


@api_bp.route("/hw-tasks", methods=["GET"])
def get_tasks():
    worker = request.args.get("worker_name")
    return jsonify(get_hw_tasks(worker))


@api_bp.route("/hw-tasks", methods=["POST"])
def post_hw_task():
    data = request.get_json(force=True)
    worker_name = (data.get("worker_name") or "").strip()
    task_description = (data.get("task_description") or "").strip()
    if not worker_name or not task_description:
        return jsonify({"error": "worker_name and task_description are required."}), 400

    return jsonify(create_hw_task(
        worker_name=worker_name,
        task_description=task_description,
        patient_name=data.get("patient_name", ""),
        due_date=data.get("due_date"),
        priority=data.get("priority", "NORMAL"),
    )), 201


# ─── Dashboard ────────────────────────────────────────────────────────────────

@api_bp.route("/dashboard", methods=["GET"])
def dashboard():
    from datetime import datetime, timedelta

    pending = [f for f in followup_store if f["status"] == "PENDING"]
    completed = [f for f in followup_store if f["status"] == "COMPLETED"]

    today = datetime.now().strftime("%Y-%m-%d")
    upcoming = [
        f for f in pending
        if f["recommended_date"] >= today
    ]
    upcoming_sorted = sorted(upcoming, key=lambda x: x["recommended_date"])[:5]

    # Risk distribution from interaction history
    risk_counts = {"LOW": 0, "MODERATE": 0, "URGENT": 0}
    pathway_counts: dict = {}
    for h in interaction_history:
        if h.get("risk_level"):
            risk_counts[h["risk_level"]] = risk_counts.get(h["risk_level"], 0) + 1

    return jsonify({
        "total_requests": len(interaction_history),
        "pending_followups": len(pending),
        "completed_followups": len(completed),
        "upcoming_appointments": upcoming_sorted,
        "risk_distribution": risk_counts,
        "recent_interactions": interaction_history[:8],
        "total_followups": len(followup_store),
    })


# ─── Health check ─────────────────────────────────────────────────────────────

@api_bp.route("/health", methods=["GET"])
def health_check():
    import os
    return jsonify({
        "status": "ok",
        "service": "SwasthyaSetu AI",
        "watsonx_configured": bool(os.environ.get("WATSONX_API_KEY")),
        "demo_mode": not bool(os.environ.get("WATSONX_API_KEY")),
    })
