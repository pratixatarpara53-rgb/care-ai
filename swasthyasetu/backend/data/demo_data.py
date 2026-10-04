"""
Demo seed data for SwasthyaSetu AI.
This module pre-populates in-memory stores with realistic sample data
for academic demonstration purposes.
"""

from datetime import datetime, timedelta


def _days_from_now(n: int) -> str:
    return (datetime.now() + timedelta(days=n)).strftime("%Y-%m-%d")


def _days_ago(n: int) -> str:
    return (datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d")


# ──────────────────────────────────────────────
# Follow-up store (mutable list shared across app)
# ──────────────────────────────────────────────
followup_store = [
    {
        "id": "FU001",
        "patient_name": "Ramila Bhen",
        "concern": "Persistent cough and mild fever for 5 days",
        "recommended_date": _days_from_now(1),
        "notes": "Monitor temperature twice daily. Visit PHC if fever exceeds 102°F.",
        "pathway": "PHC",
        "contact": "+91-98765-11111",
        "status": "PENDING",
        "created_at": _days_ago(2),
        "completed_at": None,
    },
    {
        "id": "FU002",
        "patient_name": "Govindbhai Patel",
        "concern": "Blood pressure monitoring post-hypertension education",
        "recommended_date": _days_from_now(3),
        "notes": "Advised low-salt diet. Schedule BP check at PHC.",
        "pathway": "PHC",
        "contact": "+91-98765-22222",
        "status": "PENDING",
        "created_at": _days_ago(4),
        "completed_at": None,
    },
    {
        "id": "FU003",
        "patient_name": "Savitaben Desai",
        "concern": "Prenatal care – second trimester checkup",
        "recommended_date": _days_from_now(5),
        "notes": "Ensure iron and folic acid supplements as prescribed by doctor.",
        "pathway": "PHC",
        "contact": "+91-98765-33333",
        "status": "PENDING",
        "created_at": _days_ago(1),
        "completed_at": None,
    },
    {
        "id": "FU004",
        "patient_name": "Arjun Thakor",
        "concern": "Mild dehydration follow-up after ORS treatment",
        "recommended_date": _days_ago(1),
        "notes": "Completed ORS treatment. Recovering well. No further action needed.",
        "pathway": "LOCAL_HEALTH_WORKER",
        "contact": "+91-98765-44444",
        "status": "COMPLETED",
        "created_at": _days_ago(5),
        "completed_at": _days_ago(1),
    },
    {
        "id": "FU005",
        "patient_name": "Manjuben Solanki",
        "concern": "Child vaccination schedule (DPT booster)",
        "recommended_date": _days_from_now(7),
        "notes": "Child age 18 months. Due for DPT and OPV booster at anganwadi.",
        "pathway": "LOCAL_HEALTH_WORKER",
        "contact": "+91-98765-55555",
        "status": "PENDING",
        "created_at": _days_ago(0),
        "completed_at": None,
    },
    {
        "id": "FU006",
        "patient_name": "Dhirubhai Chauhan",
        "concern": "Diabetes education and dietary counselling",
        "recommended_date": _days_ago(3),
        "notes": "Completed dietary counselling session. Referred to doctor for HbA1c test.",
        "pathway": "DOCTOR_CONSULTATION",
        "contact": "+91-98765-66666",
        "status": "COMPLETED",
        "created_at": _days_ago(10),
        "completed_at": _days_ago(3),
    },
]

# ──────────────────────────────────────────────
# Medicine reminders store
# ──────────────────────────────────────────────
medicine_reminders_store = [
    {
        "id": "MR001",
        "patient_name": "Govindbhai Patel",
        "medicine_name": "Amlodipine 5mg (as prescribed by doctor)",
        "reminder_time": "08:00 AM",
        "frequency": "Once daily",
        "notes": "Take after breakfast. Doctor-prescribed.",
        "created_at": _days_ago(4),
        "active": True,
    },
    {
        "id": "MR002",
        "patient_name": "Savitaben Desai",
        "medicine_name": "Iron & Folic Acid tablet (doctor-prescribed)",
        "reminder_time": "09:00 AM",
        "frequency": "Once daily",
        "notes": "Take with a glass of water. Avoid with tea/coffee.",
        "created_at": _days_ago(1),
        "active": True,
    },
    {
        "id": "MR003",
        "patient_name": "Ramila Bhen",
        "medicine_name": "ORS Solution (oral rehydration)",
        "reminder_time": "Every 4 hours",
        "frequency": "As needed",
        "notes": "Prepare fresh ORS each time. Follow ASHA worker instructions.",
        "created_at": _days_ago(2),
        "active": True,
    },
]

# ──────────────────────────────────────────────
# Healthcare worker tasks store
# ──────────────────────────────────────────────
hw_tasks_store = [
    {
        "id": "HWT001",
        "worker_name": "Kantaben ASHA",
        "task_description": "Home visit – check on Ramila Bhen's fever and cough",
        "patient_name": "Ramila Bhen",
        "due_date": _days_from_now(1),
        "priority": "HIGH",
        "status": "PENDING",
        "created_at": _days_ago(2),
    },
    {
        "id": "HWT002",
        "worker_name": "Kantaben ASHA",
        "task_description": "Conduct child immunization drive at Rajpur village anganwadi",
        "patient_name": "Community",
        "due_date": _days_from_now(3),
        "priority": "HIGH",
        "status": "PENDING",
        "created_at": _days_ago(1),
    },
    {
        "id": "HWT003",
        "worker_name": "Nalini ANM",
        "task_description": "Prenatal checkup for Savitaben Desai – record weight, BP, fetal heartbeat",
        "patient_name": "Savitaben Desai",
        "due_date": _days_from_now(5),
        "priority": "NORMAL",
        "status": "PENDING",
        "created_at": _days_ago(1),
    },
    {
        "id": "HWT004",
        "worker_name": "Nalini ANM",
        "task_description": "Completed hypertension awareness session at Chandrpur PHC",
        "patient_name": "Community",
        "due_date": _days_ago(2),
        "priority": "NORMAL",
        "status": "COMPLETED",
        "created_at": _days_ago(7),
    },
]

# ──────────────────────────────────────────────
# Interaction history store
# ──────────────────────────────────────────────
interaction_history = [
    {
        "id": "INT001",
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        "patient_name": "Anonymous",
        "agent_used": "Health Guidance Agent",
        "query_summary": "Asked about prevention of malaria during monsoon",
        "risk_level": None,
        "language": "Gujarati",
    },
    {
        "id": "INT002",
        "timestamp": (datetime.now() - timedelta(hours=5)).isoformat(),
        "patient_name": "Ramila Bhen",
        "agent_used": "Risk Screening Agent",
        "query_summary": "Reported persistent cough, mild fever, fatigue for 5 days",
        "risk_level": "MODERATE",
        "language": "English",
    },
    {
        "id": "INT003",
        "timestamp": (datetime.now() - timedelta(hours=5, minutes=3)).isoformat(),
        "patient_name": "Ramila Bhen",
        "agent_used": "Care Navigation Agent",
        "query_summary": "Recommended PHC visit for fever and cough evaluation",
        "risk_level": "MODERATE",
        "language": "English",
    },
    {
        "id": "INT004",
        "timestamp": (datetime.now() - timedelta(hours=18)).isoformat(),
        "patient_name": "Anonymous",
        "agent_used": "Health Guidance Agent",
        "query_summary": "Asked about safe drinking water and water-borne disease prevention",
        "risk_level": None,
        "language": "Gujarati",
    },
    {
        "id": "INT005",
        "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
        "patient_name": "Govindbhai Patel",
        "agent_used": "Risk Screening Agent",
        "query_summary": "Reported occasional headaches and dizziness – history of hypertension",
        "risk_level": "MODERATE",
        "language": "English",
    },
    {
        "id": "INT006",
        "timestamp": (datetime.now() - timedelta(days=1, hours=2)).isoformat(),
        "patient_name": "Anonymous",
        "agent_used": "Health Guidance Agent",
        "query_summary": "Asked about child nutrition and supplementary feeding",
        "risk_level": None,
        "language": "Gujarati",
    },
]
