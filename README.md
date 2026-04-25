# 🎯 AI Talent Scout

> **Catalyst Hackathon — Deccan AI**  
> An AI-powered recruitment agent that reads a Job Description, discovers matching candidates, simulates outreach conversations, and produces a dual-scored ranked shortlist — instantly.

---

## 📋 Table of Contents

- [Demo](#demo)
- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Architecture](#architecture)
- [Scoring Logic](#scoring-logic)
- [Tech Stack](#tech-stack)
- [Local Setup](#local-setup)
- [Sample Inputs & Outputs](#sample-inputs--outputs)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)

---

## 🎬 Demo

| | |
|---|---|
| **Demo Video** | [Watch on Loom](https://www.loom.com/share/b96f6eb56749417b95acc65c54f77e73) |
| **Live App** | [Live App](https://ai-talent-scout-9ghzwwwfawdeovmagkfpbs.streamlit.app) |

---

## 🧩 Problem Statement

Recruiters spend hours manually:
1. Reading job descriptions and extracting requirements
2. Sifting through candidate profiles for skill/experience matches
3. Sending outreach messages and guessing interest levels
4. Shortlisting candidates without a clear scoring rationale

**AI Talent Scout** automates the entire pipeline — from JD parsing to a ranked, explainable shortlist — in under 2 minutes.

---

## 🚀 Solution Overview

```
Job Description (text)
        │
        ▼
┌─────────────────────┐
│   JD Parser (LLM)   │  → Extracts: skills, experience, role title
└─────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  Candidate Matching Engine  │  → Skill match + Exp fit + Role fit
│  (Hybrid: rule + LLM)       │
└─────────────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│  Conversational Outreach     │  → LLM simulates realistic reply
│  Simulation (LLM)            │
└──────────────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│  Interest Classifier (LLM)  │  → High / Medium / Low + score
└──────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────┐
│  Ranked Shortlist                        │
│  Final Score = Match×0.7 + Interest×0.3 │
└──────────────────────────────────────────┘
```

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│  • JD input    • Score sliders    • Ranked cards + CSV  │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                    app.py  (Orchestrator)                │
│  parse_jd → match candidates → simulate → classify      │
└──────────────────────────┬───────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌─────────────────────┐    ┌─────────────────────────────┐
│   utils.py          │    │   prompts.py                │
│   Scoring functions │    │   4 prompt templates        │
│   LLM call wrapper  │    │   JD / Role / Outreach /    │
│   JSON cleaner      │    │   Interest classifier       │
└──────────┬──────────┘    └─────────────────────────────┘
           │
           ▼
┌─────────────────────┐
│   Groq API          │
│   llama-3.1-8b-inst │
└─────────────────────┘
```

### Component Responsibilities

| Component | Role |
|-----------|------|
| `app.py` | UI, orchestration, progress tracking, results display |
| `utils.py` | LLM calls, JSON parsing, scoring maths |
| `prompts.py` | All 4 LLM prompt templates |
| `candidates.json` | Candidate pool (20 profiles; swap for real DB/ATS) |
| Groq API | Fast LLM inference (llama-3.1-8b-instant) |

---

## 📐 Scoring Logic

### 1. Skill Match Score
```
skill_score = |JD_skills ∩ Candidate_skills| / |JD_skills|
```
Case-insensitive Jaccard-style overlap. Rewards exact skill matches.

### 2. Experience Fit Score
```python
if actual >= required:
    exp_score = min(1.0, 1.0 + (actual - required) * 0.05)  # slight bonus for over-qualified
else:
    gap = required - actual
    exp_score = max(0.0, 1.0 - gap * 0.25)  # 25% penalty per missing year
```

### 3. Role Fit Score (LLM-generated)
The LLM compares the job title and candidate's current role, returning a score (0–1) with a one-sentence human-readable explanation.

### 4. Match Score (weighted composite)
```
match_score = skill_score × W_skill + exp_score × W_exp + role_score × W_role
```
Default weights: 0.5 / 0.3 / 0.2 (adjustable via sidebar sliders).

### 5. Interest Score (LLM-generated)
The LLM simulates how the candidate would respond to a recruiter cold-message, then a second LLM call classifies that response into High/Medium/Low with a numeric score.

| Level  | Score Range | Meaning |
|--------|-------------|---------|
| High   | 0.75–1.0   | Enthusiastic, ready to talk |
| Medium | 0.40–0.74  | Open but cautious |
| Low    | 0.00–0.39  | Disinterested or declining |

### 6. Final Score
```
final_score = match_score × 0.7 + interest_score × 0.3
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| LLM | Groq API (llama-3.1-8b-instant) |
| Language | Python 3.10+ |
| Data | JSON (candidates.json) |
| Export | Pandas + CSV download |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ai-talent-scout.git
cd ai-talent-scout
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the app
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📦 requirements.txt

```
streamlit>=1.32.0
groq>=0.5.0
python-dotenv>=1.0.0
pandas>=2.0.0
```

---

## 🧪 Sample Inputs & Outputs

### Sample JD Input
```
We are looking for an ML Engineer with 4+ years of experience in 
Deep Learning, PyTorch, and Computer Vision. You will build and 
deploy real-time object detection pipelines at scale.
```

### Parsed JD
```json
{
  "skills": ["Deep Learning", "PyTorch", "Computer Vision"],
  "experience": 4,
  "role": "ML Engineer"
}
```

### Sample Output (Top 3)
| Rank | Name | Role | Match | Interest | Final |
|------|------|------|-------|----------|-------|
| 🥇 1 | Ananya Gupta | ML Engineer | 92% | High (0.88) | 91% |
| 🥈 2 | Arun Kumar | CV Engineer | 78% | High (0.82) | 79% |
| 🥉 3 | Rajan Bose | ML Engineer | 65% | Medium (0.55) | 62% |

### Simulated Candidate Response (Ananya Gupta)
> *"This sounds like it could be a great fit — I'm currently working on object detection projects and I'd love to learn more. When can we connect?"*

### Interest Classification
```json
{
  "interest": "High",
  "score": 0.88
}
```

---

## 📁 Project Structure

```
ai-talent-scout/
├── app.py              # Streamlit app & orchestration
├── utils.py            # LLM calls, scoring functions
├── prompts.py          # All LLM prompt templates
├── candidates.json     # Candidate pool (20 profiles)
├── requirements.txt    # Dependencies
├── .env.example        # Template for API key
└── README.md           # This file
```

---

## 🔮 Future Improvements

- **Live candidate discovery** — Connect to LinkedIn API or ATS systems
- **Resume parsing** — Accept PDF/DOCX candidate resumes
- **Multi-round outreach** — Simulate a full 3-message conversation thread
- **Explainability dashboard** — Visual breakdown of each scoring component
- **Human-in-the-loop** — Recruiter can edit/override interest assessments
- **Persistent database** — Store results across sessions with SQLite

---

## 👤 Author

**Abishek Velan M**  
Submitted for: Catalyst Hackathon — Deccan AI  
Deadline: April 27, 2026

---

*Built with ❤️ and too much coffee.*
