"""
Agent 4 – Follow-up Agent
Manages patient follow-up reminders, medicine reminders, and healthcare-worker tasks.
All data stored in-memory (replace with a database for production).
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional
from ..data.demo_data import followup_store, medicine_reminders_store, hw_tasks_store


def create_followup(
    patient_name: str,
    concern: str,
    recommended_date: Optional[str] = None,
    notes: str = "",
    pathway: str = "PHC",
    contact: str = "",
) -> dict:
    """Create a new follow-up reminder."""
    followup_id = str(uuid.uuid4())[:8].upper()
    if not recommended_date:
        dt = datetime.now() + timedelta(days=3)
        recommended_date = dt.strftime("%Y-%m-%d")

    record = {
        "id": followup_id,
        "patient_name": patient_name,
        "concern": concern,
        "recommended_date": recommended_date,
        "notes": notes,
        "pathway": pathway,
        "contact": contact,
        "status": "PENDING",
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
    }
    followup_store.append(record)
    return {"agent": "Follow-up Agent", "action": "created", "followup": record}


def get_all_followups(status: Optional[str] = None) -> dict:
    """Retrieve follow-up records, optionally filtered by status."""
    if status:
        records = [r for r in followup_store if r["status"].upper() == status.upper()]
    else:
        records = list(followup_store)
    records_sorted = sorted(records, key=lambda x: x["recommended_date"])
    return {
        "agent": "Follow-up Agent",
        "total": len(records_sorted),
        "followups": records_sorted,
    }


def complete_followup(followup_id: str) -> dict:
    """Mark a follow-up as completed."""
    for record in followup_store:
        if record["id"] == followup_id:
            record["status"] = "COMPLETED"
            record["completed_at"] = datetime.now().isoformat()
            return {"agent": "Follow-up Agent", "action": "completed", "followup": record}
    return {"error": f"Follow-up {followup_id} not found."}


def add_medicine_reminder(
    patient_name: str,
    medicine_name: str,
    reminder_time: str,
    frequency: str = "Once daily",
    notes: str = "",
) -> dict:
    """
    Store a medicine reminder entered by the user.
    IMPORTANT: Medicine names here are user-entered (e.g., OTC supplements).
    This system does NOT generate prescriptions or recommend prescription medicines.
    """
    reminder_id = str(uuid.uuid4())[:8].upper()
    record = {
        "id": reminder_id,
        "patient_name": patient_name,
        "medicine_name": medicine_name,
        "reminder_time": reminder_time,
        "frequency": frequency,
        "notes": notes,
        "created_at": datetime.now().isoformat(),
        "active": True,
    }
    medicine_reminders_store.append(record)
    return {
        "agent": "Follow-up Agent",
        "action": "medicine_reminder_created",
        "reminder": record,
        "disclaimer": (
            "This reminder was created based on information you provided. "
            "SwasthyaSetu does not prescribe medicines. Always follow your doctor's instructions."
        ),
    }


def get_medicine_reminders(patient_name: Optional[str] = None) -> dict:
    """Retrieve medicine reminders."""
    if patient_name:
        records = [r for r in medicine_reminders_store if r["patient_name"].lower() == patient_name.lower()]
    else:
        records = list(medicine_reminders_store)
    return {"agent": "Follow-up Agent", "total": len(records), "reminders": records}


def create_hw_task(
    worker_name: str,
    task_description: str,
    patient_name: str = "",
    due_date: Optional[str] = None,
    priority: str = "NORMAL",
) -> dict:
    """Create a healthcare worker task."""
    task_id = str(uuid.uuid4())[:8].upper()
    if not due_date:
        dt = datetime.now() + timedelta(days=1)
        due_date = dt.strftime("%Y-%m-%d")

    task = {
        "id": task_id,
        "worker_name": worker_name,
        "task_description": task_description,
        "patient_name": patient_name,
        "due_date": due_date,
        "priority": priority,
        "status": "PENDING",
        "created_at": datetime.now().isoformat(),
    }
    hw_tasks_store.append(task)
    return {"agent": "Follow-up Agent", "action": "hw_task_created", "task": task}


def get_hw_tasks(worker_name: Optional[str] = None) -> dict:
    """Retrieve healthcare worker tasks."""
    if worker_name:
        tasks = [t for t in hw_tasks_store if t["worker_name"].lower() == worker_name.lower()]
    else:
        tasks = list(hw_tasks_store)
    return {"agent": "Follow-up Agent", "total": len(tasks), "tasks": tasks}
