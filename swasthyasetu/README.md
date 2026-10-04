# SwasthyaSetu AI
## Rural Preventive Healthcare & Care Navigation Agent

> **IBM Academic Project Demonstration**
> Powered by **IBM Granite / Watsonx.ai**
> SDG 3 – Good Health & Well-Being | SDG 10 – Reduced Inequalities

---

## ⚠️ Medical Disclaimer

> SwasthyaSetu AI provides **health education and navigational guidance only**.
> It does **NOT** diagnose diseases, generate prescriptions, or recommend specific
> prescription medicines. This system does **NOT** replace qualified medical professionals.
> **In a medical emergency, call 108 immediately.**

---

## 📋 Project Overview

SwasthyaSetu AI (Sanskrit: "Health Bridge") is an AI-powered rural healthcare
assistance platform that addresses critical gaps in rural healthcare access across India.

### Problem Statement

Rural and underserved communities face:
- Limited healthcare awareness
- Long travel distances to medical facilities
- Shortage of specialists
- Language barriers (Hindi/English vs regional languages)
- Poor follow-up support
- Difficulty identifying when to seek emergency vs routine care

### Solution: Four Specialized AI Agents

| Agent | Purpose |
|-------|---------|
| 💬 **Health Guidance Agent** | Simple health education in English & Gujarati |
| 🔍 **Risk Screening Agent** | Categorize urgency: Low / Moderate / Urgent |
| 🗺️ **Care Navigation Agent** | Recommend appropriate healthcare pathway |
| 📅 **Follow-up Agent** | Reminders, medicine tracking, HW task management |

---

## 🏗️ Architecture

```
swasthyasetu/
├── backend/
│   ├── agents/
│   │   ├── granite_client.py        # IBM Granite / Watsonx.ai API client
│   │   ├── health_guidance_agent.py # Agent 1: Health education
│   │   ├── risk_screening_agent.py  # Agent 2: Urgency classification
│   │   ├── care_navigation_agent.py # Agent 3: Pathway recommendation
│   │   └── followup_agent.py        # Agent 4: Follow-up management
│   ├── data/
│   │   └── demo_data.py             # In-memory demo seed data
│   ├── routes/
│   │   └── api_routes.py            # Flask REST API endpoints
│   └── app.py                       # Flask application factory
├── frontend/
│   ├── css/styles.css               # Complete stylesheet
│   ├── js/
│   │   ├── i18n.js                  # English/Gujarati translations
│   │   └── app.js                   # Frontend application logic
│   └── index.html                   # Single-page application
├── run.py                           # Application entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variable template
└── README.md                        # This file
```

### Technology Stack

| Layer | Technology |
|-------|-----------|
| AI/LLM | IBM Granite (`ibm/granite-13b-instruct-v2`) via Watsonx.ai |
| Backend | Python 3.9+, Flask, Flask-CORS |
| Frontend | Vanilla HTML5, CSS3, JavaScript (no build tools required) |
| Languages | English, Gujarati (Devanagari) |
| Auth | IBM Cloud IAM token (via API key in environment variable) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- IBM Cloud account (for Watsonx.ai credentials — optional; works in demo mode without)

### 1. Clone / Download the Project

```bash
cd swasthyasetu
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the template
cp .env.example .env

# Edit .env and fill in your IBM Cloud credentials
# See .env.example for details
```

> **Never commit your `.env` file to version control.**

### 5. Run the Application

```bash
python run.py
```

Open your browser at: **http://localhost:5000**

---

## 🔑 Environment Variables

See [`.env.example`](.env.example) for a full list. Key variables:

| Variable | Description |
|----------|-------------|
| `WATSONX_API_KEY` | IBM Cloud API Key (IAM) |
| `WATSONX_PROJECT_ID` | Watsonx.ai Project ID |
| `WATSONX_API_URL` | Watsonx.ai endpoint (default: `https://us-south.ml.cloud.ibm.com`) |
| `GRANITE_MODEL_ID` | IBM Granite model ID (default: `ibm/granite-13b-instruct-v2`) |
| `FLASK_DEBUG` | Set to `true` for development |
| `PORT` | Server port (default: `5000`) |

### Demo Mode (No Credentials Required)

If `WATSONX_API_KEY` is not set, the application runs in **Demo Mode** with
pre-configured educational responses. All UI features remain functional.

---

## 📡 API Reference

All endpoints are prefixed with `/api`.

### Health Guidance Agent

```
POST /api/health-guidance
Body: { "question": "...", "language": "english|gujarati", "patient_name": "..." }
```

### Risk Screening Agent

```
POST /api/risk-screening
Body: { "symptoms": "...", "age": "35", "gender": "Female", "patient_name": "..." }
```

### Care Navigation Agent

```
POST /api/care-navigation
Body: { "symptoms": "...", "risk_level": "LOW|MODERATE|URGENT", "location": "...", "patient_name": "..." }
```

### Follow-up Management

```
GET  /api/followup                      # List all follow-ups
POST /api/followup                      # Create follow-up
PATCH /api/followup/{id}/complete       # Mark as complete

GET  /api/medicine-reminder             # List medicine reminders
POST /api/medicine-reminder             # Create reminder

GET  /api/hw-tasks                      # List HW tasks
POST /api/hw-tasks                      # Create task
```

### Dashboard

```
GET /api/dashboard    # Summary statistics and recent interactions
GET /api/health       # Health check and mode status
```

---

## 🌐 Features

### UI Features
- ✅ Responsive design (mobile & desktop)
- ✅ English / Gujarati language toggle
- ✅ Large accessible buttons for rural users
- ✅ Clear emergency warning section (persistent banner)
- ✅ Medical disclaimer throughout
- ✅ Privacy policy section
- ✅ Dark/High-contrast accessible colors

### Agent Features
- ✅ Health education without diagnosis
- ✅ Risk categorization (Low / Moderate / Urgent)
- ✅ Care pathway navigation (5 levels)
- ✅ Follow-up reminder management
- ✅ Medicine reminder tracking (user-entered only)
- ✅ Healthcare worker task management
- ✅ Live dashboard with statistics

### Safety Features
- ✅ Hard-coded emergency detection (immediate 108 routing)
- ✅ No disease diagnosis claims anywhere
- ✅ No prescription generation
- ✅ Consistent disclaimer in every AI response
- ✅ Graceful degradation (demo mode without API keys)

---

## 🔐 Security

- API keys and secrets are **never in source code** — environment variables only
- `.env` is listed in `.gitignore`
- CORS configured via environment variable
- Input sanitization on all user inputs (frontend + backend)
- No persistent storage of sensitive patient data in demo mode

---

## 📚 IBM Granite Integration

IBM Granite `ibm/granite-13b-instruct-v2` is used via the Watsonx.ai REST API for:

1. **Health Guidance**: Generating safe, educational health information
2. **Risk Screening**: Classifying symptom urgency with structured prompts
3. **Care Navigation**: Recommending appropriate healthcare pathways

Prompt engineering principles applied:
- System context with strict safety rules
- Structured output format (key: value)
- Low temperature (0.2–0.3) for consistent, safe responses
- Repetition penalty to avoid loops
- Conservative fallbacks for all parsing

---

## 👥 Target Users

| User | Use Case |
|------|---------|
| Rural patient | Health questions, symptom screening, care navigation |
| Family member | Follow-up tracking, medicine reminders |
| ASHA / ANM worker | Task management, patient follow-up |
| Healthcare administrator | Dashboard, metrics, resource planning |

---

## 📊 SDG Alignment

| SDG | Contribution |
|-----|-------------|
| **SDG 3** – Good Health & Well-Being | Improving healthcare access and awareness in rural communities |
| **SDG 10** – Reduced Inequalities | Bridging the urban-rural healthcare gap with multilingual AI assistance |

---

## 🛠️ Development

### Running in Debug Mode

```bash
FLASK_DEBUG=true python run.py
```

### Project Structure Notes

- **In-memory data store**: Demo data is in `backend/data/demo_data.py`. For production, replace with a proper database (PostgreSQL, SQLite, etc.).
- **No build tools**: The frontend is pure HTML/CSS/JS — no npm, webpack, or React required. Suitable for IBM BOB deployment.

---

## 📄 License

This project is developed for academic demonstration as part of an IBM project submission.

**Built with IBM Granite | Aligned with SDG 3 & SDG 10**
